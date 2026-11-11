import subprocess, os, sys, json, math
sys.path.insert(0,'/home/claude/tutorialpet/data/vsl/natasha/scripts')
from PIL import Image, ImageDraw, ImageFont
FONT="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
B='/home/claude/vsl8'; C=B+'/clips'; W=B+'/work'; V=B+'/voz'
CARDS='/home/claude/tutorialpet/data/vsl/natasha/cards_v16'
SC='/home/claude/tutorialpet/data/vsl/natasha/scripts'
MUS='/home/claude/tutorialpet/biblioteca/musica/gr0za-party-party-music-569750.mp3'
LEVE = '--leve' in sys.argv
def sh(c):
    r=subprocess.run(c,shell=True,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-2000:]); raise SystemExit(1)
    return r.stdout
def dur(f): return float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{f}"').strip())
d1,d2,d3=[dur(f'{V}/vsl8_voz_natasha_F{x}.mp3') for x in ('01-F06','07-F09','10-F11')]
o2=d1; o3=d1+d2; T=d1+d2+d3
print('offsets',o2,o3,T)
# ---------- cenas ----------
clip={'dog':'vsl8_F1_cachorro_espera_porta','party':'vsl8_F2_despedida_festa','phone':'vsl8_F3_mulher_celular_noite',
      'neigh':'vsl8_F3_vizinho_corredor','mess':'vsl8_F5_sala_destruida','cry':'vsl8_F6_mulher_chora_chao',
      'train':'vsl8_F8_treino_celular','hug':'vsl8_F9_abraco_chegada'}
cnt={}
plan=[ # (t0,t1,[clips])
 (0,1.4,['dog']),(1.4,2.8,['party']),
 (2.8,6.3,['party']),
 (6.3,8.8,['dog','cry']),(8.8,11.6,['mess']),(11.6,12.9,['neigh']),
 (12.9,16.0,['mess','phone']),   # REC
 (16.0,19.3,['mess','neigh']),
 (19.3,26.2,['cry','phone']),
 (26.2,30.84,['train']),(30.84,38.3,['party','train']),
 (38.3,o3,['hug']),
 (o3,o3+7.3,['hug','train','party']),
 (o3+7.3,T,['__prod__'])]
ZS=[1.0,1.14,1.06,1.2,1.0,1.10]
segs=[]
for t0,t1,cl in plan:
    L=t1-t0
    if cl==['__prod__']:
        segs.append((t0,t1,'__prod__',0,1.0)); continue
    n=max(1,math.ceil(L/1.4)); step=L/n
    for i in range(n):
        c=cl[i%len(cl)]; k=cnt.get(c,0); cnt[c]=k+1
        src=(k*1.9)%6.2
        segs.append((t0+i*step,t0+(i+1)*step,c,src,ZS[k%len(ZS)]))
print(len(segs),'cortes; maior',max(b-a for a,b,*_ in segs))
parts=[]
import itertools
for i,(a,b,c,src,z) in enumerate(segs):
    out=f'{W}/seg_{i:03d}.mp4'; L=b-a; nf=round(b*30)-round(a*30)
    if c=='__prod__': continue
    cx=0.5+0.04*((i%3)-1)*(z>1)
    vf=(f"scale=1080:1920:flags=bicubic,crop=iw/{z}:ih/{z}:(iw-iw/{z})*{cx}:(ih-ih/{z})*0.5,scale=1080:1920,fps=30,format=yuv420p")
    sh(f'ffmpeg -v error -y -ss {src:.3f} -t {L+0.05:.3f} -i {C}/{clip[c]}.mp4 -an -vf "{vf}" -frames:v {nf} -c:v libx264 -preset veryfast -crf 20 {out}')
    parts.append((a,b,out))
# F11: produto_anim + anim2 loop
prodL=T-(o3+7.3)
PULSE="scale=w=1080*(1.03+0.035*sin(2*PI*t*1.6)):h=1920*(1.03+0.035*sin(2*PI*t*1.6)):eval=frame,crop=1080:1920,setsar=1"
sh(f'ffmpeg -v error -y -stream_loop 3 -i {SC}/produto_anim.mp4 -stream_loop 3 -i {SC}/produto_anim2.mp4 -filter_complex "[0:v]trim=0:3,setpts=PTS-STARTPTS,fps=30,split[a][a2];[1:v]trim=0:3,setpts=PTS-STARTPTS,fps=30[b];[a][b][a2]concat=n=3:v=1,{PULSE},format=yuv420p,trim=0:{prodL+0.2:.3f},fps=30[o]" -frames:v {round(T*30)-round((o3+7.3)*30)} -map "[o]" -an -c:v libx264 -preset veryfast -crf 20 {W}/prod.mp4')
parts.append((o3+7.3,T,f'{W}/prod.mp4'))
parts.sort()
with open(f'{W}/list.txt','w') as f:
    for a,b,p in parts: f.write(f"file '{p}'\n")
sh(f'ffmpeg -v error -y -f concat -safe 0 -i {W}/list.txt -c copy {W}/base.mp4')
print('base',dur(f'{W}/base.mp4'))
json.dump({'segs':[(round(a,2),round(b,2),c,round(s,2),z) for a,b,c,s,z in segs],'T':T,'o2':o2,'o3':o3},open(f'{B}/out/vsl8_cortes.json','w'))
