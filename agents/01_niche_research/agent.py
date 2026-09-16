"""Agente 01 — Niche Research.

Busca volume de busca e CPC reais por palavra-chave (Google Ads API) e calcula um
score de oportunidade. Sem credenciais, gera data/keyword_research/manual_todo.csv
para o operador preencher com dados do Keyword Planner e reimporta o que já foi
preenchido.

Uso isolado:
    python agents/01_niche_research/agent.py --site pets-tutores-iniciantes
"""
from __future__ import annotations

import argparse
import csv
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_env_file, load_keyword_filters, load_site  # noqa: E402
from core.io import normalize_term, now_iso, strip_accents, write_json  # noqa: E402
from core.log import get_logger  # noqa: E402
from keyword_client import KeywordPlannerClient, KeywordResearchError, credentials_status  # noqa: E402

AGENT_NAME = "01_niche_research"
SCHEMA_VERSION = "1.0"
RESEARCH_DIR = ROOT / "data" / "keyword_research"
MANUAL_TODO = RESEARCH_DIR / "manual_todo.csv"
MANUAL_COLUMNS = ["site_id", "pilar", "termo", "volume_mensal", "cpc_medio", "concorrencia", "observacoes"]
COMPETITION_ALIASES = {
    "baixa": "BAIXA", "low": "BAIXA",
    "media": "MEDIA", "medium": "MEDIA",
    "alta": "ALTA", "high": "ALTA",
}


# --------------------------------------------------------------------------- parsing
def normalize_competition(value) -> str:
    return COMPETITION_ALIASES.get(normalize_term(value or ""), "DESCONHECIDA")


def _parse_number(token: str, integer: bool) -> float:
    t = strip_accents(token).lower().replace("r$", "").strip()
    multiplier = 1
    for suffix, mult in (("mil", 1_000), ("mi", 1_000_000), ("k", 1_000)):
        if t.endswith(suffix):
            multiplier, t = mult, t[: -len(suffix)].strip()
            break
    t = t.replace(" ", "")
    if "," in t and "." in t:
        t = t.replace(".", "").replace(",", ".")
    elif "," in t:
        t = t.replace(",", ".")
    elif integer and re.fullmatch(r"\d{1,3}(\.\d{3})+", t):
        t = t.replace(".", "")
    try:
        return float(t) * multiplier
    except ValueError:
        raise ValueError(f"valor não numérico: '{token}'") from None


def _split_range(text: str) -> list[str]:
    return [p for p in re.split(r"\s*(?:–|—|-|\ba\b)\s*", strip_accents(str(text)).strip()) if p]


def parse_volume(text: str) -> tuple[int, bool]:
    """'1 mil – 10 mil' -> (1000, True). Faixas usam o limite inferior (conservador)."""
    values = [_parse_number(p, integer=True) for p in _split_range(text)]
    if not values:
        raise ValueError("volume vazio")
    return int(min(values)), len(values) > 1


def parse_cpc(text: str) -> float:
    """'R$ 0,80 - R$ 2,10' -> 1.45 (média entre lance baixo e alto)."""
    values = [_parse_number(p, integer=False) for p in _split_range(text)]
    return round(sum(values) / len(values), 2) if values else 0.0


# --------------------------------------------------------------------------- scoring
def opportunity_score(volume: int, cpc: float, competition: str, cfg: dict) -> float:
    s = cfg["score"]
    vol_score = min(math.log10(volume + 1) / math.log10(s["volume_referencia"] + 1), 1.0) if volume > 0 else 0.0
    cpc_score = min(cpc / s["cpc_referencia"], 1.0) if cpc > 0 else 0.0
    factor = s["fator_concorrencia"].get(competition, s["fator_concorrencia"]["DESCONHECIDA"])
    return round(100 * (s["peso_volume"] * vol_score + s["peso_cpc"] * cpc_score) * factor, 1)


