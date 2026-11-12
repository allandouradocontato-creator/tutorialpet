"""VSL9 — legendas, cards, carimbo, botao, sonoplastia, mix -14 LUFS e render. Rodar depois de vsl9_build.py."""
import subprocess, json, os, sys
sys.path.insert(0,'/home/claude/tutorialpet/data/vsl/natasha/scripts')
from PIL import Image, ImageDraw, ImageFont
import numpy as np
B='/home/claude/vsl9'; W=B+'/work'; O=B+'/out'; V=B+'/voz'
CARDS='/home/claude/tutorialpet/data/vsl/natasha/cards_v16'
SF='/home/claude/tutorialpet/data/vsl/natasha/sfx'
CAR='/home/claude/tutorialpet/assets/carimbo_tutorialpet.png'
V8W='/home/claude/vsl8/work'
FONT="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
def sh(c):
    r=subprocess.run(c,shell=True,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-2500:]); raise SystemExit(1)
    return r.stdout
M=json.load(open(W+'/meta.json')); B2,B3,T,NT0=M['B2'],M['B3'],M['T'],M['NT0']; NL=T-NT0
def caption_png(text,path,size=72):
    f=ImageFont.truetype(FONT,size); W_=940
    lines=[];cur=""
    for w in text.split():
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
# legendas = fala aprovada (nenhuma palavra muda)
caps=[(0.0,4.3,"E se você pudesse ver o que o seu cachorro faz quando você fecha a porta?"),
(4.64,6.0,"Você sai para o trabalho."),(6.16,8.4,"Um minuto depois, começa o choro."),
(8.56,11.1,"Uma hora depois, o sofá já era."),(11.32,13.95,"Duas horas depois, ele ainda late."),
(14.2,15.85,"E aí o seu celular toca:"),(15.98,16.9,"é o vizinho."),
(17.02,19.5,"Você pensa: ele faz de pirraça."),(19.7,20.9,"É bagunceiro."),(21.0,22.5,"Será que vou ter que doar?"),
(22.68,24.3,"Mas olha de novo a câmera."),(24.42,25.75,"Isso não é bagunça…"),(25.88,27.8,"é pânico de ficar sozinho."),(27.92,29.75,"E pânico tem treino."),

(B2+3.82,B2+5.4,"dez minutos por dia."),(B2+5.58,B2+8.3,"E o aplicativo diz o que fazer a cada dia."),
(B2+8.44,B2+11.6,"Filhote, idoso, vira-lata ou de raça."),
(B2+11.78,B2+14.4,"Catorze dias depois, você abre a câmera…"),(B2+14.5,B2+16.2,"e ele está tranquilo."),
(B3+0.0,B3+2.7,"De noventa e sete por vinte e sete reais."),(B3+3.0,B3+4.7,"Catorze dias de garantia:"),(B3+4.8,B3+6.45,"não gostou? Devolvemos tudo.")]
inputs=[]; flt=[]; n=1; last='[0:v]'
def add_png(path,x,y,t0,t1,float_=False):
    global n,last
    inputs.append(f'-i {path}'); idx=n; n+=1
    yy=f"'{y}+20*sin(2*PI*t*1.3)'" if float_ else y
    flt.append(f"{last}[{idx}:v]overlay={x}:{yy}:enable='between(t,{t0:.3f},{t1:.3f})'[v{idx}]"); last=f'[v{idx}]'
# --- cenas de fundo escurecidas atras dos cards (F10)
flt.append(f"{last}eq=brightness=-0.22:enable='between(t,{B3:.3f},{NT0:.3f})'[vdim]"); last='[vdim]'
# --- carimbo (todo o video; na Natasha desce p/ faixa do tronco)
inputs.append(f'-i {CAR}'); ci=n; n+=1
flt.append(f"[{ci}:v]scale=300:-1,split=2[carm][carm2]")
flt.append(f"{last}[carm]overlay=500:150:enable='lt(t,{NT0:.3f})'[vcar]"); last='[vcar]'
flt.append(f"{last}[carm2]overlay=(W-w)/2:1545:enable='gte(t,{NT0:.3f})'[vcar2]"); last='[vcar2]'
add_png(V8W+'/nat_lab.png',(1080-int(Image.open(V8W+'/nat_lab.png').width))//2,1655,NT0,T)
# --- viewfinder REC da F9 (camera: "ele esta dormindo")
im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); f=ImageFont.truetype(FONT,40)
for (x,y,dx,dy) in ((50,330,1,1),(1030,330,-1,1),(50,1500,1,-1),(1030,1500,-1,-1)):
    d.line((x,y,x+dx*110,y),fill=(255,255,255,235),width=7); d.line((x,y,x,y+dy*110),fill=(255,255,255,235),width=7)
