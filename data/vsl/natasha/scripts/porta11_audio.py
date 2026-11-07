# porta11_audio.py (parte 1): monta a trilha de voz v7 + tempos + palavras de legenda
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
GAIN={V+'B3.mp3':-2.5}
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
def span(b,pre=0.06,post=0.18):
    w=json.load(open(f'{V}w_{b}.json')); return max(0,w[0][0]-pre),w[-1][1]+post
B={k:span(k) for k in ['B1','B2','B3','B4']}
B['B5']=(0,json.load(open(V+'w_B5.json'))[-1][1]+0.15)
B['B6']=(0,json.load(open(V+'w_B6.json'))[-1][1]+0.2)
B['B7']=(0,json.load(open(V+'w_B7.json'))[-1][1]+0.2)
# ---- ato 1
n=lambda k:(V+k+'.mp3',)+B[k]
pos1,d1=block([(A1,0,63.30),n('B3'),(A1,65.78,76.18),n('B4')],W+'blk_ato1.wav')
dl=pos1[2]-65.78   # deslocamento do que era 65.78 em diante
# ---- B7b
Q=P9%'B7b'
pos2,d2=block([(Q,0,2.35),n('B1'),(Q,4.15,8.65),n('B2'),(Q,11.15,22.674)],W+'blk_b7b.wav')
def mo(r):  # tempo relativo antigo (B7b) -> relativo novo
    if r<2.35: return r
    if r<8.65: return pos2[2]+(r-4.15)
    return pos2[4]+(r-11.15)
block([(P9%'B8',0,dur(P9%'B8'))],W+'blk_b8.wav'); d8=dur(W+'blk_b8.wav')
block([n('B5')],W+'blk_b5.wav'); d5=dur(W+'blk_b5.wav')
block([n('B6')],W+'blk_b6.wav'); d6=dur(W+'blk_b6.wav')
block([n('B7')],W+'blk_b7.wav'); d7=dur(W+'blk_b7.wav')
block([(FE,0,dur(FE))],W+'blk_fe.wav')
A_END=d1; O7=A_END+0.5; O8=O7+d2+0.4; O9=O8+d8+0.4; BLK=0.4
O9b=O9+d5+BLK; O10=O9b+d6+0.4; FE_AT=O10+d7+0.3; END=round(FE_AT+5.95,2)
# ---- monta voz final
blks=[(W+'blk_ato1.wav',0),(W+'blk_b7b.wav',O7),(W+'blk_b8.wav',O8),(W+'blk_b5.wav',O9),(W+'blk_b6.wav',O9b),(W+'blk_b7.wav',O10),(W+'blk_fe.wav',FE_AT)]
ins=[];fl=[]
for i,(f,t) in enumerate(blks):
    ins+=['-i',f]; fl.append(f'[{i}:a]aresample=44100,aformat=channel_layouts=mono,adelay={int(round(t*1000))}[v{i}]')
fl.append(''.join(f'[v{i}]' for i in range(len(blks)))+f'amix=inputs={len(blks)}:normalize=0:duration=longest,apad=whole_dur={END},atrim=0:{END}[o]')
run(['ffmpeg','-y','-loglevel','error']+ins+['-filter_complex',';'.join(fl),'-map','[o]','-ar','44100','/tmp/p11/voz11.wav'])
# ---- palavras (legenda)
words=[]
Aw=json.load(open('/tmp/p7/words_a5.json'))
def fixname(t):
    t2=t.rstrip(',.!?'); p=t[len(t2):]
    m={'torre':'Thor','tor':'Thor','pirrasa':'pirraça','pirraça':'pirraça','800':'oitocentos'}
    return m.get(t2.lower(),t2)+p
for s,e,t in Aw:
    if s<63.30: words.append([s,e,fixname(t)])
    elif 65.78<=s<76.18: words.append([s+dl,e+dl,fixname(t)])
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
    elif 4.15<=s<8.65: words.append([mo(s)+O7,mo(e)+O7,t])
    elif s>=11.15:
        t={'800':'oitocentos','fide,':'o feed,','tor':'Thor'}.get(t,t); words.append([mo(s)+O7,mo(e)+O7,t])
