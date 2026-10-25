"""Portão de gancho (regra de 22/10/2026, Criador de Audiência).

Uso:
    python scripts/portao_gancho.py <slug> [<slug>...]
    python scripts/portao_gancho.py --todos
Saída: "OK slug | gancho" ou "BANIDO slug | gancho | motivo". Código 2 se algum for banido.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROTEIROS = ROOT / "data" / "social" / "roteiros"

ABERTURAS = [
    (r"esse erro t[áa] silenciosamente", 'abertura banida "Esse erro tá silenciosamente"'),
    (r"aquele momento em que", 'abertura banida "Aquele momento em que"'),
    (r"para de ignorar", 'abertura banida "Para de ignorar"'),
    (r"para de\b", 'imperativo de bronca "Para de ..."'),
    (r"voc[êe] sabia", 'abertura banida "Você sabia" (diagnóstico 25/10/2026: pior retenção)'),
    (r"sabia que\b", 'abertura banida "Sabia que ..." (mesmo molde do "Você sabia")'),
]
MAX_PALAVRAS_TELA = 6  # texto de dor no frame 0 (diagnóstico 25/10/2026)
PALAVRA_CAO = re.compile(r"\bc[ãa]o(?:zinho)?s?\b".replace("[ãa]", "ã"), re.IGNORECASE)


def _tela0(slug: str) -> str | None:
    f = ROTEIROS / f"{slug}.json"
    if not f.exists():
        return None
    cenas = json.loads(f.read_text(encoding="utf-8")).get("cenas") or []
    return str((cenas[0] or {}).get("texto_na_tela") or "") if cenas else None


def avaliar_tela0(texto: str | None) -> tuple[bool, str]:
    """Texto de dor no frame 0: obrigatório, até 6 palavras, sem abertura banida."""
    t = (texto or "").strip()
    if not t:
        return False, "sem texto de dor na tela no frame 0"
    n = len(t.split())
    if n > MAX_PALAVRAS_TELA:
        return False, f"texto do frame 0 com {n} palavras (máx. {MAX_PALAVRAS_TELA})"
    ok, motivo = avaliar(t)
    return (ok, f"texto do frame 0: {motivo}" if not ok else "")


def _gancho(slug: str) -> str | None:
    f = ROTEIROS / f"{slug}.json"
    if not f.exists():
        return None
    return str(json.loads(f.read_text(encoding="utf-8")).get("gancho_3s") or "")


def avaliar(gancho: str) -> tuple[bool, str]:
    g = gancho.strip().lstrip("\"'“‘«").replace("’", "'")
    for padrao, motivo in ABERTURAS:
        if re.match(padrao, g, re.IGNORECASE):
            return False, motivo
    if PALAVRA_CAO.search(g):
        return False, 'contém "cão/cãozinho"'
    return True, ""


def verificar(slug: str) -> tuple[bool, str]:
    """(ok, motivo). Roteiro ausente ou sem gancho_3s não é tratado como banido (motivo explica)."""
    try:
        g = _gancho(slug)
    except Exception as e:  # JSON quebrado não derruba o lote
        return True, f"roteiro ilegível ({e}); portão não aplicado"
    if g is None:
        return True, "roteiro não encontrado; portão não aplicado"
    if not g:
        return True, "sem gancho_3s; portão não aplicado"
    ok, motivo = avaliar(g)
    if not ok:
        return ok, motivo
    try:
        return avaliar_tela0(_tela0(slug))
    except Exception as e:
        return True, f"cenas ilegíveis ({e}); frame 0 não verificado"


def listar_slugs() -> list[str]:
    return sorted(p.stem for p in ROTEIROS.glob("*.json") if not p.name.endswith(".original.json"))


def main(argv: list[str]) -> int:
    slugs = listar_slugs() if "--todos" in argv else [a for a in argv if not a.startswith("--")]
    if not slugs:
        print(__doc__)
        return 1
    banidos = []
    for s in slugs:
        ok, motivo = verificar(s)
        g = _gancho(s) or ""
        if ok:
            print(f"OK {s} | {g}")
        else:
            banidos.append(s)
            print(f"BANIDO {s} | {g} | {motivo}")
    if "--todos" in argv:
        print(f"\nRESUMO: {len(slugs)} roteiros, {len(banidos)} banidos, {len(slugs) - len(banidos)} OK")
        for s in banidos:
            print(f"  - {s}")
    return 2 if banidos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