d.ellipse((66,70,102,106),fill=(230,20,20,255)); d.text((116,64),"REC  00:14:32",font=f,fill=(255,255,255,255),stroke_width=4,stroke_fill=(0,0,0,255))
im.save(W+'/f9_rec.png')  # v2: F9 ja traz REC embutido (clipe da camera) - sem overlay
# --- card do produto (F7): traz a propria fala (legenda = fala)
cw,chh=920,410
im=Image.new('RGBA',(cw,chh),(0,0,0,0)); d=ImageDraw.Draw(im)
d.rounded_rectangle((0,0,cw-1,chh-1),radius=36,fill=(255,255,255,255),outline=(232,93,4,255),width=7)
f0=ImageFont.truetype(FONT,40); f1=ImageFont.truetype(FONT,66); f2=ImageFont.truetype(FONT,46)
t0="O"; d.text(((cw-f0.getlength(t0))/2,30),t0,font=f0,fill=(36,36,62,255))
t1="SOZINHO EM CASA"; d.text(((cw-f1.getlength(t1))/2,66),t1,font=f1,fill=(232,93,4,255))
d.line((150,162,cw-150,162),fill=(232,93,4,255),width=5)
for i,t in enumerate(("monta um treino personalizado","pro seu amiguinho:")):
    d.text(((cw-f2.getlength(t))/2,186+i*72),t,font=f2,fill=(36,36,62,255))
im.save(W+'/card_produto.png'); CARDBOX=(80,1215,1000,1215+chh)
add_png(W+'/card_produto.png',80,1215,B2+0.1,B2+3.85,float_=True)
# --- cards preco / garantia (F10)
add_png(V8W+'/card_preco.png',90,300,B3,B3+3.0,float_=True)
add_png(V8W+'/card_gar.png',90,300,B3+3.0,NT0,float_=True)
# --- legendas (posicao: fora de rosto/cachorro via YOLO)
from ultralytics import YOLO
YM=YOLO('yolov8n.pt')
def boxes_at(ts):
    bx=[]
    for t in ts:
        fp=f'{W}/yf.jpg'; sh(f'ffmpeg -v error -y -ss {t:.2f} -i {W}/base.mp4 -frames:v 1 {fp}')
        r=YM(fp,verbose=False,conf=0.15)[0]
        for b,c in zip(r.boxes.xyxy.tolist(),r.boxes.cls.tolist()):
            if int(c)==16: bx.append([b[0],b[1],b[2],b[1]+0.6*(b[3]-b[1])])
            if int(c)==0: bx.append([b[0],b[1],b[2],b[1]+0.4*(b[3]-b[1])])
    return bx
def best_y(a,b,h):
    if a>=B3-0.01: return 1300,0
    if 14.1<a<16.0: return 880,0
    ts=[a+(b-a)*k for k in (0.05,0.3,0.55,0.8,0.95)]
    bx=boxes_at(ts)
    if B2<=a<B2+3.9: bx.append(list(CARDBOX))
    best=None
    for y in range(330,1500-h,20):
        ov=0
        for x0,y0,x1,y1 in bx:
            ox=max(0,min(1080,x1)-max(0,x0)); oy=max(0,min(y+h+20,y1+20)-max(y-20,y0)); ov+=ox*oy
        pen=ov*10+abs(y-1250)*0.02
        if best is None or pen<best[2]: best=(y,ov,pen)
    return best[0],best[1]
LOG=[]
for i,(a,b,t) in enumerate(caps):
    p=f'{W}/cap9_{i:02d}.png'; h=caption_png(t,p); y,ov=best_y(a,b,h)
    LOG.append((round(a,2),round(b,2),y,int(ov),t)); print(f'legenda {i} y={y} sobreposicao_px={int(ov)}'); add_png(p,0,y,a,b)
# --- botao piscando (F11)
for nm,par in (('btn_a',0),('btn_b',1)):
    inputs.append(f'-i {CARDS}/{nm}.png'); idx=n; n+=1
    flt.append(f"{last}[{idx}:v]overlay=106:1400:enable='gte(t,{NT0:.3f})*eq(mod(floor(t*2),2),{par})'[v{idx}]"); last=f'[v{idx}]'