def rejection_reasons(item: dict, cfg: dict) -> list[str]:
    reasons = []
    if item["volume_mensal"] < cfg["volume_mensal_minimo"]:
        reasons.append(f"volume {item['volume_mensal']} < {cfg['volume_mensal_minimo']}")
    if item["cpc_medio"] < cfg["cpc_medio_minimo"]:
        reasons.append(f"CPC {item['cpc_medio']:.2f} < {cfg['cpc_medio_minimo']:.2f}")
    if item["concorrencia"] not in cfg["concorrencia_aceita"]:
        reasons.append(f"concorrência {item['concorrencia']} não aceita")
    term = normalize_term(item["termo"])
    for blocked in cfg.get("excluir_contendo") or []:
        if normalize_term(blocked) in term:
            reasons.append(f"contém termo excluído '{blocked}'")
    return reasons


# --------------------------------------------------------------------------- seeds
def collect_seeds(site: dict, pauta: str | None) -> list[dict]:
    seeds = [
        {"termo": s["termo"], "pilar": s["pilar"], "sensivel": bool(s.get("sensivel"))}
        for s in site["termos_semente"]
    ]
    if pauta and normalize_term(pauta) not in {normalize_term(s["termo"]) for s in seeds}:
        seeds.append({"termo": pauta, "pilar": "pauta_especifica", "sensivel": False})
    return seeds


def is_sensitive(term: str, site: dict, seed_flags: dict[str, bool]) -> bool:
    key = normalize_term(term)
    if seed_flags.get(key):
        return True
    return any(normalize_term(signal) in key for signal in site.get("sinais_ymyl") or [])


# --------------------------------------------------------------------------- API path
def research_via_api(site: dict, seeds: list[dict], cfg: dict, log) -> list[dict]:
    ads = site["google_ads"]
    client = KeywordPlannerClient(ads["language_constant_id"], ads["geo_target_constant_ids"])
    seed_keys = {normalize_term(s["termo"]) for s in seeds}
    by_pilar: dict[str, list[str]] = defaultdict(list)
    for s in seeds:
        by_pilar[s["pilar"]].append(s["termo"])

    rows, seen = [], set()
    for pilar, terms in by_pilar.items():
        log.info(f"[{AGENT_NAME}] Google Ads API: pilar '{pilar}' com {len(terms)} sementes")
        ideas = client.generate_keyword_ideas(terms)
        ideas.sort(key=lambda i: i["volume_mensal"], reverse=True)
        kept = 0
        for idea in ideas:
            key = normalize_term(idea["termo"])
            if key in seen:
                continue
            is_seed = key in seed_keys
            if not is_seed and kept >= cfg["max_ideias_por_pilar"]:
                continue
            seen.add(key)
            kept += 0 if is_seed else 1
            rows.append({**idea, "pilar": pilar, "fonte": "google_ads_api", "semente": is_seed, "volume_em_faixa": False})
        log.info(f"[{AGENT_NAME}]   {len(ideas)} ideias recebidas, {kept} mantidas além das sementes")
    return rows


# --------------------------------------------------------------------------- manual path
class SemicolonDialect(csv.excel):
    delimiter = ";"


def read_manual_csv() -> list[dict]:
    if not MANUAL_TODO.exists():
        return []
    with MANUAL_TODO.open(encoding="utf-8-sig", newline="") as fh:
        sample = fh.read(4096)
        fh.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=";,\t")
        except csv.Error:
            dialect = SemicolonDialect
        return [dict(r) for r in csv.DictReader(fh, dialect=dialect)]


