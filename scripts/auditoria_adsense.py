"""Auditoria de prontidao para o AdSense (Allan, 22/10/2026: 'precisamos reler o que falta e nao deixar buracos').
Le site/build e data/ (sem rede) e grava data/auditoria/adsense.md com PASSA/FALHA por item e a lista do que corrigir.
Regras: biblioteca/regras_plataformas/google.md secao 2-3 (fontes oficiais). Uso: python scripts/auditoria_adsense.py"""
import datetime as dt, hashlib, re, sys
from collections import defaultdict
from pathlib import Path
R = Path(__file__).resolve().parents[1]
B = R / "site/build"
def txt(h): return re.sub(r"\s+", " ", re.sub(r"<(script|style)[^>]*>.*?</\1>|<[^>]+>", " ", h, flags=re.S))
art = {}
for f in B.glob("*.html"):
    h = f.read_text(encoding="utf-8")
    if 'class="article"' in h: art[f.stem] = h
res, falhas = [], []
def ck(nome, ok, detalhe="", corr=""):
    res.append(f"| {nome} | {'PASSA' if ok else 'FALHA'} | {detalhe} |")
    if not ok: falhas.append(f"- **{nome}**: {detalhe} -> {corr}")
# 1 paginas obrigatorias e arquivos
for p in ["sobre", "contato", "politica-de-privacidade", "termos"]:
    ck(f"pagina {p}", (B / f"{p}.html").exists(), "", f"criar {p}.html")
ck("ads.txt com pub-id", "pub-7204207473239947" in (B / "ads.txt").read_text() if (B / "ads.txt").exists() else False, "", "publicar ads.txt na raiz")
rb = (B / "robots.txt").read_text() if (B / "robots.txt").exists() else ""
ck("robots.txt nao bloqueia Mediapartners/Google", not re.search(r"Disallow:\s*/\s*$", rb, re.M), "", "liberar rastreamento")
ck("sitemap.xml", (B / "sitemap.xml").exists(), "", "gerar sitemap")
# 2 volume e ritmo
datas = []
for s, h in art.items():
    m = re.search(r'datetime="(\d{4}-\d{2}-\d{2})"', h)
    if m: datas.append(dt.date.fromisoformat(m.group(1)))
ck("volume >= 30 artigos", len(art) >= 30, f"{len(art)} artigos", "produzir ate 30 de qualidade")
if datas:
    ult = max(datas); dias = (dt.date.today() - ult).days
    ck("ultimo artigo <= 2 dias", dias <= 2, f"ultimo em {ult} ({dias} dias)", "publicar hoje; buraco de ritmo derruba confianca")
    d = sorted(set(datas)); buracos = [(a, b) for a, b in zip(d, d[1:]) if (b - a).days > 3]
    ck("sem buracos > 3 dias nos ultimos 30 dias", not [x for x in buracos if (dt.date.today() - x[1]).days <= 30], f"buracos: {[(str(a), str(b)) for a, b in buracos if (dt.date.today()-b).days<=30][:4]}", "manter 1+ artigo/dia")
# 3 qualidade por artigo
curtos = [s for s, h in art.items() if len(txt(h).split()) < 900]
ck("artigos >= 900 palavras", not curtos, f"{len(curtos)} curtos: {curtos[:5]}", "reforcar")
sem_h2 = [s for s, h in art.items() if len(re.findall(r"<h2", h)) < 3]
ck("estrutura com >= 3 subtitulos", not sem_h2, f"{sem_h2[:5]}", "estruturar")
sem_meta = [s for s, h in art.items() if 'name="description"' not in h]
ck("meta description em todos", not sem_meta, f"{sem_meta[:5]}", "gerar")
sem_autor = [s for s, h in art.items() if 'class="byline"' not in h]
ck("autoria/assinatura visivel", not sem_autor, f"{sem_autor[:5]}", "byline")
nai = [s for s, h in art.items() if not re.search(r'href="/[a-z0-9-]+"', h.split("</header>")[-1][:100000].replace('href="/sobre"', '').replace('href="/contato"', ''))]
# 4 imagens
img = {}
for s, h in art.items():
    m = re.search(r'class="hero-img" src="/([^"?]+)', h)
    if m and (B / m.group(1)).exists(): img[s] = hashlib.md5((B / m.group(1)).read_bytes()).hexdigest()
por = defaultdict(list)
for s, hh in img.items(): por[hh].append(s)
dup = [v for v in por.values() if len(v) > 1]
ck("capa unica por artigo", not dup, f"{sum(len(v) for v in dup)} artigos em {len(dup)} grupos repetidos", "refazer por tema (config/capas_refazer.txt)")
proib = set()
pf = R / "config/fotos_proibidas.txt"
if pf.exists(): proib = {l.split()[0] for l in pf.read_text().splitlines() if l.strip() and not l.startswith("#")}
ck("sem capa proibida (agressiva)", not [s for s, hh in img.items() if hh in proib], f"{[s for s, hh in img.items() if hh in proib]}", "trocar")
sem_img = [s for s in art if s not in img]
ck("todos com capa", not sem_img, f"{sem_img[:5]}", "gerar capa")
# 5 saude (YMYL)
saude = [s for s in art if re.search(r"vacin|doenc|veterin|toxic|alimentos-proibidos|obesidade|peso|dentes|cio|castra|vermif", s)]
sem_aviso = [s for s in saude if not re.search(r"veterin", txt(art[s]), re.I)]
ck("artigos de saude citam veterinario", not sem_aviso, f"{sem_aviso[:6]}", "aviso e fonte (YMYL)")
sem_fonte = [s for s in saude if not re.search(r"fonte|segundo|(conselho|CFMV|AVMA|WSAVA|MAPA)", txt(art[s]))]
ck("artigos de saude com fonte citada", not sem_fonte, f"{len(sem_fonte)} sem fonte: {sem_fonte[:4]}", "citar fonte confiavel")
# 6 privacidade
pv = (B / "politica-de-privacidade.html").read_text(encoding="utf-8") if (B / "politica-de-privacidade.html").exists() else ""
ck("privacidade cita Google/AdSense e cookies", bool(re.search(r"AdSense|Google", pv)) and "cookie" in pv.lower(), "", "acrescentar secao de anuncios e cookies (exigencia do AdSense)")
out = ["# Auditoria AdSense (" + dt.date.today().isoformat() + ")", "", "| Item | Resultado | Detalhe |", "|---|---|---|"] + res + ["", f"## Corrigir ({len(falhas)})"] + (falhas or ["- nada"])
(R / "data/auditoria/adsense.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
