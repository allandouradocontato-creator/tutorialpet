# porta12_build.py : VSL v8 (reveal R1+DO, botão de compra, gate 3.0)  [base v7 "tudo em video" (sem still, sem congelar)
import subprocess,json,os,shutil
T=json.load(open('/tmp/p11/times.json'))
pos8=T['pos8']
for k in ['A_END','O7','O8','O9','O9b','O10','FE_AT','END','dl','d5','d6','d7','d8']: globals()[k]=T[k]
O='/mnt/user-data/outputs'; DL='/mnt/user-data/uploads/Downloads/'
D='/home/claude/allandouradocontato-creator/tutorialpet/data/vsl/natasha'
SEG='/tmp/p11/seg'; shutil.rmtree(SEG,ignore_errors=True); os.makedirs(SEG); os.makedirs('/tmp/p11/cap',exist_ok=True)
V18=DL+'VSL_Sozinho_em_Casa/teste_v2_v5/v18/vsl_c1_culpa_B_v18_natasha_1080.mp4'
N='/tmp/p11/clips/'
C={'C1':DL+'Caramel_dog_waiting_by_door_a405e05d.mp4','C2':DL+'Dog_sitting_among_feathers_af874c50.mp4','C3':DL+'Dog_sitting_and_lying_down_5603756d.mp4','C4':DL+'Woman_looking_at_dog_with_f9343197.mp4','T':O+'/porta5/porta5_flow_thor_neutro_porta_v2.mp4','P':D+'/scripts/produto_anim2.mp4','V2':'/tmp/p8/V2.mp4','V3':'/tmp/p8/V3.mp4','V4':'/tmp/p8/V4.mp4','V5':'/tmp/p8/V5.mp4','F':V18,
 'JS':DL+'Dog_jumps_onto_sofa_2e10365b.mp4','PW':DL+'Puppy_wakes_tired_woman_0adcaac7.mp4','DS':DL+'Dog_paces_and_scratches_door_26711b26.mp4','WD':DL+'Woman_working_with_dog_on_273fd071.mp4','DO':DL+'Woman_opening_apartment_door_36d8a8cd.mp4',
 'f_b1':N+'f_b1_filhote_corre.mp4','f_b2':N+'f_b2_carol_brinca_filhote.mp4','f_n':N+'f_n_primeira_noite.mp4','f_s':N+'f_s_choro_banheiro_v2.mp4','f_d1':N+'f_d1_thor_chinelo.mp4','f_d2':N+'f_d2_thor_manta.mp4',
 'f3b':N+'f3b_babacam_circulos.mp4','f_g':N+'f_g_corredor_vizinho.mp4','f_h':N+'f_h_porta_tensa.mp4','R1':N+'f_r1_casa_arrumada_thor_calmo.mp4','f5':N+'f5_noite_celular.mp4','f_r':N+'f_r_controle_remoto.mp4'}
C['Db']=DL+'Dog_pacing_by_door_bd053778.mp4'; C['Tb']=C['T']
ZM={'P':0.10}
NANNY={'Tb','Db','DS','f3b'}
OV={'iR':('/tmp/p7/card_preco_v3.png',(120,380,840,740)),'iG':('/tmp/p7/card_garantia_crmv.png',(120,380,840,845))}
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
DUR={k:dur(v) for k,v in C.items()}
p2=T['pos2']; L9a=T['L9a']; L9b=T['L9b']
def mo(r):
    if r<2.35: return r
    if r<6.55: return p2[2]+(r-4.15)*L9a/2.4
    if r<8.65: return p2[3]+(r-6.55)
    if r<13.65: return p2[5]+(r-11.15)
    if r<17.62: return p2[6]+(r-13.65)*L9b/3.97
    return p2[7]+(r-17.62)
def mo8(r):
    if r<18.32: return r
    if r<20.46: return pos8[1]+(r-18.38)
    return pos8[2]+(r-20.46)
q=lambda r:O7+mo(r)
q8=lambda r:O8+mo8(r)
B5M=T['b5map']
def g5(t):  # tempo antigo no B5 -> novo (take A)
    import bisect
    xs=[a for a,b in B5M]
    if t<=xs[0]: return B5M[0][1]
    if t>=xs[-1]: return B5M[-1][1]+(t-xs[-1])
    i=bisect.bisect_right(xs,t)-1; (a0,b0),(a1,b1)=B5M[i],B5M[i+1]
    return b0+(t-a0)*(b1-b0)/(a1-a0)
