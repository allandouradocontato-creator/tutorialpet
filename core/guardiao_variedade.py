"""Registro de variedade da fábrica (usado pelo Guardião de Marca e Variedade, agente 26).

Guarda, entre uma rodada e outra, quais clipes (Pexels/Pixabay) e quais faixas de música cada vídeo usou, para:
  - nunca reaproveitar um clipe dos últimos JANELA_VIDEOS vídeos;
  - nunca repetir o mesmo clipe duas vezes dentro do mesmo vídeo;
  - alternar a música (não repetir as últimas faixas).
O arquivo fica na branch media (variável CLIPS_REGISTRO) para sobreviver entre as rodadas na nuvem.
Se o filtro não achar clipe novo, a fábrica NÃO para: reaproveita e o Guardião marca o pacote para revisão.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JANELA_VIDEOS = 20
JANELA_MUSICA = 3

_slug_atual = ""
_ids_rodada: set[str] = set()
_reusos_rodada: list[str] = []


def _caminho() -> Path:
    return Path(os.environ.get("CLIPS_REGISTRO") or ROOT / "data" / "biblioteca" / "clips_usados.json")


def _carregar() -> dict:
    p = _caminho()
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {"videos": []}


def _salvar(dados: dict) -> None:
    p = _caminho()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")


def iniciar_video(slug: str) -> None:
    """Chamar no começo da montagem de cada vídeo."""
    global _slug_atual
    _slug_atual = slug
    _ids_rodada.clear()
    _reusos_rodada.clear()


def _chave(fonte: str, item_id) -> str:
    return f"{fonte}:{item_id}"


def ids_recentes() -> set[str]:
    videos = _carregar().get("videos", [])[-JANELA_VIDEOS:]
    return {c for v in videos if v.get("slug") != _slug_atual for c in v.get("clipes", [])}


def pode_usar(fonte: str, item_id) -> bool:
    """False se o clipe já está neste vídeo ou nos últimos vídeos."""
    k = _chave(fonte, item_id)
    return k not in _ids_rodada and k not in ids_recentes()


def marcar(fonte: str, item_id, reuso: bool = False) -> None:
    k = _chave(fonte, item_id)
    _ids_rodada.add(k)
    if reuso:
        _reusos_rodada.append(k)


def musicas_recentes() -> list[str]:
    videos = [v for v in _carregar().get("videos", []) if v.get("slug") != _slug_atual]
    return [v["musica"] for v in videos[-JANELA_MUSICA:] if v.get("musica")]


def finalizar_video(musica: str = "") -> None:
    """Grava os clipes e a música deste vídeo (substitui o registro anterior do mesmo slug)."""
    dados = _carregar()
    dados["videos"] = [v for v in dados.get("videos", []) if v.get("slug") != _slug_atual]
    dados["videos"].append({
        "slug": _slug_atual, "quando": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "clipes": sorted(_ids_rodada), "reusos": list(_reusos_rodada), "musica": musica,
    })
    dados["videos"] = dados["videos"][-200:]
    _salvar(dados)
