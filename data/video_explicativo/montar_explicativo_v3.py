"""Monta o vídeo explicativo da landing (9:16, 720x1280): Duda abre e fecha (cartão, versão grátis), miolo com e-book, clipes, app.
Uso: python montar_explicativo_v2.py <saida.mp4>   (falas em audios_v4/explicativo_fala_NN.mp3; imagens em app/, paginas_ebook/, clipes/)"""
import json,subprocess,sys,os,re,textwrap,glob
H=os.path.dirname(os.path.abspath(__file__));out=sys.argv[1];W=f'/tmp/gr/expl';os.makedirs(W,exist_ok=True)
F=json.load(open(f'{H}/falas_explicativo_v3.json'))
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';BG='0xFFF3E3'
def dur(p):return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
aud={k:f'{H}/audios_v4/explicativo_fala_{k.zfill(2)}.mp3' for k in F};D={k:dur(aud[k])+0.25 for k in F}
g=lambda pat:sorted(glob.glob(f'{H}/{pat}'))[0]
app=lambda n:g(f'app/app_sozinho_em_casa_{n}_*');pg=lambda n:g(f'paginas_ebook/*_{n}_*')
cl=lambda n:g(f'clipes/pexels_{n}_*')
DC=lambda n:f'{H}/duda_clips_heygen/{n}.mp4'
PET=lambda n:g(f'clipes_pets/pexels_{n}_*')
MUSICA=f'{H}/../../biblioteca/musica/gr0za-party-party-music-569750.mp3'  # mesma da VSL
# clipes fofos (gatos, filhotes, treino, carinho); banidos/descartados fora: 10164584, 30346566, 35556872, 8498743
CAT=[]  # produto só para cachorro: NUNCA gato
PUP=['13260951','14562775','17921122','35172441','9314159']
TRE=['7189527','7189535','7189541','7189598','7197703','7515913','7525615']
AFE=['6568510','6574015','6825849','7572163','8498665']
SS=[0.3,2.4,4.4,6.2];usados=set();idx={}
def pick(cats):
    # próximo trecho de clipe fofo ainda não usado, alternando entre as categorias
    i=idx.get(id(cats),0)
    for _ in range(400):
        c=cats[i%len(cats)];ss=SS[(i//len(cats))%len(SS)];i+=1
        if (c,ss) not in usados:
            usados.add((c,ss));idx[id(cats)]=i;return ('clip',PET(c),ss)
    raise SystemExit('sem clipes')
def mont(imgs,secs,cats,per=0.92):
    n=max(1,round(secs/per));out=[];k=0
    for i in range(n):
        if i%2==0:out.append(('img',imgs[k%len(imgs)],0));k+=1
        else:out.append(pick(cats))
    return out
def mont_clips(secs,cats,per=0.95):
    return [pick(cats) for _ in range(max(1,round(secs/per)))]
B=lambda n:g(f'bonus/{n}*')
P8=lambda n:g(f'paginas_v8/p{n}-*')
PRAT=[pg('03'),P8('11'),P8('12'),pg('04'),P8('16'),pg('05'),P8('17')]
TEO=[P8('27'),P8('29'),pg('06'),P8('33'),P8('35'),P8('37')]
Z={}
Z['1']=[('dclip',DC('gancho_duda_sozinha'),0,2.3),('mont',[pg('01')],None,[AFE])]
Z['2']=[('mont',[],0.42,[AFE,PUP]),('mont',[pg('01'),P8('02')],0.30,[TRE]),('mont',[app('04'),app('06')],None,[PUP])]
Z['3']=[('mont',PRAT,'S0',[TRE,PUP]),('mont',TEO,'S1',[AFE,PUP]),('mont',[P8('59'),P8('02'),P8('59')],'S2',[PUP,AFE])]
Z['4']=[('dclip',DC('app_junto'),0,5.02),('mont',[app('04'),app('03')],1.4,[PUP]),('mont',[app('05'),app('06'),app('07'),app('08')],None,[TRE,PUP,AFE])]
Z['5']=[('mont',[app('10'),app('11')],'S0',[TRE,PUP]),('mont',[app('12')],'W0.17',[PUP]),('mont',[app('14')],'W0.17',[AFE]),('mont',[app('13')],'W0.16',[PUP])]
Z['6']=[('mont',[B('kit_capa'),B('pnp_capa')],'S0',[PUP]),('mont',[B('kit_faro'),B('kit_planner'),B('kit_capa')],'S1',[PUP,AFE]),('mont',[B('pnp_capa'),B('pnp_semaforo'),B('pnp_chocolate')],'S2',[AFE,PUP])]
Z['7']=[('mont_clips',None,3.3,[AFE]),('mont_clips',None,3.6,[PUP,AFE]),('mont_clips',None,3.46,[AFE,PUP]),('dclip',DC('climax_duda_sozinha'),0,8.44),('mont_clips',None,11.8,[PUP,AFE,TRE]),('mont',[pg('07')],None,[PUP])]
OF=DC('oferta_duda_sozinha');SFX8=[];
def fecho():
    L=[('dclip',OF,0,10.4)];t=10.4;pup=[('13588264',0.5),('13588262',1.5),('14562775',2.0),('35172441',3.0),('8498665',1.0),('9314159',1.2)];i=0
    while 19.22-t>2.9:
        c,ss=pup[i%len(pup)];i+=1
        L.append(('clip',PET(c) if c in ('14562775','35172441','8498665','9314159') else f'/tmp/gr/grp/{c}.mp4',ss,0.9));SFX8.append(t);t+=0.9
        d=min(1.4,19.22-t-2.0);L.append(('dclip',OF,t,d));t+=d
    L.append(('dclip',OF,t,19.22-t));return L
Z['8']=fecho()
S={}
def sent_w(k):
    sents=[x for x in re.split(r'(?<=[.!?])\s+',re.sub(r'^\[\w+\]\s*','',F[k])) if x.strip()];n=[len(x) for x in sents];return [x/sum(n) for x in n]
for k,ents in Z.items():
    num=lambda e:(e[3] if e[0] in ('dclip','clip') else (e[2] if e[0].startswith('mont') and isinstance(e[2],(int,float)) else 0))
    fixed=sum(num(e) for e in ents);strs=[e for e in ents if e[0]=='mont' and isinstance(e[2],str)]
    nones=[e for e in ents if e[0].startswith('mont') and e[2] is None]
    Tfree=D[k]-fixed;SW=sent_w(k);wt=lambda e:(SW[int(e[2][1:])] if e[2][0]=='S' else float(e[2][1:]))
    tw=sum(wt(e) for e in strs) or 1;rem=Tfree/max(1,len(nones)) if nones else 0;L=[]
    for e in ents:
        if e[0] in ('dclip','clip'):L.append(e);continue
        sec=(Tfree*wt(e)/tw) if isinstance(e[2],str) else (e[2] if e[2] is not None else rem)
        if e[0]=='mont':items=mont(e[1],sec,e[3][0] if len(e[3])==1 else sum(e[3],[])) if e[1] else mont_clips(sec,sum(e[3],[]))
        else:items=mont_clips(sec,sum(e[3],[]))
        per=sec/len(items);L+=[it+(per,) for it in items]
    S[k]=L
def cap_chunks(k):
    sents=[s.strip() for s in re.split(r'(?<=[.!?])\s+',re.sub(r'^\[\w+\]\s*','',F[k])) if s.strip()];ch=[]
    for s in sents:
        w=textwrap.wrap(s,23)
        for j in range(0,len(w),2):ch.append('\n'.join(w[j:j+2]))
    return ch
shots=[];caps=[];t=0.0;n=0
for k in F:
    sh=S[k];fixed=sum(x[3] for x in sh if len(x)>3);free=[x for x in sh if len(x)<=3];per0=(D[k]-fixed)/max(1,len(free))
    for x in sh:
        typ,f,ss=x[:3];per=x[3] if len(x)>3 else per0
        o=f'{W}/s{n:03d}.mp4';n+=1
        if typ=='clip':
            vf=f"scale=-2:1280,crop=720:1280:(iw-720)/2:0,fps=30,setsar=1"
            cmd=['ffmpeg','-v','error','-y','-ss',str(ss),'-t',f'{per:.3f}','-i',f,'-vf',vf,'-an']
        elif typ=='dclip':
            cmd=['ffmpeg','-v','error','-y','-ss',str(ss),'-t',f'{per:.3f}','-i',f,'-vf','scale=720:1280,fps=30,setsar=1,tpad=stop_mode=clone:stop_duration=1','-t',f'{per:.3f}','-an']
        elif typ=='duda':
            cmd=['ffmpeg','-v','error','-y','-loop','1','-t',f'{per:.3f}','-i',f'{H}/duda_capa_cartao.jpg','-vf',
              f"scale=640:-2,pad=720:1280:40:260:color={BG},fps=30,drawtext=fontfile={FONT}:text='Duda · imagem criada com IA':fontsize=24:fontcolor=#9a8a78:x=(w-text_w)/2:y=830",'-an']
        else:
            sc=1100 if typ=='img' else 1040
            cmd=['ffmpeg','-v','error','-y','-loop','1','-t',f'{per:.3f}','-i',f,'-vf',f"scale=-2:{sc},zoompan=z='1+0.0006*on':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=-1x-1:fps=30,pad=720:1280:(720-iw)/2:30:color={BG}",'-an']
            cmd[cmd.index('-vf')+1]=f"scale=640:{sc}:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:30:color={BG},fps=30"
        cmd+=['-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p',o];subprocess.run(cmd,check=True);shots.append(o)
    # legendas
    ch=cap_chunks(k);tot=sum(len(c) for c in ch);tt=t
    for c in ch:
        sg=(D[k]-0.25)*len(c)/tot;fn=f'{W}/c{len(caps)}.txt';open(fn,'w').write(c);caps.append((fn,tt,tt+sg));tt+=sg
    t+=D[k]
open(f'{W}/lista.txt','w').write(''.join(f"file '{s}'\n" for s in shots))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{W}/lista.txt','-c','copy',f'{W}/mudo.mp4'],check=True)
inp=['-i',f'{W}/mudo.mp4'];fc=[];lab=[];tt=0.0
for i,k in enumerate(F):
    inp+=['-i',aud[k]];ms=int(tt*1000);fc.append(f'[{i+1}:a]adelay={ms}|{ms}[a{i}]');lab.append(f'[a{i}]');tt+=D[k]
fc.append(''.join(lab)+f'amix=inputs={len(F)}:normalize=0[vo]')
t8=sum(D[k] for k in F if k!='8');LAT=sorted(glob.glob('/home/claude/sozinho-em-casa-app/landing/app/som/real/latido*.mp3'));sx=[]
for j,tt0 in enumerate(SFX8):
    inp+=['-i',LAT[j%len(LAT)]];ms=int((t8+tt0)*1000);fc.append(f'[{len(F)+1+j}:a]atrim=0:0.9,volume=0.35,adelay={ms}|{ms}[x{j}]');sx.append(f'[x{j}]')
if sx:fc.append('[vo]'+''.join(sx)+f'amix=inputs={len(sx)+1}:normalize=0[vo2]')
else:fc.append('[vo]anull[vo2]')
inp+=['-stream_loop','-1','-i',MUSICA];mi=len(F)+1+len(SFX8);TT=sum(D.values())
fc.append(f'[{mi}:a]atrim=0:{TT:.2f},volume=0.13,afade=t=in:d=1,afade=t=out:st={TT-2.5:.2f}:d=2.5[mu]')
fc.append('[vo2][mu]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5[ao]')
dt=','.join(f"drawtext=fontfile={FONT}:textfile={fn}:fontsize=46:fontcolor=white:borderw=4:bordercolor=#1B1464:line_spacing=10:x=(w-text_w)/2:y=1030:enable='between(t,{a:.2f},{b:.2f})'" for fn,a,b in caps)
fc.append(f'[0:v]{dt}[v]')
subprocess.run(['ffmpeg','-v','error','-y']+inp+['-filter_complex',';'.join(fc),'-map','[v]','-map','[ao]','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-t',f'{TT-1.5:.2f}',out],check=True)
print('ok',out,round(t,1),'s',len(shots),'cenas')
