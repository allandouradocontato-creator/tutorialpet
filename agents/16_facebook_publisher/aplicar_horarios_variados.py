"""Aplica horário variado (sorteado dentro de `janelas_horarios` do config) na fila:
substitui o rodízio fixo antigo, que repetia sempre a mesma sequência de 4 dias e ficava
identificável como automação. O primeiro item (ordem 1) recebe 1 horário, sorteado dentro
de uma janela que ainda não passou hoje; os demais recebem `max_posts_por_dia` horários
por dia a partir de amanhã, um por janela. Preserva a ordem relativa dos itens. Sorteio
determinístico por `semente_aleatoria` do config — auditável, documentado em
`agent.py:proxima_data_rotacao`.

Uso:
    python aplicar_horarios_variados.py --config <config.yaml>
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_yaml  # noqa: E402
from agent import get_marketing_logger, proxima_data_rotacao  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Aplica horário variado (sorteado) na fila")
    parser.add_argument("--config", required=True)
    parser.add_argument("--fila")
    args = parser.parse_args()

    cfg = load_yaml(Path(args.config))
    if not cfg.get("janelas_horarios"):
        raise SystemExit("config sem 'janelas_horarios' — nada a aplicar.")

    fila_path = Path(args.fila or cfg["fila"])
    if not fila_path.is_absolute():
        fila_path = ROOT / fila_path

    log = get_marketing_logger()
    tz = ZoneInfo(cfg["fuso_horario"])
    agora = datetime.now(tz)

    fila = json.loads(fila_path.read_text(encoding="utf-8"))
    fila_ordenada = sorted(fila, key=lambda r: r.get("ordem", 0))

    for item in fila_ordenada:
        quando = proxima_data_rotacao(item["ordem"], cfg, agora, log)
        item["data_prevista"] = quando.strftime("%Y-%m-%d %H:%M %z")
        item["scheduled_publish_time_unix"] = int(quando.timestamp())

    fila_path.write_text(json.dumps(fila_ordenada, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Horários variados aplicados: {len(fila_ordenada)} itens (semente_aleatoria="
          f"{cfg.get('semente_aleatoria', 0)}).")
    for item in fila_ordenada[:6]:
        print(f"  {item['ordem']:>2}  {item['data_prevista']}  {item['slug']}")
    print("  ...")
    print(f"  {fila_ordenada[-1]['ordem']:>2}  {fila_ordenada[-1]['data_prevista']}  {fila_ordenada[-1]['slug']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
