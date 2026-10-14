"""Filtro de estilo visual (regra da casa, 07/10/2026): imagem de pet tem que ser FOFA e ATRAENTE.

Problema visto: foto de gato com ração espalhada no chão parecia pedido de doação / abrigo, e o bicho parecia
doente. Aqui a descrição do banco de imagens (slug da URL e texto alt do Pexels) vira nota: palavras de
carinho, brincadeira e saúde sobem; palavras de tristeza, doença, abrigo, sujeira e bagunça eliminam.
"""
from __future__ import annotations

import re

POSITIVAS = {
    "cute": 3, "adorable": 3, "happy": 3, "playful": 3, "playing": 3, "fluffy": 3, "smiling": 3, "puppy": 2,
    "kitten": 2, "cuddle": 2, "cuddling": 2, "funny": 2, "curious": 2, "running": 2, "jumping": 2, "toy": 1,
    "portrait": 1, "close": 1, "golden": 1, "sunlight": 1, "cozy": 2, "sleeping": 1, "lovely": 2, "bed": 1,
}
ELIMINATORIAS = (
    "sad", "sick", "ill", "injured", "stray", "shelter", "cage", "caged", "abandoned", "homeless", "dirty",
    "skinny", "thin", "starving", "hungry", "begging", "scattered", "spilled", "mess", "messy", "trash", "garbage",
    "dead", "blood", "wound", "bandage", "chain", "chained", "aggressive", "fight", "fighting",
    "lonely", "alone", "crying", "rescue", "kibble", "bowl", "food", "eating", "feeding", "litter", "poop",
    "vet", "syringe", "injection", "surgery", "cone",
)


def _palavras(texto: str) -> set[str]:
    return set(re.findall(r"[a-z]+", (texto or "").lower()))


def nota(slug_url: str, alt: str = "") -> int | None:
    """None = eliminado (não usar). Número maior = mais atraente."""
    p = _palavras(slug_url.replace("/", " ")) | _palavras(alt)
    if any(w in p for w in ELIMINATORIAS):
        return None
    return sum(v for k, v in POSITIVAS.items() if k in p)


# Modo "gente feliz com o pet" (decisão do Allan, 14/10/2026: capas com pessoas interagindo com os animais).
# Exige uma palavra de pessoa na descrição; relaxa só as eliminatórias ligadas ao tema (comida, vet, banho).
PESSOA = {"woman", "man", "girl", "boy", "child", "children", "kid", "kids", "family", "owner", "couple", "people",
          "person", "hug", "hugging", "kiss", "kissing", "friends", "together", "smiling", "laughing", "walking", "hand", "hands"}
POSITIVAS_PESSOA = {"hug": 3, "hugging": 3, "kiss": 3, "kissing": 3, "smiling": 3, "laughing": 3, "together": 2, "family": 2,
                    "woman": 1, "man": 1, "girl": 1, "boy": 1, "owner": 2, "playing": 3, "cuddling": 3, "love": 2}
ELIMINATORIAS_PESSOA = tuple(w for w in ELIMINATORIAS if w not in {"food", "eating", "feeding", "bowl", "vet", "kibble", "cone", "alone", "lonely", "rescue", "syringe", "injection"}) + ("sad", "crying", "shelter")


def ordenar(itens: list[dict], chave_url: str = "url", chave_alt: str = "alt", pessoas: bool = False) -> list[dict]:
    """Remove os eliminados e ordena do mais atraente para o menos (estável)."""
    pontuados = []
    for i, it in enumerate(itens):
        if pessoas:
            pal = _palavras(str(it.get(chave_url, "")).replace("/", " ")) | _palavras(str(it.get(chave_alt, "")))
            if not (pal & PESSOA) or any(w in pal for w in ELIMINATORIAS_PESSOA):
                continue
            n = sum(v for k, v in {**POSITIVAS, **POSITIVAS_PESSOA}.items() if k in pal)
        else:
            n = nota(str(it.get(chave_url, "")), str(it.get(chave_alt, "")))
        if n is not None:
            pontuados.append((-n, i, it))
    pontuados.sort(key=lambda t: (t[0], t[1]))
    return [t[2] for t in pontuados]
