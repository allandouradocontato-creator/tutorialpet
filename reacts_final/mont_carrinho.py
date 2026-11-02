#!/usr/bin/env python3
"""Video do carrinho de passeio pet (idoso): fotos reais do anuncio em tela cheia + voz Marianne + legenda em blocos + carimbo + musica.
Uso: python3 reacts_final/mont_carrinho.py  (voz em animaticos/carrinho/voz_c1..c5.mp3). Saida em OUT (padrao /tmp/claude-0/carrinho_out)."""
import subprocess, os, glob, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = f"{R}/animaticos/carrinho"; P = f"{R}/reacts_final/carrinho_fotos"
OUT = os.environ.get("OUT", "/tmp/claude-0/carrinho_out"); os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"; STAMP = f"{R}/assets/carimbo_tutorialpet.png"
MUS = sorted(glob.glob(f"{R}/biblioteca/musica/*.mp3"))[0]
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode())
# cena: (fala, foto, [blocos de legenda])
S = [("c1","p4.jpg",["SEU CACHORRO IDOSO","AINDA QUER PASSEAR,","MAS AS JUNTAS","JÁ NÃO AJUDAM?"]),
     ("c2","p3.jpg",["CARRINHO DOBRÁVEL","LEVA SEU CACHORRO","ATÉ 15 QUILOS"]),
     ("c3","p5.jpg",["PASSEIA SEM SE CANSAR","E LEVA SEU","MELHOR AMIGO","PRA RUA"]),
     ("c4","p1.jpg",["NOTA 4,9 NA SHOPEE","MAIS DE 300","VENDIDOS"]),
     ("c5","p4.jpg",["LINK NO FACEBOOK","DO TUTORIAL PET","É SÓ TOCAR!"])]
GAP = 0.25; ds = [dur(f"{V}/voz_{c}.mp3") for c,_,_ in S]; starts = []; t = 0.0
for d in ds: starts.append(t); t += d + GAP
T = t + 0.4
ins = []; fc = []; lab = []
for i,(c,img,_) in enumerate(S):
    L = ds[i] + GAP + (0.4 if i == len(S)-1 else 0)
    ins += ["-loop","1","-t",f"{L:.2f}","-i",f"{P}/{img}"]
    fc.append(f"[{i}:v]split[b{i}][f{i}];[b{i}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:5,eq=brightness=-0.08[bg{i}];"
              f"[f{i}]scale=1080:1080,zoompan=z='1.0+0.0006*on':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1080:fps=30[fg{i}];"
              f"[bg{i}][fg{i}]overlay=0:380,format=yuv420p,setsar=1[s{i}]")
fc.append("".join(f"[s{i}]" for i in range(len(S))) + f"concat=n={len(S)}:v=1:a=0[vv]")
cur = "vv"; j = 0
def esc(x): return x.replace("'", "").replace(":", "\\:")
for i,(c,_,bl) in enumerate(S):
    seg = ds[i] / len(bl)
    for k,b in enumerate(bl):
        s = starts[i] + k*seg; e = s + seg
        fc.append(f"[{cur}]drawtext=fontfile={FONT}:text='{esc(b)}':fontsize=66:fontcolor=white:borderw=8:bordercolor=black:x=(w-text_w)/2:y=1560:enable='between(t,{s:.2f},{e:.2f})'[t{j}]"); cur = f"t{j}"; j += 1
n = len(S)
ins += ["-i", STAMP]
fc.append(f"[{n}:v]scale=170:-1[stmp];[{cur}][stmp]overlay=W-w-30:H-h-30[vout]")
ai = []
for i,(c,_,_) in enumerate(S): ins += ["-i", f"{V}/voz_{c}.mp3"]
ins += ["-stream_loop","-1","-i",MUS]
a = [f"[{n+1+i}:a]adelay={int(starts[i]*1000)}|{int(starts[i]*1000)},volume=1.3[a{i}]" for i in range(n)]
a.append(f"[{2*n+1}:a]volume=0.10,atrim=0:{T:.2f}[mu]")
a.append("".join(f"[a{i}]" for i in range(n)) + f"[mu]amix=inputs={n+1}:duration=longest:normalize=0,atrim=0:{T:.2f},loudnorm=I=-14:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo[aout]")
out = f"{OUT}/carrinho_idoso_v1.mp4"
subprocess.run(["ffmpeg","-loglevel","error","-y"]+ins+["-filter_complex",";".join(fc+a),"-map","[vout]","-map","[aout]","-t",f"{T:.2f}","-c:v","libx264","-preset","veryfast","-b:v","2400k","-maxrate","3000k","-bufsize","5000k","-c:a","aac","-b:a","128k","-movflags","+faststart",out],check=True)
print(out, round(T,1), "s", round(os.path.getsize(out)/1e6,2), "MB")
