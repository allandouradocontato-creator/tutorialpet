#!/usr/bin/env python3
"""Gera pin vertical 1000x1500 (Pinterest) a partir da capa do artigo: python3 scripts/gerar_pin.py <slug> "Titulo do pin"
Saida: site/build/pins/<slug>.jpg (URL https://tutorialpet.com.br/pins/<slug>.jpg)."""
import sys, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parent.parent
slug, titulo = sys.argv[1], sys.argv[2]
cap = Image.open(ROOT/"site/build/imagens"/f"{slug}.jpg").convert("RGB")
W, H = 1000, 1500
s = H / cap.height
cap = cap.resize((int(cap.width*s), H), Image.LANCZOS)
x0 = (cap.width - W)//2
img = cap.crop((x0, 0, x0+W, H))
ov = Image.new("RGBA", (W, H), (0,0,0,0)); d = ImageDraw.Draw(ov)
for y in range(600, H):
    d.line([(0,y),(W,y)], fill=(0,0,0,int(235*((y-600)/(H-600))**0.8)))
img = Image.alpha_composite(img.convert("RGBA"), ov); d = ImageDraw.Draw(img)
f = ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", 84)
fs = ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", 40)
linhas = textwrap.wrap(titulo, 20)
y = 1340 - len(linhas)*100
for l in linhas:
    d.text((60, y), l, font=f, fill="white"); y += 100
d.text((60, 1400), "🐾 tutorialpet.com.br".replace("🐾 ",""), font=fs, fill=(255,214,102))
out = ROOT/"site/build/pins"; out.mkdir(parents=True, exist_ok=True)
img.convert("RGB").save(out/f"{slug}.jpg", quality=90)
print(out/f"{slug}.jpg")
