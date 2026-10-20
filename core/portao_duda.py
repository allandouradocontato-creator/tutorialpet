"""Portão da Duda: confere o ROTEIRO antes de gastar créditos de voz e antes de qualquer pacote ir para a fila.

Nasceu em 20/10/2026: os 4 últimos vídeos do TikTok saíram sem tags de emoção e sem o padrão da Duda
(a fábrica seguia com o roteiro original quando o padrão falhava), e a voz ficou neutra e artificial.
O auditor só avisava DEPOIS. Aqui o erro vira BLOQUEIO: roteiro reprovado não é narrado nem entregue.

Uso:  python -m core.portao_duda <slug>     (sai com código 1 se reprovar)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTA_VERBOS = re.compile(r"segue|comenta|compartilha|salva|manda|conta nos|tutorialpet\.com\.br|vem com a gente", re.I)
TAG = re.compile(r"\[([^\]]*)\]")


def _permitidas() -> set[str]:
    try:
        import yaml
        d = yaml.safe_load((ROOT / "config" / "duda.yaml").read_text(encoding="utf-8")) or {}
        return {str(t).strip().lower() for t in d.get("tags_elevenlabs_permitidas", [])}
    except Exception:  # noqa: BLE001
        return {"warmly", "smiling", "excited", "thoughtful", "softly", "happy", "short pause"}


def validar_roteiro(rot: dict) -> list[str]:
    """Devolve a lista de problemas (vazia = pode narrar)."""
    erros: list[str] = []
    cenas = rot.get("cenas") or []
    if len(cenas) < 3:
        erros.append(f"roteiro com só {len(cenas)} cena(s)")
        return erros
    if not rot.get("molde_gancho"):
        erros.append("padrão da Duda NÃO foi aplicado (sem molde de gancho): roteiro original, sem emoção")
    narracao = [str(c.get("narracao", "")) for c in cenas]
    chamada = str(rot.get("chamada_final", ""))
    todas = " ".join(narracao) + " " + chamada
    tags = [t.strip().lower() for t in TAG.findall(todas)]
    permitidas = _permitidas()
    if len(set(tags)) < 2:
        erros.append(f"tags de emoção insuficientes ({sorted(set(tags)) or 'nenhuma'}): a voz sai reta e artificial")
    fora = sorted({t for t in tags if t not in permitidas})
    if fora:
        erros.append(f"tags não permitidas: {fora}")
    if tags.count("excited") > 1:
        erros.append("mais de um [excited]")
    if "laughs" in tags:
        erros.append("risada proibida")
    if any("[" in str(c.get("texto_na_tela", "")) for c in cenas):
        erros.append("tag de emoção aparece na tela")
    cta = chamada or narracao[-1]
    if not CTA_VERBOS.search(cta):
        erros.append("CTA ausente (seguir, comentar, compartilhar, salvar ou blog)")
    if "Duda" not in cta:
        erros.append("CTA sem a assinatura da Duda")
    gancho = re.sub(r"\s+", " ", TAG.sub("", str(rot.get("gancho_3s", "")))).strip()
    primeira = re.sub(r"\s+", " ", TAG.sub("", narracao[0])).strip()
    if not gancho or gancho.lower().rstrip("?.! ") not in primeira.lower():
        erros.append("gancho não é FALADO na 1ª cena")
    return erros


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit("uso: python -m core.portao_duda <slug>")
    rot = json.loads((ROOT / "data" / "social" / "roteiros" / f"{sys.argv[1]}.json").read_text(encoding="utf-8"))
    erros = validar_roteiro(rot)
    if erros:
        print("PORTÃO DA DUDA: REPROVADO\n" + "\n".join(f"- {e}" for e in erros))
        return 1
    print("PORTÃO DA DUDA: aprovado (tags de emoção, assinatura e gancho falado conferidos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
