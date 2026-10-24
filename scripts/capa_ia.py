"""Plano B de capa (Allan, 24/10/2026): quando o Pexels nao entrega foto do tema, gera 3 candidatas por IA (CF FLUX, gratis)
e grava em data/visual/candidatos/<slug>/ no mesmo formato; o juiz (core.capa) escolhe depois. SO animal, sem pessoa/texto.
Uso: python scripts/capa_ia.py <slug>"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import gerar_foto_ia as g  # noqa: E402

CENAS = {  # slug -> 3 prompts em ingles (so animal e objeto, sem pessoa)
    "como-escolher-comedouro-duplo-elevado-para-gatos-idosos": [
        "Professional photograph of an elderly tabby cat eating from a raised double pet bowl stand, one bowl food one bowl water, cozy home kitchen, soft daylight",
        "Professional photograph of a senior gray cat standing at an elevated double cat feeder, eating kibble, warm indoor light, shallow depth of field",
        "Professional photograph of a calm older cat next to a raised ceramic double bowl feeder on a wooden floor, soft natural light",
    ],
    "como-acostumar-gato-filhote-a-usar-a-escova-de-dentes": [
        "Professional photograph of a cute kitten sniffing a small cat toothbrush lying on a table, mouth closed, curious eyes, soft daylight",
        "Professional photograph of a fluffy kitten sitting next to a pet toothbrush and a tube of cat toothpaste, mouth closed, cozy home",
        "Professional photograph of a curious kitten looking at the camera with a small finger toothbrush for cats beside it, mouth closed, warm light",
    ],
}
SUFIXO = " Sharp focus, realistic fur detail, anatomically correct, no people, no hands, no text, no logo."


def main() -> int:
    slug = sys.argv[1]
    cenas = CENAS.get(slug)
    if not cenas:
        print("sem cenas IA para", slug)
        return 1
    pasta = ROOT / "data" / "visual" / "candidatos" / slug
    pasta.mkdir(parents=True, exist_ok=True)
    cjson = pasta / "candidatos.json"
    lista = json.loads(cjson.read_text(encoding="utf-8")) if cjson.exists() else []
    prox = max([c["indice"] for c in lista], default=-1) + 1
    n = 0
    for i, cena in enumerate(cenas):
        dest = pasta / f"{prox + n}.jpg"
        g.MODELO  # noqa: B018
        # reaproveita gerar(), trocando o prompt pelo da cena
        orig = g.prompt_para
        g.prompt_para = lambda raca, v=0, _c=cena: _c + SUFIXO
        ok, msg = g.gerar(slug, dest, i)
        g.prompt_para = orig
        print(f"[ia {i}] {ok} {msg}")
        if ok:
            lista.append({"fonte": "ia-flux", "id": f"ia{i}", "url_download": "", "url_pagina": "https://www.tutorialpet.com.br",
                          "fotografo": "Tutorial Pet (imagem gerada por IA)", "fotografo_url": "https://www.tutorialpet.com.br",
                          "query": cena[:80], "indice": prox + n, "arquivo": str(dest.relative_to(ROOT))})
            n += 1
    cjson.write_text(json.dumps(lista, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main())
