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


def _cf_llava(imagens: list[bytes], tema: str) -> list[dict]:
    conta, tok = os.environ["CF_ACCOUNT_ID"], os.environ["CF_API_TOKEN"]
    url = f"https://api.cloudflare.com/client/v4/accounts/{conta}/ai/run/@cf/llava-hf/llava-1.5-7b-hf"
    def ask(b, q):
        body = json.dumps({"image": list(b), "prompt": q, "max_tokens": 40}).encode()
        req = urllib.request.Request(url, data=body, headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read())["result"]["description"].strip().lower()
    en = tema  # tema em portugues do slug; o llava entende, mas a pergunta vai em ingles
    out = []
    for b in imagens:
        t = ask(b, f"This is a photo for a pet blog article about: '{en}'. Does the photo clearly show the subject of the article (the object, situation or condition of the animal mentioned)? Answer yes or no.")
        a = ask(b, "Is the animal snarling, showing teeth aggressively, scared, sick, injured, or is the photo dark and gloomy? Answer yes or no.")
        out.append({"mostra_o_tema": t.startswith("yes"), "bonita_agradavel": not a.startswith("yes"),
                    "agressiva_ou_triste": a.startswith("yes"), "motivo": f"llava tema={t[:3]} agressiva={a[:3]}"})
    return out


def avaliar_alternativo(imagens: list[bytes], tema: str) -> list[dict] | None:
    if os.environ.get("CF_ACCOUNT_ID") and os.environ.get("CF_API_TOKEN"):
        try:
            return _cf_llava(imagens, tema)
        except Exception as exc:  # noqa: BLE001
            print("[capa] cloudflare falhou:", str(exc)[:80])
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
