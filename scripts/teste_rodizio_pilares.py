"""Teste do rodizio de pilares (rotina_diaria.escolher_proximo). Roda sem LLM e sem rede: python scripts/teste_rodizio_pilares.py
Regra testada (28/10/2026): nunca repetir pilar no mesmo dia enquanto houver alternativa; virada de dia nao repete o pilar do
ultimo artigo do dia anterior; sem alternativa, usa o pilar MENOS usado hoje (nao cai em pendentes[0]).
Sai com codigo 1 se algum caso falhar (pode entrar no vigia/CI)."""
from __future__ import annotations

import copy
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import rotina_diaria as rd  # noqa: E402

PILARES = ["cuidados_diarios", "alimentacao", "comportamento", "primeiros_passos_filhotes", "produtos_compras"]
PRIORITARIOS = ["adocao", "utilidade_publica"]
falhas: list[str] = []


def checar(ok: bool, msg: str) -> None:
    print(("OK   " if ok else "FALHA ") + msg)
    if not ok:
        falhas.append(msg)


def fila_sintetica(n_por_pilar: int = 6, usados: list[tuple[str, str]] | None = None) -> dict:
    temas = [{"termo": f"tema {p} {i}", "pilar": p, "status": "pendente"} for i in range(n_por_pilar) for p in PILARES]
    for d, p in usados or []:
        temas.append({"termo": f"usado {p} {d}", "pilar": p, "status": "rascunho_pronto", "data": d})
    return {"temas": temas}


def produzir(fila: dict, dia: str, n: int) -> list[str]:
    """Simula n producoes no dia: escolhe, marca como pronto com a data do dia."""
    seq = []
    for _ in range(n):
        t = rd.escolher_proximo(fila, hoje=dia)
        if t is None:
            break
        t["status"], t["data"] = "rascunho_pronto", dia
        seq.append(t["pilar"])
    return seq


# 1) 3 artigos/dia durante 6 dias: 3 pilares distintos por dia e o 1o do dia nao repete o ultimo do dia anterior
fila = fila_sintetica()
ultimo = None
for k in range(6):
    dia = f"2026-11-{k + 1:02d}"
    seq = produzir(fila, dia, 3)
    checar(len(set(seq)) == 3, f"{dia}: 3 artigos em 3 pilares diferentes {seq}")
    if ultimo is not None:
        checar(seq[0] != ultimo, f"{dia}: 1o artigo ({seq[0]}) difere do ultimo do dia anterior ({ultimo})")
    ultimo = seq[-1]

# 2) disparos manuais: 5 no mesmo dia usam os 5 pilares; do 6o em diante, o pilar menos usado (nunca pendentes[0] cego)
fila = fila_sintetica()
seq = produzir(fila, "2026-12-01", 7)
checar(len(set(seq[:5])) == 5, f"5 primeiros do dia cobrem os 5 pilares {seq[:5]}")
cont = Counter(seq)
checar(max(cont.values()) - min(cont.values()) <= 1, f"7 no dia ficam equilibrados {dict(cont)}")

# 3) caso real de 28/10: ja usados cuidados, produtos e alimentacao hoje -> so sobram comportamento e primeiros passos
fila = fila_sintetica(usados=[("2026-10-28", "cuidados_diarios"), ("2026-10-28", "produtos_compras"),
                              ("2026-10-28", "alimentacao")])
seq = produzir(fila, "2026-10-28", 2)
checar(set(seq) == {"comportamento", "primeiros_passos_filhotes"}, f"28/10 com 3 pilares usados: proximos {seq}")

# 4) so ha pendentes de pilares ja usados hoje: nao trava e escolhe o menos usado
fila = {"temas": [{"termo": "a", "pilar": "alimentacao", "status": "pendente"},
                  {"termo": "b", "pilar": "comportamento", "status": "pendente"},
                  {"termo": "u1", "pilar": "alimentacao", "status": "rascunho_pronto", "data": "2026-10-28"},
                  {"termo": "u2", "pilar": "alimentacao", "status": "rascunho_pronto", "data": "2026-10-28"},
                  {"termo": "u3", "pilar": "comportamento", "status": "rascunho_pronto", "data": "2026-10-28"}]}
t = rd.escolher_proximo(fila, hoje="2026-10-28")
checar(t is not None and t["pilar"] == "comportamento", "sem alternativa: escolhe o pilar menos usado hoje")

# 5) fila real do repositorio: a escolha de hoje nao repete pilar ja usado hoje (se houver alternativa)
real = yaml.safe_load((ROOT / "config" / "fila_temas.yaml").read_text(encoding="utf-8")) or {"temas": []}
hoje = rd.hoje_fortaleza()
usados_hoje = {t["pilar"] for t in real["temas"] if str(t.get("data", "")) == hoje and t.get("status") != "pendente"}
prox = rd.escolher_proximo(copy.deepcopy(real), hoje=hoje)
alternativa = any(t.get("status") == "pendente" and t.get("pilar") not in usados_hoje for t in real["temas"])
checar(prox is None or not alternativa or prox["pilar"] not in usados_hoje,
       f"fila real ({hoje}): proximo = {prox and prox['pilar']}; ja usados hoje = {sorted(usados_hoje)}")

# --- series prioritarias (28/10/2026): adocao e utilidade_publica 1/dia cada, 3o slot do rodizio original
def fila_series(n=12):
    temas = [{"termo": f"tema {p} {i}", "pilar": p, "status": "pendente"} for i in range(n) for p in PRIORITARIOS + PILARES]
    return {"temas": temas}

fs = fila_series()
dias = ["2026-10-29", "2026-10-30", "2026-10-31"]
for d in dias:
    seq = produzir(fs, d, 3)
    checar(len(set(seq)) == 3, f"series {d}: 3 pilares diferentes no dia: {seq}")
    checar(all(p in seq for p in PRIORITARIOS), f"series {d}: adocao e utilidade_publica saem 1x cada: {seq}")
    checar(seq.count("adocao") == 1 and seq.count("utilidade_publica") == 1, f"series {d}: no maximo 1/dia por serie")

print("\nRESULTADO:", "TUDO OK" if not falhas else f"{len(falhas)} falha(s)")
sys.exit(1 if falhas else 0)
