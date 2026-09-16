"""Agente 08 — Analytics.

Analisa desempenho de páginas publicadas (Search Console + GA4) e sugere candidatos a
atualização ou poda. Como ainda não há site real publicado, roda em dois modos:

  - Com --gsc-csv/--ga-csv apontando para exports reais: analisa os dados de verdade.
  - Sem eles (padrão): gera um relatório de AMOSTRA com dados fictícios, claramente
    marcados como tal, só para mostrar o formato do relatório final.

A classificação de candidatos usa o mesmo código nos dois modos — só os dados mudam.

Uso isolado:
    python agents/08_analytics/agent.py --site pets-tutores-iniciantes
    python agents/08_analytics/agent.py --site pets-tutores-iniciantes \
        --gsc-csv caminho/Pages.csv --ga-csv caminho/paginas_e_telas.csv
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_env_file, load_site  # noqa: E402
from core.io import now_iso  # noqa: E402
from core.log import get_logger  # noqa: E402
from csv_parsers import CsvFormatError, parse_ga_csv, parse_gsc_csv  # noqa: E402

AGENT_NAME = "08_analytics"
SCHEMA_VERSION = "1.0"
ANALYTICS_DIR = ROOT / "data" / "analytics"

IMPRESSOES_MIN_PARA_OTIMIZAR = 500
CTR_BAIXO = 0.02
CTR_BOM = 0.03
POSICAO_QUASE_PAGINA1 = (11, 20)
POSICAO_PODAR = 20

SAMPLE_GSC = [
    {"pagina": "/como-cortar-unha-de-cachorro", "cliques": 142, "impressoes": 6800, "ctr": 0.0209, "posicao_media": 8.4},
    {"pagina": "/racao-para-filhote-de-cachorro", "cliques": 12, "impressoes": 3100, "ctr": 0.0039, "posicao_media": 14.2},
    {"pagina": "/gato-arranhando-o-sofa", "cliques": 3, "impressoes": 890, "ctr": 0.0034, "posicao_media": 27.6},
    {"pagina": "/como-dar-banho-em-gato", "cliques": 205, "impressoes": 4200, "ctr": 0.0488, "posicao_media": 5.1},
    {"pagina": "/primeiros-dias-do-filhote-em-casa", "cliques": 0, "impressoes": 60, "ctr": 0.0, "posicao_media": 42.0},
]
SAMPLE_GA = [
    {"pagina": "/como-cortar-unha-de-cachorro", "visualizacoes": 168, "usuarios": 151, "engajamento_medio_seg": 96.0},
    {"pagina": "/racao-para-filhote-de-cachorro", "visualizacoes": 14, "usuarios": 13, "engajamento_medio_seg": 22.0},
    {"pagina": "/gato-arranhando-o-sofa", "visualizacoes": 4, "usuarios": 4, "engajamento_medio_seg": 18.0},
    {"pagina": "/como-dar-banho-em-gato", "visualizacoes": 230, "usuarios": 201, "engajamento_medio_seg": 140.0},
    {"pagina": "/primeiros-dias-do-filhote-em-casa", "visualizacoes": 0, "usuarios": 0, "engajamento_medio_seg": 0.0},
]


# --------------------------------------------------------------------------- classificação
def classify_page(gsc_row: dict) -> tuple[str, str]:
    impressoes, cliques, ctr, posicao = gsc_row["impressoes"], gsc_row["cliques"], gsc_row["ctr"], gsc_row["posicao_media"]
    if posicao > POSICAO_PODAR and cliques == 0:
        return "atualizar_ou_podar", ("Posição baixa e nenhum clique — considerar reescrever com mais "
                                       "profundidade/E-E-A-T, consolidar com outro artigo, ou despriorizar.")
    if POSICAO_QUASE_PAGINA1[0] <= posicao <= POSICAO_QUASE_PAGINA1[1]:
        return "quase_primeira_pagina", ("Já está perto da primeira página — pequenos ajustes de SEO on-page "
                                          "ou mais profundidade podem empurrar para o top 10.")
    if impressoes >= IMPRESSOES_MIN_PARA_OTIMIZAR and ctr < CTR_BAIXO:
        return "otimizar_titulo_meta", ("Muitas impressões mas poucos cliques — título/meta description "
                                         "provavelmente não estão atraentes o suficiente para a posição atual.")
    if posicao <= 10 and ctr >= CTR_BOM:
        return "bom_desempenho", "Desempenho saudável — manter e usar como referência de estrutura para outros artigos."
    return "monitorar", "Sem sinal forte ainda — continuar monitorando nas próximas coletas."


# --------------------------------------------------------------------------- relatório
def render_report(site: dict, gsc_rows: list[dict], ga_rows: list[dict], amostra: bool, fontes: dict) -> str:
    ga_by_page = {normalize_page(r["pagina"]): r for r in ga_rows}
    linhas_tabela = []
    contagem = {}
    for row in gsc_rows:
        categoria, acao = classify_page(row)
        contagem[categoria] = contagem.get(categoria, 0) + 1
        ga = ga_by_page.get(normalize_page(row["pagina"]))
        linhas_tabela.append((row, categoria, acao, ga))
    linhas_tabela.sort(key=lambda t: t[0]["posicao_media"])

    hoje = now_iso()
    L = [f"# Relatório de Analytics — {site['site_id']}", ""]
    if amostra:
        L += ["> ⚠️ **AMOSTRA — não é dado real.** Nenhum export de Search Console ou GA4 foi informado; "
              "os números abaixo são fictícios, só para mostrar o formato deste relatório.", ""]
    L += [
        f"- **Gerado em:** {hoje}",
        f"- **Fonte Search Console:** {fontes['gsc']}",
        f"- **Fonte GA4:** {fontes['ga']}",
        f"- **Páginas analisadas:** {len(gsc_rows)}",
        "",
        "## Resumo por categoria", "",
        "| Categoria | Páginas |", "|---|---|",
    ]
    rotulos = {
        "atualizar_ou_podar": "Atualizar ou podar (posição ruim, zero cliques)",
        "quase_primeira_pagina": "Quase primeira página (posição 11–20)",
        "otimizar_titulo_meta": "Otimizar título/meta (CTR baixo, alta impressão)",
        "bom_desempenho": "Bom desempenho (manter)",
        "monitorar": "Monitorar (sem sinal forte)",
    }
    L += [f"| {rotulos[cat]} | {contagem.get(cat, 0)} |" for cat in rotulos if contagem.get(cat)]
    L += ["", "## Detalhe por página", "",
          "| Página | Cliques | Impressões | CTR | Posição média | Visualizações (GA4) | Categoria |",
          "|---|---|---|---|---|---|---|"]
    for row, categoria, _acao, ga in linhas_tabela:
        views = ga["visualizacoes"] if ga else "—"
        L.append(f"| {row['pagina']} | {row['cliques']} | {row['impressoes']} | {row['ctr']:.2%} | "
                  f"{row['posicao_media']:.1f} | {views} | {rotulos[categoria]} |")
    L += ["", "## Candidatos a atualização (ação recomendada)", ""]
    acionaveis = [t for t in linhas_tabela if t[1] in ("atualizar_ou_podar", "quase_primeira_pagina", "otimizar_titulo_meta")]
    if acionaveis:
        for row, categoria, acao, _ga in acionaveis:
            L.append(f"- **{row['pagina']}** ({rotulos[categoria]}): {acao}")
    else:
        L.append("Nenhum candidato claro com os dados atuais.")
    L += [
        "",
        "## Limitações desta análise",
        "",
        "- Esta é uma foto de um único período — comparar tendência ao longo do tempo exige "
        "guardar exports de datas diferentes e comparar manualmente (não implementado nesta fase).",
        "- Os limiares de classificação (impressões, CTR, posição) são heurísticas de referência, "
        "não regras universais — ajustar conforme o nicho e o volume real do site.",
    ]
    return "\n".join(L) + "\n"


def normalize_page(path: str) -> str:
    return path.strip().rstrip("/").lower()


# --------------------------------------------------------------------------- entrypoint
def run(context: dict) -> dict:
    log = context["logger"]
    site_id = context["site_id"]
    site = context.get("site") or load_site(site_id)

    gsc_path, ga_path = context.get("gsc_csv"), context.get("ga_csv")
    fontes = {"gsc": "AMOSTRA (fictícia)", "ga": "AMOSTRA (fictícia)"}
    amostra = True
    erros = []

    if gsc_path:
        try:
            gsc_rows = parse_gsc_csv(Path(gsc_path))
            fontes["gsc"] = str(gsc_path)
            amostra = False
        except (CsvFormatError, OSError) as ex:
            log.error(f"[{AGENT_NAME}] falha ao ler CSV do Search Console ({gsc_path}): {ex}")
            erros.append(f"Search Console: {ex}")
            gsc_rows = SAMPLE_GSC
    else:
        gsc_rows = SAMPLE_GSC

    if ga_path:
        try:
            ga_rows = parse_ga_csv(Path(ga_path))
            fontes["ga"] = str(ga_path)
            amostra = False if gsc_path else amostra
        except (CsvFormatError, OSError) as ex:
            log.error(f"[{AGENT_NAME}] falha ao ler CSV do GA4 ({ga_path}): {ex}")
            erros.append(f"GA4: {ex}")
            ga_rows = SAMPLE_GA
    else:
        ga_rows = SAMPLE_GA

    relatorio_md = render_report(site, gsc_rows, ga_rows, amostra, fontes)
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = ANALYTICS_DIR / f"relatorio_{date_str}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(relatorio_md, encoding="utf-8")

    candidatos = [classify_page(r)[0] for r in gsc_rows]
    pendencias = []
    if amostra:
        pendencias.append("Relatório em modo amostra — conecte exports reais do Search Console/GA4 "
                           "(--gsc-csv/--ga-csv) assim que o site estiver publicado e indexado.")
    if erros:
        pendencias += [f"[erro de leitura] {e}" for e in erros]
    n_acionaveis = sum(1 for c in candidatos if c in ("atualizar_ou_podar", "quase_primeira_pagina", "otimizar_titulo_meta"))
    if n_acionaveis:
        pendencias.append(f"{n_acionaveis} página(s) com ação recomendada — ver seção 'Candidatos a atualização' no relatório.")

    output = {
        "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "site_id": site_id, "gerado_em": now_iso(),
        "status": "ok", "amostra": amostra, "n_paginas_analisadas": len(gsc_rows),
        "n_candidatos_acao": n_acionaveis, "relatorio": str(out_path.relative_to(ROOT)),
        "pendencias_humanas": pendencias,
    }
    log.info(f"[{AGENT_NAME}] amostra={amostra} páginas={len(gsc_rows)} candidatos_acao={n_acionaveis} → {out_path.relative_to(ROOT)}")
    return output


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 08 — analytics de desempenho (uso isolado)")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    parser.add_argument("--gsc-csv", help="caminho de um export CSV do Google Search Console")
    parser.add_argument("--ga-csv", help="caminho de um export CSV do Google Analytics 4")
    args = parser.parse_args()

    load_env_file()
    run_id = f"{now_iso().replace(':', '').replace('+0000', 'Z')}-{AGENT_NAME}"
    output = run({"site_id": args.site, "gsc_csv": args.gsc_csv, "ga_csv": args.ga_csv, "logger": get_logger(run_id)})
    return 0 if output["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
