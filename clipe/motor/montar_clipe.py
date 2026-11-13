#!/usr/bin/env python3
"""Motor do Clipe do Pet: monta um vídeo vertical 9:16 (até ~50 s) a partir das fotos/vídeos do cliente.

Uso:
  python3 clipe/motor/montar_clipe.py --molde homenagem --midias pasta_com_fotos \
      --nome Thor --frase "Te amamos" --saida clipe.mp4 [--leve] [--musica arquivo.mp3]

- molde: homenagem | aniversario | retrospectiva | um_dia | diversao (clipe/moldes/*.json)
- midias: pasta com 2 a 20 arquivos (jpg/png/webp; mp4/mov), usados em ordem de nome. De cada VÍDEO o motor escolhe os melhores
  trechos (escolher_trechos.py); arquivo NN_anim.mp4 = foto já animada (entra inteira, sem recorte)
- --musica: arquivo externo (ex.: a Música do Pet do cliente); sem ele usa a trilha do molde
- --leve: 540x960, arquivo pequeno (versão de teste/prévia)
Só ffmpeg + Pillow, sem serviço pago e sem depender do PC de ninguém.
"""
import argparse, json, math, shutil, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
from escolher_trechos import escolher as escolher_trechos  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
MOTOR = Path(__file__).resolve().parent
MOLDES = MOTOR.parent / "moldes"
MUSICAS = RAIZ / "biblioteca" / "musica"
FONTE_XB = MOTOR / "fonte" / "Inter-ExtraBold.otf"
FONTE_B = MOTOR / "fonte" / "Inter-Bold.otf"
CARIMBO = MOTOR / "carimbo_tutorialpet.png"
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
VID_EXT = {".mp4", ".mov", ".m4v", ".webm"}
MAX_SEG = 50.0      # duração máxima do clipe (base)
ABERTURA = 3.0      # abertura (1ª mídia com título)
FINAL = 3.4         # fechamento
XF = 0.35           # crossfade entre cenas
FPS = 30


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError("ffmpeg/ffprobe falhou:\n" + " ".join(map(str, cmd))[:400] + "\n" + r.stderr[-1500:])
    return r


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def quebra(draw, texto, fonte, largura):
    palavras, linhas, atual = texto.split(), [], ""
    for p in palavras:
        teste = (atual + " " + p).strip()
        if draw.textlength(teste, font=fonte) <= largura or not atual:
            atual = teste
        else:
            linhas.append(atual)
            atual = p
    if atual:
        linhas.append(atual)
    return linhas


