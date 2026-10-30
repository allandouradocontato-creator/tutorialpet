#!/usr/bin/env python3
"""Animático do react (clipe + voz Marianne + Duda PARADA, sem HeyGen). Versão FINAL com clipes HeyGen no gancho e no fechamento. Uso: python3 scripts/react_lote6_heygen.py h1 [h2 ...]
Receita: react_duda_padrao.md (tela dividida 1080x1920, Duda 1080x672, clipe 1080x1248, legenda Poppins Bold 62, carimbo)."""
import subprocess, sys, os, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = f"{R}/animaticos/lote6/voz"; I = f"{R}/animaticos/lote6/img"; O = f"{R}/animaticos/lote6"; HG = f"{R}/animaticos/lote6/heygen"
CL = f"{R}/curadoria/lote6"
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
STAMP = f"{R}/assets/carimbo_tutorialpet.png"
MUS = sorted(glob.glob(f"{R}/biblioteca/musica/*.mp3"))[:1]

# t = segundos DO CLIPE em que a fala começa (P) ; C começa ao fim do clipe.
REELS = {
 "h1": dict(cid="h1", cut=(8, 28), layout="top", W="b1_W_opcao1", C="b1_W_opcao1", ogvol=0.5,
   P=[("h1_P1_briga_de_casal", None), ("h1_P2_ele_respondeu", 8.0)], Cv="h1_C_quem_responde",
   txt=[("BRIGA DE CASAL, VERSÃO PET", "h", 0, 0), ("ELE RESPONDEU: OU O QUÊ?", "c", 8, 19.9), ("QUEM RESPONDE EM CASA?", "t", 0, 0)]),
 "h2": dict(cid="h2", cut=(0, 12), layout="bottom", W="b2r_W", C="b2r_C", ogvol=1.0,
   P=[("h2_P1_golden_uma_palavra", None), ("h2_P2_mamae", 4.0)], Cv="h2_C_ja_te_chamou",
   txt=[("O GOLDEN APRENDEU UMA PALAVRA", "h", 0, 0), ("MAMÃE, MAMÃE, MAMÃE…", "c", 4, 11.9), ("O SEU JÁ TE CHAMOU DE ALGO?", "t", 0, 0)]),
 "h3": dict(cid="h3", cut=(0, 22), layout="top", W="b1_W_opcao1", C="b1_W_opcao1", ogvol=0.7,
   P=[("h3_P1_faz_que_nao_quer", None), ("h3_P2_para_continua", 14.0)], Cv="h3_C_time_para",
   txt=[("ELA FAZ QUE NÃO QUER…", "h", 0, 0), ("PARA… NÃO, CONTINUA!", "c", 14, 21.9), ("TIME PARA OU TIME CONTINUA?", "t", 0, 0)]),
 "h4": dict(cid="h4", cut=(0, 34), layout="bottom", W="b2r_W", C="b2r_C", ogvol=0.8,
   P=[("h4_P1_toda_bronca", None), ("h4_P2_girou_de_novo", 26.5)], Cv="h4_C_igual_crianca",
   txt=[("TODA BRONCA TEM A MESMA RESPOSTA", "h", 0, 0), ("GIROU DE NOVO!", "c", 26.5, 33.9), ("O SEU FINGE QUE NÃO OUVE?", "t", 0, 0)]),
 "h5": dict(cid="h5", cut=(0, 26.5), layout="top", W="b1_W_opcao1", C="b1_W_opcao1", ogvol=0.5,
   P=[("h5_P1_hoje_nao_tem_janta", None), ("h5_P2_respondeu", 22.3)], Cv="h5_C_resmunga",
   txt=[("HOJE NÃO TEM JANTA!", "h", 0, 0), ("RESPONDEU! ADOLESCENTE PET", "c", 22.3, 26.4), ("O SEU RESMUNGA NA BRONCA?", "t", 0, 0)]),
}

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())

