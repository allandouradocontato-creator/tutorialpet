import subprocess, json, sys, os
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
] # fecho da Dra.: tela limpa (so carimbo, nome/CRMV e botao), a pedido do Allan 12/11
inputs=[]; flt=[]; n=1; last='[0:v]'
def add_png(path,x,y,t0,t1,extra='',float_=False):
    global n,last
    inputs.append(f'-i {path}')
    idx=n; n+=1
    yy=f"'{y}+28*sin(2*PI*t*1.3)'" if float_ else y
    flt.append(f"{last}[{idx}:v]overlay={x}:{yy}:enable='between(t,{t0:.3f},{t1:.3f})'{extra}[v{idx}]"); last=f'[v{idx}]'
CAPY=340; caphs=[]
NT0=o3+7.3; NL=T-NT0
HG='/home/claude/vsl8/heygen/natasha_fala_heygen.mp4'
if os.path.exists(HG):
    # Natasha FALANDO (HeyGen Avatar, voz do fecho). O clipe comeca 0,15 s antes de NT0.
    sh(f'ffmpeg -v error -y -i {HG} -an -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p" -c:v libx264 -crf 18 {W}/nat_pres.mp4')
    NTS=NT0-0.15
else:
    sh(f'ffmpeg -v error -y -stream_loop 3 -i {SC}/natasha_full.mp4 -t {NL+0.2:.2f} -an -vf "scale=w=\'1080*(1+0.36*t/{NL:.2f})\':h=\'1920*(1+0.36*t/{NL:.2f})\':eval=frame,crop=1080:1920,fps=30,format=yuv420p" -c:v libx264 -crf 18 {W}/nat_pres.mp4')
    NTS=NT0
inputs.append(f'-i {W}/nat_pres.mp4'); _pi=n; n+=1
flt.append(f"[{_pi}:v]setpts=PTS+{NTS:.3f}/TB[nps]"); flt.append(f"{last}[nps]overlay=0:0:enable='gte(t,{NTS:.3f})'[vnp]"); last='[vnp]'
# selo da Dra. (como no VSL1): foto redonda + carimbo + nome/CRMV, no topo esquerdo, o video todo
sh(f'ffmpeg -v error -y -i {SC}/natasha_full.mp4 -frames:v 1 -vf "crop=520:520:280:390,scale=220:220" {W}/nat_c.png')
_ph=Image.open(W+'/nat_c.png').convert('RGBA'); _m=Image.new('L',(220,220),0); ImageDraw.Draw(_m).ellipse((0,0,219,219),fill=255); _ph.putalpha(_m)
ImageDraw.Draw(_ph).ellipse((2,2,217,217),outline=(255,255,255,255),width=6); _ph.save(W+'/nat_circ.png')
_f=ImageFont.truetype(FONT,30); _t="Dra. Natasha Braga · CRMV 6174"; _w=int(_f.getlength(_t))+36
_lb=Image.new('RGBA',(_w,62),(0,0,0,0)); _d=ImageDraw.Draw(_lb); _d.rounded_rectangle((0,0,_w-1,61),radius=18,fill=(20,20,20,150)); _d.text((18,9),_t,font=_f,fill=(255,255,255,255)); _lb.save(W+'/nat_lab.png')
add_png(W+'/nat_circ.png',50,150,0,NTS)
inputs.append('-i /home/claude/tutorialpet/assets/carimbo_tutorialpet.png'); _ci=n; n+=1
flt.append(f"[{_ci}:v]scale=300:-1,split=2[carm][carm2]"); flt.append(f"{last}[carm]overlay=290:165:enable='lt(t,{NTS:.3f})'[vcar]"); last='[vcar]'
add_png(W+'/nat_lab.png',290,253,0,NTS)
# no trecho da apresentadora o selo desce (fora do rosto): carimbo + nome/CRMV centralizados na faixa do tronco
flt.append(f"{last}[carm2]overlay=(W-w)/2:1545:enable='gte(t,{NTS:.3f})'[vcar2]"); last='[vcar2]'
add_png(W+'/nat_lab.png',(1080-_w)//2,1655,NTS,T)
from ultralytics import YOLO
import glob, os
YM=YOLO('yolov8n.pt')
def boxes_at(ts):
    bx=[]
    for t in ts:
        fp=f'{W}/yf.jpg'; sh(f'ffmpeg -v error -y -ss {t:.2f} -i {W}/base_v2.mp4 -frames:v 1 {fp}')
        r=YM(fp,verbose=False,conf=0.15)[0]
        for b,c in zip(r.boxes.xyxy.tolist(),r.boxes.cls.tolist()):
            if int(c)==16: bx.append([b[0],b[1],b[2],b[1]+0.55*(b[3]-b[1])])  # cabeca/tronco do cachorro
            if int(c)==0: bx.append([b[0],b[1],b[2],b[1]+0.35*(b[3]-b[1])])  # rosto da pessoa
    return bx
def best_y(a,b,h):
    if a>=o3+7.3: return 1500,0
    ts=[a+(b-a)*k for k in (0.05,0.25,0.5,0.75,0.95)]
    bx=boxes_at(ts); best=None
    # zona alta (apos o selo) e zona baixa (acima da interface do Reels, ~1500)
    for y in range(330,1500-h,20):
        ov=0
        for x0,y0,x1,y1 in bx:
            ox=max(0,min(1080,x1)-max(0,x0)); oy=max(0,min(y+h+20,y1+20)-max(y-20,y0)); ov+=ox*oy
        pen=ov*10+abs(y-1250)*0.02
        if best is None or pen<best[2]: best=(y,ov,pen)
    return best[0],best[1]

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
 ('sfx_moeda_win',o3,1.2,-10),('sfx_click_botao',T-1.2,0.5,-8),
 # v2e (12/11 15:54): mais sonoplastia pontuando momentos-chave
 ('sfx_whoosh_passos',2.98,1.0,-14),('sfx_horror_drum',13.78,1.3,-13),('sfx_bass_hit',S(11.76),0.8,-13),
 ('sfx_whoosh_passos',S(19.42),1.2,-15),('sfx_bass_hit',S(21.12),0.8,-12),('sfx_suspense_swell',S(23.18),3.0,-14),
 ('sfx_whoosh_passos',o2+4.94,1.0,-14),('sfx_chimes_vitoria',o2+6.62,1.5,-16),('sfx_whoosh_passos',o2+12.0,1.0,-14),
 ('sfx_chimes_vitoria',o3+3.2,1.5,-14),('sfx_click_botao',o3+6.0,0.5,-11),('sfx_click_botao',o3+7.3,0.5,-9)]
