#!/usr/bin/env python3
"""Animático do react (clipe + voz Marianne + Duda PARADA, sem HeyGen). Uso: python3 scripts/animatico_lote4.py r4_1 [r4_2 r4_p1 r4_p2]
Receita: react_duda_padrao.md (tela dividida 1080x1920, Duda 1080x672, clipe 1080x1248, legenda Poppins Bold 62, carimbo)."""
import subprocess, sys, os, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = f"{R}/animaticos/lote4/voz"; I = f"{R}/animaticos/lote4/img"; O = f"{R}/animaticos/lote4"
CL = "/mnt/user-data/outputs/lote4"
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
STAMP = f"{R}/assets/carimbo_tutorialpet.png"
MUS = sorted(glob.glob(f"{R}/biblioteca/musica/*.mp3"))[:1]

# t = segundos DO CLIPE em que a fala começa (P) ; C começa ao fim do clipe.
REELS = {
 "r4_1": dict(clip="a06_metropolesoficial_ele_ama_carinho", cut=(0, 23.0), layout="bottom", W="b2r_W", C="b2r_C", ogvol=0.6,
   P=[("r4_1_P1_ela_chama", None), ("r4_1_P2_dengoso", 11.0), ("r4_1_P3_patinhas", 22.6)], Cv="r4_1_C_voz_aguda",
   txt=[("ELA CHAMA… E OLHA QUEM VEM", "h", 0, 0), ("CHEGOU O DENGOSO", "c", 11, 22.5), ("VOZ AGUDA + NOME = ELE VEM", "t", 0, 0)]),
 "r4_2": dict(clip="a11_d3faultus3r_gatinho_caixa_areia_cheia", cut=(0, 24.0), layout="top", W="b1_W_opcao1", C="b1_W_opcao1", ogvol=0.25,
   P=[("r4_2_P1_caixa_tamanho", None), ("r4_2_P2_nadando", 11.7)], Cv="r4_2_C_areia_demais",
   txt=[("POV: ENCHEU A CAIXA DE AREIA", "h", 0, 0), ("NADANDO NA AREIA", "c", 11.7, 23.9), ("O CERTO: 5 A 7 CM", "t", 0, 0)]),
 "r4_p1": dict(clip="b03_yana_denise_descobri_que_nao", cut=(0, 33.0), layout="bottom", W="b2r_W", C="b2r_C", ogvol=0.4,
   P=[("r4_p1_P1_xixi_vivi", None), ("r4_p1_P2_spray_onde_nao", 18.0), ("r4_p1_P3_tapete_salvou", 27.0)], Cv="r4_p1_C_kit_link",
   txt=[("EU VIVI ISSO", "h", 0, 0), ("XIXI NÃO / XIXI SIM", "c", 18, 32.9), ("SPRAY + ROTINA = XIXI NO LUGAR", "t", 0, 0)]),
 "r4_p2": dict(clip="b09_sofpet_cl_menos_saltos_mas", cut=(0, 10.5), layout="bottom", W="b2r_W", C="b2r_C", ogvol=0.15,
   P=[("r4_p2_P1_cachorro_pula", None), ("r4_p2_P2_subiu_sem_pular", 7.0)], Cv="r4_p2_C_escadinha",
   txt=[("SEU CACHORRO PULA DA CAMA?", "h", 0, 0), ("SUBIU SEM PULAR", "c", 7, 10.4), ("PEQUENO OU IDOSO: ESCADA, NÃO PULO", "t", 0, 0)]),
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
    clip = f"{CL}/{r['clip']}.mp4"
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
    out = f"{O}/animatico_{k}_{r['clip'][:3]}.mp4"
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i", clip, "-loop", "1", "-framerate", "30", "-i", f"{I}/{r['W']}.jpg",
           "-loop", "1", "-framerate", "30", "-i", f"{I}/{r['C']}.jpg", "-i", STAMP] + cmd_in + \
          ["-filter_complex", ";".join(fc + a), "-map", "[vout]", "-map", "[aout]", "-t", f"{T:.2f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
           "-pix_fmt", "yuv420p", "-b:v", "2900k", "-maxrate", "3500k", "-bufsize", "6000k", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print(k, out, f"gancho {H:.1f}s clipe {L:.1f}s total {T:.1f}s", os.path.getsize(out)//1024, "KB")

for k in (sys.argv[1:] or REELS):
    build(k)
