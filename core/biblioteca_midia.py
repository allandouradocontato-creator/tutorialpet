"""Biblioteca de mídia da fábrica: várias fontes gratuitas de vídeo/imagem num só lugar.

Regra da casa (07/10/2026): só fontes GRÁTIS e com licença de uso comercial; todo clipe passa pelo filtro de
estilo (fofo e atraente). Cada fonte só liga se a chave existir no ambiente (GitHub Secrets / .env):
  - Pexels   (PEXELS_API_KEY)  -> já usada em agents/17_video/montar_video6.py
  - Pixabay  (PIXABAY_API_KEY) -> vídeos e fotos; licença Pixabay permite uso comercial
Descartadas: Coverr API (versão grátis proíbe uso comercial e exige logotipo), Envato Elements (assinatura paga,
sem API grátis; fica na lista de ferramentas pagas para depois).
Cada clipe usado é registrado em data/biblioteca/catalogo.json (fonte, id, página, tags, fotógrafo).
"""
from __future__ import annotations

import json
import os
import subprocess
import urllib.parse
from datetime import datetime
from pathlib import Path

from core.estilo_visual import nota

ROOT = Path(__file__).resolve().parent.parent
CATALOGO = ROOT / "data" / "biblioteca" / "catalogo.json"


def _curl(args: list[str], saida=None) -> subprocess.CompletedProcess:
    return subprocess.run(["curl", "-sS", "-L", "-m", "120", *args], capture_output=True,
                          text=saida is None, encoding="utf-8" if saida is None else None, errors="replace")


def registrar(fonte: str, item_id, pagina: str, tags: str, autor: str, arquivo: str, busca: str) -> None:
    try:
        dados = json.loads(CATALOGO.read_text(encoding="utf-8")) if CATALOGO.exists() else []
        dados.append({"fonte": fonte, "id": item_id, "pagina": pagina, "tags": tags, "autor": autor,
                      "busca": busca, "arquivo": arquivo, "usado_em": datetime.now().isoformat(timespec="seconds")})
        CATALOGO.parent.mkdir(parents=True, exist_ok=True)
        CATALOGO.write_text(json.dumps(dados[-2000:], ensure_ascii=False, indent=1), encoding="utf-8")
    except Exception:  # noqa: BLE001 - catálogo é só histórico, nunca derruba o vídeo
        pass


def videos_pixabay(busca: str, quantos: int, destino: Path, tag: str, tem_gente=None) -> list[Path]:
    chave = os.environ.get("PIXABAY_API_KEY", "").strip()
    if not chave:
        return []
    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode(
        {"key": chave, "q": busca[:100], "per_page": 50, "safesearch": "true", "min_width": 720})
    saidas: list[Path] = []
    try:
        hits = json.loads(_curl([url]).stdout).get("hits", [])
        pontuados = []
        for h in hits:
            n = nota(h.get("tags", "").replace(",", " "), h.get("tags", ""))
            if n is None:
                continue
            pontuados.append((n, h))
        pontuados.sort(key=lambda x: -x[0])
        from core import guardiao_variedade as gv  # variedade: não repetir clipe (agente 26)
        inedito = [x for x in pontuados if gv.pode_usar("pixabay", x[1].get("id"))]
        repetido = [x for x in pontuados if x not in inedito and gv._chave("pixabay", x[1].get("id")) not in gv._ids_rodada]
        for _, h in inedito + repetido:
            if tem_gente and tem_gente({"url": h.get("tags", "")}):
                continue
            opcoes = h.get("videos", {})
            alvo = next((opcoes[k] for k in ("large", "medium") if opcoes.get(k, {}).get("url")), None)
            if not alvo:
                continue
            out = destino / f"{tag}_px{len(saidas)}.mp4"
            r = _curl(["-o", str(out), alvo["url"]], saida=False)
            if r.returncode == 0 and out.exists() and out.stat().st_size > 10000:
                saidas.append(out)
                gv.marcar("pixabay", h.get("id"), reuso=(_, h) in repetido)
                registrar("pixabay", h.get("id"), h.get("pageURL", ""), h.get("tags", ""), h.get("user", ""), out.name, busca)
            if len(saidas) >= quantos:
                break
    except Exception as exc:  # noqa: BLE001
        print("  pixabay:", exc)
    return saidas
