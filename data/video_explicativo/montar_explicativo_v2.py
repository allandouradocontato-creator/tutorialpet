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
# (tipo, arquivo, início do clipe)
DC=lambda n:f'{H}/duda_clips_heygen/{n}.mp4'
S={'1':[('dclip',DC('gancho'),0,2.78)],
'2':[('img',pg('01'),0),('app',app('04'),0)],
'3':[('img',pg('02'),0),('img',pg('03'),0),('img',pg('04'),0),('img',pg('05'),0),('img',pg('06'),0)],
'4':[('dclip',DC('app_celular'),0,6.0),('app',app('04'),0),('app',app('03'),0),('app',app('05'),0)],
'5':[('app',app('10'),0),('app',app('11'),0),('app',app('12'),0),('app',app('14'),0),('app',app('13'),0)],
'6':[('img',g(f'bonus/kit_capa*'),0),('img',g(f'bonus/kit_faro*'),0),('img',g(f'bonus/pnp_capa*'),0),('img',g(f'bonus/pnp_semaforo*'),0),('img',g(f'bonus/pnp_chocolate*'),0)],
'7':[('clip',cl('6477490'),3.0,3.5),('clip',cl('7676931'),0.5,3.5),('clip',cl('8730835'),4.0,3.5),('dclip',DC('climax'),0,8.5),('clip',cl('7682708'),3.0),('clip',cl('7676931'),6.0),('clip',cl('8730835'),9.0),('clip',cl('7682708'),9.0),('img',pg('07'),0)],
'8':[('dclip',DC('oferta'),0,13.6)]}
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
    ch=cap_chunks(k);tot=sum(len(c) for c in ch);tt=t+0.1
    for c in ch:
        sg=(D[k]-0.25)*len(c)/tot;fn=f'{W}/c{len(caps)}.txt';open(fn,'w').write(c);caps.append((fn,tt,tt+sg));tt+=sg
    t+=D[k]
open(f'{W}/lista.txt','w').write(''.join(f"file '{s}'\n" for s in shots))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{W}/lista.txt','-c','copy',f'{W}/mudo.mp4'],check=True)
inp=['-i',f'{W}/mudo.mp4'];fc=[];lab=[];tt=0.0
for i,k in enumerate(F):
    inp+=['-i',aud[k]];ms=int((tt+0.1)*1000);fc.append(f'[{i+1}:a]adelay={ms}|{ms}[a{i}]');lab.append(f'[a{i}]');tt+=D[k]
fc.append(''.join(lab)+f'amix=inputs={len(F)}:normalize=0[ao]')
dt=','.join(f"drawtext=fontfile={FONT}:textfile={fn}:fontsize=46:fontcolor=white:borderw=4:bordercolor=#1B1464:line_spacing=10:x=(w-text_w)/2:y=1030:enable='between(t,{a:.2f},{b:.2f})'" for fn,a,b in caps)
fc.append(f'[0:v]{dt}[v]')
subprocess.run(['ffmpeg','-v','error','-y']+inp+['-filter_complex',';'.join(fc),'-map','[v]','-map','[ao]','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k',out],check=True)
print('ok',out,round(t,1),'s',len(shots),'cenas')