ins=''; fc=''; labs=''
for k,(f,t0,d,db) in enumerate(cues):
    ins+=f' -i {SF}/{f}.mp3'
    fc+=f'[{k}:a]atrim=0:{d},asetpts=PTS-STARTPTS,volume={db}dB,afade=t=out:st={max(d-0.15,0.01):.2f}:d=0.15,aresample=44100,aformat=channel_layouts=mono,adelay={int(t0*1000)}:all=1[c{k}];'
    labs+=f'[c{k}]'
sh(f'ffmpeg -v error -y{ins} -filter_complex "{fc}{labs}amix=inputs={len(cues)}:duration=longest:normalize=0,apad=whole_dur={T:.3f},atrim=0:{T:.3f}[o]" -map "[o]" {O}/vsl8_sfx_SEM_voz.wav')
MU0=o2-0.4
sh(f'ffmpeg -v error -y -i {MUS} -af "atrim=8:{8+T-MU0+1:.2f},asetpts=PTS-STARTPTS,aformat=channel_layouts=mono,aresample=44100,volume=-15dB,afade=t=in:st=0:d=1.2,afade=t=out:st={T-MU0-1.8:.2f}:d=1.8" -t {T-MU0:.3f} {W}/musica_raw.wav')
# v2f (12/11 16:02): abertura com musica de SUSPENSE (drone grave + tremolo + batida) ate o "Calma"; depois a party-music
ST=MU0+1.2
SUSP='/home/claude/vsl8/mus/mixkit_suspense_mystery_bass.mp3'  # Mixkit (licenca livre) "Suspense mystery bass"
sh(f'ffmpeg -v error -y -i {SUSP} -stream_loop -1 -i {SF}/sfx_heartbeat_impact.mp3 -filter_complex "[0:a]atrim=0:{ST:.3f},asetpts=PTS-STARTPTS,aformat=channel_layouts=mono,aresample=44100,volume=-6dB[s];[1:a]aformat=channel_layouts=mono,aresample=44100,atrim=0:1.2,apad=whole_dur=1.2,aloop=loop=-1:size=60000,volume=-23dB,atrim=0:{ST:.3f}[h];[s][h]amix=inputs=2:normalize=0,afade=t=in:st=0:d=0.6,afade=t=out:st={ST-1.5:.2f}:d=1.5[o]" -map "[o]" {W}/suspense_v2.wav')
sh(f'ffmpeg -v error -y -f lavfi -i anullsrc=r=44100:cl=mono -i {W}/musica_raw.wav -i {W}/suspense_v2.wav -filter_complex "[0:a]atrim=0:{MU0:.3f}[z];[z][1:a]concat=n=2:v=0:a=1,atrim=0:{T:.3f}[m];[m][2:a]amix=inputs=2:duration=first:normalize=0,atrim=0:{T:.3f}[o]" -map "[o]" {W}/musica_v2.wav')
sh(f'ffmpeg -v error -y -i {W}/voz_v2.wav -i {O}/vsl8_sfx_SEM_voz.wav -i {W}/musica_v2.wav -filter_complex "[0:a]apad=whole_dur={T:.3f},aformat=channel_layouts=mono,asplit=2[v][vk];[1:a]aformat=channel_layouts=mono[s];[2:a]aformat=channel_layouts=mono[m0];[m0][vk]sidechaincompress=threshold=0.02:ratio=4:attack=20:release=300[m];[v][s][m]amix=inputs=3:duration=first:normalize=0[o]" -map "[o]" -t {T:.3f} {W}/mix_raw_v2.wav')
import re
m=sh(f'ffmpeg -hide_banner -i {W}/mix_raw_v2.wav -af loudnorm=I=-14:TP=-1.5:LRA=7:print_format=json -f null - 2>&1')
mj=json.loads(m[m.rindex('{'):m.rindex('}')+1])
sh(f'ffmpeg -v error -y -i {W}/mix_raw_v2.wav -af "loudnorm=I=-14:TP=-1.5:LRA=7:measured_I={mj["input_i"]}:measured_TP={mj["input_tp"]}:measured_LRA={mj["input_lra"]}:measured_thresh={mj["input_thresh"]}:offset={mj["target_offset"]}:linear=true" -ar 44100 {W}/mix_v2.wav')
cmd=f'ffmpeg -v error -y -i {W}/base_v2.mp4 {" ".join(inputs)} -i {W}/mix_v2.wav -filter_complex_script {W}/flt.txt -map "[vout]" -map {n}:a -t {T:.3f} -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 160k -movflags +faststart {O}/vsl8_camera_v2_1080.mp4'
sh(cmd)
sh(f'ffmpeg -v error -y -i {O}/vsl8_camera_v2_1080.mp4 -vf scale=540:960 -c:v libx264 -preset veryfast -crf 29 -c:a aac -b:a 96k -movflags +faststart {O}/vsl8_camera_v2_leve.mp4')
print('ok')
