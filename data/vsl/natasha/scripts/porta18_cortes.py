# porta18_cortes.py: PORTA 18 — Corte Resumo (<60 s)
import subprocess,os,json,sys,re,numpy as np
sys.path.insert(0,'/tmp/p11')
from cortes14 import snap_start,snap_end,SIL,T,FE,END,BL0,BL1,CAPS
from norm14 import normalize_mux,measure,sh
OUT=os.environ.get('OUT','/mnt/user-data/outputs/porta18'); os.makedirs(OUT,exist_ok=True); W='/tmp/p11/c18/'; os.makedirs(W,exist_ok=True)
V='/tmp/p11/voz/'; DL='/mnt/user-data/uploads/Downloads/'; SFX='/tmp/p7/sfx/'
fnt='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
def lufs(f,ss=None,t=None):
    c=['ffmpeg','-nostats','-hide_banner']+(['-ss',str(ss),'-t',str(t)] if ss is not None else [])+['-i',f,'-af','ebur128','-f','null','-']
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS',subprocess.run(c,capture_output=True,text=True).stderr)[-1])
REF=lufs('/tmp/p11/voz14.wav',170.86,13.3)
# ---------- pontes: voz
BR={}
def wend(k,idx,post=0.10):
    w=json.load(open(V+f'w_{k}.json')); return w[idx][2]+post
raw=lambda f:np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
def energy_end(f,a,b):
    y=raw(f);h=160;n=len(y)//h;r=np.sqrt((y[:n*h].reshape(n,h)**2).mean(1));thr=r.max()*10**(-35/20)
    for i in range(int(a*100),min(n,int(b*100))):
        if r[i]<thr: return i*0.01+0.05
    return b
SPEC={'P1f':(0,None),'P4':(0,None),'P5':(0,None),'P3':(0,'short'),'P3full':(0,None),'P5s':(0,None)}
BASE={'P1':'P1','P1f':'P1','P2':'P2','P3full':'P3','P3':'P3','P4':'P4','P5':'P5','P5s':'P5s'}
def mkvoice(name):
    bn=BASE[name]; lead=0.0 if name=='P1f' else 0.10
    src=V+bn+'.mp3'; w=json.load(open(V+f'w_{bn}.json'))
    if name=='P3': end=energy_end(src,w[2][2],w[3][1])
    else: end=min(dur(src),w[-1][2]+0.12); end=energy_end(src,w[-1][2],w[-1][2]+0.4) if name!='P3full' else end
    g=max(-6,min(6,REF-lufs(src)))
    L=lead+end+0.04
    f=W+f'v_{name}.wav'
    sh(['ffmpeg','-y','-loglevel','error','-i',src,'-af',f'volume={g}dB,atrim=0:{end:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={end-0.03:.3f}:d=0.03,adelay={int(lead*1000)},apad=whole_dur={L:.3f},aformat=channel_layouts=mono','-ar','44100',f])
    return dict(name=name,voice=f,L=L,end=end,gain=round(g,1),lead=lead)
