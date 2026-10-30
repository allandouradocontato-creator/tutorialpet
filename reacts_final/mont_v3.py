#!/usr/bin/env python3
"""V3 conversa (N = fala de amiga, Duda só no gancho e no fechamento C2). Base V2 (Allan 30/10: Duda some no meio p/ economizar HeyGen; voz explica o produto). Montagem final dos reacts de PRODUTO do lote 5 com clipes HeyGen (Duda W/C) + voz limpa Marianne.
Uso: python3 reacts_final/mont.py b32 [b03 b31]   (precisa de DL=pasta dos clipes e OR=pasta dos originais)"""
import subprocess, sys, os, glob, json, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = f"{R}/animaticos/lote5/voz"; E = f"{R}/animaticos/lote5/explicacao"
DL = os.environ.get("DL", "/tmp/claude-0/dl"); OR = os.environ.get("OR", "/mnt/user-data/uploads/Tutorial Pet/reacts/originais_lote5")
OUT = os.environ.get("OUT", "/tmp/claude-0/final")
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
STAMP = f"{R}/assets/carimbo_tutorialpet.png"
MUS = sorted(glob.glob(f"{R}/biblioteca/musica/*.mp3"))[0]
OGVOL = 0.25
YS = {"top": int(os.environ.get("YS_TOP", 110)), "bottom": int(os.environ.get("YS_BOT", 300))}

# linhas do meio: (tipo, nome, início em segundos do CLIPE, atempo, legenda). tipo P = fala original (voz/), E = explicação (explicacao/)
REELS = {
 "b32": dict(slug="escova_secadora", orig="b32_valentina_shihtzu2_escova_secadora_para.mp4", cut=(0, 33.0), layout="bottom", wn="37s",
   P1="b32_P1_pelo_da_trabalho", Cv="b32_C2", hook="PELO DÁ TRABALHO? OLHA ISSO", tag="ESCOVA SECADORA PET · SHOPEE",
   L=[("N","b32_N1",0.3,1,'Gente, olha essa cena. Quem tem cachorro peludo conhece o drama: uma hora de secador e o bicho tremendo.'),
      ("P","b32_P2_seca_e_escova",8.7,1,"SECA E ESCOVA JUNTO"),
      ("N","b32_N2",13.4,1,'Olha, é uma escova que sopra ar quente. Você penteia e seca junto, numa passada só, e o nó nem forma.'),
      ("N","b32_N3",21.8,1,'Sério, pra mim isso é mão na roda: nada de banho e tosa toda semana, e custa menos de cinquenta reais.'),
      ("N","b32_N4",29.6,1,'Dez mil tutores já levaram. Tem motivo.')]),
 "b03": dict(slug="toca_de_gato", orig="b03_mimoracat_esta_fue_la.mp4", cut=(0, 20.0), ext=True, layout="top", wn="18s",
   P1="b03_P1_desde_que_comprei", Cv="b03_C2", hook="DESDE QUE EU COMPREI ISSO…", tag="TOCA DE GATO · SHOPEE",
   L=[("N","b03_N1",0.2,1,'Amiga, gato dormindo em cima de você e pelo no travesseiro? Olha o que essa menina fez.'),
      ("P","b03_P2_cada_no_seu_cantinho",6.5,1,"CADA UM NO SEU CANTINHO"),
      ("N","b03_N2",12.15,1.08,'É quentinha, é fofa, o gato entra e não sai mais. Menos de quarenta reais, e mais de três mil já levaram.')]),
 "b31": dict(slug="fonte_automatica", orig="b31_laarissatenorio_bebedouro_fonte_de.mp4", cut=(0, 33.5), layout="bottom", wn="37s",
   P1="b31_P1_pet_bebe_agua_parada", Cv="b31_C2", hook="SEU PET BEBE ÁGUA PARADA?", tag="FONTE AUTOMÁTICA · SHOPEE",
   L=[("N","b31_N1",0.3,1,'Gente, água parada no pote esquenta, junta pelo, poeira… e o bicho vai bebendo cada vez menos.'),
      ("P","b31_P2_agua_fresca_sensor",8.1,1,"O SENSOR LIGA SOZINHO"),
      ("N","b31_N2",13.1,1,'E pet que bebe pouca água é o que mais dá problema de rim, qualquer veterinário te fala isso.'),
      ("N","b31_N3",19.55,1,'Essa aqui não tem fio, liga sozinha quando ele chega, e a água sai sempre fresquinha. Olha a carinha dele.'),
      ("N","b31_N4",27.2,1,'Isso é mão na roda, sério. Milhares de tutores já levaram.')]),
}
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode())
def sh(c): subprocess.run(c, check=True)
def wrap(t):
    if len(t) <= 26: return [t]
    mid = len(t)//2; i = min([j for j,c in enumerate(t) if c==" "], key=lambda j: abs(j-mid)); return [t[:i], t[i+1:]]
