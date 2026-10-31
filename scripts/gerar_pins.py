"""Gera o pin vertical (1000x1500, 2:3) de cada artigo para o Pinterest: capa + título + marca.
Saída: site/build/pins/<slug>.jpg. Roda no build; sem Pillow, não gera nada (o site continua normal).
Criado em 31/10/2026: a capa do blog é horizontal e o Pinterest só aceita vertical."""
from __future__ import annotations
import re, textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONTE_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def titulo_pin(t: str) -> str:
    t = re.sub(r"\s*[:\-–]\s*guia pr[aá]tico\s*$", "", t.strip(), flags=re.I)
    return t.replace("''", "'")


def gerar(slug: str, titulo: str, capa: Path, saida: Path) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except Exception:
        return False
    if not capa.exists():
        return False
    W, H, FOTO = 1000, 1500, 960
    img = Image.new("RGB", (W, H), (255, 244, 230))
    foto = ImageOps.fit(Image.open(capa).convert("RGB"), (W, FOTO), method=Image.LANCZOS, centering=(0.5, 0.4))
    img.paste(foto, (0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, FOTO, W, H], fill=(255, 244, 230))
    d.rectangle([0, FOTO, W, FOTO + 12], fill=(255, 138, 61))
    f = ImageFont.truetype(FONTE, 62)
    linhas = textwrap.wrap(titulo_pin(titulo), width=24)[:4]
    y = FOTO + 55
    for ln in linhas:
        d.text((60, y), ln, font=f, fill=(51, 36, 28))
        y += 76
    fs = ImageFont.truetype(FONTE, 34)
    d.text((60, H - 130), "🐾" if False else "Tutorial Pet", font=fs, fill=(255, 138, 61))
    d.text((60, H - 80), "tutorialpet.com.br · revisão veterinária", font=ImageFont.truetype(FONTE_R, 28), fill=(110, 90, 80))
    saida.parent.mkdir(parents=True, exist_ok=True)
    img.save(saida, "JPEG", quality=86, optimize=True)
    return True


def main(build: Path | None = None) -> int:
    build = build or ROOT / "site" / "build"
    n = 0
    for f in sorted((ROOT / "data/seo_onpage/otimizados").glob("*.md")):
        t = f.read_text(encoding="utf-8")
        fm = t.split("\n---\n")[0]
        g = lambda k: (re.search(rf"^{k}:\s*(.*)$", fm, re.M) or [None, ""])[1].strip().strip("'\"")
        capa, tit, slug = g("imagem_capa"), g("titulo"), g("slug") or f.stem
        if not capa:
            continue
        origem = ROOT / "data/visual" / capa
        if gerar(slug, tit, origem, build / "pins" / f"{slug}.jpg"):
            n += 1
    print(f"[pins] {n} pins verticais gerados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
