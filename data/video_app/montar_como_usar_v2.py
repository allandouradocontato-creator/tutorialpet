"""Monta o vídeo 'como usar o app' v2: telas gravadas + falas (ElevenLabs, voz da Duda) + legenda grande.
Uso: python montar_como_usar_v2.py <pasta_rec> <saida.mp4>"""
import json,subprocess,sys,glob,textwrap,os,re
rec,out=sys.argv[1],sys.argv[2]
here=os.path.dirname(os.path.abspath(__file__))
marks=json.load(open(f'{rec}/marcas.json'));falas=json.load(open(f'{here}/falas_v2.json'))
webm=glob.glob(f'{rec}/*.webm')[0]
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
keys=list(falas.keys())
def dur(k):
    return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{here}/audios_v2/como_usar_app_fala_{k.zfill(2)}.mp3'],capture_output=True,text=True).stdout)
OFF=float(os.environ.get('OFF','0.0'))
inputs=['-i',webm];fc=[];lab=[];dt=[]
for i,k in enumerate(keys):
    inputs+=['-i',f'{here}/audios_v2/como_usar_app_fala_{k.zfill(2)}.mp3']
    ms=int((marks[k]+OFF+0.15)*1000)
    fc.append(f'[{i+1}:a]adelay={ms}|{ms}[a{i}]');lab.append(f'[a{i}]')
    # legenda: quebra em frases e distribui pelo tempo da fala
    sents=[s.strip() for s in re.split(r'(?<=[.!?])\s+',falas[k]) if s.strip()]
    chunks=[]
    for s in sents:
        w=textwrap.wrap(s,23)
        for j in range(0,len(w),2):chunks.append('\n'.join(w[j:j+2]))
    tot=sum(len(c) for c in chunks);t=marks[k]+OFF+0.15;d=dur(k)
    for c in chunks:
        seg=d*len(c)/tot;fn=f'/tmp/gr/leg_{k}_{len(dt)}.txt';open(fn,'w').write(c)
        dt.append(f"drawtext=fontfile={FONT}:textfile={fn}:fontsize=42:fontcolor=#1B1464:line_spacing=10:x=(w-text_w)/2:y=1080:enable='between(t,{t:.2f},{t+seg:.2f})'")
        t+=seg
fc.append(''.join(lab)+f'amix=inputs={len(keys)}:normalize=0[aout]')
vf=f"[0:v]scale=560:-2,pad=720:1280:80:20:color=#FFF3E3,{','.join(dt)}[v]"
fc.append(vf)
subprocess.run(['ffmpeg','-v','error','-y']+inputs+['-filter_complex',';'.join(fc),'-map','[v]','-map','[aout]','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','128k',out],check=True)
print('ok',out)
