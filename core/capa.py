"""Capa coerente (Allan, 22/10/2026): a foto tem de MOSTRAR o assunto do artigo (caixa de transporte -> animal na caixa,
peso -> animal visivelmente acima do peso, cinto -> animal com cinto no carro...), ser bonita e agradavel, sem agressividade,
sem pobreza, sem animal maltratado/doente, e nunca repetir a capa de outro artigo (o AdSense e o leitor julgam pela imagem).
Uso: python -m core.capa <slug>   -> escolhe a melhor candidata, aplica (agente 15) e imprime 'CAPA <indice>' ou 'SEM_CAPA'."""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from core.llm import GEMINI_URL, _post

ROOT = Path(__file__).resolve().parents[1]
SITE = "pets-tutores-iniciantes"


def _md5(p: Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def proibidas() -> set[str]:
    f = ROOT / "config" / "fotos_proibidas.txt"
    if not f.exists():
        return set()
    return {l.split()[0] for l in f.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}


def usadas_por_outros(slug: str) -> set[str]:
    return {_md5(f) for f in (ROOT / "data" / "visual" / "imagens").glob("*.jpg") if f.stem != slug}


def avaliar(imagens: list[bytes], tema: str) -> list[dict]:
    chave = os.environ.get("GEMINI_API_KEY", "")
    if not chave:
        raise RuntimeError("GEMINI_API_KEY ausente")
    pedido = (f"Artigo de blog de pets sobre: '{tema}'. Para CADA imagem, na ordem, responda um objeto JSON: "
              '{"mostra_o_tema": true|false, "bonita_agradavel": true|false, "agressiva_ou_triste": true|false, "motivo": "<=12 palavras"}. '
              "mostra_o_tema = true SOMENTE se a foto mostra o assunto concreto do artigo (o objeto, a situação ou a condição do animal citada no tema: "
              "ex.: 'caixa de transporte' exige animal DENTRO ou ao lado de uma caixa de transporte; 'acima do peso' exige animal visivelmente gordinho; "
              "'cinto de segurança' exige animal com cinto/peitoral de carro dentro de veículo; 'patas no inverno' exige patas/neve/botinhas; "
              "'legumes' exige o animal com legumes). Rosto genérico NÃO mostra o tema. "
              "agressiva_ou_triste = true se mostra dentes à mostra, rosnado, latido agressivo, medo, doença, ferimento, sujeira, abandono, pobreza, jaula, ou foto escura/sombria. "
              "bonita_agradavel = false (reprova, regra do Juiz 22/10) se houver pessoa, rosto, mão, perna ou colo humano em destaque, logotipo/marca legível, marca d'água, ou animal cortado pelo enquadramento. "
              "Inclua tambem \"nota\": 0-10 (10 = mostra o objeto exato do tema, animal certo, bonita, bem enquadrada para 16:9). "
              "Responda SOMENTE um array JSON, um objeto por imagem.")
    partes = [{"text": pedido}] + [{"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(b).decode()}} for b in imagens]
    modelo = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
    import time
    if getattr(avaliar, "gemini_fora", False):
        raise RuntimeError("Gemini indisponivel (429 nesta rodada; sem novas tentativas)")
    for tent in range(4):   # 22/10: HTTP 429 (limite do Gemini gratis) -> espera e tenta de novo
        try:
            d = _post(GEMINI_URL.format(model=modelo), {"contents": [{"role": "user", "parts": partes}],
                      "generationConfig": {"temperature": 0.1, "maxOutputTokens": 2000, "responseMimeType": "application/json"}},
                      {"x-goog-api-key": chave}, timeout=60, tentativas=1)
            break
        except Exception as exc:  # noqa: BLE001
            if "429" not in str(exc):
                raise
            if tent >= 1:
                avaliar.gemini_fora = True   # 2 tentativas bastam: o resto da rodada vai direto para a alternativa gratis
                raise
            time.sleep(25)
    txt = "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"])
    return json.loads(re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip())


def escolher(slug: str) -> tuple[int | None, str]:
    """Indice da melhor candidata (tema + bonita + nao repetida + nao proibida) ou (None, motivo)."""
    cand = ROOT / "data" / "visual" / "candidatos" / slug
    fotos = sorted(cand.glob("*.jpg"), key=lambda f: int(f.stem))
    if not fotos:
        return None, "sem candidatas"
    ban, usadas = proibidas(), usadas_por_outros(slug)
    livres = [f for f in fotos if _md5(f) not in ban and _md5(f) not in usadas]
    if not livres:
        return None, "todas as candidatas sao proibidas ou ja usadas em outro artigo"
    try:
        res = avaliar([f.read_bytes() for f in livres], slug.replace("-", " "))
    except Exception as exc:  # noqa: BLE001
        # Gemini gratis no limite: alternativas gratis, na ordem (regra do Allan, 22/10/2026)
        print("[capa] Gemini indisponivel:", str(exc)[:80], "-> tentando alternativas gratis", flush=True)
        res = None
        try:
            from core.capa_alt import avaliar_alternativo
            res = avaliar_alternativo([f.read_bytes() for f in livres], slug.replace("-", " "))
        except Exception as e2:  # noqa: BLE001
            print("[capa] alternativas por API falharam:", str(e2)[:80], flush=True)
        if res is None:
            try:
                from core.capa_local import avaliar as _clip
                mapa = {c.get("indice"): c.get("query", "") for c in json.loads((cand / "candidatos.json").read_text(encoding="utf-8"))}
                res = _clip([f.read_bytes() for f in livres], [mapa.get(int(f.stem)) or slug.replace("-", " ") for f in livres])
            except Exception as e3:  # noqa: BLE001
                return None, f"visao indisponivel: {str(e3)[:80]}"
    bons = [(f, r) for f, r in zip(livres, res) if isinstance(r, dict) and r.get("mostra_o_tema") and r.get("bonita_agradavel") and not r.get("agressiva_ou_triste")]
    # regra do Juiz (22/10): pontuar TODAS as candidatas e escolher a de maior nota, nunca a primeira por padrao
    bons.sort(key=lambda fr: -float(fr[1].get("nota", 5) or 5))
    escolher.bons = [int(f.stem) for f, _ in bons]
    if bons:
        return int(bons[0][0].stem), f"nota {bons[0][1].get('nota', '?')}: " + str(bons[0][1].get("motivo", ""))
    return None, "nenhuma candidata mostra o tema com foto bonita: " + "; ".join(f"{f.stem}={r.get('motivo','?')}" for f, r in zip(livres, res) if isinstance(r, dict))


def main() -> int:
    slug = sys.argv[1]
    i, motivo = escolher(slug)
    if i is None:
        print("SEM_CAPA", slug, "-", motivo)
        return 2
    subprocess.run([sys.executable, str(ROOT / "agents" / "15_visual" / "agent.py"), "--site", SITE, "--selecionar", slug, str(i)], check=True)
    print("CAPA", slug, i, "-", motivo)
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    sys.exit(main())
