import subprocess, json, sys
sys.path.insert(0,'/home/claude/tutorialpet/data/vsl/natasha/scripts')
from PIL import Image, ImageDraw, ImageFont
import numpy as np
B='/home/claude/vsl8'; W=B+'/work'; V=B+'/voz'; O=B+'/out'
CARDS='/home/claude/tutorialpet/data/vsl/natasha/cards_v16'
SC='/home/claude/tutorialpet/data/vsl/natasha/scripts'
MUS='/home/claude/tutorialpet/biblioteca/musica/gr0za-party-party-music-569750.mp3'
FONT="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
def sh(c):
    r=subprocess.run(c,shell=True,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-2500:]); raise SystemExit(1)
    return r.stdout
J=json.load(open(O+'/vsl8_v2_meta.json')); T=J['T2']; o2=J['o2']; o3=J['o3']; PA=J['PA']
def S(t): return t+PA if t>=6.31 else t
def caption_png(text,path,size=72):
    f=ImageFont.truetype(FONT,size); W_=940
    words=text.split(); lines=[];cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if f.getlength(t)<=W_: cur=t
        else: lines.append(cur);cur=w
    lines.append(cur)
    lh=int(size*1.22); H=lh*len(lines)+30
    im=Image.new("RGBA",(1080,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    for i,l in enumerate(lines):
        x=(1080-f.getlength(l))/2; y=10+i*lh
        d.text((x,y),l,font=f,fill=(255,255,255,255),stroke_width=9,stroke_fill=(20,20,20,255))
    im.save(path); return H
# legendas = fala aprovada (global)
caps=[(0,2.98,"O que o seu cachorro faz quando você fecha a porta?"),
(2.98,6.56+PA,"Logo depois de mais uma despedida com festa…"),
(S(6.56),S(8.9),"Minuto um: começa o choro."),(S(8.98),S(11.6),"Duas horas depois, ele ainda late."),
(S(11.76),S(13.0),"E o vizinho liga."),(S(13.08),S(16.0),"Ela abre a câmera… e é ainda pior."),
(S(16.12),S(19.3),"Na hora do almoço, ela não come: corre pra casa."),
(S(19.42),S(21.0),"Você já pensou como ela?"),(S(21.12),S(23.0),"Será que eu só estou criando problema?"),
(S(23.18),o2,"Ou desisto e entrego pra doação, ou…"),
(o2,o2+4.64,"Calma. O Sozinho em Casa monta um treino personalizado pro seu amiguinho."),
(o2+4.94,o2+6.5,"Sem virar adestradora:"),
(o2+6.62,o2+11.9,"dez minutos por dia, e ele diz o que fazer a cada dia, conforme o resultado anterior."),
(o2+12.0,o2+14.9,"Catorze dias depois, você abre a porta…"),
(o2+15.0,o3,"e sente a satisfação dessa conquista."),
(o3,o3+3.2,"De noventa e sete por vinte e sete reais."),
(o3+3.2,o3+7.2,"Catorze dias de garantia: não gostou, devolvemos tudo."),
(o3+7.3,o3+13.0,"Garanta agora o Sozinho em Casa: tranquilidade pro seu melhor amigo e paz com os vizinhos."),
(o3+13.05,T,"Clique no botão!")]
inputs=[]; flt=[]; n=1; last='[0:v]'
def add_png(path,x,y,t0,t1,extra='',float_=False):
    global n,last
    inputs.append(f'-i {path}')
    idx=n; n+=1
    yy=f"'{y}+28*sin(2*PI*t*1.3)'" if float_ else y
    flt.append(f"{last}[{idx}:v]overlay={x}:{yy}:enable='between(t,{t0:.3f},{t1:.3f})'{extra}[v{idx}]"); last=f'[v{idx}]'
CAPY=340; caphs=[]
from ultralytics import YOLO
import glob, os
YM=YOLO('yolov8n.pt')
def boxes_at(ts):
    bx=[]
    for t in ts:
        fp=f'{W}/yf.jpg'; sh(f'ffmpeg -v error -y -ss {t:.2f} -i {W}/base_v2.mp4 -frames:v 1 {fp}')
        r=YM(fp,verbose=False)[0]
        for b,c in zip(r.boxes.xyxy.tolist(),r.boxes.cls.tolist()):
            if int(c)==16: bx.append(b)
            if int(c)==0: bx.append([b[0],b[1],b[2],b[1]+0.28*(b[3]-b[1])])  # só a cabeça
    return bx
def best_y(a,b,h):
    if a>=o3+7.3: return CAPY,0
    ts=[a+(b-a)*k for k in (0.1,0.35,0.6,0.85)]
    bx=boxes_at(ts); best=None
    for y in range(330,931-h,20):
        ov=0
        for x0,y0,x1,y1 in bx:
            ox=max(0,min(1080,x1)-max(0,x0)); oy=max(0,min(y+h,y1)-max(y,y0)); ov+=ox*oy
        if best is None or ov<best[1]: best=(y,ov)
    return best

for i,(a,b,t) in enumerate(caps):
    p=f'{W}/cap_{i:02d}.png'; h=caption_png(t,p); caphs.append((a,b,h))
    y,ov=best_y(a,b,h); print(f'legenda {i} y={y} sobreposicao_px={int(ov)}'); add_png(p,0,y,a,b)
# REC (F4)
im=Image.new('RGBA',(520,90),(0,0,0,0)); d=ImageDraw.Draw(im); f=ImageFont.truetype(FONT,44)
d.ellipse((6,18,58,70),fill=(230,20,20,255)); d.text((76,16),"REC  00:14:32",font=f,fill=(255,255,255,255),stroke_width=4,stroke_fill=(0,0,0,255)); im.save(W+'/rec.png')
add_png(W+'/rec.png',60,CAPY+230,13.78,16.4)
# cartões
def card(name):
    im=Image.open(f'{CARDS}/{name}.png').convert('RGB'); a=np.array(im).astype(int)
    bg=np.array([254,243,228]); m=(np.abs(a-bg).sum(2)>30)
    ys,xs=np.where(m); box=(xs.min(),ys.min(),xs.max()+1,ys.max()+1); return im,box
im,box=card('preco_v16')
# remover o selo "só até domingo (08/11)" (data vencida) pintando de branco
a=np.array(im).astype(int); x0,y0,x1,y1=box
sub=a[y0:y1,x0:x1]; org=(sub[:,:,0]>200)&(sub[:,:,1]<150)&(sub[:,:,2]<80)
rows=np.where(org.sum(1)>(x1-x0)*0.2)[0]
print('linhas laranja largas',rows[:3],rows[-3:],'altura card',y1-y0)
pill=[r for r in rows if (y1-y0)*0.7<r<(y1-y0)-8]
if pill:
    g=[pill[0]]
    for r in pill[1:]:
        if r==g[-1]+1: g.append(r)
        else: break
    pill=g
if pill:
    pa,pb=min(pill),max(pill)
    # pintar o selo e encolher o cartão (corta abaixo do texto): mantém borda inferior
    d=ImageDraw.Draw(im); d.rectangle((x0+6,y0+pa-4,x1-7,y0+pb+4),fill=(255,255,255))
    print('selo removido',pa,pb)
im.save(W+'/preco_sem_selo.png')
cards={}
for nm,path in (('preco',W+'/preco_sem_selo.png'),('gar',CARDS+'/garantia2.png'),('prova',CARDS+'/prova_v16.png')):
    im=Image.open(path).convert('RGB'); a=np.array(im).astype(int); m=(np.abs(a-np.array([254,243,228])).sum(2)>30)
    ys,xs=np.where(m); c=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    sc=900/c.width; c=c.resize((900,int(c.height*sc))); 
    mask=Image.new('L',c.size,0); ImageDraw.Draw(mask).rounded_rectangle((0,0,c.width-1,c.height-1),radius=36,fill=255)
    c=c.convert('RGBA'); c.putalpha(mask); c.save(f'{W}/card_{nm}.png'); cards[nm]=c.size
print(cards)
add_png(W+'/card_preco.png',90,760,o3,o3+3.2,float_=True)
add_png(W+'/card_gar.png',90,760,o3+3.2,o3+6.0,float_=True)
add_png(W+'/card_prova.png',90,760,o3+6.0,o3+7.3,float_=True)
# Natasha (recorte do rosto, círculo) no fecho
sh(f'ffmpeg -v error -y -stream_loop 3 -i {SC}/natasha_full.mp4 -vf "crop=520:520:280:390,scale=300:300" -t 8 -an -c:v libx264 -crf 18 {W}/nat_face.mp4')
ring=Image.new('RGBA',(300,300),(0,0,0,0)); ImageDraw.Draw(ring).ellipse((2,2,297,297),outline=(255,255,255,255),width=8); ring.save(W+'/ring.png')
cm=Image.new('L',(300,300),0); ImageDraw.Draw(cm).ellipse((0,0,299,299),fill=255); cm.save(W+'/circ.png')
inputs.append(f'-i {W}/nat_face.mp4'); ni=n; n+=1
inputs.append(f'-loop 1 -i {W}/circ.png'); nc=n; n+=1
flt.append(f"[{ni}:v][{nc}:v]alphamerge[nf]")
flt.append(f"{last}[nf]overlay=700:1010:enable='gte(t,{o3+7.3:.3f})':shortest=0[vn]"); last='[vn]'
add_png(W+'/ring.png',700,1010,o3+7.3,T)
# botão piscando y=1400
for nm,par in (('btn_a',0),('btn_b',1)):
    inputs.append(f'-i {CARDS}/{nm}.png'); idx=n; n+=1
    flt.append(f"{last}[{idx}:v]overlay=106:1400:enable='gte(t,{o3+7.3:.3f})*eq(mod(floor(t*2),2),{par})'[v{idx}]"); last=f'[v{idx}]'
open(W+'/flt.txt','w').write(';\n'.join(flt)+f";\n{last}format=yuv420p[vout]")

# ---------------- AUDIO v2: voz + sonoplastia no ar, SEM musica de fundo ----------------
SF='/home/claude/vsl8/sfx'
sh(f'ffmpeg -v error -y -i {V}/vsl8_voz_natasha_F01-F06.mp3 -i {V}/vsl8_voz_natasha_F07-F09.mp3 -i {V}/vsl8_voz_natasha_F10-F11.mp3 -filter_complex "[0:a]loudnorm=I=-16:TP=-2[a];[1:a]loudnorm=I=-16:TP=-2[b];[2:a]loudnorm=I=-16:TP=-2[c];[a][b][c]concat=n=3:v=0:a=1,aresample=44100[o]" -map "[o]" {W}/voz_total.wav')
# pausa C3: 0,7 s de silencio no meio do silencio da voz (6,14-6,48 s)
sh(f'ffmpeg -v error -y -i {W}/voz_total.wav -filter_complex "[0:a]atrim=0:6.31,asetpts=PTS-STARTPTS[x];[0:a]atrim=6.31,asetpts=PTS-STARTPTS[y];anullsrc=r=44100:cl=mono,atrim=0:{PA}[s];[x][s][y]concat=n=3:v=0:a=1[o]" -map "[o]" {W}/voz_v2.wav')
cues=[('sfx_bass_hit',0.0,1.0,-4),('sfx_bass_hit',0.42,1.0,-7),('sfx_porta_batendo',5.5,1.0,-9),
 ('sfx_heartbeat_impact',6.31,0.75,-3),('sfx_heartbeat_impact',6.68,0.6,-5),
 ('sfx_cachorro_choro',7.3,2.0,-10),('sfx_cachorro_latindo',9.4,2.6,-9),('sfx_telefone_toque',12.0,1.7,-11),
 ('sfx_suspense_swell',13.6,2.8,-12),('sfx_notificacao_celular',16.4,1.0,-9),('sfx_whoosh_passos',17.7,2.0,-10),
 ('sfx_brass_strings_suspense',20.0,6.0,-19),('sfx_chimes_vitoria',o2,2.0,-12),('sfx_conquista',o2+14.9,2.0,-12),
 ('sfx_moeda_win',o3,1.2,-10),('sfx_click_botao',T-1.2,0.5,-8)]
ins=''; fc=''; labs=''
for k,(f,t0,d,db) in enumerate(cues):
    ins+=f' -i {SF}/{f}.mp3'
    fc+=f'[{k}:a]atrim=0:{d},asetpts=PTS-STARTPTS,volume={db}dB,afade=t=out:st={max(d-0.15,0.01):.2f}:d=0.15,aresample=44100,aformat=channel_layouts=mono,adelay={int(t0*1000)}:all=1[c{k}];'
    labs+=f'[c{k}]'
sh(f'ffmpeg -v error -y{ins} -filter_complex "{fc}{labs}amix=inputs={len(cues)}:duration=longest:normalize=0,apad=whole_dur={T:.3f},atrim=0:{T:.3f}[o]" -map "[o]" {O}/vsl8_sfx_SEM_voz.wav')
sh(f'ffmpeg -v error -y -i {W}/voz_v2.wav -i {O}/vsl8_sfx_SEM_voz.wav -filter_complex "[0:a]apad=whole_dur={T:.3f},aformat=channel_layouts=mono[v];[1:a]aformat=channel_layouts=mono[s];[v][s]amix=inputs=2:duration=first:normalize=0[o]" -map "[o]" -t {T:.3f} {W}/mix_raw_v2.wav')
import re
m=sh(f'ffmpeg -hide_banner -i {W}/mix_raw_v2.wav -af loudnorm=I=-14:TP=-1.5:LRA=7:print_format=json -f null - 2>&1')
mj=json.loads(m[m.rindex('{'):m.rindex('}')+1])
sh(f'ffmpeg -v error -y -i {W}/mix_raw_v2.wav -af "loudnorm=I=-14:TP=-1.5:LRA=7:measured_I={mj["input_i"]}:measured_TP={mj["input_tp"]}:measured_LRA={mj["input_lra"]}:measured_thresh={mj["input_thresh"]}:offset={mj["target_offset"]}:linear=true" -ar 44100 {W}/mix_v2.wav')
cmd=f'ffmpeg -v error -y -i {W}/base_v2.mp4 {" ".join(inputs)} -i {W}/mix_v2.wav -filter_complex_script {W}/flt.txt -map "[vout]" -map {n}:a -t {T:.3f} -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 160k -movflags +faststart {O}/vsl8_camera_v2_1080.mp4'
sh(cmd)
sh(f'ffmpeg -v error -y -i {O}/vsl8_camera_v2_1080.mp4 -vf scale=540:960 -c:v libx264 -preset veryfast -crf 29 -c:a aac -b:a 96k -movflags +faststart {O}/vsl8_camera_v2_leve.mp4')
print('ok')