def build(k):
    r = REELS[k]
    H = dur(f"{V}/voz_{r['P'][0][0]}.mp3") + 0.3        # gancho: quadro 0 congelado
    cs, ce = r["cut"]; L = ce - cs
    Cd = dur(f"{V}/voz_{r['Cv']}.mp3")
    Tc = H + L                                            # fim do clipe
    T = Tc + 0.3 + Cd + 0.5
    clip = f"{CL}/{r['cid']}/original.mp4"
    top = r["layout"] == "top"
    # Duda: 1080 de largura; recorte 672 em torno do rosto
    ys = 430 if r["W"].startswith("b1") else 300   # video HeyGen 1080x1920: b1 face maior
    fc = []
    fc.append(f"[0:v]trim={cs}:{ce},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1248:(iw-1080)/2:60,fps=30,tpad=start_duration={H}:start_mode=clone,tpad=stop_mode=clone:stop_duration={T-Tc+0.1},trim=duration={T},setpts=PTS-STARTPTS[cv]")
    fc.append(f"[1:v]scale=1080:-1,crop=1080:672:0:{ys},fps=30,format=yuv420p,tpad=stop_mode=clone:stop_duration=40,trim=duration={Tc+0.3},setpts=PTS-STARTPTS[dw]")
    fc.append(f"[2:v]scale=1080:-1,crop=1080:672:0:{ys},fps=30,format=yuv420p,tpad=stop_mode=clone:stop_duration=40,trim=duration={T-Tc-0.3},setpts=PTS-STARTPTS[dcc]")
    fc.append("[dw][dcc]concat=n=2:v=1:a=0[dud]")
    stack = "[dud][cv]vstack" if top else "[cv][dud]vstack"
    fc.append(f"{stack}[st]")
    # legendas
    seam = 672 if top else 1248
    y_cap = (seam - 190) if True else 0
    cur = "st"; i = 0
    for text, kind, a, b in r["txt"]:
        if kind == "h": s, e = 0.0, H
        elif kind == "c": s, e = H + a, H + b
        else: s, e = Tc + 0.3, T
        t = text.replace("'", "").replace(":", "\\:")
        fc.append(f"[{cur}]drawtext=fontfile={FONT}:text='{t}':fontsize=58:fontcolor=white:borderw=7:bordercolor=black:x=(w-text_w)/2:y={seam-110 if not top else seam+30}:enable='between(t,{s:.2f},{e:.2f})'[t{i}]")
        cur = f"t{i}"; i += 1
    fc.append(f"[3:v]scale=170:-1[stmp];[{cur}][stmp]overlay=W-w-30:H-h-30[vout]")
    # áudio
    a = [f"[0:a]atrim={cs}:{ce},asetpts=PTS-STARTPTS,volume={r['ogvol']},adelay={int(H*1000)}|{int(H*1000)}[og]"]
    labs = ["[og]"]; inp = 4
    cmd_in = []
    for n, (nm, tt) in enumerate(r["P"]):
        start = 0.0 if tt is None else H + tt
        cmd_in += ["-i", f"{V}/voz_{nm}.mp3"]
        a.append(f"[{inp}:a]adelay={int(start*1000)}|{int(start*1000)},volume=1.3[v{n}]"); labs.append(f"[v{n}]"); inp += 1
    cmd_in += ["-i", f"{V}/voz_{r['Cv']}.mp3"]
    st = Tc + 0.3
    a.append(f"[{inp}:a]adelay={int(st*1000)}|{int(st*1000)},volume=1.3[vc]"); labs.append("[vc]"); inp += 1
    if MUS:
        cmd_in += ["-stream_loop", "-1", "-i", MUS[0]]
        a.append(f"[{inp}:a]volume=0.10,atrim=0:{T}[mu]"); labs.append("[mu]")
    a.append(f"{''.join(labs)}amix=inputs={len(labs)}:duration=longest:normalize=0,atrim=0:{T},loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=level=0[aout]")
    out = f"{O}/react_lote6_{k}_{r['cid']}.mp4"
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i", clip, "-i", f"{HG}/heygen_{k}_P1.mp4", "-i", f"{HG}/heygen_{k}_C.mp4", "-i", STAMP] + cmd_in + \
          ["-filter_complex", ";".join(fc + a), "-map", "[vout]", "-map", "[aout]", "-t", f"{T:.2f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
           "-pix_fmt", "yuv420p", "-b:v", "2900k", "-maxrate", "3500k", "-bufsize", "6000k", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print(k, out, f"gancho {H:.1f}s clipe {L:.1f}s total {T:.1f}s", os.path.getsize(out)//1024, "KB")

for k in (sys.argv[1:] or REELS):
    build(k)
