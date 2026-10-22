"""Avaliador de capa SEM API paga e sem limite (fallback quando o Gemini gratis estoura, Allan 22/10/2026):
CLIP roda no proprio runner do GitHub (gratis). Compara a foto com a descricao em ingles do tema (a busca que a achou)
contra descricoes genericas e contra 'agressivo/triste'. Menos fino que o Gemini, mas nunca fica sem avaliar."""
from __future__ import annotations

import io
import subprocess
import sys

_M = {}


def _carregar():
    if _M:
        return _M
    try:
        import torch  # noqa: F401
        import transformers  # noqa: F401
    except Exception:  # noqa: BLE001
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--index-url", "https://download.pytorch.org/whl/cpu", "torch"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "transformers", "pillow"], check=True)
    import torch
    from transformers import CLIPModel, CLIPProcessor
    _M["m"] = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").eval()
    _M["p"] = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    _M["t"] = torch
    return _M


def avaliar(imagens: list[bytes], consultas: list[str]) -> list[dict]:
    M = _carregar()
    from PIL import Image
    torch, m, p = M["t"], M["m"], M["p"]
    out = []
    for b, q in zip(imagens, consultas):
        img = Image.open(io.BytesIO(b)).convert("RGB")
        tema = f"a photo of {q}"
        textos = [tema, "a close-up portrait of a dog", "a close-up portrait of a cat", "a photo of a landscape or a building",
                  "a photo of a person"]
        ruins = ["an aggressive dog snarling and showing teeth", "a sad sick or injured animal", "a dark gloomy black and white photo",
                 "a cute happy pet in a bright pleasant photo"]
        with torch.no_grad():
            e = p(text=textos, images=img, return_tensors="pt", padding=True)
            pt = m(**e).logits_per_image.softmax(dim=1)[0]
            e2 = p(text=ruins, images=img, return_tensors="pt", padding=True)
            pr = m(**e2).logits_per_image.softmax(dim=1)[0]
        out.append({"mostra_o_tema": bool(pt[0] >= 0.5), "bonita_agradavel": bool(pr[3] >= 0.4),
                    "agressiva_ou_triste": bool(pr[0] + pr[1] + pr[2] >= 0.6), "motivo": f"clip tema={float(pt[0]):.2f} bom={float(pr[3]):.2f}"})
    return out
