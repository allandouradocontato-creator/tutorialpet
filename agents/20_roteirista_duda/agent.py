"""Agente 20 — Roteirista da Duda (+ Diretor de Criativos, versão por regras).

Transforma o roteiro do dia (data/social/roteiros/<slug>.json) na FALA da Duda: texto curto, com a
personalidade de config/duda.yaml, pronto para o ElevenLabs (com tags de emoção) e uma versão
simples (sem tags) para o edge-tts. Também escolhe a estrutura do vídeo (alterna, nunca repete a
do dia anterior).

Segurança de marca: valida a fala contra tom proibido (sensual, alegar credencial), tamanho e
tags. Fala reprovada NÃO é gravada.

Uso:
    python agents/20_roteirista_duda/agent.py <slug>           # montagem por regras (sem LLM)
    python agents/20_roteirista_duda/agent.py <slug> --llm     # reescreve com o LLM e valida
Saída: data/social/duda/<slug>.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

CFG = ROOT / "config" / "duda.yaml"
SAIDA = ROOT / "data" / "social" / "duda"
BLOQUEIO_TOM = [r"\bsexy\b", r"\bsensual", r"\bgostosa", r"\bflerte", r"\bamor da minha vida\b",
                r"\bsou veterinaria\b", r"\bsou medica\b", r"\bestudos? comprovam", r"\b\d+% dos (caes|cachorros|gatos)\b"]


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def cfg() -> dict:
    return yaml.safe_load(CFG.read_text(encoding="utf-8"))


def escolher_estrutura(c: dict, slug: str) -> dict:
    """Alterna as estruturas; lê a última usada em data/social/duda/*.json para não repetir."""
    ests = c["estruturas"]
    usadas = []
    if SAIDA.exists():
        for f in sorted(SAIDA.glob("*.json"), key=lambda p: p.stat().st_mtime):
            if f.stem != slug:
                try:
                    usadas.append(json.loads(f.read_text(encoding="utf-8")).get("estrutura"))
                except ValueError:
                    pass
    ultima = usadas[-1] if usadas else None
    ids = [e["id"] for e in ests]
    prox = ids[(ids.index(ultima) + 1) % len(ids)] if ultima in ids else ids[0]
    return next(e for e in ests if e["id"] == prox)


def montar_por_regras(r: dict, c: dict) -> str:
    """Fala curta: assinatura + gancho + 2 primeiras ideias + chamada. Sem inventar fato novo."""
    cenas = [x["narracao"].strip() for x in r.get("cenas", []) if x.get("narracao")]
    gancho = r.get("gancho_3s", cenas[0] if cenas else "").strip()
    corpo = [c_ for c_ in cenas if c_ != gancho][:2]
    chamada = r.get("chamada_final", "O guia completo está no link da legenda.").strip()
    return " ".join([f"[warmly] Oi! {c['assinatura']}", f"[smiling] {gancho}", *corpo, f"[happy] {chamada}"])


def pedir_ao_llm(r: dict, c: dict, estrutura: dict, falha_anterior: str = "") -> str:
    from core.llm import gerar_texto
    prompt = (
        f"Reescreva este roteiro como FALA da {c['nome']}, apresentadora do Tutorial Pet.\n"
        f"Personalidade: {'; '.join(c['personalidade'])}.\nPROIBIDO: {'; '.join(c['tom_proibido'])}.\n"
        f"Estrutura do vídeo: {' → '.join(estrutura['passos'])}.\n"
        f"Tamanho: entre {c['limites']['min_caracteres_fala']} e {c['limites']['max_caracteres_fala']} caracteres.\n"
        f"Comece com: \"{c['assinatura']}\". Use no máximo 4 tags de emoção entre colchetes, só entre: "
        f"{', '.join(c['tags_elevenlabs_permitidas'])}. Não invente fatos, números nem estudos.\n"
        + (f"A versão anterior foi recusada: {falha_anterior}. Corrija.\n" if falha_anterior else "")
        + f"\nROTEIRO:\n{json.dumps(r, ensure_ascii=False)[:3500]}\n\nResponda SÓ com o texto da fala.")
    return gerar_texto(prompt, sistema="Você escreve falas curtas, calorosas e honestas em pt-BR.",
                       temperatura=0.8, max_tokens=700).strip().strip('"')


def validar(fala: str, c: dict) -> list[str]:
    erros = []
    sem_tags = re.sub(r"\[[^\]]*\]", "", fala).strip()
    n = len(sem_tags)
    lim = c["limites"]
    if n > lim["max_caracteres_fala"]:
        erros.append(f"longa demais ({n} > {lim['max_caracteres_fala']} caracteres)")
    if n < lim["min_caracteres_fala"]:
        erros.append(f"curta demais ({n} < {lim['min_caracteres_fala']} caracteres)")
    permitidas = set(c["tags_elevenlabs_permitidas"])
    for tag in re.findall(r"\[([^\]]*)\]", fala):
        if tag.strip().lower() not in permitidas:
            erros.append(f"tag não permitida: [{tag}]")
    nf = norm(fala)
    for pad in BLOQUEIO_TOM:
        if re.search(pad, nf):
            erros.append(f"tom/alegação proibida (padrão {pad})")
    return erros


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--llm", action="store_true")
    a = ap.parse_args()
    c = cfg()
    rot = ROOT / "data" / "social" / "roteiros" / f"{a.slug}.json"
    if not rot.exists():
        sys.exit(f"roteiro não encontrado: {rot}")
    roteiro = json.loads(rot.read_text(encoding="utf-8"))
    estrutura = escolher_estrutura(c, a.slug)

    fala, erros = "", []
    for tentativa in range(3 if a.llm else 1):
        fala = pedir_ao_llm(roteiro, c, estrutura, "; ".join(erros)) if a.llm else montar_por_regras(roteiro, c)
        erros = validar(fala, c)
        if not erros:
            break
    if erros:
        print("FALA REPROVADA:", *erros, sep="\n - ")
        print("Texto:", fala)
        return 1

    simples = re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", fala)).strip()
    SAIDA.mkdir(parents=True, exist_ok=True)
    out = {"slug": a.slug, "estrutura": estrutura["id"], "texto_elevenlabs": fala, "texto_simples": simples,
           "caracteres": len(simples), "creditos_elevenlabs_estimados": len(simples)}
    (SAIDA / f"{a.slug}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK — estrutura {estrutura['id']}, {len(simples)} caracteres (~{len(simples)} créditos ElevenLabs)")
    print(fala)
    return 0


if __name__ == "__main__":
    sys.exit(main())
