"""Coerência de raça/espécie (regra do Allan, 15/10/2026): quando o conteúdo cita uma raça, imagem e vídeo
têm de mostrar AQUELA raça; gato é gato e cachorro é cachorro. Roda DENTRO da produção (Guardião de Marca e
publicação do artigo), com visão do Gemini sobre os quadros do vídeo e a capa. Falha fechada para raça."""
from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import tempfile
import unicodedata
from pathlib import Path

from core.llm import GEMINI_URL, LLMError, _post

ROOT = Path(__file__).resolve().parents[1]


def _norm(t: str) -> str:
    t = unicodedata.normalize("NFD", str(t).lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def _cfg() -> dict:
    try:
        import yaml
        return yaml.safe_load((ROOT / "config" / "coerencia_racas.yaml").read_text(encoding="utf-8")) or {}
    except Exception:  # noqa: BLE001
        return {}


def detectar(texto: str) -> tuple[str, str]:
    """(especie, raca) pedidas pelo texto (titulo/slug/roteiro). '' quando não citado."""
    t = " " + _norm(re.sub(r"[-_]", " ", texto)) + " "
    raca = ""
    for r in sorted(_cfg().get("racas", []), key=len, reverse=True):
        if f" {_norm(r)} " in t or f" {_norm(r)}s " in t:
            raca = r
            break
    gato = bool(re.search(r" (gato|gatos|gatinho|gatinhos|felino)", t))
    cao = bool(re.search(r" (cachorro|cachorros|cao|caes|cadela|filhote de cachorro)", t))
    especie = "gato" if gato and not cao else "cachorro" if cao and not gato else ""
    if raca and not especie:
        especie = "gato" if _norm(raca) in {"siames", "persa", "maine coon", "ragdoll", "sphynx", "angora"} else "cachorro"
    return especie, raca


def _perguntar(imagens: list[bytes], especie: str, raca: str) -> list[dict]:
    chave = os.environ.get("GEMINI_API_KEY", "")
    if not chave:
        raise LLMError("GEMINI_API_KEY ausente")
    pedido = (f"Para CADA imagem, na ordem, responda um objeto JSON: "
              f'{{"animal": "cachorro"|"gato"|"outro"|"nenhum", "raca_provavel": "<raça>", "e_{ "raca" if raca else "especie" }_pedida": true|false}}. '
              f"Raça pedida: '{raca or 'qualquer'}'. Espécie pedida: '{especie or 'qualquer'}'. "
              "Seja rigoroso: galgo italiano (italian greyhound) é pequeno, muito fino, orelhas dobradas para trás, focinho afilado; "
              "whippet, galgo inglês, vira-lata, spitz, golden e outras NÃO são galgo italiano. Se a imagem não mostra animal, animal=nenhum e true. "
              "Responda SOMENTE um array JSON, um objeto por imagem.")
    partes = [{"text": pedido}] + [{"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(b).decode()}} for b in imagens]
    modelo = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
    dados = _post(GEMINI_URL.format(model=modelo), {"contents": [{"role": "user", "parts": partes}],
                  "generationConfig": {"temperature": 0.1, "maxOutputTokens": 2000, "responseMimeType": "application/json"}},
                  {"x-goog-api-key": chave}, tentativas=4)
    txt = "".join(p.get("text", "") for p in dados["candidates"][0]["content"]["parts"])
    return json.loads(re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip())


def verificar_imagens(imagens: list[bytes], especie: str, raca: str, primeira_obrigatoria: bool = True) -> tuple[bool, str]:
    """True se as imagens batem com a raça (ou espécie) pedida. Falha fechada quando há raça."""
    if not (especie or raca):
        return True, "sem raça/espécie citada: nada a conferir"
    try:
        res = _perguntar(imagens, especie, raca)
    except Exception as exc:  # noqa: BLE001
        return (not raca), f"coerência não verificada (visão indisponível: {str(exc)[:80]})"
    chave = "e_raca_pedida" if raca else "e_especie_pedida"
    animais = [(i, r) for i, r in enumerate(res) if isinstance(r, dict) and r.get("animal") != "nenhum"]
    if not animais:
        return True, "nenhum animal nos quadros"
    erradas = [i for i, r in animais if not r.get(chave, False)]
    if especie:
        outra = [i for i, r in animais if r.get("animal") in ("cachorro", "gato") and r.get("animal") != especie]
        if outra:
            return False, f"espécie errada (esperado {especie}) nos quadros {[i + 1 for i in outra]}"
    if raca:
        primeira_ruim = primeira_obrigatoria and animais[0][0] in erradas
        if primeira_ruim or len(erradas) / len(animais) > 0.2:
            vistos = ", ".join(sorted({str(r.get('raca_provavel', '?')) for _, r in animais if r.get(chave) is False}))
            return False, f"raça errada: pedida '{raca}', apareceu {vistos or 'outra'} em {len(erradas)}/{len(animais)} quadros" + (" (o primeiro quadro é de outra raça)" if primeira_ruim else "")
    return True, f"{len(animais) - len(erradas)}/{len(animais)} quadros conferem"


def quadros_do_video(video: Path, n: int = 6) -> list[bytes]:
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-vf", "fps=1/7,scale=480:-2",
                        "-frames:v", str(n), "-q:v", "4", f"{d}/q_%d.jpg"], check=False, timeout=120)
        return [p.read_bytes() for p in sorted(Path(d).glob("q_*.jpg"))]
