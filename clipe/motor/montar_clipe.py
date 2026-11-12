#!/usr/bin/env python3
"""Motor do Clipe do Pet: monta um vídeo vertical 9:16 (até ~50 s) a partir das fotos/vídeos do cliente.

Uso:
  python3 clipe/motor/montar_clipe.py --molde homenagem --midias pasta_com_fotos \
      --nome Thor --frase "Te amamos" --saida clipe.mp4 [--leve] [--musica arquivo.mp3]

- molde: homenagem | aniversario | retrospectiva | um_dia (clipe/moldes/*.json)
- midias: pasta com 3 a 20 arquivos (jpg/png/webp/heic não; mp4/mov ok), usados em ordem de nome
- --musica: arquivo externo (ex.: a Música do Pet do cliente); sem ele usa a trilha do molde
- --leve: 540x960, arquivo pequeno (versão de teste/prévia)
Só ffmpeg + Pillow, sem serviço pago e sem depender do PC de ninguém.
"""
import argparse, json, math, shutil, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

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
        a = int(150 * math.sin(math.pi * y / n) ** 0.6)
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


def segmento(midia, kind, dur, W, H, texto_png, zoom_in, saida, crf):
    entrada = ["-loop", "1", "-t", f"{dur}", "-i", str(midia)] if kind == "img" else ["-t", f"{dur}", "-i", str(midia)]
    f = filtro_base(W, H, dur, zoom_in)
    if texto_png:
        entrada += ["-loop", "1", "-t", f"{dur}", "-i", str(texto_png)]
        f += f";[1:v]format=rgba,fade=t=in:st=0.25:d=0.45:alpha=1[tx];[base][tx]overlay=0:0,format=yuv420p[v]"
    else:
        f += ";[base]null[v]"
    run(["ffmpeg", "-v", "error", "-y", *entrada, "-filter_complex", f, "-map", "[v]", "-an", "-r", str(FPS),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", str(saida)])


def juntar(segs, durs, saida_video, crf):
    ins = []
    for s in segs:
        ins += ["-i", str(s)]
    if len(segs) == 1:
        shutil.copy(segs[0], saida_video)
        return
    f, acum = "", durs[0]
    prev = "[0:v]"
    for i in range(1, len(segs)):
        off = acum - XF
        out = f"[x{i}]"
        f += f"{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}{out};"
        prev = out
        acum = off + durs[i]
    f = f.rstrip(";")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", f, "-map", prev, "-r", str(FPS),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", str(saida_video)])
    return acum


def duracao(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).stdout.strip())


def montar(molde_id, midias_dir, nome, frase, saida, leve=False, musica=None, max_seg=MAX_SEG):
    molde = json.loads((MOLDES / f"{molde_id}.json").read_text(encoding="utf-8"))
    W, H, crf = (540, 960, 30) if leve else (1080, 1920, 23)
    arqs = sorted(p for p in Path(midias_dir).iterdir() if tipo(p))
    if len(arqs) < 3:
        raise SystemExit("Mande pelo menos 3 fotos ou vídeos.")
    arqs = arqs[:20]
    seg = molde["seg_dur"]
    # quantas cenas cabem em max_seg: abertura + N fotos + final (com crossfade)
    n_max = int((max_seg - ABERTURA - FINAL + 3 * XF) // (seg - XF))
    corpo = arqs[1:1 + max(1, n_max)]  # a 1ª mídia abre e fecha o clipe
    cor = molde["cor"]
    nome = (nome or "Meu pet").strip()
    fmt = lambda t: t.replace("{nome}", nome)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        cenas = []  # (midia, kind, dur, titulo, subtitulo, grande, escurecer)
        cenas.append((arqs[0], ABERTURA, fmt(molde["abertura"]["titulo"]), fmt(molde["abertura"]["subtitulo"]), True, False))
        for i, p in enumerate(corpo):
            leg = molde["legendas"][i % len(molde["legendas"])]
            cenas.append((p, seg, leg, "", False, False))
        sub = fmt(molde["final"]["subtitulo"])
        if frase:
            sub = frase.strip()
        cenas.append((arqs[0], FINAL, fmt(molde["final"]["titulo"]), sub, True, True))
        segs, durs = [], []
        for i, (p, dur, t, s, grande, esc) in enumerate(cenas):
            k = tipo(p)
            src = p
            if k == "img":
                src = td / f"m{i}.jpg"
                preparar_imagem(p, src)
            png = td / f"t{i}.png"
            camada_texto(W, H, t, s, cor, png, grande=grande, escurecer=esc)
            out = td / f"s{i}.mp4"
            segmento(src, k, dur, W, H, png, zoom_in=(i % 2 == 0), saida=out, crf=crf)
            segs.append(out)
            durs.append(dur)
        video = td / "video.mp4"
        total = juntar(segs, durs, video, crf)
        # carimbo (patinha + marca) fixo no topo, abaixo da zona cortada pelas redes
        cw = int(W * 0.36)
        vc = td / "video_carimbo.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(CARIMBO), "-filter_complex",
             f"[1:v]scale={cw}:-1,format=rgba,colorchannelmixer=aa=0.92[c];[0:v][c]overlay=(W-w)/2:{int(H * 0.085)}[v]",
             "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", str(vc)])
        # música: trilha do molde (livre de direitos) ou arquivo externo; mix final em -14 LUFS, pico <= -1 dB
        mus = Path(musica) if musica else MUSICAS / molde["musica"]
        ini = 0 if musica else molde.get("musica_inicio", 0)
        fade = f"afade=t=in:st=0:d=0.8,afade=t=out:st={max(total - 2.2, 0):.2f}:d=2.2"
        af = f"[1:a]atrim=start={ini},asetpts=PTS-STARTPTS,atrim=end={total:.2f},{fade},loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.89:level=disabled[a]"
        saida = Path(saida)
        saida.parent.mkdir(parents=True, exist_ok=True)
        run(["ffmpeg", "-v", "error", "-y", "-i", str(vc), "-stream_loop", "-1", "-i", str(mus), "-filter_complex", af,
             "-map", "0:v", "-map", "[a]", "-t", f"{total:.2f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k" if not leve else "96k",
             "-ar", "44100", "-movflags", "+faststart", str(saida)])
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