def sync_manual_todo(site_id: str, seeds: list[dict]) -> list[dict]:
    """(Re)gera o CSV preservando valores já preenchidos, linhas extras e linhas de outros sites."""
    existing = read_manual_csv()
    other_sites = [r for r in existing if (r.get("site_id") or "").strip() != site_id]
    mine = {normalize_term(r.get("termo", "")): r for r in existing if (r.get("site_id") or "").strip() == site_id}

    rows, seed_keys = [], set()
    for s in seeds:
        key = normalize_term(s["termo"])
        seed_keys.add(key)
        prev = mine.get(key, {})
        rows.append({
            "site_id": site_id, "pilar": s["pilar"], "termo": s["termo"],
            **{c: (prev.get(c) or "").strip() for c in ("volume_mensal", "cpc_medio", "concorrencia", "observacoes")},
        })
    # Ideias adicionais que o operador colou do Keyword Planner
    rows += [{c: (r.get(c) or "").strip() for c in MANUAL_COLUMNS} for k, r in mine.items() if k and k not in seed_keys]

    MANUAL_TODO.parent.mkdir(parents=True, exist_ok=True)
    with MANUAL_TODO.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=MANUAL_COLUMNS, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(other_sites + rows)
    return rows


def parse_manual_rows(rows: list[dict], seed_keys: set[str]) -> tuple[list[dict], list[dict], list[dict]]:
    parsed, pending, invalid = [], [], []
    for r in rows:
        if not r["volume_mensal"]:
            pending.append({"termo": r["termo"], "pilar": r["pilar"]})
            continue
        try:
            volume, in_range = parse_volume(r["volume_mensal"])
            cpc = parse_cpc(r["cpc_medio"]) if r["cpc_medio"] else 0.0
        except ValueError as ex:
            invalid.append({"termo": r["termo"], "pilar": r["pilar"], "erro": str(ex)})
            continue
        parsed.append({
            "termo": r["termo"], "volume_mensal": volume, "cpc_medio": cpc,
            "concorrencia": normalize_competition(r["concorrencia"]), "pilar": r["pilar"] or "extra",
            "fonte": "keyword_planner_manual", "semente": normalize_term(r["termo"]) in seed_keys,
            "volume_em_faixa": in_range,
        })
    return parsed, pending, invalid


# --------------------------------------------------------------------------- output
def finalize(rows: list[dict], site: dict, seeds: list[dict], cfg: dict) -> tuple[list[dict], list[dict]]:
    seed_flags = {normalize_term(s["termo"]): s["sensivel"] for s in seeds}
    approved, rejected = [], []
    for r in rows:
        item = {
            "termo": r["termo"],
            "volume_mensal": int(r["volume_mensal"]),
            "cpc_medio": float(r["cpc_medio"]),
            "concorrencia": r["concorrencia"],
            "score_oportunidade": opportunity_score(int(r["volume_mensal"]), float(r["cpc_medio"]), r["concorrencia"], cfg),
            "pilar": r["pilar"],
            "fonte": r["fonte"],
            "semente": r["semente"],
            "sensivel_ymyl": is_sensitive(r["termo"], site, seed_flags),
            "volume_em_faixa": r.get("volume_em_faixa", False),
        }
        reasons = rejection_reasons(item, cfg)
        (rejected if reasons else approved).append({**item, "motivos_descarte": reasons} if reasons else item)
    approved.sort(key=lambda i: i["score_oportunidade"], reverse=True)
    rejected.sort(key=lambda i: i["score_oportunidade"], reverse=True)
    return approved, rejected