def camada_texto(W, H, titulo, subtitulo, cor, destino, grande=False, escurecer=False):
    """PNG transparente com legenda grande (stroke) na zona segura (acima da UI das redes)."""
    esc = W / 1080
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if escurecer:
        d.rectangle([0, 0, W, H], fill=(0, 0, 0, 120))
    f1 = ImageFont.truetype(str(FONTE_XB), int((92 if grande else 80) * esc))
    f2 = ImageFont.truetype(str(FONTE_B), int(52 * esc))
    margem = int(80 * esc)
    l1 = quebra(d, titulo, f1, W - 2 * margem)
    l2 = quebra(d, subtitulo, f2, W - 2 * margem) if subtitulo else []
    alt1 = int(f1.size * 1.18)
    alt2 = int(f2.size * 1.25)
    bloco = len(l1) * alt1 + (int(26 * esc) + len(l2) * alt2 if l2 else 0)
    # faixa de leitura: centro do bloco em ~63 % da altura (acima dos 22 % de baixo cortados pelas redes)
    topo = int(H * 0.63 - bloco / 2)
    faixa = [0, topo - int(50 * esc), W, topo + bloco + int(50 * esc)]
    grad = Image.new("RGBA", (W, faixa[3] - faixa[1]), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    n = grad.size[1]
    for y in range(n):
        a = int(190 * math.sin(math.pi * y / n) ** 0.6)
        gd.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    im.alpha_composite(grad, (0, faixa[1]))
    y = topo
    stroke = max(3, int(7 * esc))
    for t in l1:
        w = d.textlength(t, font=f1)
        d.text(((W - w) / 2, y), t, font=f1, fill=(255, 255, 255, 255), stroke_width=stroke, stroke_fill=(20, 20, 20, 255))
        y += alt1
    if l2:
        y += int(26 * esc)
        for t in l2:
            w = d.textlength(t, font=f2)
            d.text(((W - w) / 2, y), t, font=f2, fill=hex_rgb(cor) + (255,), stroke_width=max(2, int(5 * esc)), stroke_fill=(20, 20, 20, 255))
            y += alt2
    im.save(destino)


def tipo(p):
    e = p.suffix.lower()
    return "img" if e in IMG_EXT else "vid" if e in VID_EXT else None


def preparar_imagem(src, destino):
    """Corrige rotação EXIF e salva JPG padronizado (limite 2400 px)."""
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((2400, 2400))
    im.save(destino, quality=92)


def filtro_base(W, H, dur, zoom_in, tem_pan=True):
    """Fundo desfocado + foto inteira no centro (qualquer proporção) + zoom lento (Ken Burns)."""
    z0, z1 = (1.0, 1.10) if zoom_in else (1.10, 1.0)
    z = f"({z0}+({z1}-{z0})*t/{dur})"
    return (
        f"[0:v]fps={FPS},split[a][b];"
        f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=24:3,eq=brightness=-0.12[bg];"
        f"[b]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
        f"[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p,"
        f"scale=w='trunc({W}*{z}/2)*2':h=-2:eval=frame,crop={W}:{H}[base]"
    )


def segmento(midia, kind, dur, W, H, texto_png, zoom_in, saida, crf, ss=0.0, fade=(0.25, 0.45)):
    if kind == "img":
        entrada = ["-loop", "1", "-t", f"{dur}", "-i", str(midia)]
    else:
        entrada = (["-ss", f"{ss}"] if ss else []) + ["-t", f"{dur}", "-i", str(midia)]
    f = filtro_base(W, H, dur, zoom_in)
    if texto_png:
        entrada += ["-loop", "1", "-t", f"{dur}", "-i", str(texto_png)]
        f += f";[1:v]format=rgba,fade=t=in:st={fade[0]}:d={fade[1]}:alpha=1[tx];[base][tx]overlay=0:0,format=yuv420p[v]"
    else:
        f += ";[base]null[v]"
    run(["ffmpeg", "-v", "error", "-y", *entrada, "-filter_complex", f, "-map", "[v]", "-an", "-r", str(FPS),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", str(saida)])


def juntar(segs, durs, saida_video, crf, xf=XF):
    ins = []
    for s in segs:
        ins += ["-i", str(s)]
    if len(segs) == 1:
        shutil.copy(segs[0], saida_video)
        return
    f, acum = "", durs[0]
    prev = "[0:v]"
    for i in range(1, len(segs)):
        off = acum - xf
        out = f"[x{i}]"
        f += f"{prev}[{i}:v]xfade=transition=fade:duration={xf}:offset={off:.3f}{out};"
        prev = out
        acum = off + durs[i]
    f = f.rstrip(";")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", f, "-map", prev, "-r", str(FPS),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", str(saida_video)])
    return acum


def duracao(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).stdout.strip())


def pico_real(arq):
    """Pico real (true peak, dBFS) do arquivo final, medido com ebur128; None se não conseguir medir."""
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(arq), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    pico = None
    for linha in r.stderr.splitlines():
        t = linha.strip()
        if t.startswith("Peak:"):
            try:
                pico = float(t.split()[1])
            except (IndexError, ValueError):
                pass
    return pico


def eh_animada(p):
    return p.suffix.lower() in VID_EXT and p.stem.endswith("_anim")


