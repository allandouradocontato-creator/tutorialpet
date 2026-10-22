"""Acrescenta fotos no meio do artigo: python scripts/add_imagens_corpo.py <slug> <idx,idx> ["alt 1|alt 2"]
Copia data/visual/candidatos/<slug>/<idx>.jpg para data/visual/imagens/<slug>-corpo-N.jpg e grava imagens_corpo no front-matter."""
import json, shutil, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
slug, idxs = sys.argv[1], [int(x) for x in sys.argv[2].split(",")]
alts = sys.argv[3].split("|") if len(sys.argv) > 3 else []
cand = json.loads((R / "data/visual/candidatos" / slug / "candidatos.json").read_text(encoding="utf-8"))
por_i = {c["indice"]: c for c in cand}
blocos = []
for n, i in enumerate(idxs, 1):
    nome = f"{slug}-corpo-{n}.jpg"
    shutil.copy(R / "data/visual/candidatos" / slug / f"{i}.jpg", R / "data/visual/imagens" / nome)
    c = por_i.get(i, {})
    q = lambda t: "'" + str(t).replace("'", "''") + "'"
    blocos.append(f"- arquivo: imagens/{nome}\n  alt: {q(alts[n-1] if n-1 < len(alts) else slug.replace('-', ' '))}\n  fotografo: {q(c.get('fotografo',''))}\n  fonte_url: {q(c.get('url_pagina',''))}")
md = R / "data/seo_onpage/otimizados" / f"{slug}.md"
t = md.read_text(encoding="utf-8")
ini, resto = t.split("---\n", 2)[1], t.split("---\n", 2)[2]
import re
ini = re.sub(r"^imagens_corpo:\n(?:(?:- |  ).*\n)*", "", ini, flags=re.M)
md.write_text("---\n" + ini + "imagens_corpo:\n" + "\n".join(blocos) + "\n---\n" + resto, encoding="utf-8")
print("ok", slug, idxs)
