"""Agente 24 — Curador do Blog: confere cada artigo contra o que o Google AdSense e o E-E-A-T exigem.

Uso:
    python agents/24_curador_blog/agent.py                 # audita todos os rascunhos e grava o relatório
    python agents/24_curador_blog/agent.py --slug <slug>   # audita um só (código 1 se houver bloqueante)
Saída: data/curador_blog/relatorio.md
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
RASC = ROOT / "data" / "content_writer" / "rascunhos"
SAIDA = ROOT / "data" / "curador_blog"
MIN_PALAVRAS, MAX_PALAVRAS = 850, 1600
SAUDE = re.compile(r"vacina|vermifug|doen[cç]a|v[oô]mito|diarreia|sintoma|medicament|rem[eé]dio|parasit|pulga|carrapato|dentes|unha|sa[uú]de", re.I)
PROIBIDO = re.compile(r"sou (m[eé]dic[oa]\s*)?veterin[aá]ri|como veterin[aá]ri|estudos? (comprovam|mostram|provam)|\b\d{2,3}% dos (c[aã]es|cachorros|gatos)", re.I)


def ler(path: Path) -> tuple[dict, str]:
    t = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", t, re.S)
    return (yaml.safe_load(m.group(1)) or {}, m.group(2)) if m else ({}, t)


def todos_slugs() -> set[str]:
    """Slugs que já estão NO AR (site/build/<slug>.html): link interno só vale para página publicada."""
    build = ROOT / "site" / "build"
    return {p.stem for p in RASC.glob("*.md") if (build / f"{p.stem}.html").exists()}


def auditar(slug: str, fm: dict, body: str, slugs: set[str]) -> list[tuple[str, str]]:
    """Devolve [(nivel, mensagem)]; nivel = 'bloqueante' | 'aviso'."""
    p: list[tuple[str, str]] = []
    n = len(re.findall(r"\w+", body))
    if n < MIN_PALAVRAS:
        p.append(("bloqueante", f"conteúdo raso: {n} palavras (mínimo {MIN_PALAVRAS})"))
    elif n > MAX_PALAVRAS:
        p.append(("aviso", f"muito longo: {n} palavras"))
    if (fm.get("autor") or "").strip():
        p.append(("bloqueante", f"autor preenchido ('{fm.get('autor')}'): a assinatura é Equipe Tutorial Pet"))
    persona = str(fm.get("persona") or "")
    nome = persona.split("(")[0].strip()
    if persona:
        p.append(("bloqueante", "front-matter ainda tem 'persona' fictícia"))
    if nome and (nome.lower() in (fm.get("titulo") or "").lower() or nome.lower() in body.lower()):
        p.append(("bloqueante", f"persona '{nome}' aparece no título ou no texto"))
    if re.search(r"personagem (100% )?fict", body, re.I):
        p.append(("bloqueante", "texto menciona personagem fictício"))
    links = re.findall(r"\]\(/([a-z0-9\-]+)\)", body)
    validos = [s for s in set(links) if s in slugs and s != slug]
    invalidos = [s for s in set(links) if s not in slugs]
    if len(validos) < 2:
        p.append(("bloqueante", f"links internos insuficientes: {len(validos)} (mínimo 2)"))
    if invalidos:
        p.append(("bloqueante", f"link interno para página inexistente: {', '.join(sorted(invalidos))}"))
    if not re.search(r"^##\s+Perguntas frequentes", body, re.M | re.I):
        p.append(("bloqueante", "sem seção 'Perguntas frequentes'"))
    else:
        faq = body.split("Perguntas frequentes", 1)[1].split("\n## ", 1)[0]
        q = len(re.findall(r"\*\*[^*\n]+\?\*\*", faq))
        if not 3 <= q <= 5:
            p.append(("aviso", f"FAQ com {q} perguntas (ideal 3 a 5)"))
    if not re.search(r"^##\s+Para fechar", body, re.M | re.I):
        p.append(("bloqueante", "sem seção 'Para fechar'"))
    if len(re.findall(r"^##\s", body, re.M)) < 4:
        p.append(("aviso", "menos de 4 seções H2"))
    if PROIBIDO.search(body):
        p.append(("bloqueante", "alegação de credencial ou estudo/estatística sem fonte"))
    if SAUDE.search((fm.get("titulo") or "") + " " + body[:1500]) and not re.search(r"m[eé]dico[- ]veterin[aá]ri", body, re.I):
        p.append(("bloqueante", "tema de saúde sem orientar a procurar o médico-veterinário"))
    if len(fm.get("titulo") or "") > 70:
        p.append(("aviso", f"título com {len(fm.get('titulo'))} caracteres (ideal até 70)"))
    meta = str(fm.get("meta_description") or "")
    if not 60 <= len(meta) <= 160:
        p.append(("aviso", f"meta description com {len(meta)} caracteres (ideal 60 a 160)"))
    for para in re.split(r"\n\s*\n", body):
        if not para.lstrip().startswith(("#", ">", "-", "|")) and len(para.split()) > 130:
            p.append(("aviso", "parágrafo acima de 130 palavras"))
            break
    return p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug")
    a = ap.parse_args()
    slugs = todos_slugs()
    alvos = [RASC / f"{a.slug}.md"] if a.slug else sorted(RASC.glob("*.md"))
    linhas, bloq = [], 0
    for path in alvos:
        fm, body = ler(path)
        probs = auditar(path.stem, fm, body, slugs)
        b = [m for n, m in probs if n == "bloqueante"]
        bloq += 1 if b else 0
        linhas.append(f"- {'REPROVADO' if b else 'ok'} | {path.stem}" + ("".join(f"\n    - [{n}] {m}" for n, m in probs)))
    SAIDA.mkdir(parents=True, exist_ok=True)
    cab = f"# Relatório do Curador do Blog — {datetime.now():%d/%m/%Y %H:%M}\n\n{len(alvos)} artigos auditados, {bloq} com problema bloqueante.\n\n"
    (SAIDA / "relatorio.md").write_text(cab + "\n".join(linhas) + "\n", encoding="utf-8")
    print(cab + "\n".join(linhas[:60]))
    return 1 if bloq and a.slug else 0


if __name__ == "__main__":
    sys.exit(main())