def planejar(arqs, molde, max_seg, xf):
    """Monta a lista de cenas (abertura, corpo, final). Cada cena: dict(src, kind, ss, dur, papel).
    - foto = 1 cena; foto já animada (NN_anim.mp4) = 1 cena inteira; vídeo do cliente = até `max_trechos` melhores trechos.
    - molde com "batida" (bpm): todo corte cai na batida da trilha (foto/abertura/final em N batidas).
    - molde com "mistura": intercala uma cena de cada mídia (foto, trecho do vídeo 1, trecho do vídeo 2, foto...)."""
    bat = molde.get("batida")
    seg = molde["seg_dur"]
    if bat:
        B = 60.0 / bat["bpm"]
        d_ab, d_foto, d_vid, d_fim = bat["abertura"] * B + xf, bat["foto"] * B + xf, bat["video"] * B + xf, bat["final"] * B
    else:
        d_ab, d_foto, d_vid, d_fim = ABERTURA, seg, min(seg, 3.0), FINAL
    k_max = int(molde.get("max_trechos", 3))
    primeira = arqs[0]

    def trechos(p, k, dur):
        return escolher_trechos(p, dur, k)  # [(inicio, duracao, nota)]

    cena = lambda src, kind, ss, dur, papel: dict(src=src, kind=kind, ss=ss, dur=dur, papel=papel)
    pool = {}
    for p in arqs:
        if tipo(p) == "vid" and not eh_animada(p):
            pool[p] = trechos(p, k_max + (2 if p == primeira else 0), d_vid)
    # abertura e final: a 1ª mídia (foto: a mesma foto; vídeo: o melhor trecho abre, o 2º melhor fecha)
    if tipo(primeira) == "img" or eh_animada(primeira):
        k1 = "img" if tipo(primeira) == "img" else "vid"
        ab, fim = cena(primeira, k1, 0.0, d_ab, "ab"), cena(primeira, k1, 0.0, d_fim, "fim")
    else:
        w = pool.get(primeira) or []
        if not w:
            raise SystemExit("O primeiro vídeo é curto demais ou está ilegível. Mande outro.")
        por_nota = sorted(w, key=lambda t: -t[2])
        w_ab, w_fim = por_nota[0], (por_nota[1] if len(por_nota) > 1 else por_nota[0])
        pool[primeira] = [t for t in w if t not in (w_ab, w_fim)][:k_max]
        ab = cena(primeira, "vid", w_ab[0], min(d_ab, w_ab[1]), "ab")
        fim = cena(primeira, "vid", w_fim[0], min(d_fim, w_fim[1]), "fim")
    # corpo: fila de cenas por mídia
    filas = []
    for p in arqs:
        if p == primeira and tipo(p) == "img":
            continue
        if p == primeira and eh_animada(p):
            continue
        if tipo(p) == "img":
            filas.append([cena(p, "img", 0.0, d_foto, "corpo")])
        elif eh_animada(p):
            filas.append([cena(p, "vid", 0.0, d_foto, "corpo")])
        else:
            filas.append([cena(p, "vid", t[0], min(d_vid, t[1]), "corpo") for t in pool.get(p, [])[:k_max]])
    if molde.get("mistura"):
        corpo = []
        for r in range(max([len(f) for f in filas] + [0])):
            for f in filas:
                if r < len(f):
                    corpo.append(f[r])
    else:
        corpo = [c for f in filas for c in f]
    # orçamento de tempo: cabe em max_seg
    sobra = max_seg - (ab["dur"] - xf) - fim["dur"]
    cheio = []
    for c in corpo:
        custo = c["dur"] - xf
        if sobra - custo < 0:
            break
        cheio.append(c)
        sobra -= custo
    if not cheio:
        raise SystemExit("Mande pelo menos 2 fotos ou vídeos.")
    return [ab] + cheio + [fim]


