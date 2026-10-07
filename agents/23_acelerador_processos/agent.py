"""Agente 23 — Acelerador de Processos.

Recebe a descrição de uma ferramenta, oferta ou gargalo e diz qual etapa da fábrica ela acelera, quanto
ganha, como testar de graça, o risco e um veredito com data. Usa config/mapa_processo.yaml como contexto.
Nunca compra nada e nunca mexe em conta de terceiros: só devolve um parecer em texto.

Uso:
    python agents/23_acelerador_processos/agent.py --entrada "texto sobre a ferramenta"
    python agents/23_acelerador_processos/agent.py --arquivo descricao.txt
    python agents/23_acelerador_processos/agent.py --entrada "..." --dry     # só mostra o prompt montado
O parecer é salvo em data/acelerador/ (pasta local, fora do que a fábrica publica).
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

MAPA = ROOT / "config" / "mapa_processo.yaml"
SAIDA = ROOT / "data" / "acelerador"


def montar_prompt(entrada: str) -> tuple[str, str]:
    sistema = (AGENT_DIR / "prompt.md").read_text(encoding="utf-8")
    mapa = yaml.safe_load(MAPA.read_text(encoding="utf-8"))
    mapa_txt = yaml.safe_dump(mapa, allow_unicode=True, sort_keys=False)
    prompt = f"MAPA DO PROCESSO:\n{mapa_txt}\n\nTEXTO A AVALIAR:\n{entrada.strip()}\n"
    return sistema, prompt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", help="texto com a descrição da ferramenta/oferta/gargalo")
    ap.add_argument("--arquivo", help="arquivo de texto com a descrição")
    ap.add_argument("--dry", action="store_true", help="só mostra o prompt, não chama o LLM")
    a = ap.parse_args()
    entrada = a.entrada or (Path(a.arquivo).read_text(encoding="utf-8") if a.arquivo else "")
    if not entrada.strip():
        print("informe --entrada ou --arquivo")
        return 2
    sistema, prompt = montar_prompt(entrada)
    if a.dry:
        print(sistema, "\n---\n", prompt)
        return 0
    from core.config import load_env_file
    from core.llm import LLMError, gerar_texto
    load_env_file()
    try:
        parecer = gerar_texto(prompt, sistema=sistema, temperatura=0.3, max_tokens=1500)
    except LLMError as exc:
        print("ERRO do LLM:", exc)
        return 1
    SAIDA.mkdir(parents=True, exist_ok=True)
    arq = SAIDA / f"{datetime.now():%Y%m%d_%H%M%S}.md"
    arq.write_text(parecer + "\n", encoding="utf-8")
    print(parecer)
    print(f"\n[salvo em {arq.relative_to(ROOT)}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