# (tempo, clipe, ss, stretch, overlay)
S=[(0,'C4',3.3),(3.0,'JS',.3),(6.0,'V4',1.8),(11.6,'f_b1',0),(15.5,'f_b2',0),(19.9,'V2',0),(23.4,'PW',.2),(27.2,'f_d1',0),(30.4,'f_n',0),(33.2,'C3',.5),
(36.0,'V3',0),(40.5,'f_d2',0),(44.0,'C4',3.0),(48.4,'f_d1',3.3),(50.9,'C1',.3),(54.5,'C2',.5),(59.3,'f_d2',4.1),(63.0,'f_s',1.0),
(T['pos1'][2],'f_d1',2.9),(71.0+dl,'Tb',.3),(74.0+dl,'DS',.3),(T['pos1'][3]+1.9,'f3b',1.3),(83.0,'Db',2.0),
(A_END,'f5',0),(O7+p2[2],'f_d2',.2),(O7+p2[3],'C2',.5),(O7+p2[5],'C4',3.5),(O7+p2[6],'V5',4.5),(q(16.3),'V5',6.0),(q(17.6),'V4',3.0),(q(19.88)-0.18,'Db',.5),
(O8,'P',0),(O8+3.2,'f_b2',2.4),(O8+8.7,'f_r',2.8),(O8+12.2,'C4',4.0),(O8+16.0,'WD',.3),(O8+19.2,'C1',.5),(q8(20.5),'C2',2.0),
(O9,'f_g',0),(O9+g5(3.0),'f_g',5.1),(O9+g5(5.75),'f_h',.4),(O9+g5(9.6),'f_h',4.25),(O9+g5(11.0),'f3b',2.2),(O9+g5(13.3),'f_h',5.65),(O9+d5-2.3,'DO',0),(O9+d5,'K',0),
(O9b,'R1',0),(O9b+7.9,'DO',2.6),
(O10,'f_r',3.7),(O10+4.1,'f_b2',3.0),(O10+7.3,'P',0),(O10+10.5,'WD',5.5),(O10+12.4,'f_b1',.5),(O10+13.25,'C3',1.0),(O10+13.95,'C1',1.0),(O10+14.65,'C2',1.0),(O10+15.5,'WD',2.8),
(O10+20.4,'T',.5,1,'iR'),(O10+23.8,'f_b1',3.0,1,'iG'),(T['FE_AT'],'F',52.06,1.06)]
S=[(s+(None,)*(5-len(s))) if len(s)<5 else s for s in S]
S=[(a,k,ss,(st or 1.0),ov) for a,k,ss,st,ov in S]
S.sort(key=lambda s:s[0]); END=T['END']
fnt='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
EQ="eq=contrast=1.05:saturation=1.1"
fr=lambda t:int(round(t*30))
paths=[]; log=[]
for i,(a,k,ss,st,ov) in enumerate(S):
    b=S[i+1][0] if i+1<len(S) else END
    n=fr(b)-fr(a); L=n/30
    out=f'{SEG}/s{i:02d}.mp4'; src=L/st
    if k!='K':
        if ss+src>DUR[k]-0.05+1e-6:
            need=L/(DUR[k]-ss-0.05)
            if need<=1.15: st=round(need+0.005,3); src=L/st
            else: raise SystemExit(f'FREEZE seg {i} {k} t={a:.2f} L={L:.2f} ss={ss} dur={DUR[k]:.2f}')
        assert ss+src<=DUR[k]-0.05+1e-6,(i,k)
    if k=='K':
        cmd=['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','color=c=black:s=1080x1920:r=30','-frames:v',str(n),'-pix_fmt','yuv420p','-c:v','libx264','-crf','18',out]
    else:
        base=f"scale=1080:1920:flags=lanczos,setsar=1,fps=30,setpts={st}*PTS"
        if k in ZM: base+=f",scale=w='1080*(1+{ZM[k]}*t/{L:.3f})':h=-2:eval=frame,crop=1080:1920,setsar=1"
        if k in NANNY:
            base+=f",eq=contrast=1.15:saturation=0.55:brightness=-0.04,noise=alls=24:allf=t,vignette=PI/3.2,drawtext=fontfile={fnt}:text='REC':x=70:y=90:fontsize=48:fontcolor=red:borderw=3:bordercolor=black,drawtext=fontfile={fnt}:text='CAM 01  03\\:12\\:07':x=70:y=1800:fontsize=40:fontcolor=white:borderw=3:bordercolor=black"
        elif k not in ('P','F'): base+=','+EQ
        if ov:
            png,(x,y,w,h)=OV[ov]
            fc=f"[0:v]{base},format=yuv420p[b];[1:v]crop={w}:{h}:{x}:{y},scale=760:-1,format=rgba,colorchannelmixer=aa=0.97[c];[b][c]overlay=(W-w)/2:300:format=auto,format=yuv420p[o]"
            cmd=['ffmpeg','-y','-loglevel','error','-ss',str(ss),'-t',f'{src+0.1:.3f}','-i',C[k],'-i',png,'-filter_complex',fc,'-map','[o]','-frames:v',str(n),'-an','-c:v','libx264','-crf','18',out]
        else:
            cmd=['ffmpeg','-y','-loglevel','error','-ss',str(ss),'-t',f'{src+0.1:.3f}','-i',C[k],'-vf',base+',format=yuv420p','-frames:v',str(n),'-an','-c:v','libx264','-crf','18',out]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print('ERR',i,k,r.stderr[-300:])
    got=int(subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v','-show_entries','stream=nb_read_frames','-of','csv=p=0',out],capture_output=True,text=True).stdout or 0)
    if got!=n: print('FRAMES',i,k,n,got)
    paths.append(out); log.append(dict(i=i,t=round(a,2),end=round(b,2),clip=k,ss=ss,stretch=st,src_len=round(src,2),overlay=ov))
json.dump(log,open('/tmp/p11/seglog.json','w'),indent=0)
open('/tmp/p11/list.txt','w').write(''.join(f"file '{p}'\n" for p in paths))
# ---- legendas
words=T['words']
def manual(k,off,blocks,wf):
    w=json.load(open(f'/tmp/p11/voz/w_{k}.json')); out=[]
    for a,b,t in blocks: out.append([w[a][0]+off,w[b][1]+off,t])
    return out
man=[]
man+=manual('B5A',O9,[(0,1,'Dia catorze.'),(2,4,'Oito horas fora.'),(5,8,'No corredor, o vizinho:'),(9,12,'Você doou o Thor?'),(13,18,'Faz tempo que eu não ouço'),(19,21,'nem o latido dele.'),(22,23,'Ela gelou.'),(24,26,'Será que fugiu?'),(27,31,'Será que aconteceu alguma coisa?'),(32,36,'Ela abriu a porta devagar…'),(37,42,'e adivinha o que ela viu?')],0)
man+=manual('B6',O9b,[(0,2,'Ele estava bem.'),(3,5,'Tranquilo, no sofá.'),(6,9,'E a casa… inteira!'),(10,11,'Nada rasgado,'),(12,13,'nada arranhado.'),(14,16,'Não era manha.'),(17,18,'Era medo.'),(19,21,'E medo passa.')],0)
man+=manual('B7',O10,[(0,2,'O controle remoto'),(3,8,'nunca mais foi parar na geladeira.'),(9,10,'Não precisou!'),(11,12,'Sorte? Não.'),(13,16,'Foi ela que fez.'),(17,22,'Em casa, dez minutos por dia,'),(23,28,'com o manual e o aplicativo'),(29,32,'do Sozinho em Casa.'),(33,34,'Filhote, idoso,'),(35,38,'vira-lata ou de raça.'),(39,41,'O aplicativo monta'),(42,46,'o plano para o seu.'),(47,48,'Sem adestrador,'),(49,52,'sem gastar mais nada.'),(53,54,'De noventa e sete,'),(55,58,'por apenas vinte e sete reais.'),(59,63,'E se em catorze dias'),(64,66,'você não gostar,'),(67,68,'devolvemos tudo.')],0)
# B4 manual (palavras: 0 Na 1 camera 2 ela 3 viu 4 o 5 fegante 6 andando 7 em 8 circulos 9 ou 10 seja 11 o 12 seu 13 amiguinho 14 sozinho 15 sofrendo)
p3=T['pos1'][1]; p4=T['pos1'][3]
def span(k): w=json.load(open(f'/tmp/p11/voz/w_{k}.json')); return max(0,w[0][0]-0.06)
def man2(k,pos,blocks):
    w=json.load(open(f'/tmp/p11/voz/w_{k}.json')); a=span(k); return [[w[x][0]-a+pos,w[y][1]-a+pos,t] for x,y,t in blocks]
man+=man2('B4',p4,[(0,3,'Na câmera, ela viu:'),(4,8,'ofegante, andando em círculos.'),(9,10,'Ou seja:'),(11,13,'o seu amiguinho,'),(14,15,'sozinho, sofrendo.')])
# remove palavras automáticas já cobertas por B4/B5/B6/B7 (usamos só as de ato1/B7b/B8 + B3/B1/B2)
words=[w for w in words if w[0]<p4-0.01 or (w[0]>=O7-0.01 and w[0]<O9-0.01)]
words.sort(key=lambda w:w[0])
blocks=[];cur=[]
for w in words:
    cur.append(w); txt=' '.join(x[2] for x in cur)
    if w[2][-1] in ',.?!' or len(txt)>60: blocks.append(cur);cur=[]
if cur: blocks.append(cur)
fin=[]
for b in blocks:
    txt=' '.join(x[2] for x in b)
    if len(txt)>48: m=len(b)//2; fin+=[b[:m],b[m:]]
    else: fin.append(b)
caps=[[b[0][0],b[-1][1]+0.15,' '.join(x[2] for x in b)] for b in fin]
for a,e,t in man: caps.append([a,e+0.1,t])
caps.sort(key=lambda c:c[0])
for j in range(len(caps)-1): caps[j][1]=min(caps[j][1],caps[j+1][0]-0.02)
out=[]
for a,e,txt in caps:
    if len(txt)>24:
        ws=txt.split(' '); best=None
        for qq in range(1,len(ws)):
            l1=' '.join(ws[:qq]);l2=' '.join(ws[qq:]); d=abs(len(l1)-len(l2))
            if best is None or d<best[0]: best=(d,l1,l2)
        lines=[best[1],best[2]]
    else: lines=[txt]
    out.append((a,e,lines))
caps=out
json.dump(caps,open('/tmp/p11/caps.json','w'),ensure_ascii=False)
hooks=[(9.9,11.6),(21.8,23.5),(30.6,32.5),(48.7,50.7),(60.0,62.9),(68.8+dl,70.8+dl),
(q(16.3),q(17.6)),(q(19.88)-0.9,q(19.88)+0.5),(q8(20.4),q8(24.0)),(O9+g5(4.5),O9+g5(5.7)),(O9+g5(8.8),O9+g5(10.0)),(O9b,O9b+1.5),(O10,O10+1.8),(O10+20.9,O10+22.2)]
Z='+'.join(f"between(t,{a:.2f},{b:.2f})*0.12*(t-{a:.2f})/({b:.2f}-{a:.2f})" for a,b in hooks)
dt=[]
for j,(a,e,lines) in enumerate(caps):
    if O9+d5-0.02<a<O9b: continue
    for qq,l in enumerate(lines):
        fn=f'/tmp/p11/cap/c{j}_{qq}.txt'; open(fn,'w').write(l)
        dt.append(f"drawtext=fontfile={fnt}:textfile={fn}:fontsize=64:fontcolor=white:borderw=7:bordercolor=black:x=(w-text_w)/2:y=h*0.66+{qq*82}:enable='between(t,{a:.2f},{e:.2f})'")
vf=f"scale=w='1080*(1+{Z})':h=-2:eval=frame,crop=1080:1920,setsar=1,{','.join(dt)}"
open('/tmp/p11/vf.txt','w').write(vf)
print('segs',len(S),'END',END)
if os.environ.get('FINAL')=='1':
    BL0=O9+d5; BL1=O9b
    fc=f"[0:v]{open('/tmp/p11/vf.txt').read()}[v0];[1:v]setpts=PTS+{O8:.3f}/TB[b];[v0][b]overlay=x=(W-w)/2:y=1550:enable='between(t,{O8:.2f},{END})*not(between(t,{BL0:.3f},{BL1:.3f}))':eof_action=pass,format=yuv420p[o]"
    open('/tmp/p11/fc.txt','w').write(fc)
    r=subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i','/tmp/p11/list.txt','-stream_loop','-1','-i','/tmp/p11/btn.mov','-filter_complex_script','/tmp/p11/fc.txt','-map','[o]','-t',str(END),'-an','-r','30','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','/tmp/p11/long_v.mp4'],capture_output=True,text=True);print(r.stderr[-800:])

    # ---- gate de movimento v8: janelas de 1 s >= 3.0 (>= 2.5 dentro de clipes nanny-cam); preto proposital ignorado
    import numpy as np
    btn=os.environ.get('BTN')
    raw=subprocess.run(['ffmpeg','-v','error','-i','/tmp/p11/long_v.mp4','-vf','fps=10,scale=108:192,format=gray','-f','rawvideo','-'],capture_output=True).stdout
    a=np.frombuffer(raw,np.uint8).reshape(-1,108*192).astype(np.float32); d=np.abs(a[1:]-a[:-1]).mean(1)
    def seg_at(t):
        k=None
        for (aa,kk,*_) in S:
            if aa<=t: k=kk
        return k
    low=[]
    for i in range(0,len(d)-9,5):
        m=float(d[i:i+10].mean()); k=seg_at(i/10+0.5); th=2.5 if k in NANNY else 3.0
        if m<th and a[i].mean()>8: low.append((i/10,round(m,2),k))
    print('MOTION-GATE janelas fracas:',low)
    json.dump(low,open('/tmp/p11/motion_gate.json','w'))