addnew('B1',pos2[1],O7); addnew('B2',pos2[3],O7)
b8=json.load(open('/tmp/p9/w_B8.json'))
for s,e,t in b8:
    if t=='sozinho': t='Sozinho'
    if t=='casa.' and s<2.5: t='Casa.'
    t={'10':'Dez','14,':'catorze,','destradora.':'adestradora.'}.get(t,t)
    if t=='a' and 17.3<s<17.6: continue
    words.append([s+O8,e+O8,t])
words.sort(key=lambda w:w[0])
json.dump(dict(words=words,pos1=pos1,pos2=pos2,dl=dl,d1=d1,d2=d2,d5=d5,d6=d6,d7=d7,d8=d8,A_END=A_END,O7=O7,O8=O8,O9=O9,O9b=O9b,O10=O10,FE_AT=FE_AT,END=END,BLK=BLK,
  mo_pts=[[r,mo(r)] for r in (0,2.35,4.15,8.65,11.15,22.674)]),open('/tmp/p11/times.json','w'),ensure_ascii=False)
print({k:round(v,2) for k,v in dict(dl=dl,A_END=A_END,O7=O7,O8=O8,O9=O9,O9b=O9b,O10=O10,FE_AT=FE_AT,END=END).items()})
print('pos1',[round(x,2) for x in pos1],'pos2',[round(x,2) for x in pos2])


# ======== parte 2: sonoplastia + mix ========
# porta11_audio.py (parte 2): sonoplastia + mix + mux
import subprocess,json,os
S='/tmp/p7/sfx/'; M='/tmp/p7/music_tears.mp3'
T=json.load(open('/tmp/p11/times.json'))
for k in ['A_END','O7','O8','O9','O9b','O10','FE_AT','END','dl','d5','d6','d7','d8']: globals()[k]=T[k]
OUT=os.environ.get('OUT','/tmp/p11/out'); os.makedirs(OUT,exist_ok=True)
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode: print('ERR',r.stderr[-500:])
def mo(r):
    p=T['pos2']
    if r<2.35: return r
    if r<8.65: return p[2]+(r-4.15)
    return p[4]+(r-11.15)
