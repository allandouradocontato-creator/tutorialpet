import json, subprocess, os
from pathlib import Path
B="/mnt/user-data/uploads/Downloads/V1_completo_Duda_escovacao.mp4"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
info=json.load(open('clips/info2.json'))
def clip(k): return 'clips/'+info[k]['arq']
# (cena, duracao, texto, [fontes]) ; fontes = indice de clipe ou 'kit0'
CENAS=[
 (5.52,"Com que frequência\nescovar?",[8,11,12,15]),
 (5.32,"Ideal:\n1 vez ao dia",[0,19,20,22]),
 (8.00,"Mínimo:\n3x por semana",[24,25,3,26,27]),
 (5.96,"Apenas pasta\nveterinária",['kit0',34,38,47]),
 (6.20,"Consulte o\nmédico-veterinário",[29,23,42,2]),
]
VF="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30"
Path('seg').mkdir(exist_ok=True)
parts=[]
n=0
# gancho: 0 - 4.76 do base
subprocess.run(['ffmpeg','-v','error','-y','-i',B,'-t','4.76','-an','-vf','fps=30,setsar=1','-c:v','libx264','-crf','17','-preset','veryfast','seg/00_gancho.mp4'],check=True)
parts.append('seg/00_gancho.mp4')
for ci,(dur,txt,srcs) in enumerate(CENAS):
    per=dur/len(srcs)
    open(f'seg/t{ci}.txt','w',encoding='utf-8').write(txt)
    cuts=[]
    for j,s in enumerate(srcs):
        out=f'seg/c{ci}_{j}.mp4'
        d=per if j<len(srcs)-1 else dur-per*(len(srcs)-1)
        if s=='kit0':
            # foto do kit com zoom lento, sobre fundo claro (sem cara de slide parado: zoom + movimento)
            vf=("scale=1620:-2,zoompan=z='1.0+0.06*on/%d':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=%d:s=1080x1920:fps=30"%(int(d*30),int(d*30)+1))
            subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i','kit/foto_0.jpg','-t',f'{d:.3f}','-vf',"scale=-2:1920,crop=1080:1920,setsar=1,fps=30",'-an','-c:v','libx264','-crf','17','-preset','veryfast',out],check=True)
        else:
            subprocess.run(['ffmpeg','-v','error','-y','-ss','0.4','-t',f'{d:.3f}','-i',clip(s),'-an','-vf',VF,'-c:v','libx264','-crf','17','-preset','veryfast',out],check=True)
        cuts.append(out)
    lst=f'seg/l{ci}.txt'; open(lst,'w').write(''.join(f"file '{os.path.abspath(c)}'\n" for c in cuts))
    sc=f'seg/s{ci}.mp4'
    dt=("drawtext=fontfile=%s:textfile=seg/t%d.txt:fontcolor=white:fontsize=64:line_spacing=10:box=1:boxcolor=black@0.55:boxborderw=22:x=60:y=h*0.62:enable='between(t,0.15,%.2f)'"%(FONT,ci,dur-0.1))+",drawtext=fontfile=%s:text='Tutorial Pet':fontcolor=white@0.9:fontsize=38:x=36:y=h-110:shadowcolor=black@0.6:shadowx=2:shadowy=2"%FONT
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',lst,'-vf',dt,'-c:v','libx264','-crf','17','-preset','veryfast',sc],check=True)
    parts.append(sc)
CTA=(6.12,"E você,\nquantas vezes escova?\nConta nos comentários!",[14,30,39])
dur,txt,srcs=CTA; per=dur/len(srcs); open('seg/tcta.txt','w',encoding='utf-8').write(txt); cuts=[]
for j,sx in enumerate(srcs):
    out=f'seg/cta_{j}.mp4'; d=per if j<len(srcs)-1 else dur-per*(len(srcs)-1)
    subprocess.run(['ffmpeg','-v','error','-y','-ss','0.4','-t',f'{d:.3f}','-i',clip(sx),'-an','-vf',VF,'-c:v','libx264','-crf','17','-preset','veryfast',out],check=True); cuts.append(out)
open('seg/lcta.txt','w').write(''.join(f"file '{os.path.abspath(c)}'\n" for c in cuts))
dt=("drawtext=fontfile=%s:textfile=seg/tcta.txt:fontcolor=white:fontsize=64:line_spacing=10:box=1:boxcolor=black@0.55:boxborderw=22:x=60:y=h*0.58"%FONT)+",drawtext=fontfile=%s:text='Tutorial Pet':fontcolor=white@0.9:fontsize=38:x=36:y=h-110:shadowcolor=black@0.6:shadowx=2:shadowy=2"%FONT
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','seg/lcta.txt','-vf',dt,'-c:v','libx264','-crf','17','-preset','veryfast','seg/99_cta.mp4'],check=True)
parts.append('seg/99_cta.mp4')
open('seg/all.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','seg/all.txt','-c:v','copy','seg/video_noaudio.mp4'],check=True)
