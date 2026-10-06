"""Motor de texto (LLM) com troca de provedor por variável de ambiente.

LLM_PROVIDER = gemini | anthropic | ollama   (padrão: gemini se houver GEMINI_API_KEY)
Chaves ficam só no .env (nunca no código, nunca em log).
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
OLLAMA_URL = "http://localhost:11434/api/generate"


class LLMError(RuntimeError):
    pass


def _post(url: str, payload: dict, headers: dict, timeout: int = 180, tentativas: int = 7) -> dict:
    corpo = json.dumps(payload).encode("utf-8")
    ultimo = None
    for i in range(tentativas):
        req = urllib.request.Request(url, data=corpo, headers={"Content-Type": "application/json", **headers})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detalhe = exc.read().decode("utf-8", "ignore")[:300]
            ultimo = f"HTTP {exc.code}: {detalhe}"
            if exc.code in (429, 500, 502, 503, 504) and i < tentativas - 1:
                time.sleep(min(60, 5 * 2 ** i))
                continue
            raise LLMError(ultimo) from None
        except (urllib.error.URLError, TimeoutError) as exc:
            ultimo = f"rede: {exc}"
            if i < tentativas - 1:
                time.sleep(2 ** (i + 1))
                continue
    raise LLMError(ultimo or "falha desconhecida")


def provedor_atual() -> str:
    explicito = os.environ.get("LLM_PROVIDER", "").strip().lower()
    if explicito:
        return explicito
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    return "ollama"


def gerar_texto(prompt: str, sistema: str = "", temperatura: float = 0.8, max_tokens: int = 6000,
                provedor: str | None = None) -> str:
    prov = (provedor or provedor_atual()).lower()
    if prov == "gemini":
        chave = os.environ.get("GEMINI_API_KEY", "")
        if not chave:
            raise LLMError("GEMINI_API_KEY ausente no .env")
        modelo = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": temperatura, "maxOutputTokens": max_tokens},
        }
        if sistema:
            payload["systemInstruction"] = {"parts": [{"text": sistema}]}
        # Modelo principal + reservas (GEMINI_FALLBACK_MODELS, separadas por vírgula).
        # Se o principal estiver sobrecarregado (503) ou sem cota (429), tenta o próximo.
        reservas = [m.strip() for m in os.environ.get(
            "GEMINI_FALLBACK_MODELS", "gemini-3.8-flash-lite,gemini-3.5-flash").split(",") if m.strip()]
        modelos = [modelo] + [m for m in reservas if m != modelo]
        dados = None
        ultimo_erro = None
        for n, m in enumerate(modelos):
            try:
                dados = _post(GEMINI_URL.format(model=m), payload, {"x-goog-api-key": chave},
                              tentativas=4 if n < len(modelos) - 1 else 7)
                break
            except LLMError as exc:
                ultimo_erro = exc
                if n < len(modelos) - 1:
                    print(f"[llm] {m} falhou ({str(exc)[:80]}); tentando {modelos[n + 1]}")
                    continue
        if dados is None:
            raise ultimo_erro or LLMError("Gemini indisponível")
        try:
            partes = dados["candidates"][0]["content"]["parts"]
            return "".join(p.get("text", "") for p in partes).strip()
        except (KeyError, IndexError):
            raise LLMError(f"resposta Gemini sem texto (bloqueio de segurança ou cota): {str(dados)[:200]}") from None
    if prov == "anthropic":
        chave = os.environ.get("ANTHROPIC_API_KEY", "")
        if not chave:
            raise LLMError("ANTHROPIC_API_KEY ausente no .env")
        payload = {"model": os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5"), "max_tokens": max_tokens,
                   "temperature": temperatura, "system": sistema,
                   "messages": [{"role": "user", "content": prompt}]}
        dados = _post(ANTHROPIC_URL, payload, {"x-api-key": chave, "anthropic-version": "2023-06-01"})
        return "".join(b.get("text", "") for b in dados.get("content", [])).strip()
    if prov == "ollama":
        payload = {"model": os.environ.get("OLLAMA_MODEL", "llama3.1"), "prompt": f"{sistema}\n\n{prompt}",
                   "stream": False, "options": {"temperature": temperatura}}
        return _post(OLLAMA_URL, payload, {}).get("response", "").strip()
    raise LLMError(f"provedor desconhecido: {prov}")