for n in SPEC: BR[n]=mkvoice(n); print(BR[n])
# ---------- pontes: vídeo (sem legenda) a partir de clipes/segmentos limpos
EQ='eq=contrast=1.05:saturation=1.1'
base=lambda ss,L:f"scale=1080:1920:flags=lanczos,setsar=1,fps=30"
NANNY=f"eq=contrast=1.15:saturation=0.55:brightness=-0.04,noise=alls=24:allf=t,vignette=PI/3.2,drawtext=fontfile={fnt}:text='REC':x=70:y=282:fontsize=36:fontcolor=red:borderw=3:bordercolor=black,drawtext=fontfile={fnt}:text='CAM 01  03\\:12\\:07':x=w-text_w-70:y=286:fontsize=32:fontcolor=white:borderw=3:bordercolor=black"
def enc(args,out): sh(['ffmpeg','-y','-loglevel','error']+args+['-an','-r','30','-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p',out])
def clip(src,ss,L,vf,out): enc(['-ss',str(ss),'-t',f'{L+0.1:.3f}','-i',src,'-vf',f'{vf},format=yuv420p,trim=duration={L:.3f},setpts=PTS-STARTPTS'],out)
def clean(a,L,out): enc(['-f','concat','-safe','0','-i','/tmp/p11/list.txt','-ss',f'{a:.3f}','-t',f'{L:.3f}','-vf','format=yuv420p'],out)
def cat(parts,out):
    open(out+'.txt','w').write(''.join(f"file '{p}'\n" for p in parts)); sh(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',out+'.txt','-c','copy',out])
def vid(name):
    L=BR[name]['L']; o=W+f'raw_{name}.mp4'; Lf=round(L*30)/30
    if name in ('P1','P1f'):
        clip(DL+'Dog_jumps_onto_sofa_2e10365b.mp4',0,1.5,f"{base(0,1.5)},{EQ}",W+'a.mp4'); clip(DL+'Dog_paces_and_scratches_door_26711b26.mp4',0.3,Lf-1.5,f"{base(0,0)},{NANNY}",W+'b.mp4'); cat([W+'a.mp4',W+'b.mp4'],o)
    elif name=='P2':
        clean(69.02,2.3,W+'a.mp4'); z=0.10; clip('/home/claude/allandouradocontato-creator/tutorialpet/data/vsl/natasha/scripts/produto_anim2.mp4',0,Lf-2.3,f"scale=1080:1920:flags=lanczos,setsar=1,fps=30,scale=w='1080*(1+{z}*t/{Lf-2.3:.3f})':h=-2:eval=frame,crop=1080:1920,setsar=1",W+'b.mp4'); cat([W+'a.mp4',W+'b.mp4'],o)
    elif name.startswith('P3'): clip('/tmp/p11/clips/f_h3_corredor_abrindo.mp4',0.6,Lf,f"{base(0,0)},{EQ}",o)
    elif name=='P4': clean(87.10,Lf,o)
    elif name=='P5s': clip('/home/claude/allandouradocontato-creator/tutorialpet/data/vsl/natasha/scripts/produto_anim2.mp4',0,Lf,f"scale=1080:1920:flags=lanczos,setsar=1,fps=30,scale=w='1080*(1+0.10*t/{Lf:.3f})':h=-2:eval=frame,crop=1080:1920,setsar=1",o)
    elif name=='P5':
        clean(101.0,1.3,W+'a.mp4'); z=0.10; clip('/home/claude/allandouradocontato-creator/tutorialpet/data/vsl/natasha/scripts/produto_anim2.mp4',0,Lf-1.3,f"scale=1080:1920:flags=lanczos,setsar=1,fps=30,scale=w='1080*(1+{z}*t/{Lf-1.3:.3f})':h=-2:eval=frame,crop=1080:1920,setsar=1",W+'b.mp4'); cat([W+'a.mp4',W+'b.mp4'],o)
    return o
for n in BR: BR[n]['raw']=vid(n)
# ---------- legenda das pontes (zona por YOLO)
from ultralytics import YOLO
ym=YOLO('/tmp/p13/yolov8n.pt'); YT,YB=330,930
def zone(f,a,e):
    fr=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-vf','fps=5,scale=360:640','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout,np.uint8).reshape(-1,640,360,3)
    res=ym(list(fr),imgsz=480,conf=0.25,classes=[0,16],verbose=False); sc={'T':0,'B':0}
    for i,r in enumerate(res):
        if not (a*5<=i<=e*5): continue
        m=np.zeros((640,360),bool)
        for x0,y0,x1,y1,cf,c in r.boxes.data.cpu().numpy(): m[int(y0):int(y1 if int(c)==16 else y0+0.32*(y1-y0)),int(x0):int(x1)]=True
        for k,y in (('T',YT),('B',YB)): sc[k]+=m[int(y/3):int((y+160)/3),int(0.06*360):int(0.94*360)].mean()
    return 'T' if sc['T']<=sc['B'] else 'B'
_cp=[(0,3.6,['Seu cachorro late ou destrói','tudo quando você sai?'])]
CAPB={'P1':_cp,'P1f':_cp,'P2':[(0,2.3,['A Carol quase doou o Thor.']),(2.54,4.9,['Até descobrir','o Sozinho em Casa.'])],
'P3':[(0,BR['P3']['L'],['Catorze dias depois,'])],'P3full':[(0,BR['P3full']['L'],['Catorze dias depois,','ela abriu a porta.'])],'P4':[(0,BR['P4']['L'],['A Carol tentou de tudo','pelo Thor.'])],'P5s':[(0,BR['P5s']['L'],['E achou','o Sozinho em Casa.'])],'P5':[(0,1.3,['Ela pesquisou.']),(1.46,BR['P5']['L'],['E achou','o Sozinho em Casa.'])]}
for n,b in BR.items():
    L=b['L']; dts=[]
    for j,(a,e,ls) in enumerate(CAPB[n]):
        z=zone(b['raw'],a,min(e,L)); y0=YT if z=='T' else YB; e=min(e,L)
        for q,l in enumerate(ls):
            fn=W+f'cap_{n}_{j}_{q}.txt'; open(fn,'w').write(l)
            dts.append(f"drawtext=fontfile={fnt}:textfile={fn}:fontsize=64:fontcolor=white:borderw=7:bordercolor=black:x=(w-text_w)/2:y={y0+q*82}:enable='between(t,{a:.2f},{e:.2f})'")
    b['vid']=W+f'br_{n}.mp4'; enc(['-i',b['raw'],'-vf',','.join(dts)+',format=yuv420p'],b['vid']); b['dur']=dur(b['vid'])
    print(n,'vídeo',round(b['dur'],2),'voz L',round(L,2))
