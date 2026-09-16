"""Agente 10 — Policy Guardian.

Audita periodicamente o site contra config/policies.yaml (regras de compliance do
AdSense + sinais de risco de Helpful Content), comparando as regras com o estado atual
dos artigos publicados (data/publisher/simulado/) e da infraestrutura legal/técnica
gerada pelo agente 06 — sinalizando risco antes que vire penalização.

Uso isolado:
    python agents/10_policy_guardian/agent.py --site pets-tutores-iniciantes
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
from datetime import datetime, timedelta, timezone
from itertools import combinations
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_env_file, load_site, load_yaml, CONFIG_DIR  # noqa: E402
from core.io import now_iso  # noqa: E402
from core.log import get_logger  # noqa: E402
from core.markdown import MarkdownError, read_markdown, strip_markdown_plain  # noqa: E402

AGENT_NAME = "10_policy_guardian"
SCHEMA_VERSION = "1.0"

PUBLISHED_DIR = ROOT / "data" / "publisher" / "simulado"
LEGAL_DIR = ROOT / "data" / "platform_compliance" / "paginas_legais"
TECH_DIR = ROOT / "data" / "platform_compliance" / "arquivos_tecnicos"
GUARDIAN_DIR = ROOT / "data" / "policy_guardian"
DUPLICATE_SIMILARITY_THRESHOLD = 0.75


def load_policies() -> dict:
    return load_yaml(CONFIG_DIR / "policies.yaml")


def add_finding(findings: list[dict], area: str, severidade: str, descricao: str, alvo: str | None = None) -> None:
    findings.append({"area": area, "severidade": severidade, "descricao": descricao, "alvo": alvo})


# --------------------------------------------------------------------------- checagens de site
def check_paginas_e_arquivos(site_id: str, policies: dict, findings: list[dict]) -> None:
    legal_dir = LEGAL_DIR / site_id
    for slug in policies.get("paginas_obrigatorias", []):
        if not (legal_dir / f"{slug}.md").exists():
            add_finding(findings, "paginas_legais", "critico", f"página legal obrigatória ausente: {slug}", slug)
    tech_dir = TECH_DIR / site_id
    for nome in policies.get("arquivos_obrigatorios", []):
        if not (tech_dir / nome).exists():
            add_finding(findings, "arquivos_tecnicos", "critico", f"arquivo técnico obrigatório ausente: {nome}", nome)


def check_catalogo_pequeno(n_artigos: int, policies: dict, findings: list[dict]) -> None:
    minimo = policies.get("auditoria", {}).get("minimo_artigos_para_baixo_risco_estrutural", 15)
    if n_artigos < minimo:
        add_finding(findings, "helpful_content", "atencao",
                    f"catálogo com apenas {n_artigos} artigo(s) publicado(s) — abaixo do mínimo de referência "
                    f"({minimo}) para reduzir o risco estrutural de 'catálogo jovem' no Helpful Content Update.")


def check_conteudo_duplicado(articles: list[tuple[dict, str]], findings: list[dict]) -> None:
    corpora = {fm.get("slug", "?"): strip_markdown_plain(body)[:5000] for fm, body in articles}
    for (slug_a, text_a), (slug_b, text_b) in combinations(corpora.items(), 2):
        ratio = difflib.SequenceMatcher(None, text_a, text_b).ratio()
        if ratio >= DUPLICATE_SIMILARITY_THRESHOLD:
            add_finding(findings, "helpful_content", "critico",
                        f"'{slug_a}' e '{slug_b}' têm {ratio:.0%} de similaridade — risco de conteúdo "
                        "duplicado/quase-duplicado dentro do próprio site.", f"{slug_a} / {slug_b}")


# --------------------------------------------------------------------------- checagens por artigo
CREDENTIAL_CLAIM_PATTERNS = [
    r"sou veterinari[ao]", r"como veterinari[ao]", r"meu crmv", r"minha clinica veterinaria",
]


def _norm(text: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", text.lower()) if not unicodedata.combining(c))


def check_article(fm: dict, body: str, policies: dict, site: dict, findings: list[dict]) -> None:
    slug = fm.get("slug", "?")
    req = policies.get("requisitos_conteudo", {})
    body_plain = strip_markdown_plain(body)
    n_palavras = len(body_plain.split())

    if n_palavras < req.get("minimo_palavras_artigo", 500):
        add_finding(findings, "requisitos_conteudo", "atencao",
                    f"'{slug}': {n_palavras} palavras, abaixo do mínimo recomendado "
                    f"({req.get('minimo_palavras_artigo', 500)}).", slug)
    if req.get("exigir_autor_declarado") and not (fm.get("autor") or "").strip():
        add_finding(findings, "requisitos_conteudo", "atencao",
                    f"'{slug}': campo 'autor' ainda em branco — precisa de uma pessoa real antes de ir ao ar de verdade.", slug)
    if req.get("exigir_data_publicacao") and not fm.get("data"):
        add_finding(findings, "requisitos_conteudo", "atencao", f"'{slug}': sem campo 'data' de publicação.", slug)
    if req.get("exigir_meta_description") and not (fm.get("meta_description") or "").strip():
        add_finding(findings, "requisitos_conteudo", "atencao", f"'{slug}': sem meta description.", slug)

    if req.get("exigir_aviso_saude_em_topicos_sensiveis") and fm.get("aviso_saude_aplicavel"):
        aviso = site.get("compliance", {}).get("aviso_saude", "")
        if aviso and _norm(aviso) not in _norm(body_plain):
            add_finding(findings, "conteudo_proibido", "critico",
                        f"'{slug}' é YMYL mas não contém o aviso de saúde do site no corpo do texto.", slug)

    hits = [p for p in CREDENTIAL_CLAIM_PATTERNS if re.search(p, _norm(body_plain))]
    if hits:
        add_finding(findings, "conteudo_proibido", "critico",
                    f"'{slug}' contém possível alegação de credencial veterinária — proibido pela política do site.", slug)

    # Defesa em profundidade: repassa achados bloqueantes que já deveriam ter sido barrados
    # pelo agente 04, caso o front-matter tenha sido editado manualmente depois.
    bloqueantes_residuais = [c for c in fm.get("checagens_qualidade", []) if c.get("severidade") == "bloqueante"]
    if bloqueantes_residuais:
        add_finding(findings, "helpful_content", "critico",
                    f"'{slug}' tem {len(bloqueantes_residuais)} checagem(ns) bloqueante(s) residual(is) do "
                    "agente 04 (revisar checagens_qualidade no front-matter).", slug)


# --------------------------------------------------------------------------- relatório
def render_report(site_id: str, findings: list[dict], n_artigos: int, policies: dict) -> str:
    criticos = [f for f in findings if f["severidade"] == "critico"]
    atencao = [f for f in findings if f["severidade"] == "atencao"]
    risco = "ALTO" if criticos else ("MÉDIO" if atencao else "BAIXO")
    proxima = (datetime.now(timezone.utc) + timedelta(days=policies.get("auditoria", {}).get("frequencia_recomendada_dias", 30))).strftime("%Y-%m-%d")

    L = [
        f"# Auditoria de políticas — {site_id}", "",
        f"- **Gerado em:** {now_iso()}",
        f"- **Artigos auditados:** {n_artigos}",
        f"- **Risco geral:** {risco}",
        f"- **Próxima auditoria sugerida:** {proxima}",
        "",
        "## Resumo", "",
        f"| Achados críticos | Achados de atenção |", "|---|---|", f"| {len(criticos)} | {len(atencao)} |", "",
    ]
    if criticos:
        L += ["## 🔴 Achados críticos (risco de penalização/reprovação)", ""]
        L += [f"- **[{f['area']}]** {f['descricao']}" for f in criticos]
        L.append("")
    if atencao:
        L += ["## 🟡 Achados de atenção (melhorar, não bloqueante)", ""]
        L += [f"- **[{f['area']}]** {f['descricao']}" for f in atencao]
        L.append("")
    if not findings:
        L += ["## Nenhum achado", "", "O site está em conformidade com as checagens automatizadas deste agente.", ""]

    L += ["## Sinais de Helpful Content monitorados", ""]
    L += [f"- {s}" for s in policies.get("helpful_content", {}).get("sinais_de_risco", [])]
    L += ["", "## Lembrete", "",
          "Esta auditoria cobre o que dá para checar automaticamente (páginas obrigatórias, arquivos "
          "técnicos, requisitos mínimos de conteúdo, duplicidade, alegações proibidas). Ela não substitui "
          "uma leitura humana das diretrizes oficiais do AdSense e do Helpful Content antes de qualquer "
          "candidatura ou decisão importante."]
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- entrypoint
def run(context: dict) -> dict:
    log = context["logger"]
    site_id = context["site_id"]
    site = context.get("site") or load_site(site_id)
    policies = load_policies()

    findings: list[dict] = []
    check_paginas_e_arquivos(site_id, policies, findings)

    articles = []
    for path in sorted(PUBLISHED_DIR.glob("*.md")):
        try:
            fm, body = read_markdown(path)
        except MarkdownError:
            continue
        articles.append((fm, body))
        check_article(fm, body, policies, site, findings)

    check_catalogo_pequeno(len(articles), policies, findings)
    check_conteudo_duplicado(articles, findings)

    relatorio_md = render_report(site_id, findings, len(articles), policies)
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = GUARDIAN_DIR / f"auditoria_{date_str}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(relatorio_md, encoding="utf-8")

    criticos = [f for f in findings if f["severidade"] == "critico"]
    risco = "alto" if criticos else ("medio" if findings else "baixo")
    pendencias = [f"[{f['severidade']}/{f['area']}] {f['descricao']}" for f in findings]
    if not pendencias:
        pendencias.append("Nenhum achado nesta auditoria — manter a cadência de revisão periódica.")

    output = {
        "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "site_id": site_id, "gerado_em": now_iso(),
        "status": "ok", "risco_geral": risco, "n_achados_criticos": len(criticos),
        "n_achados_atencao": len(findings) - len(criticos), "n_artigos_auditados": len(articles),
        "relatorio": str(out_path.relative_to(ROOT)), "achados": findings, "pendencias_humanas": pendencias,
    }
    log.info(f"[{AGENT_NAME}] risco={risco} criticos={len(criticos)} atencao={len(findings) - len(criticos)} "
             f"artigos={len(articles)} → {out_path.relative_to(ROOT)}")
    return output


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 10 — auditoria de políticas (uso isolado)")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    args = parser.parse_args()

    load_env_file()
    run_id = f"{now_iso().replace(':', '').replace('+0000', 'Z')}-{AGENT_NAME}"
    output = run({"site_id": args.site, "logger": get_logger(run_id)})
    return 0 if output["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
