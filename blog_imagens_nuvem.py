"""Busca fotos candidatas (Pexels) para a capa de um artigo, sem depender do pack marketing-autonomo.

Uso: python blog_imagens_nuvem.py <slug>
Saída: data/visual/candidatos/<slug>/{0..N}.jpg + candidatos.json (mesmo formato do agente 15,
então `agents/15_visual/agent.py --selecionar <slug> <indice>` funciona direto).
Regra do projeto: a foto mostra SÓ o animal, nunca pessoa. Por isso as buscas são em inglês e
terminam com "no people"; a escolha final é sempre revisada por olhos (Publicador/Claude).
"""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "agents" / "15_visual"))
from stock_queries import QUERIES, queries_for  # noqa: E402

UA = {"User-Agent": "tutorialpet-fabrica/1.0"}


def consultas(slug: str) -> list[str]:
    if slug in QUERIES:
        return QUERIES[slug]
    try:  # tema novo: pede 2 buscas em inglês ao LLM (só o animal, nunca pessoa)
        from core.llm import gerar_texto
        txt = gerar_texto(
            f"Artigo de blog de pets: '{slug.replace('-', ' ')}'. Dê 2 buscas curtas em inglês para um banco de fotos "
            "(Pexels) que retornem SÓ o animal, sem pessoa visível. Uma por linha, sem numeração, sem aspas.",
            temperatura=0.3, max_tokens=60)
        linhas = [l.strip(" -*\"'") for l in txt.splitlines() if l.strip()][:2]
        if linhas:
            return linhas
    except Exception as exc:  # noqa: BLE001
        print(f"[imagens] LLM indisponível ({str(exc)[:80]}); usando busca genérica")
    animal = "cat" if any(p in slug for p in ("gato", "gatinho")) else "puppy" if "filhote" in slug else "dog"
    return [f"{animal} close up", f"{animal} resting indoors"]


def buscar(query: str, chave: str, n: int) -> list[dict]:
    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
        {"query": query, "per_page": n, "orientation": "landscape"})
    req = urllib.request.Request(url, headers={**UA, "Authorization": chave})
    with urllib.request.urlopen(req, timeout=60) as r:
        dados = json.loads(r.read().decode("utf-8"))
    from core.estilo_visual import ordenar
    return [{
        "fonte": "pexels", "id": p["id"], "url_download": p["src"]["large"], "url_pagina": p["url"],
        "fotografo": p["photographer"], "fotografo_url": p["photographer_url"],
        "largura": p["width"], "altura": p["height"], "query": query,
    } for p in ordenar(dados.get("photos", []), "url", "alt")]


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit("uso: python blog_imagens_nuvem.py <slug>")
    slug = sys.argv[1]
    try:  # no PC, lê a chave do .env; na nuvem ela já vem do segredo do GitHub
        from core.config import load_env_file
        load_env_file()
    except Exception:  # noqa: BLE001
        pass
    chave = os.environ.get("PEXELS_API_KEY", "").strip()
    if not chave:
        print("PEXELS_API_KEY ausente; sem candidatos de imagem")
        return 1
    out = ROOT / "data" / "visual" / "candidatos" / slug
    out.mkdir(parents=True, exist_ok=True)
    achados: list[dict] = []
    vistos: set[int] = set()
    for q in consultas(slug):
        try:
            for c in buscar(q, chave, 5):
                if c["id"] not in vistos:
                    vistos.add(c["id"])
                    achados.append(c)
        except Exception as exc:  # noqa: BLE001
            print(f"[imagens] busca '{q}' falhou: {str(exc)[:100]}")
        if len(achados) >= 6:
            break
    manifest = []
    for c in achados[:6]:
        i = len(manifest)
        try:
            req = urllib.request.Request(c["url_download"], headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                (out / f"{i}.jpg").write_bytes(r.read())
        except Exception as exc:  # noqa: BLE001
            print(f"[imagens] download falhou: {str(exc)[:100]}")
            continue
        manifest.append({**c, "indice": i, "arquivo": f"data/visual/candidatos/{slug}/{i}.jpg"})
    (out / "candidatos.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[imagens] {len(manifest)} candidata(s) para {slug}")
    return 0 if manifest else 1


if __name__ == "__main__":
    sys.exit(main())
