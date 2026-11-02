#!/usr/bin/env python3
"""React Duda (contingência, sem HeyGen), genérico. Uso: mont_react_generico.py <pasta_animaticos> <original.mp4> "<credito>" <saida.mp4>
Original em tela cheia (loop se a voz for maior) + voz Duda + legenda gerada das falas + carimbo + selo Duda + música baixa."""
import subprocess, os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V, ORIG, CRED, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"; STAMP = f"{R}/assets/carimbo_tutorialpet.png"
MUS = f"{R}/biblioteca/musica/gr0za-party-party-music-569750.mp3"
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode())
falas = json.load(open(f"{V}/falas.json")); keys = sorted(falas)
def chunks(t, n=3):
    w = t.upper().split(); return [" ".join(w[i:i+n]) for i in range(0, len(w), n)]
S = [(k, chunks(falas[k])) for k in keys]
GAP = 0.3; T0 = 0.5; ds = [dur(f"{V}/voz_{c}.mp3") for c,_ in S]; starts = []; t = T0
for d in ds: starts.append(t); t += d + GAP
T = t + 0.5
def esc(x): return x.replace("'", "").replace(":", "\\:").replace(",", "\\,")
COVER = os.environ.get("COVER")  # "x:y:w:h" caixa para cobrir texto do original
vf0 = "[0:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1" + (f",drawbox={COVER.replace(':',':',3)}:color=black@0.92:t=fill" if False else "")
fc = [vf0 + "[vv]"]; cur = "vv"; j = 0
if COVER:
    x,y,w_,h_ = COVER.split(":"); fc[0] = vf0 + f",drawbox=x={x}:y={y}:w={w_}:h={h_}:color=black@0.95:t=fill[vv]"
for i,(c,bl) in enumerate(S):
    seg = ds[i]/len(bl)
    for q,b in enumerate(bl):
        s = starts[i]+q*seg; e = s+seg
        fc.append(f"[{cur}]drawtext=fontfile={FONT}:text='{esc(b)}':fontsize=62:fontcolor=white:borderw=8:bordercolor=black:x=(w-text_w)/2:y=1530:enable='between(t,{s:.2f},{e:.2f})'[t{j}]"); cur = f"t{j}"; j += 1
fc.append(f"[{cur}]drawtext=fontfile={FONT}:text='{esc(CRED)}':fontsize=30:fontcolor=white:borderw=4:bordercolor=black:x=20:y=H-55[cr]")
n = len(S)
fc.append(f"[1:v]scale=170:-1[stmp];[cr][stmp]overlay=W-w-30:H-h-30[vs];[{2+n}:v]scale=130:130[dud];[vs][dud]overlay=W-w-220:H-h-35[vout]")
ins = ["-stream_loop","-1","-i",ORIG,"-i",STAMP]
for c,_ in S: ins += ["-i",f"{V}/voz_{c}.mp3"]
ins += ["-i",f"{R}/assets/duda_selo_redondo.png","-stream_loop","-1","-i",MUS]
a = [f"[{2+i}:a]adelay={int(starts[i]*1000)}|{int(starts[i]*1000)},volume=1.3[a{i}]" for i in range(n)]
a.append(f"[0:a]volume=0.22,atrim=0:{T:.2f}[og]"); a.append(f"[{3+n}:a]volume=0.12,atrim=0:{T:.2f}[mu]")
a.append("".join(f"[a{i}]" for i in range(n))+f"[og][mu]amix=inputs={n+2}:duration=longest:normalize=0,atrim=0:{T:.2f},loudnorm=I=-14:TP=-1.5:LRA=11,aformat=sample_rates=48000:channel_layouts=stereo[aout]")
subprocess.run(["ffmpeg","-loglevel","error","-y"]+ins+["-filter_complex",";".join(fc+a),"-map","[vout]","-map","[aout]","-t",f"{T:.2f}","-c:v","libx264","-preset","veryfast","-b:v","1300k","-maxrate","1600k","-bufsize","3000k","-c:a","aac","-b:a","96k","-movflags","+faststart",out],check=True)
print(out, round(T,1),"s", round(os.path.getsize(out)/1e6,2),"MB")