def esc(t): return t.replace("'", "").replace(":", "\\:")

def build(k):
    r = REELS[k]; os.makedirs(OUT, exist_ok=True)
    pv = lambda n: (f"{E}/voz_{n}.mp3" if re.match(r"b\d\d_(N\d|C2|V\d|E\d)", n) else f"{V}/voz_{n}.mp3")
    H = dur(pv(r["P1"])) + 0.3; cs, ce = r["cut"]; Cd = dur(pv(r["Cv"]))
    Tc = H + (ce - cs); T = Tc + 0.3 + Cd + 0.5
    W = f"{DL}/react_{k}_duda_clipe_W_olhando_clipe_{r['wn']}.mp4"; C = sorted(glob.glob(f"{DL}/react_{k}_duda_clipe_C2_camera_*s.mp4"))[-1]
    top = r["layout"] == "top"; ys = YS["top" if top else "bottom"]; seam = 672 if top else 1248
    orig = f"{OR}/{r['orig']}"
    if r.get("ext"):  # original curto: repete os segundos 8-14 para dar tempo de vender
        extf = f"{OUT}/{k}_ext.mp4"
        sh(["ffmpeg","-loglevel","error","-y","-i",orig,"-filter_complex","[0:v]trim=0:14,setpts=PTS-STARTPTS[a];[0:v]trim=8:14.08,setpts=PTS-STARTPTS[b];[0:a]atrim=0:14,asetpts=PTS-STARTPTS[c];[0:a]atrim=8:14.08,asetpts=PTS-STARTPTS[d];[a][c][b][d]concat=n=2:v=1:a=1[v][au]","-map","[v]","-map","[au]","-r","30",extf])
        orig = extf
    # ---- áudio
    a = [f"[0:a]atrim={cs}:{ce},asetpts=PTS-STARTPTS,volume={OGVOL},adelay={int(H*1000)}|{int(H*1000)}[og]"]
    labs = ["[og]"]; ins = ["-i", orig]; n = 1
    items = [(0.0, r["P1"], 1)] + [(H+t, nm, at) for (_, nm, t, at, _) in r["L"]] + [(Tc+0.3, r["Cv"], 1)]
    prev_end = 0.0
    for i, (st, nm, at) in enumerate(items):
        d = dur(pv(nm)) / at
        if st < prev_end + 0.15 - 1e-6 and i > 0: print("AVISO sobreposição", k, nm, round(st,2), "<", round(prev_end,2))
        prev_end = st + d
        ins += ["-i", pv(nm)]
        f = f"atempo={at}," if at != 1 else ""
        a.append(f"[{n}:a]{f}adelay={int(st*1000)}|{int(st*1000)},volume=1.3[v{i}]"); labs.append(f"[v{i}]"); n += 1
    ins += ["-stream_loop", "-1", "-i", MUS]; a.append(f"[{n}:a]volume=0.10,atrim=0:{T:.3f}[mu]"); labs.append("[mu]")
    a.append(f"{''.join(labs)}amix=inputs={len(labs)}:duration=longest:normalize=0,atrim=0:{T:.3f},aformat=sample_rates=48000:channel_layouts=stereo[aout]")
    mixwav = f"{OUT}/{k}_v3_mix.wav"
    sh(["ffmpeg","-loglevel","error","-y"]+ins+["-filter_complex",";".join(a),"-map","[aout]","-t",f"{T:.3f}",mixwav])
    p = subprocess.run(["ffmpeg","-hide_banner","-y","-i",mixwav,"-af","loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True).stderr
    m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p, re.S).group(0))
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,alimiter=level=0")
    nwav = f"{OUT}/{k}_v3_norm.wav"
    sh(["ffmpeg","-loglevel","error","-y","-i",mixwav,"-af",ln,"-ar","48000",nwav])
    # ---- vídeo: S = tela dividida (gancho e fechamento); F = original em tela cheia (meio, Duda some)
    fc = [f"[0:v]split[o1][o2]",
          f"[o1]trim={cs}:{ce},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1248:(iw-1080)/2:60,fps=30,tpad=start_duration={H}:start_mode=clone,tpad=stop_mode=clone:stop_duration={T-Tc+0.1},trim=duration={T:.3f},setpts=PTS-STARTPTS[cv]",
          f"[o2]trim={cs}:{ce},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,tpad=start_duration={H}:start_mode=clone,tpad=stop_mode=clone:stop_duration={T-Tc+0.1},trim=duration={T:.3f},setpts=PTS-STARTPTS[full]"]
    for n_, tag in ((1,"w"),(2,"c")):
        fc.append(f"[{n_}:v]scale=1080:-1,crop=1080:672:0:{ys},fps=30,format=yuv420p,tpad=stop_mode=clone:stop_duration=20[d{tag}0]")
    fc.append(f"[dw0]trim=duration={Tc+0.15:.3f},setpts=PTS-STARTPTS[dw];[dc0]trim=duration={T-Tc-0.15:.3f},setpts=PTS-STARTPTS[dcc];[dw][dcc]concat=n=2:v=1:a=0[dud]")
    fc.append(("[dud][cv]vstack" if top else "[cv][dud]vstack") + "[st]")
    ytxt = seam+30 if top else seam-110
    def dt(src, text, y, s, e, out, size=58):
        return f"[{src}]drawtext=fontfile={FONT}:text='{esc(text)}':fontsize={size}:fontcolor=white:borderw=7:bordercolor=black:x=(w-text_w)/2:y={y}:enable='between(t,{s:.2f},{e:.2f})'[{out}]"
    fc.append(dt("st", r["hook"], ytxt, 0.0, H, "h0"))
    fc.append(f"[h0][full]overlay=0:0:enable='between(t,{H:.3f},{Tc+0.15:.3f})'[ov]")
    cur = "ov"; j = 0
    for (kind, nm, t, at, txt), (st, _, _) in zip(r["L"], items[1:-1]):
        s_, e_ = st, st + dur(pv(nm))/at
        words = txt.upper().split(); lines_ = []; ln = ""
        for w in words:  # linhas de até 22 caracteres; 2 linhas por bloco
            if ln and len(ln) + 1 + len(w) > 22: lines_.append(ln); ln = w
            else: ln = (ln + " " + w).strip()
        if ln: lines_.append(ln)
        blocks = [lines_[i:i+2] for i in range(0, len(lines_), 2)]
        tot = sum(len(" ".join(bl)) for bl in blocks); cs_ = s_
        for bl in blocks:
            ce_ = cs_ + (e_ - s_) * len(" ".join(bl)) / tot
            for li, ln_ in enumerate(bl):
                y = 1330 + li*72 - (len(bl)-1)*36
                fc.append(dt(cur, ln_, y, cs_, ce_ + (0.1 if bl is blocks[-1] else 0), f"c{j}", 56)); cur = f"c{j}"; j += 1
            cs_ = ce_
    fc.append(dt(cur, r["tag"], ytxt, Tc+0.3, T, "tg"))
    fc.append(f"[3:v]scale=170:-1[stmp];[tg][stmp]overlay=W-w-30:H-h-30[vout]")
    bv = int(9.3*8*1024*1024/T/1000 - 128)
    out = f"{OUT}/react_{k}_{r['slug']}_duda_v3_conversa.mp4"
    sh(["ffmpeg","-loglevel","error","-y","-i",orig,"-i",W,"-i",C,"-i",STAMP,"-i",nwav,"-filter_complex",";".join(fc),"-map","[vout]","-map","4:a","-t",f"{T:.2f}",
        "-c:v","libx264","-preset","veryfast","-pix_fmt","yuv420p","-b:v",f"{bv}k","-maxrate",f"{int(bv*1.3)}k","-bufsize",f"{bv*2}k","-c:a","aac","-b:a","128k","-movflags","+faststart",out])
    print(k, out, f"H={H:.2f} Tc={Tc:.2f} T={T:.2f}", round(os.path.getsize(out)/1e6,2), "MB", "loudnorm in", m["input_i"], m["input_tp"])
for k in (sys.argv[1:] or REELS): build(k)