q=lambda r:O7+mo(r)
run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','sine=frequency=2300:duration=0.03','-af','afade=t=out:st=0.01:d=0.02,apad=pad_dur=0.97','/tmp/p11/tick1.wav'])
run(['ffmpeg','-y','-loglevel','error','-stream_loop','16','-i','/tmp/p11/tick1.wav','-t','16.5','/tmp/p11/tickbed.wav'])
up=('bass_hit','brass','suspense','boing','trombone','slide','funny','drum','horror','impacto','piano','string')
BL0=O9+d5; BL1=O9b   # preto mudo
d=dl
cues=[
(10.8,'sfx_bass_hit',-4),(11.0,'sfx_brass_strings_suspense',-9),(23.4,'sfx_cartoon_surprise_suspense',-9),(32.4,'sfx_brass_strings_suspense',-9),
(34.5,'sfx_cachorro_latindo',-12),(37.0,'sfx_boing',-9),(39.0,'sfx_metal_boing',-11),(43.9,'sfx_slide_funny',-8),(42.95,'sfx_trombone_decepcao',-10),
(50.6,'sfx_bass_hit',-4),(50.8,'sfx_horror_drum',-10),(51.4,'sfx_cachorro_latindo',-12),(53.0,'sfx_filhote_latidos',-14),
(61.7,'sfx_piano_falha',-8),(62.9,'sfx_bass_hit',-5),
(66.2+d,'sfx_click_botao',-6),(69.9+d,'sfx_heartbeat_impact',-6),(70.9+d,'sfx_brass_strings_suspense',-9),(71.6+d,'sfx_notificacao_celular',-12),
(T['pos1'][3]+1.9,'sfx_cachorro_choro',-12),
(q(16.7),'sfx_notificacao_celular@1.6',-8),(q(19.88),'sfx_bass_hit',-2),(q(19.95),'sfx_horror_drum@2.0',-9),
(O8+0.0,'sfx_chimes_vitoria',-7),(O8+2.1,'sfx_conquista',-12),(O8+15.1,'sfx_boing',-7),(O8+15.3,'sfx_slide_funny',-9),
# dia 14
(O9+0.1,'sfx_drum_roll_suspense@3.9',-8),(O9+4.5,'sfx_bass_hit',-5),
(O9+8.9,'sfx_heartbeat_impact@%.2f'%(d5-8.9-0.4),-6),(O9+13.3,'sfx_suspense_swell@3.0',-12),
# reveal
(O9b+0.0,'sfx_chimes_vitoria',-5),(O9b+0.1,'sfx_conquista',-6),(O9b+0.2,'sfx_moeda_win',-11),(O9b+5.4,'sfx_chimes_vitoria',-10),
# beneficios
(O10+4.3,'sfx_boing',-10),(O10+4.6,'sfx_conquista',-10),(O10+22.4,'sfx_moedas_clinking',-4),(O10+26.0,'sfx_chimes_vitoria',-9),
(FE_AT+4.9,'sfx_click_botao',-5),(FE_AT+5.1,'sfx_chimes_vitoria',-9)]
ins=['-i','/tmp/p11/voz11.wav','-stream_loop','-1','-i',M,'-i','/tmp/p11/tickbed.wav']
g=(f"-19+3*between(t,{O8:.2f},{O8+20.4:.2f})+3*between(t,{O9:.2f},{BL0:.2f})+4*between(t,{O9b:.2f},{O10:.2f})+3*between(t,{O10:.2f},{FE_AT:.2f})")
mute=f"between(t,{O7+19.2:.2f},{O7+19.9:.2f})+between(t,{O8+20.5:.2f},{O9+0.1:.2f})+between(t,{BL0:.2f},{BL1:.2f})"
fl=[f"[1:a]aresample=44100,aformat=channel_layouts=stereo,atrim=0:{T['END']},afade=t=in:d=1.5,afade=t=out:st={T['END']-4}:d=4,volume='pow(10,({g})/20)*(1-min(1,{mute}))':eval=frame[mus]",
    "[0:a]aformat=channel_layouts=stereo[vz]",
    f"[2:a]aresample=44100,aformat=channel_layouts=stereo,volume=-26dB,adelay={int(O7*1000)}|{int(O7*1000)}[tk]"]
lab=['vz','mus','tk']
for i,(t,n,db) in enumerate(cues):
    trim=None
    if '@' in n: n,trim=n.split('@'); trim=float(trim)
    if any(u in n for u in up) and 'cachorro' not in n: db+=3
    ins+=['-i',S+n+'.mp3']
    f=f"[{i+3}:a]"+(f"atrim=0:{trim},afade=t=out:st={max(trim-0.25,0)}:d=0.25," if trim else '')+f"aresample=44100,aformat=channel_layouts=stereo,volume={db}dB,adelay={int(t*1000)}|{int(t*1000)}[s{i}]"
    fl.append(f); lab.append(f's{i}')
# mudo total no preto (voz+sfx+musica)
fl.append(''.join(f'[{l}]' for l in lab)+f"amix=inputs={len(lab)}:normalize=0:duration=longest,volume='1-between(t,{BL0:.2f},{BL1:.2f})':eval=frame,alimiter=limit=0.95,atrim=0:{T['END']}[out]")
run(['ffmpeg','-y','-loglevel','error']+ins+['-filter_complex',';'.join(fl),'-map','[out]','-ar','44100','/tmp/p11/mix.wav'])
run(['ffmpeg','-y','-loglevel','error','-i','/tmp/p11/long_v.mp4','-i','/tmp/p11/mix.wav','-map','0:v','-map','1:a','-c:v','libx264','-preset','veryfast','-crf','24','-c:a','aac','-b:a','192k','-shortest',OUT+'/porta11_vsl_filme_v7_longa.mp4'])
run(['ffmpeg','-y','-loglevel','error','-i',OUT+'/porta11_vsl_filme_v7_longa.mp4','-vf','scale=-2:640','-c:v','libx264','-crf','30','-preset','veryfast','-c:a','aac','-b:a','96k',OUT+'/porta11_vsl_filme_v7_longa_leve.mp4'])
for f in ['porta11_vsl_filme_v7_longa','porta11_vsl_filme_v7_longa_leve']: print(f,os.path.getsize(OUT+'/'+f+'.mp4'))
