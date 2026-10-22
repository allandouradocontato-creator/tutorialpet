"""Plano B de foto (Allan, 22/10/2026): quando o banco grátis (Pexels) não entrega foto da raça certa que passe no portão,
gerar a foto por IA grátis (Cloudflare Workers AI, modelo FLUX schnell, mesmas credenciais CF que já existem).

Uso:  python scripts/gerar_foto_ia.py "<raça ou espécie>" <saida.jpg> [variacao]
Saída: imagem JPEG/PNG gravada em <saida.jpg>; código 0 = gerou, 1 = falhou (mensagem em stderr, sem segredos).
Regras: SÓ o animal, nunca pessoa; sem texto/logo; a foto gerada passa pelo MESMO portão de raça (core/coerencia.py).
"""
from __future__ import annotations

import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

MODELO = "@cf/black-forest-labs/flux-1-schnell"

EN = {  # termo do slug -> nome em inglês para o prompt
    "yorkshire": "Yorkshire Terrier", "galgo italiano": "Italian Greyhound", "galgo": "Italian Greyhound",
    "golden retriever": "Golden Retriever", "labrador": "Labrador Retriever", "pug": "Pug", "shih tzu": "Shih Tzu",
    "bulldog": "Bulldog", "poodle": "Poodle", "spitz": "Pomeranian (Spitz alemao)", "lulu da pomerania": "Pomeranian",
    "siames": "Siamese cat", "persa": "Persian cat", "maine coon": "Maine Coon cat", "ragdoll": "Ragdoll cat",
    "gato": "domestic cat", "cachorro": "dog",
}

VARIACOES = [
    "sitting indoors near a window, soft natural daylight, looking at the camera",
    "lying on a cozy blanket at home, warm light, relaxed and happy",
    "outdoors on green grass, golden hour light, playful and cheerful",
]


def prompt_para(raca: str, variacao: int = 0) -> str:
    nome = EN.get((raca or "").lower().strip(), raca or "dog")
    cena = VARIACOES[variacao % len(VARIACOES)]
    return (f"Professional photograph of a single cute {nome}, {cena}. Sharp focus, shallow depth of field, "
            "high quality pet photography, realistic fur detail, anatomically correct, no people, no hands, no text, no logo.")


def gerar(raca: str, destino: Path, variacao: int = 0) -> tuple[bool, str]:
    try:
        conta, tok = os.environ["CF_ACCOUNT_ID"], os.environ["CF_API_TOKEN"]
    except KeyError:
        return False, "CF_ACCOUNT_ID/CF_API_TOKEN ausentes"
    url = f"https://api.cloudflare.com/client/v4/accounts/{conta}/ai/run/{MODELO}"
    corpo = json.dumps({"prompt": prompt_para(raca, variacao), "steps": 6}).encode()
    req = urllib.request.Request(url, data=corpo, headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read())
        b64 = (d.get("result") or {}).get("image")
        if not b64:
            return False, "resposta sem imagem: " + str([e.get("message") for e in d.get("errors", [])])[:120]
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(base64.b64decode(b64))
        return True, f"ok {destino.stat().st_size} bytes"
    except Exception as exc:  # noqa: BLE001
        return False, f"falhou: {str(exc)[:120]}"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit(2)
    ok, msg = gerar(sys.argv[1], Path(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 0)
    print(msg, file=sys.stderr if not ok else sys.stdout)
    raise SystemExit(0 if ok else 1)