# bed (música) para pontes: trecho só-música do bed da longa (2–8 s) + sfx
def bridge_bed(name,Lneed,out):
    fl=['[0:a]atrim=2.0:%.3f,asetpts=PTS-STARTPTS[m]'%(2.0+Lneed)]; ins=['-i','/tmp/p11/bed2.wav']; lab='[m]'; k=1
    sf={'P1':[(0.0,'sfx_bass_hit',-1)],'P1f':[(0.0,'sfx_bass_hit',-1)],'P2':[(2.3,'sfx_chimes_vitoria',-6)],'P5':[(1.5,'sfx_chimes_vitoria',-6)],'P5s':[(0.1,'sfx_chimes_vitoria',-6)]}.get(name,[])
    for t,n,db in sf:
        ins+=['-i',SFX+n+'.mp3']; fl.append(f'[{k}:a]aresample=44100,aformat=channel_layouts=stereo,volume={db}dB,adelay={int(t*1000)}|{int(t*1000)}[s{k}]'); lab+=f'[s{k}]'; k+=1
    fl.append(f'{lab}amix=inputs={k}:normalize=0:duration=first[o]')
    sh(['ffmpeg','-y','-loglevel','error']+ins+['-filter_complex',';'.join(fl),'-map','[o]','-t',f'{Lneed:.3f}','-ar','44100',out])
# ---------- montagem
def plan(items):
    P=[]
    for it in items:
        if it[0]=='B': P.append(dict(kind='B',name=it[1],a=0,b=BR[it[1]]['L'],sa=None,ea=None,sb=None,eb=None)); continue
        a,b=it[1],it[2]
        if a==0: A,sa,ea=0.0,None,None
        else: A,sa,ea,_=snap_start(a)
        if BL0-0.01<=A<BL1: A=BL1-0.12
        if b>=END-1e-6: B,sb,eb=END,None,None
        else: B,sb,eb,_=snap_end(b)
        if P and P[-1]['kind']=='L' and 0<=A-P[-1]['b']<0.35: P[-1]['b']=B;P[-1]['sb']=sb;P[-1]['eb']=eb
        else: P.append(dict(kind='L',a=A,b=B,sa=sa,ea=ea,sb=sb,eb=eb))
    return P
