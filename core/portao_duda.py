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


def preflight_voz(rot: dict) -> list[str]:
    """Antes de narrar (NÃO gasta crédito): a chave vale, a voz da Duda existe e o saldo cobre este vídeo.

    Só bloqueia diante de resposta clara da ElevenLabs (401/403/404 ou saldo insuficiente); falha de rede só avisa.
    Sem chave configurada, não bloqueia (modo de teste com voz grátis).
    """
    import os
    import urllib.error
    import urllib.request
    chave = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not chave:
        return []
    try:
        import yaml
        cfg = yaml.safe_load((ROOT / "config" / "voz_elevenlabs.yaml").read_text(encoding="utf-8")) or {}
    except Exception:  # noqa: BLE001
        cfg = {}
    voz_id = (os.environ.get("ELEVENLABS_VOICE_ID", "").strip() or str(cfg.get("voice_id") or "")).strip()
    if cfg.get("voice_id") and voz_id and voz_id != cfg["voice_id"]:
        return [f"ELEVENLABS_VOICE_ID ({voz_id}) é diferente da voz oficial da Duda ({cfg['voice_id']})"]
    texto = " ".join(str(c.get("narracao", "")) for c in rot.get("cenas", [])) + " " + str(rot.get("chamada_final", ""))
    necessarios = len(re.sub(r"\s+", " ", TAG.sub("", texto)).strip())

    def pegar(url: str):
        req = urllib.request.Request(url, headers={"xi-api-key": chave})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)

    problemas: list[str] = []
    try:
        sub = pegar("https://api.elevenlabs.io/v1/user/subscription")
        restantes = int(sub.get("character_limit", 0)) - int(sub.get("character_count", 0))
        if restantes < necessarios * 1.1:
            problemas.append(f"saldo da ElevenLabs insuficiente: restam {restantes}, este vídeo precisa de ~{necessarios}")
    except urllib.error.HTTPError as e:
        corpo = ""
        try:
            corpo = e.read().decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            pass
        if "missing_permissions" in corpo:  # chave restrita (só voz): não lê saldo, mas pode narrar; não bloqueia
            print("aviso: chave sem permissão de leitura do saldo; preflight do saldo ignorado", flush=True)
        elif e.code in (401, 403):
            problemas.append(f"ElevenLabs recusou a chave (HTTP {e.code}): a voz cairia na grátis")
    except Exception as e:  # noqa: BLE001
        print(f"aviso: preflight da voz não conseguiu ler o saldo ({type(e).__name__}); seguindo", flush=True)
    if not problemas and voz_id:
        try:
            pegar(f"https://api.elevenlabs.io/v1/voices/{voz_id}")
        except urllib.error.HTTPError as e:
            if e.code in (400, 404, 422):  # 401/403 aqui pode ser só falta de permissão de leitura: não bloqueia
                problemas.append(f"voz da Duda ({voz_id}) não acessível nesta conta (HTTP {e.code})")
        except Exception as e:  # noqa: BLE001
            print(f"aviso: preflight não conseguiu conferir a voz ({type(e).__name__}); seguindo", flush=True)
    return problemas


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
