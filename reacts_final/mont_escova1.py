#!/usr/bin/env python3
"""Escova vídeo 1 (cachorro rastafari): clipes Pexels (cachorro idoso, cachorros no carrinho) + fotos reais do anuncio + voz Marianne + legenda em blocos + carimbo + musica.
Uso: python3 reacts_final/mont_escova1.py  -> OUT/escova_rastafari_v2.mp4"""
import subprocess, os, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = f"{R}/animaticos/escova1"; P = f"{R}/reacts_final/escova1_fotos"; C = f"{R}/reacts_final/escova1_clipes"
OUT = os.environ.get("OUT", "/tmp/claude-0/escova1_out"); os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"; STAMP = f"{R}/assets/carimbo_tutorialpet.png"
MUS = f"{R}/biblioteca/musica/fesliyan-rasta-dreads-reggae.mp3"
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode())
# fala -> visuais [(tipo, arquivo, fracao do tempo)] e blocos de legenda
S = [("e1",[("v","fluffy_puppy_20485427.mp4",0.35),("v","shaggy_dog_8498675.mp4",0.35),("v","golden_retriever_fur_7197666.mp4",0.30)],["SEU CACHORRO VIROU","O BOB MARLEY","DOS PETS?","DREADLOCK DE GRAÇA!"]),
     ("e2",[("v","shih_tzu_28856889.mp4",0.5),("v","dog_brushing_fur_8498487.mp4",0.5)],["NÓ NO PELO","NÃO É ESTILO,","É DESCONFORTO.","BORA DESEMBARAÇAR!"]),
     ("e3",[("v","dog_shaking_off_water_30306548.mp4",0.5),("v","dog_brushing_fur_10914659.mp4",0.5)],["REGRA 1:","NUNCA MOLHE O NÓ.","ÁGUA APERTA TUDO","E VIRA RASTAFÁRI!"]),
     ("e4",[("v","dog_blow_drying_8498484.mp4",0.35),("v","dog_grooming_salon_6132703.mp4",0.3),("v","long_haired_dog_11256762.mp4",0.35)],["REGRA 2:","SEGURE O PELO","PERTO DA PELE","SOLTE DA PONTA","PRA RAIZ.","SEM PRESSA!"]),
     ("e5",[("v","dog_blow_drying_8498485.mp4",0.5),("v","golden_retriever_fur_36121834.mp4",0.5)],["REGRA 3:","DEPOIS DO BANHO,","SEQUE ATÉ EMBAIXO.","LÁ OS NÓS VOLTAM!"]),
     ("e6",[("p","p1.jpg",0.35),("p","p3.jpg",0.3),("p","p4.jpg",0.35)],["ESCOVA QUE","PENTEIA E SECA","DE UMA VEZ.","LINK NA DESCRIÇÃO","LOGO ABAIXO","ONE LOVE!"])]
GAP = 0.25; ds = [dur(f"{V}/voz_{c}.mp3") for c,_,_ in S]; starts = []; t = 0.0
for d in ds: starts.append(t); t += d + GAP
T = t + 0.4
ins = []; fc = []; segs = []; k = 0
for i,(c,vis,_) in enumerate(S):
    L = ds[i] + GAP + (0.4 if i == len(S)-1 else 0)
    for (ty,fn,fr) in vis:
        l = L*fr
        if ty == "v":
            ins += ["-ss","1","-t",f"{l:.2f}","-i",f"{C}/{fn}"]
            fc.append(f"[{k}:v]trim=0:{l:.2f},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p,setsar=1[s{k}]")
        else:
            ins += ["-loop","1","-t",f"{l:.2f}","-i",f"{P}/{fn}"]
            fc.append(f"[{k}:v]split[b{k}][f{k}];[b{k}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:5,eq=brightness=-0.08[bg{k}];"
                      f"[f{k}]scale=1080:1080,zoompan=z='1.0+0.0006*on':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1080:fps=30[fg{k}];"
                      f"[bg{k}][fg{k}]overlay=0:380,format=yuv420p,setsar=1[s{k}]")
        segs.append(f"[s{k}]"); k += 1
fc.append("".join(segs) + f"concat=n={k}:v=1:a=0[vv]")
cur = "vv"; j = 0
def esc(x): return x.replace("'", "").replace(":", "\\:")
for i,(c,_,bl) in enumerate(S):
    seg = ds[i] / len(bl)
    for q,b in enumerate(bl):
        s = starts[i] + q*seg; e = s + seg
        fc.append(f"[{cur}]drawtext=fontfile={FONT}:text='{esc(b)}':fontsize=66:fontcolor=white:borderw=8:bordercolor=black:x=(w-text_w)/2:y=1560:enable='between(t,{s:.2f},{e:.2f})'[t{j}]"); cur = f"t{j}"; j += 1
n = len(S); ns = k
ins += ["-i", STAMP]
fc.append(f"[{ns}:v]scale=170:-1[stmp];[{cur}][stmp]overlay=W-w-30:H-h-30[vout]")
for c,_,_ in S: ins += ["-i", f"{V}/voz_{c}.mp3"]
ins += ["-stream_loop","-1","-ss","12","-i",MUS]
a = [f"[{ns+1+i}:a]adelay={int(starts[i]*1000)}|{int(starts[i]*1000)},volume=1.3[a{i}]" for i in range(n)]
a.append(f"[{ns+1+n}:a]volume=0.30,atrim=0:{T:.2f}[mu]")
a.append("".join(f"[a{i}]" for i in range(n)) + f"[mu]amix=inputs={n+1}:duration=longest:normalize=0,atrim=0:{T:.2f},loudnorm=I=-14:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo[aout]")
out = f"{OUT}/escova_rastafari_v2.mp4"
subprocess.run(["ffmpeg","-loglevel","error","-y"]+ins+["-filter_complex",";".join(fc+a),"-map","[vout]","-map","[aout]","-t",f"{T:.2f}","-c:v","libx264","-preset","veryfast","-b:v","1300k","-maxrate","1600k","-bufsize","3000k","-c:a","aac","-b:a","96k","-movflags","+faststart",out],check=True)
print(out, round(T,1), "s", round(os.path.getsize(out)/1e6,2), "MB")