def montar(molde_id, midias_dir, nome, frase, saida, leve=False, musica=None, max_seg=MAX_SEG):
    molde = json.loads((MOLDES / f"{molde_id}.json").read_text(encoding="utf-8"))
    W, H, crf = (540, 960, 30) if leve else (1080, 1920, 23)
    arqs = sorted(p for p in Path(midias_dir).iterdir() if tipo(p))
    if len(arqs) < 2:
        raise SystemExit("Mande pelo menos 2 fotos ou vídeos.")
    arqs = arqs[:20]
    xf = float(molde.get("xfade", XF))
    bat = molde.get("batida")
    plano = planejar(arqs, molde, max_seg, xf)
    cor = molde["cor"]
    nome = (nome or "Meu pet").strip()
    fmt = lambda t: t.replace("{nome}", nome)
    a_cada = int(molde.get("legenda_a_cada", 1))
    fade = (0.04, 0.12) if bat else (0.25, 0.45)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        sub_final = fmt(molde["final"]["subtitulo"])
        if frase:
            sub_final = frase.strip()
        segs, durs, vistos = [], [], 0
        for i, c in enumerate(plano):
            if c["papel"] == "ab":
                t, s_, grande, esc = fmt(molde["abertura"]["titulo"]), fmt(molde["abertura"]["subtitulo"]), True, False
            elif c["papel"] == "fim":
                t, s_, grande, esc = fmt(molde["final"]["titulo"]), sub_final, True, True
            else:
                t, s_, grande, esc = molde["legendas"][vistos % len(molde["legendas"])], "", False, False
                if vistos % a_cada != 0:
                    t = ""
                vistos += 1
            src = c["src"]
            if c["kind"] == "img":
                src = td / f"m{i}.jpg"
                preparar_imagem(c["src"], src)
            png = None
            if t:
                png = td / f"t{i}.png"
                camada_texto(W, H, t, s_, cor, png, grande=grande, escurecer=esc)
            out = td / f"s{i}.mp4"
            segmento(src, c["kind"], round(c["dur"], 3), W, H, png, zoom_in=(i % 2 == 0), saida=out, crf=crf, ss=c["ss"], fade=fade)
            segs.append(out)
            durs.append(round(c["dur"], 3))
        print("plano:", " | ".join(f"{c['papel']}:{Path(c['src']).name}@{c['ss']}+{c['dur']:.2f}" for c in plano), file=sys.stderr)
        video = td / "video.mp4"
        total = juntar(segs, durs, video, crf, xf)
        # carimbo (patinha + marca) fixo no topo, abaixo da zona cortada pelas redes
        cw = int(W * 0.36)
        vc = td / "video_carimbo.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(CARIMBO), "-filter_complex",
             f"[1:v]scale={cw}:-1,format=rgba,colorchannelmixer=aa=0.92[c];[0:v][c]overlay=(W-w)/2:{int(H * 0.085)}[v]",
             "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", str(vc)])
        # música: trilha do molde (livre de direitos) ou arquivo externo; mix final em -14 LUFS, pico <= -1 dB
        mus = Path(musica) if musica else MUSICAS / molde["musica"]
        ini = 0 if musica else molde.get("musica_inicio", 0)
        if bat and not musica:  # cada corte do vídeo cai numa batida: começa a trilha meia transição antes da 1ª batida
            B = 60.0 / bat["bpm"]
            ini = bat["primeira"] - xf / 2
            while ini < 0:
                ini += B
        fade_a = f"afade=t=in:st=0:d=0.8,afade=t=out:st={max(total - 2.2, 0):.2f}:d=2.2"
        saida = Path(saida)
        saida.parent.mkdir(parents=True, exist_ok=True)
        # o AAC estoura o pico (+2 dBFS medido em 13/11): codifica, MEDE o pico real do arquivo e, se passar de -1 dBFS, baixa o teto e refaz (só o áudio)
        teto = 0.89
        for _ in range(4):
            af = f"[1:a]atrim=start={ini:.3f},asetpts=PTS-STARTPTS,atrim=end={total:.2f},{fade_a},loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit={teto:.3f}:level=disabled[a]"
            run(["ffmpeg", "-v", "error", "-y", "-i", str(vc), "-stream_loop", "-1", "-i", str(mus), "-filter_complex", af,
                 "-map", "0:v", "-map", "[a]", "-t", f"{total:.2f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k" if not leve else "96k",
                 "-ar", "44100", "-movflags", "+faststart", str(saida)])
            tp = pico_real(saida)
            if tp is None or tp <= -1.0:
                break
            teto *= 10 ** (-(tp + 1.4) / 20)
    return saida, total


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--molde", required=True, choices=[p.stem for p in MOLDES.glob("*.json")])
    ap.add_argument("--midias", required=True)
    ap.add_argument("--nome", default="")
    ap.add_argument("--frase", default="")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--musica", default=None)
    ap.add_argument("--leve", action="store_true")
    ap.add_argument("--max", type=float, default=MAX_SEG, help="duração máxima em segundos (plano base: 50)")
    a = ap.parse_args()
    out, total = montar(a.molde, a.midias, a.nome, a.frase, a.saida, a.leve, a.musica, a.max)
    print(f"OK {out} ({total:.1f}s, {out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
