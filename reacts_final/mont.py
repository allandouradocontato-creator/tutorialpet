#!/usr/bin/env python3
"""Montagem final dos reacts de PRODUTO do lote 5 com clipes HeyGen (Duda W/C) + voz limpa Marianne.
Uso: python3 reacts_final/mont.py b32 [b03 b31]   (precisa de DL=pasta dos clipes e OR=pasta dos originais)"""
import subprocess, sys, os, glob, json, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = f"{R}/animaticos/lote5/voz"
DL = os.environ.get("DL", "/tmp/claude-0/dl"); OR = os.environ.get("OR", "/mnt/user-data/uploads/Tutorial Pet/reacts/originais_lote5")
OUT = os.environ.get("OUT", "/tmp/claude-0/final")
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
STAMP = f"{R}/assets/carimbo_tutorialpet.png"
MUS = sorted(glob.glob(f"{R}/biblioteca/musica/*.mp3"))[0]
OGVOL = 0.25
YS = {"top": int(os.environ.get("YS_TOP", 110)), "bottom": int(os.environ.get("YS_BOT", 300))}
REELS = {
 "b32": dict(slug="escova_secadora", orig="b32_valentina_shihtzu2_escova_secadora_para.mp4", cut=(0, 33.0), layout="bottom", t2=12.0, wn="37s", cn="6s",
   P=["b32_P1_pelo_da_trabalho", "b32_P2_seca_e_escova"], Cv="b32_C_escova_shopee",
   txt=[("PELO DÁ TRABALHO? OLHA ISSO", "h", 0, 0), ("SECA E ESCOVA JUNTO", "c", 12, 32.9), ("ESCOVA SECADORA PET · SHOPEE", "t", 0, 0)]),
 "b03": dict(slug="toca_de_gato", orig="b03_mimoracat_esta_fue_la.mp4", cut=(0, 14.0), layout="top", t2=6.0, wn="18s", cn="5s",
   P=["b03_P1_desde_que_comprei", "b03_P2_cada_no_seu_cantinho"], Cv="b03_C_toca_shopee",
   txt=[("DESDE QUE EU COMPREI ISSO…", "h", 0, 0), ("A CAMA VOLTOU A SER SUA", "c", 6, 13.9), ("TOCA DE GATO · SHOPEE", "t", 0, 0)]),
 "b31": dict(slug="fonte_automatica", orig="b31_laarissatenorio_bebedouro_fonte_de.mp4", cut=(0, 33.5), layout="bottom", t2=3.0, wn="37s", cn="6s",
   P=["b31_P1_pet_bebe_agua_parada", "b31_P2_agua_fresca_sensor"], Cv="b31_C_fonte_shopee",
   txt=[("SEU PET BEBE ÁGUA PARADA?", "h", 0, 0), ("O SENSOR LIGA SOZINHO", "c", 3, 33.4), ("FONTE AUTOMÁTICA · SHOPEE", "t", 0, 0)]),
}
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode())
def sh(c): subprocess.run(c, check=True)

