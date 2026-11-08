# porta12_audio.py (parte 1): trilha de voz v8 (cortes A1-A5, B5 take A, fim de fala por energia)
import subprocess,json,os
W='/tmp/p11/w/'; V='/tmp/p11/voz/'
A1='/mnt/user-data/outputs/porta7/vsl_filme_ato1_voz_v4.mp3'
P9='/mnt/user-data/outputs/porta9/vsl_filme_p9_%s_voz.mp3'
FE='/home/claude/allandouradocontato-creator/tutorialpet/data/vsl/natasha/fecho/FECHO_gravado_sem_Eu_sou_a_doutora_Natasha.mp3'
XF=0.04
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode: raise SystemExit(r.stderr[-600:])
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
import numpy as np,re
def lufs(f,ss=None,t=None):
    c=['ffmpeg','-nostats','-hide_banner']+(['-ss',str(ss),'-t',str(t)] if ss is not None else [])+['-i',f,'-af','ebur128','-f','null','-']
    o=subprocess.run(c,capture_output=True,text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS',o)[-1])
def eend(src,wend,minpost):
    raw=subprocess.run(['ffmpeg','-v','error','-i',src,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    y=np.frombuffer(raw,np.float32); h=160; n=len(y)//h
    r=np.sqrt((y[:n*h].reshape(n,h)**2).mean(1)); thr=r.max()*10**(-40/20)
    idx=np.where(r>thr)[0]; act=(idx[-1]+1)*h/16000 if len(idx) else wend
    return min(max(wend+minpost,act+0.05),dur(src))
GAIN={V+'B3.mp3':-2.5}
B11F=V+'B11.wav'
QQ='/mnt/user-data/outputs/porta9/vsl_filme_p9_B7b_voz.mp3'; B8F='/mnt/user-data/outputs/porta9/vsl_filme_p9_B8_voz.mp3'
_lq=lufs(QQ); _l8=lufs(B8F)
for k,ref in [('B9a',_lq),('B9b',_lq),('B10a',_l8)]:
    GAIN[V+k+'.mp3']=max(-4,min(4,ref-lufs(V+k+'.mp3')))
_l7=lufs(V+'B7.mp3',14.8,5.7)   # trecho falado do B7 (aplicativo ... nada.)
GAIN[B11F]=max(-6,min(6,_l7-lufs(B11F)+1.5))
print('GAIN',GAIN)
def piece(src,a,b,out):
    g=GAIN.get(src,0)
    run(['ffmpeg','-y','-loglevel','error','-i',src,'-af',f'volume={g}dB,atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=mono,afade=t=in:d={XF/2},afade=t=out:st={b-a-XF/2}:d={XF/2}','-ar','44100',out])
    return b-a
def block(pieces,out):
    """pieces=[(src,a,b)] -> wav com crossfade; devolve posições de início de cada peça."""
    pos=[];t=0;fl=[];ins=[]
    for i,(src,a,b) in enumerate(pieces):
        f=f'/tmp/p11/w/p_{os.path.basename(out)}_{i}.wav'; L=piece(src,a,b,f)
        pos.append(t); ins+=['-i',f]
        fl.append(f'[{i}:a]adelay={int(round(t*1000))}[x{i}]'); t=t+L-XF
    fl.append(''.join(f'[x{i}]' for i in range(len(pieces)))+f'amix=inputs={len(pieces)}:normalize=0:duration=longest,loudnorm=I=-16:TP=-1.5[o]')
    run(['ffmpeg','-y','-loglevel','error']+ins+['-filter_complex',';'.join(fl),'-map','[o]','-ar','44100',out])
    return pos,dur(out)
def span(b,pre=0.06,post=0.18,src=None):
    w=json.load(open(f'{V}w_{b}.json')); return max(0,w[0][0]-pre),eend(V+(src or b)+'.mp3',w[-1][1],post)
B={k:span(k) for k in ['B1','B3','B4']}
B['B2']=span('B2',post=0.40)      # A3: 'Caro demais' sem engolir o S
B['B9a']=span('B9a',pre=0.0,post=0.10); B['B9b']=span('B9b',pre=0.0,post=0.10); B['B10a']=span('B10a',pre=0.0,post=0.08)
B['B5']=(0,eend(V+'B5A.mp3',json.load(open(V+'w_B5A.json'))[-1][1],0.15))
B['B6']=(0,json.load(open(V+'w_B6.json'))[-1][1]+0.2)
B['B7']=(0,json.load(open(V+'w_B7.json'))[-1][1]+0.2)
print({k:[round(x,2) for x in v] for k,v in B.items()})
# ---- ato 1
n=lambda k:(V+('B5A' if k=='B5' else k)+'.mp3',)+B[k]
pos1,d1=block([(A1,0,63.30),n('B3'),(A1,65.78,75.14),n('B4')],W+'blk_ato1.wav')
dl=pos1[2]-65.78   # deslocamento do que era 65.78 em diante
# ---- B7b
Q=P9%'B7b'
pos2,d2=block([(Q,0,2.35),n('B1'),n('B9a'),(Q,6.55,8.65),n('B2'),(Q,11.15,13.65),n('B9b'),(Q,17.62,22.674)],W+'blk_b7b.wav')
L9a=B['B9a'][1]-B['B9a'][0]; L9b=B['B9b'][1]-B['B9b'][0]
def mo(r):  # tempo relativo antigo (B7b) -> relativo novo
    if r<2.35: return r
    if r<6.55: return pos2[2]+(r-4.15)*L9a/2.4
    if r<8.65: return pos2[3]+(r-6.55)
    if r<13.65: return pos2[5]+(r-11.15)
    if r<17.62: return pos2[6]+(r-13.65)*L9b/3.97
    return pos2[7]+(r-17.62)
P8=P9%'B8'; D8=dur(P8)
pos8,d8=block([(P8,0,18.32),n('B10a'),(P8,20.46,D8)],W+'blk_b8.wav')
def mo8(r):
    if r<18.32: return r
    if r<20.46: return pos8[1]+(r-18.38)
    return pos8[2]+(r-20.46)
block([n('B5')],W+'blk_b5.wav'); d5=dur(W+'blk_b5.wav')
block([n('B6')],W+'blk_b6.wav'); d6=dur(W+'blk_b6.wav')
# ---- B7 + B11 (Por tempo limitado,) antes de 'De noventa e sete'
w7=json.load(open(V+'w_B7.json')); iDe=[i for i,x in enumerate(w7) if x[2]=='De' and x[0]>20][0]; tDe=w7[iDe][0]
CUT_A=w7[iDe-1][1]+0.22; CUT_B=tDe-0.15
pos7,d7=block([(V+'B7.mp3',0,CUT_A),(B11F,0.06,1.36),(V+'B7.mp3',CUT_B,B['B7'][1])],W+'blk_b7.wav')
def mo7(r):
    if r<CUT_A: return r
    return pos7[2]+(r-CUT_B)
w11=json.load(open('/tmp/p11/w_B11.json')); T11=(pos7[1]+max(0,w11[0][1]-0.06), pos7[1]+(w11[-1][2]-0.06))
print('B11',[round(x,2) for x in pos7],'iDe',iDe,'tDe',tDe,'T11',T11,'mo7(tDe)',mo7(tDe),'d7',d7)
block([(FE,0,dur(FE))],W+'blk_fe.wav')
A_END=d1; O7=A_END+0.5; O8=O7+d2+0.4; O9=O8+d8+0.4; BLK=0.4
O9b=O9+d5+BLK; O10=O9b+d6+0.4; FE_AT=O10+d7+0.3; END=round(FE_AT+5.95,2)
# ---- monta voz final
blks=[(W+'blk_ato1.wav',0),(W+'blk_b7b.wav',O7),(W+'blk_b8.wav',O8),(W+'blk_b5.wav',O9),(W+'blk_b6.wav',O9b),(W+'blk_b7.wav',O10),(W+'blk_fe.wav',FE_AT)]
ins=[];fl=[]
for i,(f,t) in enumerate(blks):
    ins+=['-i',f]; fl.append(f'[{i}:a]aresample=44100,aformat=channel_layouts=mono,adelay={int(round(t*1000))}[v{i}]')
fl.append(''.join(f'[v{i}]' for i in range(len(blks)))+f'amix=inputs={len(blks)}:normalize=0:duration=longest,apad=whole_dur={END},atrim=0:{END}[o]')
run(['ffmpeg','-y','-loglevel','error']+ins+['-filter_complex',';'.join(fl),'-map','[o]','-ar','44100','/tmp/p11/voz14.wav'])
# ---- palavras (legenda)
words=[]
Aw=json.load(open('/tmp/p7/words_a5.json'))
def fixname(t):
    t2=t.rstrip(',.!?'); p=t[len(t2):]
    m={'torre':'Thor','tor':'Thor','pirrasa':'pirraça','pirraça':'pirraça','800':'oitocentos'}
    return m.get(t2.lower(),t2)+p
for s,e,t in Aw:
    if s<63.30: words.append([s,e,fixname(t)])
    elif 65.78<=s<75.14: words.append([s+dl,e+dl,fixname(t)])
def addnew(k,pos,off,mp=None):
    w=json.load(open(f'{V}w_{k}.json')); a=B[k][0]
    for s,e,t in w:
        t=(mp or {}).get(t,t); words.append([s-a+pos+off,e-a+pos+off,t])
addnew('B3',pos1[1],0); addnew('B4',pos1[3],0,{'o':'o','fegante':'ofegante,'})
b4=[w for w in words if w[0]>=pos1[3]]
# B4: junta "o"+"fegante"
for i,w in enumerate(b4[:-1]):
    pass
Bw=json.load(open(W+'../voz/w_B1.json'))
bw=json.load(open('/tmp/p9/w_B7b.json'))
for s,e,t in bw:
    if s<2.35: words.append([s+O7,e+O7,t.replace('tor','Thor') if t=='tor' else t])
    elif 6.55<=s<8.65: words.append([mo(s)+O7,mo(e)+O7,t])
    elif 11.15<=s<13.65 or s>=17.62:
        t={'800':'oitocentos','fide,':'o feed,','tor':'Thor'}.get(t,t); words.append([mo(s)+O7,mo(e)+O7,t])
addnew('B1',pos2[1],O7); addnew('B2',pos2[4],O7)
addnew('B9a',pos2[2],O7,{'ligada.':'ligada…'}); addnew('B9b',pos2[6],O7,{'feed,':'o feed,','fide,':'o feed,'})
b8=json.load(open('/tmp/p9/w_B8.json'))
for s,e,t in b8:
    if t=='sozinho': t='Sozinho'
    if t=='casa.' and s<2.5: t='Casa.'
    t={'10':'Dez','14,':'catorze,','destradora.':'adestradora.'}.get(t,t)
    if t=='a' and 17.3<s<17.6: continue
    if 18.3<=s<20.5: continue
    words.append([mo8(s)+O8,mo8(e)+O8,t])
addnew('B10a',pos8[1],O8,{'dia.':'dia,'})
words.sort(key=lambda w:w[0])
json.dump(dict(words=words,pos1=pos1,pos2=pos2,pos7=pos7,T11=T11,CUT_A=CUT_A,CUT_B=CUT_B,iDe=iDe,dl=dl,d1=d1,d2=d2,d5=d5,d6=d6,d7=d7,d8=d8,A_END=A_END,O7=O7,O8=O8,O9=O9,O9b=O9b,O10=O10,FE_AT=FE_AT,END=END,BLK=BLK,
  pos8=pos8,b5map=[[o[0],a[j][0]] for i,o in enumerate(json.load(open(V+'w_B5.json'))) for j in [i if i<=19 else i-1] if i!=20 and j<len(json.load(open(V+'w_B5A.json'))) for a in [json.load(open(V+'w_B5A.json'))]],L9a=L9a,L9b=L9b,mo_pts=[[r,mo(r)] for r in (0,2.35,4.15,6.55,8.65,11.15,13.65,17.62,22.674)],mo8_pts=[[r,mo8(r)] for r in (0,18.32,18.38,20.46,20.5,23.78)]),open('/tmp/p11/times.json','w'),ensure_ascii=False)
print({k:round(v,2) for k,v in dict(dl=dl,A_END=A_END,O7=O7,O8=O8,O9=O9,O9b=O9b,O10=O10,FE_AT=FE_AT,END=END).items()})
print('pos8',[round(x,2) for x in pos8]);print('pos1',[round(x,2) for x in pos1],'pos2',[round(x,2) for x in pos2])