open(W+'/flt9.txt','w').write(';\n'.join(flt)+f";\n{last}format=yuv420p[vout]")
json.dump(LOG,open(W+'/caps_log.json','w'),ensure_ascii=False)
# ---------------- AUDIO: voz + sonoplastia, SEM musica ----------------
def norm(k): sh(f'ffmpeg -v error -y -i {V}/vsl9_voz_natasha_{k}.mp3 -af "loudnorm=I=-16:TP=-2,aresample=44100,aformat=channel_layouts=mono" {W}/vn_{k}.wav')
for k in ('F01-F06','F07-F09','F10-F11'): norm(k)
sh(f'ffmpeg -v error -y -ss 0.12 -t {NL:.3f} -i /home/claude/vsl8/heygen/natasha_fala_heygen.mp4 -vn -af "loudnorm=I=-16:TP=-2,aresample=44100,aformat=channel_layouts=mono" {W}/vn_nat.wav')
sh(f'ffmpeg -v error -y -i {W}/vn_F01-F06.wav -f lavfi -t 0.10 -i anullsrc=r=44100:cl=mono -i {W}/vn_F07-F09.wav -f lavfi -t 0.10 -i anullsrc=r=44100:cl=mono -i {W}/vn_F10-F11.wav -i {W}/vn_nat.wav -filter_complex "[0][1][2][3]concat=n=4:v=0:a=1[a];[4]atrim=0:{NT0-B3:.3f},afade=t=out:st={NT0-B3-0.05:.3f}:d=0.05[b];[a][b]concat=n=2:v=0:a=1,apad=whole_dur={T:.3f}[c];[5]adelay={int(NT0*1000)}:all=1[n];[c][n]amix=inputs=2:duration=longest:normalize=0,atrim=0:{T:.3f}[o]" -map "[o]" {W}/voz9.wav')
cues=[('sfx_bass_hit',0.0,1.0,-4),('sfx_brass_strings_suspense',0.4,3.9,-19),
 ('sfx_porta_batendo',5.0,1.0,-9),('sfx_cachorro_choro',7.0,2.0,-10),
 ('sfx_cachorro_latindo',11.3,2.7,-9),('sfx_telefone_toque',14.2,1.7,-11),
 ('sfx_heartbeat_impact',17.0,1.2,-5),('sfx_suspense_swell',17.6,4.6,-13),
 ('sfx_horror_drum',25.88,1.3,-12),('sfx_bass_hit',25.88,0.9,-10),
 ('sfx_chimes_vitoria',B2,2.0,-12),('sfx_conquista',B2+15.1,2.0,-12),
 ('sfx_whoosh_passos',4.45,0.8,-15),('sfx_whoosh_passos',8.45,0.8,-15),('sfx_whoosh_passos',22.55,0.9,-13),
 ('sfx_notificacao_celular',16.0,1.0,-13),('sfx_whoosh_passos',B2-0.05,0.9,-13),
 ('sfx_whoosh_passos',B2+8.3,0.6,-14),('sfx_whoosh_passos',B2+9.15,0.6,-14),('sfx_whoosh_passos',B2+9.85,0.6,-14),('sfx_whoosh_passos',B2+10.65,0.6,-14),
 ('sfx_whoosh_passos',B2+11.65,0.8,-14),('sfx_chimes_vitoria',B2+13.9,1.6,-13),('sfx_whoosh_passos',NT0-0.1,0.9,-13),
 ('sfx_moeda_win',B3,1.2,-10),('sfx_click_botao',B3+3.0,0.5,-12),('sfx_click_botao',NT0+6.0,0.5,-8)]
ins='';fc='';labs=''
for k,(f,t0,d,db) in enumerate(cues):
    ins+=f' -i {SF}/{f}.mp3'
    fc+=f'[{k}:a]atrim=0:{d},asetpts=PTS-STARTPTS,volume={db}dB,afade=t=out:st={max(d-0.15,0.01):.2f}:d=0.15,aresample=44100,aformat=channel_layouts=mono,adelay={int(t0*1000)}:all=1[c{k}];'
    labs+=f'[c{k}]'