def render_report(out: dict, site: dict) -> str:
    pilares = site.get("pilares", {})
    L = [
        f"# Relatório de oportunidade — {site['site_id']}",
        "",
        f"- **Nicho:** {site['nicho']}",
        f"- **Gerado em:** {out['gerado_em']}",
        f"- **Status:** `{out['status']}`",
        f"- **Fonte de dados:** {out['fonte_dados']}",
        f"- **Google Ads API:** {out['credenciais']['motivo']}",
        f"- **Filtros:** volume ≥ {out['filtros_aplicados']['volume_mensal_minimo']}, "
        f"CPC ≥ {out['filtros_aplicados']['cpc_medio_minimo']:.2f}, "
        f"concorrência ∈ {out['filtros_aplicados']['concorrencia_aceita']}",
        "",
        "## Resumo",
        "",
        f"| Termos-semente | Termos com métricas | Aprovados no filtro | Descartados | Pendentes de dados | Inválidos |",
        f"|---|---|---|---|---|---|",
        f"| {out['resumo']['termos_semente']} | {out['resumo']['termos_com_metricas']} | {out['resumo']['aprovados']} "
        f"| {out['resumo']['descartados']} | {out['resumo']['pendentes']} | {out['resumo']['invalidos']} |",
        "",
    ]
    if out["oportunidades"]:
        L += ["## Oportunidades (ordenadas por score)", "",
              "| # | Termo | Pilar | Volume/mês | CPC médio | Concorrência | Score | YMYL |", "|---|---|---|---|---|---|---|---|"]
        for i, o in enumerate(out["oportunidades"], 1):
            vol = f"≥{o['volume_mensal']}" if o["volume_em_faixa"] else str(o["volume_mensal"])
            L.append(f"| {i} | {o['termo']} | {pilares.get(o['pilar'], o['pilar'])} | {vol} | {o['cpc_medio']:.2f} "
                     f"| {o['concorrencia']} | **{o['score_oportunidade']}** | {'⚠️' if o['sensivel_ymyl'] else ''} |")
        L.append("")
    if out["descartados"]:
        L += ["## Descartados pelo filtro", "", "| Termo | Score | Motivos |", "|---|---|---|"]
        L += [f"| {d['termo']} | {d['score_oportunidade']} | {'; '.join(d['motivos_descarte'])} |" for d in out["descartados"]]
        L.append("")
    if out["pendentes"]:
        L += ["## Termos aguardando pesquisa manual", "", "| # | Pilar | Termo-semente | YMYL |", "|---|---|---|---|"]
        seed_flags = {normalize_term(s["termo"]): s.get("sensivel") for s in site["termos_semente"]}
        for i, p in enumerate(out["pendentes"], 1):
            flag = "⚠️" if is_sensitive(p["termo"], site, seed_flags) else ""
            L.append(f"| {i} | {pilares.get(p['pilar'], p['pilar'])} | {p['termo']} | {flag} |")
        L.append("")
    if out["invalidos"]:
        L += ["## Linhas com valores inválidos no CSV", ""]
        L += [f"- **{v['termo']}**: {v['erro']}" for v in out["invalidos"]]
        L.append("")
    L += ["## Próximas ações humanas", ""] + [f"- [ ] {a}" for a in out["pendencias_humanas"]]
    return "\n".join(L) + "\n"


MANUAL_INSTRUCTIONS = (
    "Preencher data/keyword_research/manual_todo.csv: no Google Ads → Ferramentas → Planejador de palavras-chave → "
    "'Ver volume de pesquisa e previsões', cole os termos, local Brasil, idioma Português. Copie para o CSV: "
    "'Média de pesquisas mensais' → volume_mensal (aceita '1 mil – 10 mil'), "
    "'Lance na parte superior da página (intervalo menor – maior)' → cpc_medio (aceita '0,80 - 2,10'), "
    "'Concorrência' → concorrencia (Baixa/Média/Alta). Pode acrescentar linhas com ideias extras. "
    "Depois rode o agente novamente."
)


