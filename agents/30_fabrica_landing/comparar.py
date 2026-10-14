"""Compara a landing gerada com a landing de referencia: secoes, textos visiveis, links e imagens.
Uso: python agents/30_fabrica_landing/comparar.py <referencia.html> <gerada.html>"""
import re, sys
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.secoes=[]; s.txt=[]; s.hrefs=[]; s.imgs=[]; s.skip=0
    def handle_starttag(s, t, a):
        a = dict(a)
        if t in ("header","section","footer"): s.secoes.append(t+"."+(a.get("class") or "").replace(" ", "."))
        if t in ("script","style"): s.skip += 1
        if t == "a" and a.get("href"): s.hrefs.append(re.sub(r"\?.*", "", a["href"]))
        for k in ("src","poster"):
            if a.get(k) and t in ("img","source","video"): s.imgs.append(a[k])
        if t == "div" and a.get("id") == "barra": s.secoes.append("div.sticky")
    def handle_endtag(s, t):
        if t in ("script","style"): s.skip -= 1
    def handle_data(s, d):
        if not s.skip and d.strip(): s.txt.append(" ".join(d.split()))

def ler(f):
    p = P(); p.feed(open(f, encoding="utf-8").read()); return p

a, b = ler(sys.argv[1]), ler(sys.argv[2])
ok = True
for nome, x, y in (("secoes", a.secoes, b.secoes), ("textos", a.txt, b.txt), ("links", a.hrefs, b.hrefs), ("midias", a.imgs, b.imgs)):
    igual = x == y
    print(f"{nome}: {len(x)} vs {len(y)} -> {'IGUAL' if igual else 'DIFERENTE'}")
    if not igual:
        ok = False
        for i in sorted(set(x) ^ set(y)): print("   so em um dos lados:", i)
print("EQUIVALENTE" if ok else "COM DIFERENCAS")
