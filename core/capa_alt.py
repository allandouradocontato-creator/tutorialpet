"""Provedores gratis alternativos ao Gemini para avaliar capas. So usa o que tiver chave no ambiente/segredos:
OPENROUTER_API_KEY (modelo :free com visao), GROQ_API_KEY (llama-4-scout), CF_ACCOUNT_ID+CF_API_TOKEN (Cloudflare Workers AI)."""
from __future__ import annotations

import base64
import json
import os
import re
import urllib.request

PROMPT = ("Artigo de blog de pets sobre: '{tema}'. Para CADA imagem, na ordem, responda um objeto JSON: "
          '{{"mostra_o_tema": true|false, "bonita_agradavel": true|false, "agressiva_ou_triste": true|false, "motivo": "<=12 palavras"}}. '
          "mostra_o_tema so se a foto mostra o assunto concreto (objeto/situacao/condicao do animal). Rosto generico NAO mostra. "
          "agressiva_ou_triste = dentes a mostra, rosnado, medo, doenca, ferimento, abandono, pobreza, foto escura. Responda SOMENTE um array JSON.")


def _openai_like(url, chave, modelo, imagens, tema):
    partes = [{"type": "text", "text": PROMPT.format(tema=tema)}] + [
        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(b).decode()}} for b in imagens]
    req = urllib.request.Request(url, data=json.dumps({"model": modelo, "messages": [{"role": "user", "content": partes}], "temperature": 0.1}).encode(),
                                 headers={"Authorization": f"Bearer {chave}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        txt = json.loads(r.read())["choices"][0]["message"]["content"]
    return json.loads(re.search(r"\[.*\]", txt, re.S).group(0))


def avaliar_alternativo(imagens: list[bytes], tema: str) -> list[dict] | None:
    if os.environ.get("OPENROUTER_API_KEY"):
        try:
            return _openai_like("https://openrouter.ai/api/v1/chat/completions", os.environ["OPENROUTER_API_KEY"],
                                os.environ.get("OPENROUTER_VISION_MODEL", "meta-llama/llama-3.2-11b-vision-instruct:free"), imagens, tema)
        except Exception as exc:  # noqa: BLE001
            print("[capa] openrouter falhou:", str(exc)[:80])
    if os.environ.get("GROQ_API_KEY"):
        try:
            return _openai_like("https://api.groq.com/openai/v1/chat/completions", os.environ["GROQ_API_KEY"],
                                os.environ.get("GROQ_VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"), imagens, tema)
        except Exception as exc:  # noqa: BLE001
            print("[capa] groq falhou:", str(exc)[:80])
    return None
