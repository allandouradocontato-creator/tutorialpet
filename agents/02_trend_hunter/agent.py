"""Agente 02 — Trend Hunter.

Transforma as oportunidades aprovadas pelo agente 01 (data/keyword_research/<site>/
opportunities.json) em pautas diárias priorizadas, combinando três sinais — sem
scraping de fóruns ou redes sociais:

  1. score_oportunidade (volume/CPC/concorrência), já calculado pelo agente 01;
  2. sazonalidade típica do nicho de pets (heurística, não um dado de API);
  3. perguntas relacionadas coletadas manualmente (ex.: AnswerThePublic) e coladas
     em data/trend_hunter/perguntas_manuais.csv.

Uso isolado:
    python agents/02_trend_hunter/agent.py --site pets-tutores-iniciantes
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_env_file, load_site  # noqa: E402
from core.io import normalize_term, now_iso, read_json, write_json  # noqa: E402
from core.log import get_logger  # noqa: E402

AGENT_NAME = "02_trend_hunter"
SCHEMA_VERSION = "1.0"
TREND_DIR = ROOT / "data" / "trend_hunter"
QUESTIONS_CSV = TREND_DIR / "perguntas_manuais.csv"
QUESTIONS_COLUMNS = ["termo_relacionado", "pergunta", "fonte", "data_coleta"]
MAX_PAUTAS_PADRAO = 5

# --------------------------------------------------------------------------- intenção de busca
TRANSACTIONAL_PATTERNS = [
    r"\bqual\b.*\bescolher\b", r"\bmelhor(es)?\b", r"\bcomprar\b", r"\bonde comprar\b",
    r"\bprec?o\b", r"\bvale a pena\b", r"\bindicad[oa]s?\b",
]
NAVIGATIONAL_PATTERNS: list[str] = []  # nenhuma marca nos termos-semente atuais


def classify_intent(term: str) -> str:
    t = normalize_term(term)
    if any(re.search(p, t) for p in NAVIGATIONAL_PATTERNS):
        return "navegacional"
    if any(re.search(p, t) for p in TRANSACTIONAL_PATTERNS):
        return "transacional"
    return "informacional"


# --------------------------------------------------------------------------- sazonalidade
# Heurística editorial (não vem de API): picos de busca típicos do nicho de pets no Brasil.
SEASONALITY_SIGNALS = [
    {"padroes": ["filhote", "enxoval", "primeiros dias"], "meses_pico": [11, 12, 1, 2],
     "motivo": "Alta de adoções de filhotes nas festas de fim de ano e início do ano"},
    {"padroes": ["ansiedade de separacao"], "meses_pico": [1, 2],
     "motivo": "Volta à rotina de trabalho/escola após as férias aumenta os casos de ansiedade de separação"},
    {"padroes": ["caixa de transporte", "vacinas"], "meses_pico": [12, 1],
     "motivo": "Viagens de fim de ano aumentam buscas por transporte e cuidados veterinários do pet"},
]
SEASONALITY_BOOST = 15


def seasonal_signal(term: str, month: int) -> dict | None:
    t = normalize_term(term)
    for signal in SEASONALITY_SIGNALS:
        if any(normalize_term(p) in t for p in signal["padroes"]):
            active = month in signal["meses_pico"]
            return {
                "motivo": signal["motivo"], "meses_pico": signal["meses_pico"],
                "ativo_no_mes": active, "boost_aplicado": SEASONALITY_BOOST if active else 0,
            }
    return None


# --------------------------------------------------------------------------- título e gancho
def _pick(seed: str, options: list[str]) -> str:
    """Escolha determinística (não aleatória): o mesmo termo sempre gera o mesmo template,
    mas termos diferentes tendem a cair em templates diferentes — evita padrão repetitivo."""
    idx = int(hashlib.md5(normalize_term(seed).encode("utf-8")).hexdigest(), 16) % len(options)
    return options[idx]


def _cap(term: str) -> str:
    return term[:1].upper() + term[1:] if term else term


TITLE_TEMPLATES = {
    "informacional": [
        "{termo_cap}: guia passo a passo para tutores de primeira viagem",
        "Como lidar com {termo}: o que todo tutor iniciante precisa saber",
        "{termo_cap} sem sofrimento: um guia prático e sem enrolação",
    ],
    "transacional": [
        "{termo_cap}: como escolher sem se arrepender",
        "{termo_cap}? Veja o que realmente importa antes de decidir",
    ],
    "navegacional": ["{termo_cap}: tudo o que você precisa saber"],
}

HOOK_TEMPLATES = {
    "informacional": [
        "Se você chegou até aqui é porque provavelmente está no meio dessa situação agora — e a boa "
        "notícia é que ela tem solução prática, sem drama e sem precisar virar especialista.",
        "Quase todo tutor de primeira viagem passa por isso e se sente meio perdido no começo. Vamos "
        "destrinchar o assunto com calma, do jeito que eu gostaria que alguém tivesse me explicado.",
        "Erro comum: iniciante vê esse problema e já entra em pânico. Respira — dá para resolver com "
        "alguns ajustes simples na rotina, e é exatamente isso que vamos ver aqui.",
    ],
    "transacional": [
        "Prateleira cheia de opções, promessas bonitas na embalagem e nenhuma explicação clara de qual "
        "realmente funciona? Vamos comparar na prática o que faz diferença de verdade.",
        "Antes de gastar dinheiro à toa, vale entender o que separa uma boa escolha de uma decepção "
        "guardada no fundo do armário.",
    ],
    "navegacional": ["Reunimos aqui o essencial sobre o assunto, direto ao ponto."],
}


def build_pauta_content(term: str) -> tuple[str, str, str]:
    intent = classify_intent(term)
    title = _pick(term, TITLE_TEMPLATES[intent]).format(termo_cap=_cap(term), termo=term)
    hook = _pick(term + "#hook", HOOK_TEMPLATES[intent])
    return title, hook, intent


# --------------------------------------------------------------------------- perguntas manuais
def ensure_questions_csv() -> None:
    if QUESTIONS_CSV.exists():
        return
    QUESTIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with QUESTIONS_CSV.open("w", encoding="utf-8-sig", newline="") as fh:
        csv.DictWriter(fh, fieldnames=QUESTIONS_COLUMNS, delimiter=";").writeheader()


def load_questions() -> list[dict]:
    ensure_questions_csv()
    with QUESTIONS_CSV.open(encoding="utf-8-sig", newline="") as fh:
        return [r for r in csv.DictReader(fh, delimiter=";") if (r.get("pergunta") or "").strip()]


STOPWORDS = {"de", "da", "do", "para", "com", "em", "a", "o", "e", "que", "como", "no", "na", "os", "as"}


def related_questions(term: str, questions: list[dict], limit: int = 5) -> list[str]:
    term_norm = normalize_term(term)
    words = {w for w in term_norm.split() if len(w) >= 4 and w not in STOPWORDS}
    matches, seen = [], set()
    for q in questions:
        pergunta = (q.get("pergunta") or "").strip()
        if not pergunta or pergunta in seen:
            continue
        related_term = normalize_term(q.get("termo_relacionado", ""))
        q_words = {w for w in normalize_term(pergunta).split() if len(w) >= 4}
        same_term = related_term and (related_term in term_norm or term_norm in related_term)
        if same_term or (words & q_words):
            matches.append(pergunta)
            seen.add(pergunta)
    return matches[:limit]


# --------------------------------------------------------------------------- prioridade
def priority_bucket(score: float) -> str:
    if score >= 70:
        return "ALTA"
    if score >= 40:
        return "MEDIA"
    return "BAIXA"


def compute_score(base_score: float, seasonality: dict | None, n_perguntas: int, sensivel: bool) -> float:
    score = base_score
    if seasonality and seasonality["ativo_no_mes"]:
        score += seasonality["boost_aplicado"]
    score += min(n_perguntas * 3, 15)
    if sensivel:
        score -= 5  # não descarta — só sinaliza que precisa de revisão extra, não que é menos relevante
    return round(max(0.0, min(100.0, score)), 1)


# --------------------------------------------------------------------------- fonte de dados
def load_opportunities(site_id: str, context_input: dict | None) -> dict:
    if context_input and context_input.get("agent") == "01_niche_research":
        return context_input
    path = ROOT / "data" / "keyword_research" / site_id / "opportunities.json"
    return read_json(path)


def build_pautas(oportunidades: list[dict], questions: list[dict], month: int, max_pautas: int) -> list[dict]:
    pautas = []
    for op in oportunidades:
        term = op["termo"]
        title, hook, intent = build_pauta_content(term)
        season = seasonal_signal(term, month)
        related = related_questions(term, questions)
        sensivel = op.get("sensivel_ymyl", False)
        score = compute_score(op.get("score_oportunidade", 50.0), season, len(related), sensivel)
        pautas.append({
            "termo_origem": term,
            "titulo": title,
            "angulo_gancho": hook,
            "intencao_busca": intent,
            "prioridade": priority_bucket(score),
            "score_prioridade": score,
            "pilar": op.get("pilar"),
            "sensivel_ymyl": sensivel,
            "sazonalidade": season,
            "perguntas_relacionadas": related,
        })
    pautas.sort(key=lambda p: p["score_prioridade"], reverse=True)
    pautas = pautas[:max_pautas]
    for i, p in enumerate(pautas, 1):
        p["id"] = i
    return pautas


# --------------------------------------------------------------------------- entrypoint
def run(context: dict) -> dict:
    log = context["logger"]
    site_id = context["site_id"]
    site = context.get("site") or load_site(site_id)
    month = context.get("mes_referencia") or datetime.now(timezone.utc).month
    max_pautas = context.get("max_pautas") or MAX_PAUTAS_PADRAO

    opportunities_output = load_opportunities(site_id, context.get("input"))
    oportunidades = list(opportunities_output.get("oportunidades", []))
    questions = load_questions()
    log.info(f"[{AGENT_NAME}] site={site_id} oportunidades_aprovadas={len(oportunidades)} perguntas_manuais={len(questions)}")

    # Uma pauta avulsa passada via --pauta (rodada específica) também vira candidata,
    # mesmo que ainda não tenha métricas reais de keyword.
    pauta_manual = context.get("pauta")
    if pauta_manual and not any(normalize_term(o["termo"]) == normalize_term(pauta_manual) for o in oportunidades):
        oportunidades.append({"termo": pauta_manual, "pilar": "pauta_especifica",
                               "score_oportunidade": 50.0, "sensivel_ymyl": False})

    if not oportunidades:
        log.warning(f"[{AGENT_NAME}] nenhuma oportunidade aprovada pelo agente 01 — nada para propor")
        output = {
            "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "site_id": site_id,
            "gerado_em": now_iso(), "status": "sem_oportunidades_aprovadas", "pautas": [],
            "pendencias_humanas": ["Completar o agente 01 (opportunities.json precisa ter itens em "
                                    "'oportunidades') antes de gerar pautas."],
        }
    else:
        pautas = build_pautas(oportunidades, questions, month, max_pautas)
        output = {
            "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "site_id": site_id,
            "gerado_em": now_iso(), "status": "ok", "mes_referencia": month,
            "total_oportunidades_avaliadas": len(oportunidades), "perguntas_manuais_usadas": len(questions),
            "pautas": pautas,
            "pendencias_humanas": ["Escolher UMA pauta (gate 'aprovacao_pauta', campo 'pauta_id_selecionada') "
                                    "antes do agente 03."],
        }

    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = TREND_DIR / f"pautas_{date_str}.json"
    write_json(out_path, output)
    output["arquivo"] = str(out_path.relative_to(ROOT))
    log.info(f"[{AGENT_NAME}] status={output['status']} pautas_geradas={len(output.get('pautas', []))} → {out_path.relative_to(ROOT)}")
    return output


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 02 — geração de pautas priorizadas")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    parser.add_argument("--max", type=int, default=MAX_PAUTAS_PADRAO, dest="max_pautas", help="máx. de pautas geradas")
    parser.add_argument("--mes", type=int, choices=range(1, 13), help="mês de referência p/ sazonalidade (1-12); default: mês atual")
    args = parser.parse_args()

    load_env_file()
    run_id = f"{now_iso().replace(':', '').replace('+0000', 'Z')}-{AGENT_NAME}"
    output = run({"site_id": args.site, "max_pautas": args.max_pautas, "mes_referencia": args.mes,
                  "logger": get_logger(run_id)})
    return 0 if output["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
