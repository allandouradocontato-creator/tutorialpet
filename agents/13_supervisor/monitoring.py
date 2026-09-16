"""Coleta de métricas do agente 13 — lê apenas logs/configs/saídas de outros agentes
(nunca importa o código deles), consistente com a regra de nunca reescrever a lógica de
outro agente diretamente.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNS_DIR = ROOT / "data" / "runs"
LOGS_DIR = ROOT / "logs"
QUALITY_DIR = ROOT / "data" / "quality_editor"
COMPLIANCE_DIR = ROOT / "data" / "platform_compliance"
GUARDIAN_DIR = ROOT / "data" / "policy_guardian"

AGENT_NAMES = [
    "01_niche_research", "02_trend_hunter", "03_content_writer", "04_quality_editor",
    "05_seo_onpage", "06_platform_compliance", "07_publisher", "08_analytics",
    "09_monetization", "10_policy_guardian",
]

EXTERNAL_DEPENDENCIES = {
    "Google Ads API (agente 01)": ["GOOGLE_ADS_DEVELOPER_TOKEN", "GOOGLE_ADS_CLIENT_ID",
                                    "GOOGLE_ADS_CLIENT_SECRET", "GOOGLE_ADS_REFRESH_TOKEN",
                                    "GOOGLE_ADS_LOGIN_CUSTOMER_ID"],
    "LLM — Anthropic (uso futuro nos agentes 02-05, 10)": ["ANTHROPIC_API_KEY"],
    "LLM — OpenAI (uso futuro nos agentes 02-05, 10)": ["OPENAI_API_KEY"],
    "WordPress REST API (agente 07, modo real desligado)": ["WP_BASE_URL", "WP_USERNAME", "WP_APP_PASSWORD"],
    "Ghost Admin API (agente 07, modo real desligado)": ["GHOST_ADMIN_API_URL", "GHOST_ADMIN_API_KEY"],
    "Google Search Console / GA4 (agente 08)": ["GOOGLE_APPLICATION_CREDENTIALS"],
}


def read_json_safe(path: Path) -> dict | None:
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None


# --------------------------------------------------------------------------- rodadas do orchestrator
def scan_pipeline_runs() -> list[dict]:
    if not RUNS_DIR.exists():
        return []
    runs = []
    for run_dir in sorted(RUNS_DIR.iterdir()):
        state = read_json_safe(run_dir / "state.json")
        if state:
            runs.append(state)
    return runs


def compute_gate_stats(runs: list[dict]) -> dict[str, dict[str, int]]:
    stats: dict[str, dict[str, int]] = {}
    for run in runs:
        for gate_id, status in (run.get("gates") or {}).items():
            stats.setdefault(gate_id, {}).setdefault(status, 0)
            stats[gate_id][status] += 1
    return stats


def compute_agent_durations(runs: list[dict]) -> dict[str, list[float]]:
    """Duração em segundos por agente, a partir de iniciado_em/finalizado_em. Como nenhum
    agente hoje faz chamada real de LLM/rede, espere valores muito próximos de zero."""
    durations: dict[str, list[float]] = {}
    for run in runs:
        for agent_name, etapa in (run.get("etapas") or {}).items():
            try:
                inicio = datetime.fromisoformat(etapa["iniciado_em"])
                fim = datetime.fromisoformat(etapa["finalizado_em"])
            except (KeyError, ValueError):
                continue
            durations.setdefault(agent_name, []).append((fim - inicio).total_seconds())
    return durations


# --------------------------------------------------------------------------- agente 04 (qualidade)
def count_quality_editor_outcomes() -> dict[str, int]:
    aprovados = len(list((QUALITY_DIR / "aprovados").glob("*.md"))) if (QUALITY_DIR / "aprovados").exists() else 0
    reprovados = len(list((QUALITY_DIR / "reprovados").glob("*.md"))) if (QUALITY_DIR / "reprovados").exists() else 0
    return {"aprovados": aprovados, "reprovados": reprovados}


# --------------------------------------------------------------------------- agentes 06/10 (pendências)
STATUS_LINE_RE = re.compile(r"\*\*Status:\*\*\s*(.+)")
RISCO_LINE_RE = re.compile(r"\*\*Risco geral:\*\*\s*(\S+)")


def scan_compliance_reports() -> list[dict]:
    if not COMPLIANCE_DIR.exists():
        return []
    resultado = []
    for path in sorted(COMPLIANCE_DIR.glob("relatorio_prontidao_*.md")):
        texto = path.read_text(encoding="utf-8")
        m = STATUS_LINE_RE.search(texto)
        pronto = bool(m and "PRONTO" in m.group(1).upper())
        resultado.append({"arquivo": str(path.relative_to(ROOT)), "pronto": pronto})
    return resultado


def scan_policy_audits() -> list[dict]:
    if not GUARDIAN_DIR.exists():
        return []
    resultado = []
    for path in sorted(GUARDIAN_DIR.glob("auditoria_*.md")):
        texto = path.read_text(encoding="utf-8")
        m = RISCO_LINE_RE.search(texto)
        risco = m.group(1).upper() if m else "DESCONHECIDO"
        resultado.append({"arquivo": str(path.relative_to(ROOT)), "risco": risco})
    return resultado


# --------------------------------------------------------------------------- invocações isoladas (fora do orchestrator)
def count_standalone_invocations() -> dict[str, int]:
    if not LOGS_DIR.exists():
        return {}
    contagem: dict[str, int] = {}
    for path in LOGS_DIR.glob("*.jsonl"):
        for name in AGENT_NAMES:
            if path.stem.endswith(f"-{name}"):
                contagem[name] = contagem.get(name, 0) + 1
                break
    return contagem


def count_log_levels() -> dict[str, int]:
    """Conta linhas WARNING/ERROR em todos os logs .jsonl — sinal simples de saúde geral."""
    contagem = {"WARNING": 0, "ERROR": 0}
    if not LOGS_DIR.exists():
        return contagem
    for path in LOGS_DIR.glob("*.jsonl"):
        for linha in path.read_text(encoding="utf-8").splitlines():
            try:
                entrada = json.loads(linha)
            except json.JSONDecodeError:
                continue
            if entrada.get("level") in contagem:
                contagem[entrada["level"]] += 1
    return contagem


# --------------------------------------------------------------------------- dependências externas
def check_external_dependencies() -> list[dict]:
    import os
    resultado = []
    for nome, variaveis in EXTERNAL_DEPENDENCIES.items():
        configuradas = [v for v in variaveis if os.environ.get(v, "").strip()]
        resultado.append({
            "dependencia": nome, "configurada": len(configuradas) == len(variaveis),
            "variaveis_faltando": [v for v in variaveis if v not in configuradas],
        })
    return resultado