def build(k):
    r = REELS[k]; os.makedirs(OUT, exist_ok=True)
    pv = lambda n: f"{V}/voz_{n}.mp3"
    H = dur(pv(r["P"][0])) + 0.3; cs, ce = r["cut"]; L = ce - cs; Cd = dur(pv(r["Cv"]))
    Tc = H + L; T = Tc + 0.3 + Cd + 0.5
    W = f"{DL}/react_{k}_duda_clipe_W_olhando_clipe_{r['wn']}.mp4"; C = f"{DL}/react_{k}_duda_clipe_C_camera_{r['cn']}.mp4"
    top = r["layout"] == "top"; ys = YS["top" if top else "bottom"]; seam = 672 if top else 1248
    orig = f"{OR}/{r['orig']}"
    # ---- áudio: mix -> loudnorm 2 passes -> alimiter
    mixwav = f"{OUT}/{k}_mix.wav"
    a = [f"[0:a]atrim={cs}:{ce},asetpts=PTS-STARTPTS,volume={OGVOL},adelay={int(H*1000)}|{int(H*1000)}[og]"]
    labs = ["[og]"]; ins = ["-i", orig]; n = 1
    for i, nm in enumerate(r["P"]):
        st = 0.0 if i == 0 else H + r["t2"]
        ins += ["-i", pv(nm)]; a.append(f"[{n}:a]adelay={int(st*1000)}|{int(st*1000)},volume=1.3[v{i}]"); labs.append(f"[v{i}]"); n += 1
    st = Tc + 0.3
    ins += ["-i", pv(r["Cv"])]; a.append(f"[{n}:a]adelay={int(st*1000)}|{int(st*1000)},volume=1.3[vc]"); labs.append("[vc]"); n += 1
    ins += ["-stream_loop", "-1", "-i", MUS]; a.append(f"[{n}:a]volume=0.10,atrim=0:{T:.3f}[mu]"); labs.append("[mu]")
    a.append(f"{''.join(labs)}amix=inputs={len(labs)}:duration=longest:normalize=0,atrim=0:{T:.3f},aformat=sample_rates=48000:channel_layouts=stereo[aout]")
    sh(["ffmpeg","-loglevel","error","-y"]+ins+["-filter_complex",";".join(a),"-map","[aout]","-t",f"{T:.3f}",mixwav])
    p = subprocess.run(["ffmpeg","-hide_banner","-y","-i",mixwav,"-af","loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True).stderr
    m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p, re.S).group(0))
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,alimiter=level=0")
    nwav = f"{OUT}/{k}_norm.wav"
    sh(["ffmpeg","-loglevel","error","-y","-i",mixwav,"-af",ln,"-ar","48000",nwav])
    # ---- vídeo
    fc = [f"[0:v]trim={cs}:{ce},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1248:(iw-1080)/2:60,fps=30,tpad=start_duration={H}:start_mode=clone,tpad=stop_mode=clone:stop_duration={T-Tc+0.1},trim=duration={T:.3f},setpts=PTS-STARTPTS[cv]"]
    for n_, tag in ((1,"w"),(2,"c")):
        fc.append(f"[{n_}:v]scale=1080:-1,crop=1080:672:0:{ys},fps=30,format=yuv420p[d{tag}0]")
    fc.append(f"[dw0]trim=duration={Tc+0.15:.3f},setpts=PTS-STARTPTS[dw];[dc0]trim=duration={T-Tc-0.15:.3f},setpts=PTS-STARTPTS[dcc];[dw][dcc]concat=n=2:v=1:a=0[dud]")
    fc.append(("[dud][cv]vstack" if top else "[cv][dud]vstack") + "[st]")
    cur = "st"
    for i, (text, kind, a_, b_) in enumerate(r["txt"]):
        s, e = (0.0, H) if kind == "h" else ((H+a_, H+b_) if kind == "c" else (Tc+0.3, T))
        t = text.replace("'", "").replace(":", "\\:")
        fc.append(f"[{cur}]drawtext=fontfile={FONT}:text='{t}':fontsize=58:fontcolor=white:borderw=7:bordercolor=black:x=(w-text_w)/2:y={seam+30 if top else seam-110}:enable='between(t,{s:.2f},{e:.2f})'[t{i}]"); cur = f"t{i}"
    fc.append(f"[3:v]scale=170:-1[stmp];[{cur}][stmp]overlay=W-w-30:H-h-30[vout]")
    bv = int(9.3*8*1024*1024/T/1000 - 128)  # alvo < 10 MB
    out = f"{OUT}/react_{k}_{r['slug']}_duda_final.mp4"
    sh(["ffmpeg","-loglevel","error","-y","-i",orig,"-i",W,"-i",C,"-i",STAMP,"-i",nwav,"-filter_complex",";".join(fc),"-map","[vout]","-map","4:a","-t",f"{T:.2f}",
        "-c:v","libx264","-preset","veryfast","-pix_fmt","yuv420p","-b:v",f"{bv}k","-maxrate",f"{int(bv*1.3)}k","-bufsize",f"{bv*2}k","-c:a","aac","-b:a","128k","-movflags","+faststart",out])
    print(k, out, f"H={H:.2f} Tc={Tc:.2f} T={T:.2f}", os.path.getsize(out)/1e6, "MB", "loudnorm in", m["input_i"], m["input_tp"])
for k in (sys.argv[1:] or REELS): build(k)