# --------------------------------------------------------------------------- entrypoint
def run(context: dict) -> dict:
    log = context["logger"]
    site_id = context["site_id"]
    site = context.get("site") or load_site(site_id)
    cfg = load_keyword_filters(site_id)
    seeds = collect_seeds(site, context.get("pauta"))
    seed_keys = {normalize_term(s["termo"]) for s in seeds}
    creds = credentials_status()
    log.info(f"[{AGENT_NAME}] site={site_id} sementes={len(seeds)} api={'sim' if creds.ok else 'não'} ({creds.reason})")

    rows, pending, invalid, source, api_error = [], [], [], None, None
    if creds.ok:
        try:
            rows = research_via_api(site, seeds, cfg, log)
            source = "google_ads_api"
        except KeywordResearchError as ex:
            api_error = str(ex)
            log.error(f"[{AGENT_NAME}] Falha na Google Ads API, usando fallback manual: {ex}")

    if source is None:
        manual_rows = sync_manual_todo(site_id, seeds)
        rows, pending, invalid = parse_manual_rows(manual_rows, seed_keys)
        source = "keyword_planner_manual"
        log.info(f"[{AGENT_NAME}] CSV manual: {len(rows)} com métricas, {len(pending)} pendentes, {len(invalid)} inválidos → {MANUAL_TODO}")

    approved, rejected = finalize(rows, site, seeds, cfg)
    incomplete = bool(pending or invalid)
    status = "ok" if rows and (not incomplete or context.get("aceitar_parcial")) else "awaiting_manual_input"

    human_actions = []
    if status == "awaiting_manual_input":
        human_actions.append(MANUAL_INSTRUCTIONS)
    elif approved:
        human_actions.append("Revisar oportunidades e aprovar pauta (gate 'aprovacao_pauta' antes do agente 03).")
    if any(o["sensivel_ymyl"] for o in approved):
        human_actions.append("Termos marcados como YMYL exigem aviso de saúde e revisão editorial reforçada.")
    if api_error:
        human_actions.append(f"Verificar credenciais/conta Google Ads: {api_error}")

    out_dir = RESEARCH_DIR / site_id
    output = {
        "agent": AGENT_NAME,
        "schema_version": SCHEMA_VERSION,
        "site_id": site_id,
        "pauta": context.get("pauta"),
        "gerado_em": now_iso(),
        "status": status,
        "fonte_dados": source,
        "credenciais": {"api_disponivel": creds.ok, "motivo": api_error or creds.reason},
        "filtros_aplicados": {k: cfg[k] for k in ("volume_mensal_minimo", "cpc_medio_minimo", "concorrencia_aceita", "excluir_contendo")},
        "resumo": {
            "termos_semente": len(seeds), "termos_com_metricas": len(rows), "aprovados": len(approved),
            "descartados": len(rejected), "pendentes": len(pending), "invalidos": len(invalid),
        },
        "oportunidades": approved,
        "descartados": rejected,
        "pendentes": pending,
        "invalidos": invalid,
        "pendencias_humanas": human_actions,
        "arquivos": {
            "oportunidades_json": str((out_dir / "opportunities.json").relative_to(ROOT)),
            "relatorio_md": str((out_dir / "report.md").relative_to(ROOT)),
            "manual_todo_csv": str(MANUAL_TODO.relative_to(ROOT)) if source == "keyword_planner_manual" else None,
        },
    }
    write_json(out_dir / "opportunities.json", output)
    (out_dir / "report.md").write_text(render_report(output, site), encoding="utf-8")
    log.info(f"[{AGENT_NAME}] status={status} aprovados={len(approved)} relatório={output['arquivos']['relatorio_md']}")
    return output


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 01 — pesquisa de nicho e palavras-chave")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    parser.add_argument("--pauta", help="termo extra a pesquisar junto com as sementes")
    parser.add_argument("--aceitar-parcial", action="store_true", help="seguir mesmo com termos ainda sem métricas")
    parser.add_argument("--print-report", action="store_true", help="imprimir o relatório markdown no stdout")
    args = parser.parse_args()

    load_env_file()
    run_id = f"{now_iso().replace(':', '').replace('+0000', 'Z')}-{AGENT_NAME}"
    output = run({
        "site_id": args.site, "pauta": args.pauta, "aceitar_parcial": args.aceitar_parcial,
        "logger": get_logger(run_id), "dry_run": True,
    })
    if args.print_report:
        print((ROOT / output["arquivos"]["relatorio_md"]).read_text(encoding="utf-8"))
    return 0 if output["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
