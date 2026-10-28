"""Auditoria de 'conteúdo de baixo valor' (AdSense) — roda ANTES de pedir revisão e toda semana (Vigia).
Uso: python scripts/auditoria_baixo_valor_adsense.py   (le data/seo_onpage/otimizados e site/build). Código 2 se houver falha crítica.
Criada em 25/10/2026 após a reprovação 'Low value content' (24/10): a auditoria deveria ter vindo antes do pedido.
"""
from __future__ import annotations
import collections, glob, itertools, json, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = sorted(glob.glob(str(ROOT / "data/seo_onpage/otimizados/*.md")))
BUILD = ROOT / "site" / "build"


def corpo(f: str) -> str:
    t = Path(f).read_text(encoding="utf-8")
    m = re.match(r"---\n.*?\n---\n(.*)", t, re.S)
    return m.group(1) if m else t


def main() -> int:
    crit, avis = [], []
    B = {Path(f).stem: corpo(f) for f in ART}
    n = len(B)
    sem_fontes = [s for s, b in B.items() if not re.search(r"^## Fontes e refer", b, re.M)]
    if sem_fontes:
        crit.append(f"{len(sem_fontes)}/{n} artigos sem 'Fontes e referências'")
    curtos = [s for s, b in B.items() if len(re.sub(r"[#*>\[\]()]", " ", b).split()) < 700]
    if curtos:
        crit.append(f"{len(curtos)} artigos com menos de 700 palavras: {curtos[:5]}")
    S = {s: {' '.join(t[i:i + 6]) for i in range(len(t) - 5)} for s, b in B.items() for t in [re.findall(r"\w+", b.lower())]}
    alto = [(round(len(S[a] & S[b]) / max(1, len(S[a] | S[b])), 2), a, b) for a, b in itertools.combinations(S, 2)]
    alto = [x for x in alto if x[0] > 0.25]
    if alto:
        crit.append(f"pares com texto muito parecido (>25%): {alto[:3]}")
    pat = re.compile(r"PREENCHER|Nota para revis|lorem ipsum|\{\{|undefined|revisao_humana: true", re.I)
    for h in BUILD.glob("*.html"):
        t = re.sub(r"<(script|style).*?</\1>", "", h.read_text(encoding="utf-8", errors="ignore"), flags=re.S)
        if pat.search(t):
            crit.append(f"texto de modelo visível em {h.name}")
    ex = {h.stem for h in BUILD.glob("*.html")}
    quebrados = set()
    for h in BUILD.glob("*.html"):
        for l in re.findall(r'href="(/[^"#?]*)', h.read_text(encoding="utf-8", errors="ignore")):
            s = l.strip("/")
            if s and s not in ex and not (BUILD / s).exists() and not (BUILD / (s + '.html')).exists() and not s.startswith(("imagens", "radio", "videos")):
                quebrados.add(l)
    if quebrados:
        crit.append(f"links internos quebrados: {sorted(quebrados)[:5]}")
    sobre = (BUILD / "sobre.html").read_text(encoding="utf-8", errors="ignore") if (BUILD / "sobre.html").exists() else ""
    if 'id="equipe"' not in sobre:
        crit.append("página Sobre sem seção de equipe/autor")
    if sum(len(re.findall(r"\]\(https?://(?!tutorialpet)", b)) for b in B.values()) < n:
        avis.append("menos de 1 link externo por artigo, em média")
    capas = sum(1 for f in ART if re.search(r"imagem_capa:\s*\S+", Path(f).read_text(encoding="utf-8")))
    if capas < n:
        avis.append(f"{n - capas} artigos sem capa")
    eq = json.loads((ROOT / "config/sites/equipe.json").read_text(encoding="utf-8")) if (ROOT / "config/sites/equipe.json").exists() else {}
    if not eq.get("revisora_veterinaria"):
        avis.append("sem revisora veterinária cadastrada (config/sites/equipe.json)")
    print(f"ARTIGOS {n} | CRÍTICO {len(crit)} | AVISO {len(avis)}")
    for c in crit:
        print("CRÍTICO:", c)
    for a in avis:
        print("AVISO:", a)
    return 2 if crit else 0


if __name__ == "__main__":
    sys.exit(main())
