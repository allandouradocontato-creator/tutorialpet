"""Agente 22 — Guardião de Gasto (confere a campanha ANTES de publicar).

Lê um rascunho de campanha em YAML/JSON e confere contra config/regras_gasto.yaml. Se qualquer
regra for violada, devolve código 1 e a lista do que corrigir. Nunca publica nada e nunca mexe
na Meta — só dá o veredito "pode publicar" ou "NÃO publique".

Uso:
    python agents/22_guardiao_gasto/agent.py campanha.yaml
Formato do rascunho (campos): nome, conta_anuncios, pixel_id, orcamento_diario_reais, evento_otimizacao,
    posicionamento_manual (true/false), posicionamentos (lista), paises (lista), status_pagamento (opcional)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]

import yaml  # noqa: E402

REGRAS = ROOT / "config" / "regras_gasto.yaml"


def conferir(c: dict, r: dict) -> list[str]:
    erros: list[str] = []
    if r.get("exigir_posicionamento_manual") and not c.get("posicionamento_manual"):
        erros.append("posicionamentos estão AUTOMÁTICOS — use manual (só Facebook e Instagram)")
    pos = [str(p).lower() for p in c.get("posicionamentos", [])]
    if not pos:
        erros.append("nenhum posicionamento informado")
    for p in pos:
        if p in r["posicionamentos_proibidos"]:
            erros.append(f"posicionamento proibido: {p}")
        elif p not in r["posicionamentos_permitidos"]:
            erros.append(f"posicionamento fora da lista permitida: {p}")
    orc = c.get("orcamento_diario_reais")
    if orc is None:
        erros.append("orçamento diário não informado")
    elif float(orc) > float(r["orcamento_diario_max_reais"]):
        erros.append(f"orçamento diário R$ {orc} acima do teto de R$ {r['orcamento_diario_max_reais']}")
    if str(c.get("pixel_id", "")) != str(r["pixel_id_esperado"]):
        erros.append(f"pixel {c.get('pixel_id')} diferente do esperado {r['pixel_id_esperado']}")
    if str(c.get("conta_anuncios", "")) != str(r["conta_anuncios_esperada"]):
        erros.append(f"conta de anúncios {c.get('conta_anuncios')} não é a esperada")
    if c.get("evento_otimizacao") not in r["eventos_otimizacao_ok"]:
        erros.append(f"evento de otimização inválido: {c.get('evento_otimizacao')}")
    fora = [p for p in c.get("paises", []) if p not in r["paises_permitidos"]]
    if fora or not c.get("paises"):
        erros.append(f"países fora da regra: {fora or 'nenhum informado'}")
    if str(c.get("status_pagamento", "")).lower() in {"erro", "erro_no_pagamento", "falha"}:
        erros.append("conta com ERRO DE PAGAMENTO — a campanha não vai entregar; resolva antes")
    return erros


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit("uso: python agents/22_guardiao_gasto/agent.py campanha.yaml")
    texto = Path(sys.argv[1]).read_text(encoding="utf-8")
    campanha = json.loads(texto) if texto.lstrip().startswith("{") else yaml.safe_load(texto)
    regras = yaml.safe_load(REGRAS.read_text(encoding="utf-8"))
    erros = conferir(campanha, regras)
    if erros:
        print(f"NÃO PUBLIQUE a campanha '{campanha.get('nome', '?')}':")
        for e in erros:
            print(" -", e)
        return 1
    print(f"PODE PUBLICAR '{campanha.get('nome', '?')}': dentro de todas as regras de gasto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
