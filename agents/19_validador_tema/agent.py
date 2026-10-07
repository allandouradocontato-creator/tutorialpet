"""Agente 19 — Validador de Temas (mantém a fila de pauta sempre abastecida).

A fábrica produz 1 artigo/dia a partir de config/fila_temas.yaml. Fila vazia = dia sem produção.
Este agente (1) mostra o estoque por pilar e (2) repõe temas novos com o LLM, validando cada
sugestão ANTES de entrar na fila: sem duplicata, sem tema de diagnóstico/medicação (risco de
saúde), termo de busca de verdade (pergunta/long tail) e pilar conhecido.

Uso:
    python agents/19_validador_tema/agent.py --status
    python agents/19_validador_tema/agent.py --repor 10        # chama o LLM (precisa de GEMINI_API_KEY)
    python agents/19_validador_tema/agent.py --repor 10 --dry-run   # só mostra, não grava
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

FILA = ROOT / "config" / "fila_temas.yaml"
PILARES_PADRAO = ["primeiros_passos_filhotes", "cuidados_diarios", "alimentacao", "comportamento",
                  "produtos_compras", "saude_basica"]
# Fora de escopo: o blog não dá diagnóstico nem dose (política do projeto: sempre orientar o veterinário).
BLOQUEADOS = ["dose", "dosagem", "remedio", "medicamento", "diagnostico", "vermifugo quanto", "tratamento caseiro",
              "receita caseira de remedio", "como curar", "cura de"]
MINIMO_ESTOQUE = 10


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9 ]+", " ", "".join(c for c in s if unicodedata.category(c) != "Mn")).strip()


def carregar() -> dict:
    return yaml.safe_load(FILA.read_text(encoding="utf-8")) or {"temas": []}


def similar(a: str, b: str) -> bool:
    ta, tb = set(norm(a).split()), set(norm(b).split())
    if not ta or not tb:
        return False
    return len(ta & tb) / min(len(ta), len(tb)) >= 0.75


def validar(termo: str, pilar: str, existentes: list[str], pilares: list[str]) -> str | None:
    """Devolve o motivo da recusa, ou None se o tema pode entrar."""
    n = norm(termo)
    if len(n.split()) < 3:
        return "curto demais (precisa ser termo de busca de verdade)"
    if len(n.split()) > 12:
        return "longo demais"
    if pilar not in pilares:
        return f"pilar desconhecido: {pilar}"
    if any(b in n for b in BLOQUEADOS):
        return "tema de diagnóstico/medicação (fora de escopo, risco de saúde)"
    if any(similar(termo, e) for e in existentes):
        return "duplicado ou quase igual a um tema que já existe"
    return None


def status() -> int:
    temas = carregar()["temas"]
    cont = Counter((t.get("status", "?")) for t in temas)
    pend = Counter(t.get("pilar", "?") for t in temas if t.get("status") == "pendente")
    print("Por status:", dict(cont))
    print("Pendentes por pilar:", dict(pend))
    faltam = max(0, MINIMO_ESTOQUE - cont.get("pendente", 0))
    print(f"Estoque mínimo {MINIMO_ESTOQUE}: " + ("OK" if not faltam else f"faltam {faltam} temas (rode --repor {faltam})"))
    return 0


def pedir_ao_llm(n: int, existentes: list[str], pilares: list[str]) -> list[dict]:
    from core.llm import gerar_texto
    prompt = (
        f"Sugira {n} temas NOVOS de artigo para um blog brasileiro para tutores de cães e gatos de TODOS os perfis (iniciantes e experientes, filhote, adulto e idoso, multi-pet, família). No máximo 1 em cada 4 temas pode ser de iniciante.\n"
        f"Cada tema deve ser um termo de busca real em português (pergunta ou long tail), com 4 a 10 palavras.\n"
        f"Pilares permitidos: {', '.join(pilares)}. Distribua entre os pilares.\n"
        "PROIBIDO: diagnóstico, doses, remédios, tratamentos. Foque em rotina, comportamento, enxoval, alimentação "
        "geral, produtos e primeiros passos.\n"
        f"Já existem (não repita nem faça parecido): {json.dumps(existentes[:60], ensure_ascii=False)}\n"
        'Responda SOMENTE JSON: [{"termo": "...", "pilar": "..."}]')
    bruto = gerar_texto(prompt, sistema="Você é um pesquisador de SEO para pets. Responde só JSON válido.",
                        temperatura=0.7, max_tokens=2500)
    m = re.search(r"\[.*\]", bruto, flags=re.S)
    return json.loads(m.group(0)) if m else []


def repor(n: int, dry: bool, sugestoes: list[dict] | None = None) -> int:
    dados = carregar()
    temas = dados["temas"]
    pilares = sorted({t.get("pilar") for t in temas if t.get("pilar")} | set(PILARES_PADRAO))
    existentes = [t["termo"] for t in temas]
    if sugestoes is None:
        sugestoes = pedir_ao_llm(n, existentes, pilares)
    aceitos, recusados = [], []
    for s in sugestoes:
        termo, pilar = str(s.get("termo", "")).strip(), str(s.get("pilar", "")).strip()
        motivo = validar(termo, pilar, existentes + [a["termo"] for a in aceitos], pilares)
        (recusados if motivo else aceitos).append({"termo": termo, "pilar": pilar, "motivo": motivo}
                                                 if motivo else {"termo": termo, "pilar": pilar, "status": "pendente"})
    for a in aceitos:
        print("ENTRA   :", a["termo"], f"[{a['pilar']}]")
    for r in recusados:
        print("RECUSADO:", r["termo"], "->", r["motivo"])
    if not dry and aceitos:
        temas.extend(aceitos)
        FILA.write_text(yaml.safe_dump(dados, allow_unicode=True, sort_keys=False), encoding="utf-8")
        print(f"{len(aceitos)} temas gravados em {FILA.relative_to(ROOT)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--repor", type=int)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.repor:
        return repor(a.repor, a.dry_run)
    return status()


if __name__ == "__main__":
    sys.exit(main())
