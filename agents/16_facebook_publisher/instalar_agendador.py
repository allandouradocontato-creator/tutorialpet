"""Instala (ou remove) a tarefa diária do Windows Task Scheduler que roda o Agente 16.

Este script só MONTA e MOSTRA o comando `schtasks` — ele nunca executa a criação da
tarefa sozinho. Rodar `schtasks /create` de verdade cria uma configuração persistente
no sistema operacional do usuário, e isso exige uma decisão explícita, não é algo pra
um agente decidir por conta própria. Use `--executar` quando já tiver revisado o
comando e quiser aplicar de fato.

A tarefa criada roda, uma vez por dia, em horário fixo (padrão: 08:00, bem antes das
21h de publicação — dá tempo de qualquer aprovação manual acontecer antes):

    python agent.py --config <config> --processar-fila

Isso agenda no máximo 1 post por dia na Graph API (a trava fica dentro do próprio
agent.py, não depende do agendador do SO pra ser respeitada).

Em Linux/Mac, o equivalente é uma linha de crontab (mostrada abaixo também), sem
precisar de nenhum script — não há necessidade de uma versão deste instalador pra cron.

Uso:
    python instalar_agendador.py --config ../../config/facebook_publisher/tutorial_pet.yaml
    python instalar_agendador.py --config ... --hora 08:00 --executar
    python instalar_agendador.py --remover --executar
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
PYTHON = sys.executable
AGENT_SCRIPT = AGENT_DIR / "agent.py"
TASK_NAME = "BlogFactory_Agente16_FacebookPublisher"


def montar_comando_criar(config_path: str, hora: str, cada_hora: bool = False) -> list[str]:
    # Caminho absoluto sempre: o Task Scheduler não roda com o diretório de trabalho do
    # projeto, então um --config relativo quebraria silenciosamente ("Start In: N/A").
    config_abs = str(Path(config_path).resolve())
    tarefa_cmd = f'"{PYTHON}" "{AGENT_SCRIPT}" --config "{config_abs}" --processar-fila'
    if cada_hora:
        # Necessário quando o config tem janelas_horarios: os horários de publicação mudam
        # de dia pra dia, então um único horário fixo de disparo não cobre todos os casos.
        # Rodar de hora em hora garante folga sobre o mínimo de 10 min da Graph API pra
        # qualquer horário do rodízio, e o processar-fila só age quando há item devido e
        # aprovado — rodar de mais não agenda nada fora da hora certa.
        return ["schtasks", "/create", "/tn", TASK_NAME, "/tr", tarefa_cmd, "/sc", "hourly", "/mo", "1", "/f"]
    return [
        "schtasks", "/create", "/tn", TASK_NAME, "/tr", tarefa_cmd,
        "/sc", "daily", "/st", hora, "/f",
    ]


def montar_comando_remover() -> list[str]:
    return ["schtasks", "/delete", "/tn", TASK_NAME, "/f"]


def montar_linha_crontab(config_path: str, hora: str, cada_hora: bool = False) -> str:
    config_abs = str(Path(config_path).resolve())
    tarefa = f'{PYTHON} {AGENT_SCRIPT} --config {config_abs} --processar-fila'
    if cada_hora:
        return f'0 * * * * {tarefa}'
    h, m = hora.split(":")
    return f'{m} {h} * * * {tarefa}'


def main() -> int:
    parser = argparse.ArgumentParser(description="Instala/remove a tarefa diária do Agente 16 no Windows Task Scheduler")
    parser.add_argument("--config", help="Caminho do config.yaml (obrigatório pra --criar)")
    parser.add_argument("--hora", default="08:00", help="Horário diário da tarefa (HH:MM). Padrão: 08:00")
    parser.add_argument("--cada-hora", action="store_true",
                         help="Roda a cada 1h em vez de 1x/dia — necessário com janelas_horarios no config")
    parser.add_argument("--remover", action="store_true", help="Remove a tarefa em vez de criar")
    parser.add_argument("--executar", action="store_true",
                         help="Executa o comando de verdade. Sem esta flag, só mostra o que seria rodado.")
    args = parser.parse_args()

    if args.remover:
        comando = montar_comando_remover()
    else:
        if not args.config:
            parser.error("--config é obrigatório pra criar a tarefa")
        comando = montar_comando_criar(args.config, args.hora, args.cada_hora)
        print("Equivalente em cron (Linux/Mac), caso o servidor não seja Windows:")
        print(f"  {montar_linha_crontab(args.config, args.hora, args.cada_hora)}")
        print()

    print("Comando que seria executado:")
    print("  " + " ".join(comando))

    if not args.executar:
        print("\n(nada foi executado — rode de novo com --executar pra aplicar de verdade)")
        return 0

    resultado = subprocess.run(comando, capture_output=True, text=True)
    print(resultado.stdout)
    if resultado.returncode != 0:
        print(resultado.stderr, file=sys.stderr)
        return resultado.returncode
    print("Tarefa aplicada com sucesso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
