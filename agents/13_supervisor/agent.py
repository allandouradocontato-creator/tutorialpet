"""Agente 13 — Supervisor de Otimização Contínua.

Monitora custo/tempo/eficiência de todo o pipeline lendo SÓ logs, saídas e configs dos
outros agentes (nunca importa ou reescreve a lógica deles) e age em dois níveis:

  Nível 1 — aplica sozinho: ajustes de parâmetro já existentes em config/*.yaml, dentro
  de limites pré-definidos em config/supervisor_limits.yaml, só quando há amostra
  suficiente. Toda ação vai para data/supervisor/log_acoes.jsonl e pode ser revertida.

  Nível 2 — só sugere: qualquer coisa que mudaria lógica/prompt.md de outro agente, ou
  trocaria uma API/ferramenta externa. Vira um arquivo em
  data/supervisor/sugestoes_pendentes/{id}.md, com gate de aprovação humana
  (aprovacao_supervisor) — nunca aplicado sozinho.

Uso:
    python agents/13_supervisor/agent.py --site pets-tutores-iniciantes
    python agents/13_supervisor/agent.py --rollback <id_da_acao>
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import CONFIG_DIR, load_env_file, load_yaml  # noqa: E402
from core.io import now_iso  # noqa: E402
from core.log import get_logger  # noqa: E402
from core.markdown import MarkdownError, read_markdown, write_markdown  # noqa: E402
import monitoring  # noqa: E402
from yaml_edit import YamlEditError, set_scalar  # noqa: E402

AGENT_NAME = "13_supervisor"
SCHEMA_VERSION = "1.0"

SUPERVISOR_DIR = ROOT / "data" / "supervisor"
LOG_ACOES_PATH = SUPERVISOR_DIR / "log_acoes.jsonl"
SUGESTOES_DIR = SUPERVISOR_DIR / "sugestoes_pendentes"

ADJUSTABLE_FILES = {
    "keyword_filters": CONFIG_DIR / "keyword_filters.yaml",
    "publishing_schedule": CONFIG_DIR / "publishing_schedule.yaml",
}


# --------------------------------------------------------------------------- log de ações (Nível 1)
def append_action_log(entry: dict) -> None:
    LOG_ACOES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_ACOES_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_action_log() -> list[dict]:
    if not LOG_ACOES_PATH.exists():
        return []
    entries = []
    for linha in LOG_ACOES_PATH.read_text(encoding="utf-8").splitlines():
        if linha.strip():
            entries.append(json.loads(linha))
    return entries


def apply_level1_adjustment(grupo: str, key_path: list[str], novo_valor, motivo: str, log) -> dict:
    path = ADJUSTABLE_FILES[grupo]
    valor_anterior = set_scalar(path, key_path, novo_valor)
    acao = {
        "id": uuid.uuid4().hex[:12], "timestamp": now_iso(), "nivel": 1, "tipo": "ajuste_parametro",
        "arquivo": str(path.relative_to(ROOT)), "caminho": key_path,
        "valor_anterior": valor_anterior, "valor_novo": novo_valor, "motivo": motivo, "revertivel": True,
    }
    append_action_log(acao)
    log.info(f"[{AGENT_NAME}] Nível 1 aplicado: {acao['arquivo']} {'.'.join(key_path)} "
              f"{valor_anterior} → {novo_valor} ({motivo})")
    return acao


def rollback_action(action_id: str, log) -> dict:
    entries = read_action_log()
    alvo = next((e for e in entries if e["id"] == action_id and e["tipo"] == "ajuste_parametro"), None)
    if not alvo:
        raise ValueError(f"ação '{action_id}' não encontrada (ou não é revertível) em {LOG_ACOES_PATH}")
    ja_revertida = any(e.get("ref_acao_id") == action_id for e in entries if e["tipo"] == "rollback")
    if ja_revertida:
        raise ValueError(f"ação '{action_id}' já foi revertida anteriormente — ver {LOG_ACOES_PATH}")

    path = ROOT / alvo["arquivo"]
    valor_restaurado = alvo["valor_anterior"]
    # o valor foi lido como string bruta do YAML original — tenta reconverter para número
    try:
        valor_restaurado_convertido = int(valor_restaurado) if "." not in str(valor_restaurado) else float(valor_restaurado)
    except (TypeError, ValueError):
        valor_restaurado_convertido = valor_restaurado
    set_scalar(path, alvo["caminho"], valor_restaurado_convertido)

    rollback_entry = {
        "id": uuid.uuid4().hex[:12], "timestamp": now_iso(), "nivel": 1, "tipo": "rollback",
        "ref_acao_id": action_id, "arquivo": alvo["arquivo"], "caminho": alvo["caminho"],
        "valor_restaurado": valor_restaurado_convertido,
    }
    append_action_log(rollback_entry)
    log.info(f"[{AGENT_NAME}] rollback de '{action_id}': {alvo['arquivo']} {'.'.join(alvo['caminho'])} "
              f"restaurado para {valor_restaurado_convertido}")
    return rollback_entry


# --------------------------------------------------------------------------- Nível 2 (sugestões)
def find_open_suggestion(titulo: str) -> Path | None:
    """Evita duplicar a mesma sugestão a cada execução periódica: só cria uma nova se não
    houver outra com o mesmo título ainda pendente (aprovada/rejeitada pode gerar de novo,
    caso a condição que a motivou ainda exista)."""
    if not SUGESTOES_DIR.exists():
        return None
    for path in SUGESTOES_DIR.glob("*.md"):
        try:
            front_matter, _ = read_markdown(path)
        except MarkdownError:
            continue
        if front_matter.get("titulo") == titulo and front_matter.get("status") == "pendente":
            return path
    return None


def write_suggestion(titulo: str, categoria: str, motivo: str, proposta: str) -> tuple[Path, bool]:
    existente = find_open_suggestion(titulo)
    if existente:
        return existente, False
    SUGESTOES_DIR.mkdir(parents=True, exist_ok=True)
    sugestao_id = uuid.uuid4().hex[:8]
    front_matter = {
        "id": sugestao_id, "titulo": titulo, "categoria": categoria, "gerado_em": now_iso(),
        "status": "pendente", "gate": "aprovacao_supervisor", "revisor": "", "decidido_em": "", "comentarios": "",
    }
    body = f"## Motivo\n\n{motivo}\n\n## Proposta\n\n{proposta}\n\n" \
           f"## Como decidir\n\nAltere `status` para `aprovado` ou `rejeitado` neste arquivo, preencha " \
           f"`revisor` e `decidido_em`. Isto nunca é aplicado automaticamente pelo agente 13.\n"
    path = write_markdown(SUGESTOES_DIR / f"{sugestao_id}.md", front_matter, body)
    return path, True


def evaluate_level2_suggestions(deps: list[dict], log) -> list[Path]:
    """Achados que exigem mudança de lógica/prompt.md ou de dependência externa — nunca
    aplicados sozinhos, sempre viram sugestão pendente. Não duplica uma sugestão que já
    esteja pendente de uma execução anterior (ver find_open_suggestion)."""
    novos = []
    google_ads = next((d for d in deps if d["dependencia"].startswith("Google Ads API")), None)
    if google_ads and not google_ads["configurada"]:
        path, is_new = write_suggestion(
            titulo="Ativar credenciais reais da Google Ads API para o agente 01",
            categoria="troca_dependencia_externa",
            motivo=(
                "O agente 01 está rodando permanentemente no fallback manual (CSV) porque as variáveis "
                f"{', '.join(google_ads['variaveis_faltando'])} não estão configuradas. Isso significa que "
                "os dados de volume/CPC usados até agora não vêm do Keyword Planner real, e nenhum ajuste "
                "de Nível 1 nos filtros de keyword deveria se basear neles."
            ),
            proposta=(
                "Seguir `config/platform_setup/google_ads_account.md` para obter as credenciais e "
                "preencher o `.env`. Depois de confirmado (`api=sim` no log do agente 01), reexecutar a "
                "pesquisa de palavras-chave com dados reais antes de aprovar qualquer pauta em produção."
            ),
        )
        if is_new:
            novos.append(path)
            log.info(f"[{AGENT_NAME}] Nível 2: sugestão criada em {path.relative_to(ROOT)}")
        else:
            log.info(f"[{AGENT_NAME}] Nível 2: sugestão já pendente, não duplicada ({path.relative_to(ROOT)})")
    return novos


# --------------------------------------------------------------------------- Nível 1 (avaliação)
def evaluate_level1_actions(n_pipeline_runs: int, gate_stats: dict, limits: dict, log) -> tuple[list[dict], list[str]]:
    """Retorna (ações aplicadas, motivos de não-aplicação) — nunca aplica fora dos limites
    nem com amostra abaixo do mínimo configurado."""
    aplicadas: list[dict] = []
    motivos: list[str] = []
    minimos = limits.get("amostras_minimas", {})

    minimo_execucoes = minimos.get("execucoes_pipeline_para_ajustar_cadencia", 5)
    if n_pipeline_runs < minimo_execucoes:
        motivos.append(f"Cadência de publicação (config/publishing_schedule.yaml): amostra insuficiente "
                        f"({n_pipeline_runs} rodada(s) completa(s) do orchestrator, mínimo configurado é "
                        f"{minimo_execucoes}) — nenhum ajuste aplicado.")

    minimo_gates = minimos.get("gates_para_estatistica_confiavel", 10)
    total_gate_decisions = sum(sum(v.values()) for v in gate_stats.values())
    if total_gate_decisions < minimo_gates:
        motivos.append(f"Parâmetros ligados a taxa de aprovação de gates: amostra insuficiente "
                        f"({total_gate_decisions} decisão(ões) de gate registrada(s), mínimo configurado é "
                        f"{minimo_gates}) — nenhum ajuste aplicado.")

    motivos.append("Filtros de keyword (config/keyword_filters.yaml): os dados de oportunidade usados até "
                    "agora vieram de um CSV preenchido manualmente como placeholder de teste (ver histórico "
                    "do projeto), não do Keyword Planner real — o supervisor não ajusta esses filtros com "
                    "base em dados sintéticos, independente do tamanho da amostra.")
    return aplicadas, motivos


# --------------------------------------------------------------------------- custo estimado
def estimate_cost(n_llm_calls: int, n_artigos: int) -> dict:
    """Nenhum agente faz chamada real de LLM hoje — custo real observado é sempre zero.
    Isto fica pronto para quando essa integração existir (ver config/supervisor_limits.yaml
    → model_routing)."""
    return {
        "chamadas_llm_registradas": n_llm_calls,
        "custo_estimado_total": 0.0,
        "custo_estimado_por_artigo": 0.0 if n_artigos else None,
        "nota": "Nenhum agente faz chamada real de LLM ainda (todos determinísticos) — custo real é R$ 0,00.",
    }


# --------------------------------------------------------------------------- relatório
def render_report(site_id: str, ctx: dict) -> str:
    L = [f"# Relatório do Supervisor — {site_id}", "", f"- **Gerado em:** {now_iso()}", ""]

    L += ["## 1. Execuções monitoradas", "",
          f"- Rodadas completas do orchestrator (data/runs/): **{ctx['n_pipeline_runs']}**",
          f"- Artigos aprovados pelo agente 04: **{ctx['qualidade']['aprovados']}**",
          f"- Artigos reprovados pelo agente 04: **{ctx['qualidade']['reprovados']}**", ""]
    L.append("### Invocações isoladas por agente (fora do orchestrator)")
    L.append("")
    if ctx["standalone"]:
        L += ["| Agente | Execuções isoladas |", "|---|---|"]
        L += [f"| {nome} | {n} |" for nome, n in sorted(ctx["standalone"].items())]
    else:
        L.append("Nenhuma.")
    L.append("")

    L += ["## 2. Tempo por agente", ""]
    if ctx["durations"]:
        L += ["| Agente | Execuções | Duração média |", "|---|---|---|"]
        for nome, valores in sorted(ctx["durations"].items()):
            media = sum(valores) / len(valores)
            L.append(f"| {nome} | {len(valores)} | {media:.2f}s |")
        L.append("")
        L.append("*Durações próximas de zero são esperadas: nenhum agente faz chamada real de LLM ou rede "
                  "hoje — todos são determinísticos. Este indicador ganha sentido real quando a integração "
                  "de LLM (ver `config/supervisor_limits.yaml` → `model_routing`) estiver ativa.*")
    else:
        L.append("Sem dados de duração ainda (nenhuma rodada completa do orchestrator).")
    L.append("")

    L += ["## 3. Taxa de aprovação/reprovação (gates)", ""]
    if ctx["gate_stats"]:
        L += ["| Gate | Aprovado | Simulado | Pendente | Rejeitado |", "|---|---|---|---|---|"]
        for gate_id, contagem in ctx["gate_stats"].items():
            L.append(f"| {gate_id} | {contagem.get('aprovado', 0)} | {contagem.get('simulado', 0)} | "
                      f"{contagem.get('pendente', 0)} | {contagem.get('rejeitado', 0)} |")
    else:
        L.append("Sem decisões de gate registradas ainda.")
    L.append("")

    L += ["## 4. Prontidão de compliance (agente 06) e risco de política (agente 10)", "",
          f"- Relatórios de prontidão gerados: **{len(ctx['compliance_reports'])}** "
          f"({sum(1 for r in ctx['compliance_reports'] if r['pronto'])} marcados 'pronto')",
          f"- Auditorias de política geradas: **{len(ctx['policy_audits'])}** "
          f"(risco mais recente: {ctx['policy_audits'][-1]['risco'] if ctx['policy_audits'] else 'n/d'})", ""]

    L += ["## 5. Dependências externas", "", "| Dependência | Configurada | Variáveis faltando |", "|---|---|---|"]
    for dep in ctx["dependencies"]:
        status = "✅" if dep["configurada"] else "⛔"
        faltando = ", ".join(dep["variaveis_faltando"]) or "—"
        L.append(f"| {dep['dependencia']} | {status} | {faltando} |")
    L += ["", "*Nenhuma quota numérica é citada aqui porque nenhuma credencial real está configurada ainda "
          "neste projeto — consulte a documentação oficial do respectivo serviço ao ativar cada uma.*", ""]

    custo = ctx["custo"]
    L += ["## 6. Custo estimado", "",
          f"- Chamadas de LLM registradas nos logs: **{custo['chamadas_llm_registradas']}**",
          f"- Custo estimado total: **R$ {custo['custo_estimado_total']:.2f}**",
          f"- {custo['nota']}", ""]

    L += ["## 7. Ações de Nível 1 (aplicadas automaticamente)", ""]
    if ctx["acoes_nivel1"]:
        for acao in ctx["acoes_nivel1"]:
            L.append(f"- `{acao['arquivo']}` → `{'.'.join(acao['caminho'])}`: {acao['valor_anterior']} → "
                      f"{acao['valor_novo']} (id `{acao['id']}`, motivo: {acao['motivo']})")
    else:
        L.append("Nenhuma ação aplicada nesta rodada. Motivos:")
        L += [f"  - {m}" for m in ctx["motivos_nivel1"]]
    L.append("")

    L += ["## 8. Sugestões de Nível 2 (aguardando aprovação humana)", ""]
    pendentes = list(SUGESTOES_DIR.glob("*.md")) if SUGESTOES_DIR.exists() else []
    if pendentes:
        for path in sorted(pendentes):
            L.append(f"- `{path.relative_to(ROOT)}` — gate `aprovacao_supervisor`")
    else:
        L.append("Nenhuma sugestão pendente no momento.")
    L.append("")

    L += ["## Como reverter uma ação de Nível 1", "",
          "```", "python agents/13_supervisor/agent.py --rollback <id>", "```",
          f"O histórico completo (aplicações e reversões) fica em `{LOG_ACOES_PATH.relative_to(ROOT)}` — "
          "nada é apagado, um rollback só registra uma nova entrada revertendo o valor."]
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- entrypoint
def run(context: dict) -> dict:
    log = context["logger"]
    site_id = context["site_id"]

    runs = monitoring.scan_pipeline_runs()
    gate_stats = monitoring.compute_gate_stats(runs)
    durations = monitoring.compute_agent_durations(runs)
    qualidade = monitoring.count_quality_editor_outcomes()
    compliance_reports = monitoring.scan_compliance_reports()
    policy_audits = monitoring.scan_policy_audits()
    standalone = monitoring.count_standalone_invocations()
    log_levels = monitoring.count_log_levels()
    dependencies = monitoring.check_external_dependencies()
    custo = estimate_cost(n_llm_calls=0, n_artigos=qualidade["aprovados"])

    limits = load_yaml(CONFIG_DIR / "supervisor_limits.yaml")
    acoes_nivel1, motivos_nivel1 = evaluate_level1_actions(len(runs), gate_stats, limits, log)
    sugestoes_geradas = evaluate_level2_suggestions(dependencies, log)

    ctx = {
        "n_pipeline_runs": len(runs), "gate_stats": gate_stats, "durations": durations,
        "qualidade": qualidade, "compliance_reports": compliance_reports, "policy_audits": policy_audits,
        "standalone": standalone, "log_levels": log_levels, "dependencies": dependencies, "custo": custo,
        "acoes_nivel1": acoes_nivel1, "motivos_nivel1": motivos_nivel1,
    }
    relatorio_md = render_report(site_id, ctx)
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = SUPERVISOR_DIR / f"relatorio_{date_str}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(relatorio_md, encoding="utf-8")
    LOG_ACOES_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_ACOES_PATH.touch(exist_ok=True)

    pendencias = list(motivos_nivel1)
    if sugestoes_geradas:
        pendencias.append(f"{len(sugestoes_geradas)} nova(s) sugestão(ões) de Nível 2 aguardando aprovação "
                           f"(gate 'aprovacao_supervisor') em {SUGESTOES_DIR.relative_to(ROOT)}.")

    output = {
        "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "site_id": site_id, "gerado_em": now_iso(),
        "status": "ok", "n_pipeline_runs": len(runs), "n_acoes_nivel1_aplicadas": len(acoes_nivel1),
        "n_sugestoes_nivel2_geradas": len(sugestoes_geradas), "relatorio": str(out_path.relative_to(ROOT)),
        "pendencias_humanas": pendencias,
    }
    log.info(f"[{AGENT_NAME}] rodadas={len(runs)} nivel1_aplicadas={len(acoes_nivel1)} "
              f"nivel2_novas={len(sugestoes_geradas)} → {out_path.relative_to(ROOT)}")
    return output


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 13 — supervisor de otimização contínua")
    parser.add_argument("--site", help="site_id (arquivo em config/sites/)")
    parser.add_argument("--rollback", metavar="ID", help="reverte uma ação de Nível 1 pelo id em log_acoes.jsonl")
    args = parser.parse_args()

    load_env_file()
    run_id = f"{now_iso().replace(':', '').replace('+0000', 'Z')}-{AGENT_NAME}"
    log = get_logger(run_id)

    if args.rollback:
        try:
            entry = rollback_action(args.rollback, log)
        except ValueError as ex:
            log.error(f"[{AGENT_NAME}] {ex}")
            print(f"Erro: {ex}")
            return 2
        print(f"Revertido: {entry['arquivo']} {'.'.join(entry['caminho'])} → {entry['valor_restaurado']}")
        return 0

    if not args.site:
        parser.error("--site é obrigatório (ou use --rollback <id>)")
    output = run({"site_id": args.site, "logger": log})
    return 0 if output["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