sh(f'ffmpeg -v error -y{ins} -filter_complex "{fc}{labs}amix=inputs={len(cues)}:duration=longest:normalize=0,apad=whole_dur={T:.3f},atrim=0:{T:.3f}[o]" -map "[o]" {O}/vsl9_sfx_SEM_voz.wav')
# --- musica: SUSPENSE (mesma da VSL8, Mixkit) no problema ate "Mas olha de novo a camera"; depois party-music (gr0za, mesma das VSLs) ate o fim
SUSP='/home/claude/vsl8/mus/mixkit_cinematic_action_suspense.mp3'
MUSP='/home/claude/tutorialpet/biblioteca/musica/gr0za-party-party-music-569750.mp3'
SE=22.55
sh(f'ffmpeg -v error -y -i {SUSP} -stream_loop -1 -i {SF}/sfx_heartbeat_impact.mp3 -filter_complex "[0:a]atrim=6:{6+SE:.3f},asetpts=PTS-STARTPTS,highpass=f=90,aformat=channel_layouts=mono,aresample=44100,volume=3dB[s];[1:a]aformat=channel_layouts=mono,aresample=44100,atrim=0:1.2,apad=whole_dur=1.2,aloop=loop=-1:size=60000,volume=-14dB,atrim=0:{SE:.3f}[h];[s][h]amix=inputs=2:normalize=0,afade=t=in:st=0:d=0.4,afade=t=out:st={SE-0.9:.2f}:d=0.9[o]" -map "[o]" {W}/susp9.wav')
MU0=B2-0.4
sh(f'ffmpeg -v error -y -i {MUSP} -af "atrim=8:{8+T-MU0+1:.2f},asetpts=PTS-STARTPTS,aformat=channel_layouts=mono,aresample=44100,volume=-8dB,afade=t=in:st=0:d=1.2,afade=t=out:st={T-MU0-1.0:.2f}:d=1.0" -t {T-MU0:.3f} {W}/party9.wav')
sh(f'ffmpeg -v error -y -f lavfi -i anullsrc=r=44100:cl=mono -i {W}/susp9.wav -i {W}/party9.wav -filter_complex "[1:a]apad=whole_dur={MU0:.3f},atrim=0:{MU0:.3f}[sp];[sp][2:a]concat=n=2:v=0:a=1,atrim=0:{T:.3f}[m]" -map "[m]" {W}/musica9.wav')
sh(f'ffmpeg -v error -y -i {W}/voz9.wav -i {O}/vsl9_sfx_SEM_voz.wav -i {W}/musica9.wav -filter_complex "[0:a]apad=whole_dur={T:.3f},aformat=channel_layouts=mono,asplit=2[v][vk];[1:a]aformat=channel_layouts=mono[s];[2:a]aformat=channel_layouts=mono[m0];[m0][vk]sidechaincompress=threshold=0.03:ratio=2:attack=20:release=300[m];[v][s][m]amix=inputs=3:duration=first:normalize=0[o]" -map "[o]" -t {T:.3f} {W}/mix9_raw.wav')
m=sh(f'ffmpeg -hide_banner -i {W}/mix9_raw.wav -af loudnorm=I=-14:TP=-1.5:LRA=7:print_format=json -f null - 2>&1')
mj=json.loads(m[m.rindex('{'):m.rindex('}')+1])
sh(f'ffmpeg -v error -y -i {W}/mix9_raw.wav -af "loudnorm=I=-14:TP=-1.5:LRA=7:measured_I={mj["input_i"]}:measured_TP={mj["input_tp"]}:measured_LRA={mj["input_lra"]}:measured_thresh={mj["input_thresh"]}:offset={mj["target_offset"]}:linear=true" -ar 44100 {W}/mix9.wav')
cmd=f'ffmpeg -v error -y -i {W}/base.mp4 {" ".join(inputs)} -i {W}/mix9.wav -filter_complex_script {W}/flt9.txt -map "[vout]" -map {n}:a -t {T:.3f} -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 160k -movflags +faststart {O}/vsl9_e_se_fosse_voce_v4_1080.mp4'
sh(cmd)
sh(f'ffmpeg -v error -y -i {O}/vsl9_e_se_fosse_voce_v4_1080.mp4 -vf scale=540:960 -c:v libx264 -preset veryfast -crf 29 -c:a aac -b:a 96k -movflags +faststart {O}/vsl9_e_se_fosse_voce_v4_leve.mp4')
print('ok')