CUT={'corte_resumo':[('B','P1f'),('L',2.92,5.75),('B','P4'),('L',92.98,95.72),('L',74.46,79.68),('L',104.48,109.33),('B','P5'),('B','P3'),('L',147.58,151.62),('L',152.04,153.24),('L',155.30,157.34),('L',168.14,175.80),('L',184.24,END)]}
def build(name,items):
    P=plan(items)
    for p in P:
        if p['kind']=='B': p['a']=0;p['b']=BR[p['name']]['L']
    N=len(P); D=[]
    for i in range(N-1):
        m1=(P[i]['b']-P[i]['sb']) if P[i]['sb'] is not None else (0.15 if P[i]['kind']=='B' else 0.1)
        m2=(P[i+1]['ea']-P[i+1]['a']) if P[i+1]['ea'] is not None else (0.15 if P[i+1]['kind']=='B' else 0.1)
        D.append(round(max(0.08,min(0.15,m1,m2)),3))
    DB=0.4; fa=[]; ins=[]; k=0
    # cada peça: arquivos de voz e cama com comprimento exato
    vfiles=[];bfiles=[];vs=[];ve=[]
    for i,p in enumerate(P):
        h=0 if i==0 else DB/2-D[i-1]/2; t=0 if i==N-1 else DB/2-D[i]/2
        vs.append(p['a']+(D[i-1]/2 if i>0 else 0)); ve.append(p['b']-(D[i]/2 if i<N-1 else 0))
        if p['kind']=='L':
            vf=W+f'{name}_v{i}.wav'; bf=W+f'{name}_b{i}.wav'
            sh(['ffmpeg','-y','-loglevel','error','-i','/tmp/p11/voz14.wav','-af',f"atrim={p['a']:.4f}:{p['b']:.4f},asetpts=PTS-STARTPTS,aformat=channel_layouts=mono",'-ar','44100',vf])
            sh(['ffmpeg','-y','-loglevel','error','-i','/tmp/p11/bed2.wav','-af',f"atrim={max(0,p['a']-h):.4f}:{p['b']+t:.4f},asetpts=PTS-STARTPTS,aformat=channel_layouts=stereo",'-ar','44100',bf])
            p['pre']=p['a']-max(0,p['a']-h)
        else:
            b=BR[p['name']]; vf=b['voice']; bf=W+f'{name}_b{i}.wav'; bridge_bed(p['name'],b['L']+h+t,bf); p['pre']=0
        vfiles.append(vf);bfiles.append(bf)
    # voz: acrossfade D; cama: acrossfade DB (cada arquivo de cama tem h antes e t depois)
    def chain(files,Dl,tag):
        cur=files[0]
        for i in range(N-1):
            out=W+f'{name}_{tag}_{i}.wav'
            sh(['ffmpeg','-y','-loglevel','error','-i',cur,'-i',files[i+1],'-filter_complex',f'[0:a][1:a]acrossfade=d={Dl[i]}:c1=tri:c2=tri,aformat=channel_layouts=stereo[o]','-map','[o]','-ar','44100',out]); cur=out
        return cur
    cv=chain(vfiles,D,'vv'); cb=chain(bfiles,[DB]*(N-1),'bb')
    wav=W+f'{name}.wav'; sh(['ffmpeg','-y','-loglevel','error','-i',cv,'-i',cb,'-filter_complex','[0:a][1:a]amix=inputs=2:normalize=0:duration=longest[o]','-map','[o]','-ar','44100',wav])
    # vídeo
    inp=[];fv=[]
    for i,p in enumerate(P):
        if p['kind']=='L': inp+=['-ss',f'{vs[i]:.4f}','-t',f'{ve[i]-vs[i]:.4f}','-i','/tmp/p11/long_nb.mp4']
        else: inp+=['-ss',f'{(D[i-1]/2 if i>0 else 0):.4f}','-t',f'{ve[i]-vs[i]:.4f}','-i',BR[p['name']]['vid']]
        fv.append(f'[{i}:v]setpts=PTS-STARTPTS[v{i}]')
    adur=sum(e-s for s,e in zip(vs,ve))
    fv.append(''.join(f'[v{i}]' for i in range(N))+f'concat=n={N}:v=1:a=0[c]')
    t=0;hide=''
    for i,p in enumerate(P):
        if p['kind']=='L' and vs[i]<BL1 and ve[i]>BL0: hide+=f"*not(between(t,{t+max(0,BL0-vs[i]):.3f},{t+min(ve[i],BL1)-vs[i]:.3f}))"
        t+=ve[i]-vs[i]
    fv.append(f"[c][{N}:v]overlay=x=(W-w)/2:y=1100:enable='1{hide}':eof_action=pass,format=yuv420p[o]")
    vid=W+f'{name}_v.mp4'
    sh(['ffmpeg','-y','-hide_banner','-loglevel','error']+inp+['-stream_loop','-1','-i','/tmp/p11/orange.mov','-filter_complex',';'.join(fv),'-map','[o]','-t',f'{adur:.3f}','-an','-r','30','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',vid])
    out=f'{OUT}/porta18_{name}.mp4'; I,PK,tp=normalize_mux(vid,wav,out)
    sh(['ffmpeg','-y','-loglevel','error','-i',out,'-vf','scale=-2:640','-c:v','libx264','-crf','30','-preset','veryfast','-c:a','aac','-b:a','96k',out.replace('.mp4','_leve.mp4')])
    dv=dur(out); tj=[];c=0
    for i in range(N-1): c+=ve[i]-vs[i]; tj.append(round(c,3))
    rep=dict(name=name,dur=round(dv,2),I=I,TP=PK,parts=[[p['kind'],p.get('name'),round(p['a'],3),round(p['b'],3)] for p in P],D=D,vs=vs,ve=ve,juncoes=tj,
      margens=[[None if P[i]['sb'] is None else round(P[i]['b']-P[i]['sb'],3),None if P[i+1]['ea'] is None else round(P[i+1]['ea']-P[i+1]['a'],3)] for i in range(N-1)])
    json.dump(rep,open(W+f'{name}.json','w'),ensure_ascii=False,indent=1); print(name,rep['dur'],I,PK,rep['parts'],D,rep['margens'],flush=True)
if __name__=='__main__':
    for nm in (sys.argv[1:] or CUT): build(nm,CUT[nm])
