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
    """22/10 v2: llava so DESCREVE (confiavel); quem julga tema/beleza/agressividade e o llama-3.3-70b (texto), em
    portugues, com a rubrica B do Juiz. O yes/no direto do llava reprovava tudo (tema=no em 100% das candidatas)."""
    conta, tok = os.environ["CF_ACCOUNT_ID"], os.environ["CF_API_TOKEN"]
    base = f"https://api.cloudflare.com/client/v4/accounts/{conta}/ai/run/"
    hdr = {"Authorization": "Bearer " + tok, "Content-Type": "application/json"}
    def post(model, body):
        req = urllib.request.Request(base + model, data=json.dumps(body).encode(), headers=hdr)
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())["result"]
    descr = []
    for b in imagens:
        try:
            d = post("@cf/llava-hf/llava-1.5-7b-hf", {"image": list(b), "max_tokens": 120,
                     "prompt": "Describe this photo precisely: which animals (species, breed, size, color), what objects, the setting, whether any person or human body part is visible, any logo or watermark, the mood and lighting."})
            descr.append(str(d.get("description", "")).strip())
        except Exception as exc:  # noqa: BLE001
            descr.append(f"(descricao indisponivel: {str(exc)[:40]})")
    lista = "\n".join(f"{i}: {t}" for i, t in enumerate(descr))
    pedido = (f"Artigo de blog de pets sobre: '{tema}'. Abaixo, descricoes de {len(descr)} fotos candidatas a capa. "
              "Para CADA foto, na ordem, devolva um objeto JSON: {\"mostra_o_tema\": true|false, \"bonita_agradavel\": true|false, "
              "\"agressiva_ou_triste\": true|false, \"nota\": 0-10, \"motivo\": \"<=10 palavras\"}. "
              "mostra_o_tema = true se a foto mostra o objeto, a situacao ou o animal concreto do tema (ex.: 'cinto de seguranca' exige cachorro com cinto/peitoral no carro; "
              "'manchas de lagrima' exige cachorro branco de pelo claro com rosto visivel; 'gato morde' exige gato perto de mao/pessoa ou em postura de brincadeira; 'petiscos' exige gato com comida/petisco). "
              "bonita_agradavel = false se houver pessoa, mao ou perna em destaque, logotipo, marca d'agua, sujeira, ambiente feio ou foto escura. "
              "agressiva_ou_triste = true se dentes a mostra, rosnado, medo, doenca, ferimento, abandono, jaula. "
              "nota 10 = objeto exato do tema + animal certo + bonita + bem enquadrada. Responda SOMENTE um array JSON.\n\n" + lista)
    r = post("@cf/meta/llama-3.3-70b-instruct-fp8-fast", {"messages": [{"role": "user", "content": pedido}], "max_tokens": 900, "temperature": 0.1})
    txt = str(r.get("response", ""))
    m = re.search(r"\[.*\]", txt, re.S)
    out = []
    if m:
        bruto = m.group(0)
        try:
            out = json.loads(bruto)
        except json.JSONDecodeError:
            # modelo as vezes devolve aspas simples ou true/false sem aspas corretas: tenta ast
            import ast
            try:
                out = ast.literal_eval(bruto.replace("true", "True").replace("false", "False").replace("null", "None"))
            except Exception:  # noqa: BLE001
                out = []
    if not isinstance(out, list):
        out = []
    while len(out) < len(descr):
        out.append({"mostra_o_tema": False, "bonita_agradavel": False, "agressiva_ou_triste": False, "nota": 0, "motivo": "sem veredito"})
    for o, d in zip(out, descr):
        o["motivo"] = f"cf: {o.get('motivo','')} | {d[:60]}"
    return out[:len(descr)]


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
