"""Reagenda a fila inteira pra começar numa nova data, preservando a ordem dos itens
e a cadência de 1 post/dia no horário do config. Só edita o arquivo de fila local —
não chama a Graph API, não precisa de token.

Uso:
    python reagendar_fila.py --config <config.yaml>                    # começa amanhã
    python reagendar_fila.py --config <config.yaml> --a-partir-de 2026-10-01
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.config import load_yaml  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Reagenda a fila inteira preservando ordem e cadência")
    parser.add_argument("--config", required=True, help="Caminho do config.yaml")
    parser.add_argument("--fila", help="Sobrescreve o caminho de fila definido no config")
    parser.add_argument("--a-partir-de", metavar="AAAA-MM-DD", help="Data do 1º post. Padrão: amanhã")
    args = parser.parse_args()

    cfg = load_yaml(Path(args.config))
    fila_path = Path(args.fila or cfg["fila"])
    if not fila_path.is_absolute():
        fila_path = ROOT / fila_path

    tz = ZoneInfo(cfg["fuso_horario"])
    hora, minuto = (int(x) for x in cfg["hora_publicacao"].split(":"))

    if args.a_partir_de:
        inicio = datetime.strptime(args.a_partir_de, "%Y-%m-%d")
    else:
        inicio = datetime.now(tz) + timedelta(days=1)

    fila = json.loads(fila_path.read_text(encoding="utf-8"))
    fila_ordenada = sorted(fila, key=lambda r: r.get("ordem", 0))
    for i, item in enumerate(fila_ordenada):
        quando = (inicio + timedelta(days=i)).replace(hour=hora, minute=minuto, second=0, microsecond=0, tzinfo=tz)
        item["data_prevista"] = quando.strftime("%Y-%m-%d %H:%M %z")
        item["scheduled_publish_time_unix"] = int(quando.timestamp())

    fila_path.write_text(json.dumps(fila_ordenada, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Fila reagendada: {len(fila_ordenada)} itens, de {fila_ordenada[0]['data_prevista']} "
          f"a {fila_ordenada[-1]['data_prevista']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
