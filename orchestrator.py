#!/usr/bin/env python
"""Orquestrador do blog-factory: roda os agentes 01 → 07 para um site/pauta.

Contrato de cada agente (agents/NN_nome/agent.py):
    run(context: dict) -> dict   # o dict retornado precisa ter "status"
    - context["input"]   = output do agente anterior (None para o 01)
    - context["outputs"] = {agente: caminho do output JSON} das etapas já concluídas
    - context["dry_run"] = True → nada pode ser publicado/enviado de verdade

Status que permitem seguir: "ok". Qualquer outro pausa a rodada, que pode ser retomada
com --resume <run_id> depois que o humano resolver a pendência.

Exemplos:
    python orchestrator.py --site pets-tutores-iniciantes --pauta "como cortar unha de cachorro" --dry-run
    python orchestrator.py --resume 20260915T120000Z-pets-tutores-iniciantes
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core.config import load_env_file, load_site  # noqa: E402
from core.io import now_iso, read_json, slugify, write_json  # noqa: E402
from core.log import get_logger  # noqa: E402

PIPELINE = [
    "01_niche_research",
    "02_trend_hunter",
    "03_content_writer",
    "04_quality_editor",
    "05_seo_onpage",
    "06_platform_compliance",
    "07_publisher",
]

# Gates humanos verificados ANTES do agente indicado.
GATES = {
    "03_content_writer": {
        "id": "aprovacao_pauta",
        "descricao": "Aprovar a pauta (termo, ângulo, cluster) antes de gastar produção de conteúdo.",
    },
    "07_publisher": {
        "id": "aprovacao_publicacao",
        "descricao": "Aprovação final do artigo revisado, com SEO e compliance, antes de publicar.",
    },
}
# A aprovação de candidatura ao AdSense é um gate separado, fora deste pipeline (agentes 09/10).

EXIT_OK, EXIT_ERROR, EXIT_PAUSED = 0, 1, 2


def load_agent(name: str):
    path = ROOT / "agents" / name / "agent.py"
    spec = importlib.util.spec_from_file_location(f"agent_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not callable(getattr(module, "run", None)):
        raise AttributeError(f"{path} não define run(context)")
    return module


def check_gate(gate: dict, run_dir: Path, state: dict, log, simulate: bool, select_from: list[dict] | None = None) -> tuple[str, dict | None]:
    """Retorna (status, pauta_selecionada). status é 'aprovado', 'simulado', 'pendente' ou 'rejeitado'.

    `select_from` é a lista de pautas candidatas (saída do agente 02) quando este gate exige
    escolher uma delas (gate 'aprovacao_pauta'); None para gates que não fazem essa escolha.
    """
    path = run_dir / "approvals" / f"{gate['id']}.json"
    if simulate:
        selected = select_from[0] if select_from else None
        if selected:
            log.warning(f"[gate:{gate['id']}] SIMULADO (dry-run) — pauta escolhida automaticamente: "
                        f"#{selected.get('id')} \"{selected.get('titulo')}\"")
        else:
            log.warning(f"[gate:{gate['id']}] SIMULADO (dry-run) — nenhuma aprovação real registrada")
        return "simulado", selected
    if not path.exists():
        last_step = next((s for s in reversed(list(state["etapas"].values())) if s.get("output")), {})
        payload = {
            "gate": gate["id"],
            "descricao": gate["descricao"],
            "revisar": last_step.get("output"),
            "status": "pendente",
            "revisor": "",
            "decidido_em": "",
            "comentarios": "",
            "instrucoes": "Altere status para 'aprovado' ou 'rejeitado', preencha revisor e decidido_em, e rode com --resume.",
        }
        if select_from is not None:
            payload["pautas_disponiveis"] = [
                {"id": p.get("id"), "titulo": p.get("titulo"), "prioridade": p.get("prioridade"),
                 "score_prioridade": p.get("score_prioridade"), "termo_origem": p.get("termo_origem")}
                for p in select_from
            ]
            payload["pauta_id_selecionada"] = ""
            payload["instrucoes"] += " Preencha 'pauta_id_selecionada' com o campo 'id' de uma das 'pautas_disponiveis'."
        write_json(path, payload)
        log.warning(f"[gate:{gate['id']}] aguardando decisão humana em {path.relative_to(ROOT)}")
        return "pendente", None
    decision = read_json(path)
    status = decision.get("status")
    if status == "aprovado" and not decision.get("revisor", "").strip():
        log.warning(f"[gate:{gate['id']}] marcado como aprovado sem 'revisor' — tratado como pendente")
        return "pendente", None
    selected = None
    if status == "aprovado" and select_from is not None:
        wanted = decision.get("pauta_id_selecionada")
        selected = next((p for p in select_from if str(p.get("id")) == str(wanted)), None) if wanted not in (None, "") else None
        if not selected:
            log.warning(f"[gate:{gate['id']}] 'pauta_id_selecionada' ausente ou inválida ({wanted!r}) — tratado como pendente")
            return "pendente", None
    if status in ("aprovado", "rejeitado"):
        log.info(f"[gate:{gate['id']}] {status} por {decision.get('revisor')}: {decision.get('comentarios', '')}")
        return status, selected
    return "pendente", None


def print_summary(state: dict) -> None:
    print(f"\nRodada {state['run_id']} | site={state['site_id']} | dry_run={state['dry_run']}")
    for name in PIPELINE:
        step = state["etapas"].get(name)
        if step:
            print(f"  {name:<24} {step['status']}")
    for gate_id, status in state.get("gates", {}).items():
        print(f"  gate {gate_id:<19} {status}")


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Pipeline blog-factory (agentes 01–07)")
    parser.add_argument("--site", help="site_id em config/sites/")
    parser.add_argument("--pauta", help="pauta/termo específico desta rodada")
    parser.add_argument("--dry-run", action="store_true", help="simula tudo; nada é publicado")
    parser.add_argument("--respeitar-gates", action="store_true", help="no dry-run, exigir aprovações reais nos gates")
    parser.add_argument("--aceitar-parcial", action="store_true", help="agente 01 segue com dados de keyword incompletos")
    parser.add_argument("--resume", metavar="RUN_ID", help="retomar uma rodada pausada")
    parser.add_argument("--ate", choices=PIPELINE, default=PIPELINE[-1], help="último agente a executar")
    args = parser.parse_args()
    load_env_file()

    if args.resume:
        run_dir = ROOT / "data" / "runs" / args.resume
        if not (run_dir / "state.json").exists():
            parser.error(f"rodada não encontrada: {args.resume}")
        state = read_json(run_dir / "state.json")
    else:
        if not args.site:
            parser.error("--site é obrigatório (ou use --resume)")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_id = f"{stamp}-{slugify(args.site)}" + (f"-{slugify(args.pauta)[:40]}" if args.pauta else "")
        run_dir = ROOT / "data" / "runs" / run_id
        state = {
            "run_id": run_id, "site_id": args.site, "pauta": args.pauta, "dry_run": args.dry_run,
            "respeitar_gates": args.respeitar_gates, "criado_em": now_iso(), "etapas": {}, "gates": {},
        }
    # Modo da rodada é fixado na criação: uma rodada dry-run nunca vira publicação real no resume.
    dry_run = state["dry_run"]
    log = get_logger(state["run_id"])
    site = load_site(state["site_id"])
    log.info(f"Rodada {state['run_id']} {'retomada' if args.resume else 'iniciada'} | dry_run={dry_run} | pauta={state['pauta']!r}")

    previous_output, outputs = None, {}
    for name in PIPELINE[: PIPELINE.index(args.ate) + 1]:
        step = state["etapas"].get(name)
        if step and step["status"] == "ok":
            previous_output = read_json(ROOT / step["output"])
            outputs[name] = step["output"]
            log.info(f"[{name}] já concluído nesta rodada — reutilizando output")
            continue

        gate = GATES.get(name)
        if gate:
            if state["gates"].get(gate["id"]) not in ("aprovado", "simulado"):
                select_from = previous_output.get("pautas") if (gate["id"] == "aprovacao_pauta" and previous_output) else None
                decision, selected = check_gate(gate, run_dir, state, log,
                                                 simulate=dry_run and not state.get("respeitar_gates"),
                                                 select_from=select_from)
                state["gates"][gate["id"]] = decision
                if selected is not None:
                    state.setdefault("gates_selecao", {})[gate["id"]] = selected
                write_json(run_dir / "state.json", state)
                if decision in ("pendente", "rejeitado"):
                    print_summary(state)
                    print(f"\nPipeline pausado no gate '{gate['id']}' ({decision}). Retome com: "
                          f"python orchestrator.py --resume {state['run_id']}")
                    return EXIT_PAUSED

        log.info(f"[{name}] iniciando")
        started = now_iso()
        context = {
            "run_id": state["run_id"], "run_dir": run_dir, "site_id": state["site_id"], "site": site,
            "pauta": state["pauta"], "dry_run": dry_run, "aceitar_parcial": args.aceitar_parcial,
            "input": previous_output, "outputs": dict(outputs), "logger": log,
            "pauta_selecionada": state.get("gates_selecao", {}).get("aprovacao_pauta"),
        }
        try:
            output = load_agent(name).run(context)
        except Exception as ex:  # um agente com falha não pode derrubar o registro da rodada
            log.exception(f"[{name}] exceção não tratada")
            output = {"agent": name, "status": "error", "erro": repr(ex), "traceback": traceback.format_exc()}

        out_path = run_dir / f"{name}.output.json"
        write_json(out_path, output)
        rel = str(out_path.relative_to(ROOT))
        state["etapas"][name] = {"status": output.get("status", "error"), "output": rel, "iniciado_em": started, "finalizado_em": now_iso()}
        write_json(run_dir / "state.json", state)

        if output.get("status") != "ok":
            log.warning(f"[{name}] status={output.get('status')} — pipeline pausado")
            for action in output.get("pendencias_humanas", []) or [output.get("mensagem", "")]:
                if action:
                    log.warning(f"[{name}] pendência: {action}")
            print_summary(state)
            print(f"\nRetome com: python orchestrator.py --resume {state['run_id']}")
            return EXIT_ERROR if output.get("status") == "error" else EXIT_PAUSED

        log.info(f"[{name}] ok → {rel}")
        previous_output, outputs[name] = output, rel

    log.info("Pipeline concluído")
    print_summary(state)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
