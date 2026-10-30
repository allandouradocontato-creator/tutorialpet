#!/usr/bin/env python3
"""Animático do react (clipe + voz Marianne + Duda PARADA, sem HeyGen). Uso: python3 scripts/animatico_lote5.py r4_1 [r4_2 r4_p1 r4_p2]
Receita: react_duda_padrao.md (tela dividida 1080x1920, Duda 1080x672, clipe 1080x1248, legenda Poppins Bold 62, carimbo)."""
import subprocess, sys, os, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = f"{R}/animaticos/lote5/voz"; I = f"{R}/animaticos/lote5/img"; O = f"{R}/animaticos/lote5"
CL = f"{R}/curadoria/lote5"
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
STAMP = f"{R}/assets/carimbo_tutorialpet.png"
MUS = sorted(glob.glob(f"{R}/biblioteca/musica/*.mp3"))[:1]

# t = segundos DO CLIPE em que a fala começa (P) ; C começa ao fim do clipe.
REELS = {
 "a09": dict(cid="a09", cut=(0, 17.5), layout="top", W="b1_W_opcao1", C="b1_W_opcao1", ogvol=0.35,
   P=[("a09_P1_gata_copo_impressora", None), ("a09_P2_susto_parcelado", 9.5)], Cv="a09_C_barulho_subito",
   txt=[("GATA + COPO D'ÁGUA + IMPRESSORA", "h", 0, 0), ("O SUSTO PARCELADO", "c", 9.5, 17.4), ("SEU GATO TAMBÉM? COMENTA", "t", 0, 0)]),
 "a16": dict(cid="a16", cut=(0, 14.1), layout="bottom", W="b2r_W", C="b2r_C", ogvol=0.5,
   P=[("a16_P1_salsicha_chegando", None), ("a16_P2_apocalipse_carteiro", 5.0)], Cv="a16_C_time_salsicha",
   txt=[("SALSICHA CHEGANDO…", "h", 0, 0), ("O APOCALIPSE DO CARTEIRO", "c", 5, 14.0), ("TIME SOLO OU TIME MATILHA?", "t", 0, 0)]),
 "a17": dict(cid="a17", cut=(0, 25.3), layout="top", W="b1_W_opcao1", C="b1_W_opcao1", ogvol=0.35,
   P=[("a17_P1_coletiva_imprensa", None), ("a17_P2_deu_declaracao_fugiu", 21.8)], Cv="a17_C_gato_fala_com_voce",
   txt=[("COLETIVA DE IMPRENSA COM A GATA", "h", 0, 0), ("DEU A DECLARAÇÃO E FUGIU", "c", 21.8, 25.2), ("O SEU FALA COM VOCÊ?", "t", 0, 0)]),
 "b32": dict(cid="b32", cut=(0, 33.0), layout="bottom", W="b2r_W", C="b2r_C", ogvol=0.35,
   P=[("b32_P1_pelo_da_trabalho", None), ("b32_P2_seca_e_escova", 12.0)], Cv="b32_C_escova_shopee",
   txt=[("PELO DÁ TRABALHO? OLHA ISSO", "h", 0, 0), ("SECA E ESCOVA JUNTO", "c", 12, 32.9), ("ESCOVA SECADORA PET · SHOPEE", "t", 0, 0)]),
 "b03": dict(cid="b03", cut=(0, 14.0), layout="top", W="b1_W_opcao1", C="b1_W_opcao1", ogvol=0.25,
   P=[("b03_P1_desde_que_comprei", None), ("b03_P2_cada_no_seu_cantinho", 6.0)], Cv="b03_C_toca_shopee",
   txt=[("DESDE QUE EU COMPREI ISSO…", "h", 0, 0), ("A CAMA VOLTOU A SER SUA", "c", 6, 13.9), ("TOCA DE GATO · SHOPEE", "t", 0, 0)]),
 "b31": dict(cid="b31", cut=(0, 33.5), layout="bottom", W="b2r_W", C="b2r_C", ogvol=0.3,
   P=[("b31_P1_pet_bebe_agua_parada", None), ("b31_P2_agua_fresca_sensor", 3.0)], Cv="b31_C_fonte_shopee",
   txt=[("SEU PET BEBE ÁGUA PARADA?", "h", 0, 0), ("O SENSOR LIGA SOZINHO", "c", 3, 33.4), ("FONTE AUTOMÁTICA · SHOPEE", "t", 0, 0)]),
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
    ys = 110 if r["W"].startswith("b1") else 300
    fc = []
    fc.append(f"[0:v]trim={cs}:{ce},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1248:(iw-1080)/2:60,fps=30,tpad=start_duration={H}:start_mode=clone,tpad=stop_mode=clone:stop_duration={T-Tc+0.1},trim=duration={T},setpts=PTS-STARTPTS[cv]")
    for n, (nm, tag) in enumerate([(r["W"], "w"), (r["C"], "c")]):
        fc.append(f"[{1+n}:v]scale=1080:-1,crop=1080:672:0:{ys},fps=30,format=yuv420p[d{tag}0]")
    fc.append(f"[dw0]trim=duration={Tc+0.15},setpts=PTS-STARTPTS[dw];[dc0]trim=duration={T-Tc-0.15},setpts=PTS-STARTPTS[dcc];[dw][dcc]concat=n=2:v=1:a=0[dud]")
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
    out = f"{O}/animatico_{k}_{r['cid']}.mp4"
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i", clip, "-loop", "1", "-framerate", "30", "-i", f"{I}/{r['W']}.jpg",
           "-loop", "1", "-framerate", "30", "-i", f"{I}/{r['C']}.jpg", "-i", STAMP] + cmd_in + \
          ["-filter_complex", ";".join(fc + a), "-map", "[vout]", "-map", "[aout]", "-t", f"{T:.2f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
           "-pix_fmt", "yuv420p", "-b:v", "2900k", "-maxrate", "3500k", "-bufsize", "6000k", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print(k, out, f"gancho {H:.1f}s clipe {L:.1f}s total {T:.1f}s", os.path.getsize(out)//1024, "KB")

for k in (sys.argv[1:] or REELS):
    build(k)
