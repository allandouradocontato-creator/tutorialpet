"""Agente 06 — Platform Compliance.

Gera as páginas legais/institucionais e os arquivos técnicos exigidos para aplicar ao
Google AdSense com segurança, e audita a prontidão do site antes de sugerir a aplicação.
Nunca envia nada para o AdSense — só prepara o terreno e relata pendências. A decisão de
aplicar continua sendo humana (gate 'aprovacao_candidatura_adsense', fora deste agente).

Uso isolado:
    python agents/06_platform_compliance/agent.py --site pets-tutores-iniciantes
"""
from __future__ import annotations

import argparse
import difflib
import re
import socket
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_env_file, load_site  # noqa: E402
from core.io import now_iso  # noqa: E402
from core.log import get_logger  # noqa: E402
from core.markdown import read_markdown, strip_markdown_plain, write_markdown  # noqa: E402
from legal_content import RENDERERS  # noqa: E402

AGENT_NAME = "06_platform_compliance"
SCHEMA_VERSION = "1.0"

COMPLIANCE_DIR = ROOT / "data" / "platform_compliance"
# O agente 05 grava os artigos otimizados em data/seo_onpage/otimizados/ (não existe uma
# pasta "prontos/" no pipeline atual) — usamos o caminho real de saída do agente 05.
READY_ARTICLES_DIR = ROOT / "data" / "seo_onpage" / "otimizados"

MIN_ARTIGOS_PADRAO = 15
DUPLICATE_SIMILARITY_THRESHOLD = 0.75
PLACEHOLDER_DOMAIN_MARKERS = ("seu-dominio", "example.com", "localhost")


# --------------------------------------------------------------------------- páginas legais
def write_legal_pages(site_id: str, site: dict, logger) -> dict[str, str]:
    out_dir = COMPLIANCE_DIR / "paginas_legais" / site_id
    gerados = {}
    for pagina in site.get("compliance", {}).get("paginas_obrigatorias", []):
        slug = pagina["slug"].strip("/")
        renderer = RENDERERS.get(slug)
        if not renderer:
            logger.warning(f"[{AGENT_NAME}] sem template para a página obrigatória '{slug}' — pulando")
            continue
        body = renderer(site)
        front_matter = {
            "titulo": pagina.get("titulo", slug), "slug": slug, "tipo": "pagina_legal",
            "site_id": site_id, "gerado_em": now_iso(), "gerado_por": AGENT_NAME,
            "revisao_humana_pendente": True,
        }
        path = write_markdown(out_dir / f"{slug}.md", front_matter, body)
        gerados[slug] = str(path.relative_to(ROOT))
    return gerados


# --------------------------------------------------------------------------- arquivos técnicos
def render_robots(site: dict) -> str:
    dominio = site["dominio"].rstrip("/")
    return f"User-agent: *\nAllow: /\n\nSitemap: {dominio}/sitemap.xml\n"


def render_sitemap(site: dict) -> str:
    dominio = site["dominio"].rstrip("/")
    hoje = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    paginas = ["/"] + [p["slug"] for p in site.get("compliance", {}).get("paginas_obrigatorias", [])]
    urls = "\n".join(
        f"  <url>\n    <loc>{dominio}{slug}</loc>\n    <lastmod>{hoje}</lastmod>\n  </url>"
        for slug in paginas
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "  <!-- Artigos publicados entram aqui automaticamente (agente 07/08) assim que forem ao ar. -->\n"
        "</urlset>\n"
    )


def render_ads_txt(site: dict) -> str:
    placeholder = site.get("compliance", {}).get("ads_txt_placeholder", "google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0")
    return (
        f"{placeholder}\n"
        "# Substituir 'pub-0000000000000000' pelo Publisher ID real assim que a conta AdSense for aprovada.\n"
    )


def write_technical_files(site_id: str, site: dict) -> dict[str, str]:
    out_dir = COMPLIANCE_DIR / "arquivos_tecnicos" / site_id
    out_dir.mkdir(parents=True, exist_ok=True)
    files = {"robots.txt": render_robots(site), "sitemap.xml": render_sitemap(site), "ads.txt": render_ads_txt(site)}
    gerados = {}
    for name, content in files.items():
        path = out_dir / name
        path.write_text(content, encoding="utf-8")
        gerados[name] = str(path.relative_to(ROOT))
    return gerados


# --------------------------------------------------------------------------- prontidão: artigos
def list_ready_articles() -> list[Path]:
    if not READY_ARTICLES_DIR.exists():
        return []
    return sorted(READY_ARTICLES_DIR.glob("*.md"))


def check_duplicate_content(article_paths: list[Path]) -> list[dict]:
    """Similaridade básica (difflib) entre pares de artigos — não é detecção de plágio contra
    fontes externas, só um alerta de conteúdo repetitivo dentro do próprio site."""
    corpora = {}
    for path in article_paths:
        try:
            _, body = read_markdown(path)
        except Exception:
            continue
        corpora[path.stem] = strip_markdown_plain(body)[:5000]

    duplicados = []
    for (slug_a, text_a), (slug_b, text_b) in combinations(corpora.items(), 2):
        ratio = difflib.SequenceMatcher(None, text_a, text_b).ratio()
        if ratio >= DUPLICATE_SIMILARITY_THRESHOLD:
            duplicados.append({"artigo_a": slug_a, "artigo_b": slug_b, "similaridade": round(ratio, 3)})
    return duplicados


# --------------------------------------------------------------------------- prontidão: técnico
def is_placeholder_domain(dominio: str) -> bool:
    d = dominio.lower()
    return any(marker in d for marker in PLACEHOLDER_DOMAIN_MARKERS)


def check_https(dominio: str) -> dict:
    if is_placeholder_domain(dominio):
        return {"checado": False, "ok": None, "motivo": "domínio ainda é um placeholder — configure o domínio real e rode este agente de novo."}
    if not dominio.startswith("https://"):
        return {"checado": True, "ok": False, "motivo": f"domínio configurado sem https:// ({dominio})."}
    try:
        with urllib.request.urlopen(dominio, timeout=5) as resp:
            final_url = resp.geturl()
        return {"checado": True, "ok": final_url.startswith("https://"), "motivo": f"resposta HTTP {getattr(resp, 'status', '200')}."}
    except (urllib.error.URLError, socket.timeout, ssl.SSLError, ValueError) as ex:
        return {"checado": True, "ok": False, "motivo": f"não foi possível conectar: {ex}"}


def check_lighthouse(dominio: str) -> dict:
    import shutil
    if is_placeholder_domain(dominio):
        return {"checado": False, "disponivel": False, "motivo": "domínio ainda é um placeholder — pulando."}
    if not shutil.which("lighthouse"):
        return {"checado": False, "disponivel": False,
                "motivo": "Lighthouse CLI não encontrado neste ambiente. Rode manualmente quando o site estiver "
                          f"no ar: `lighthouse {dominio} --output json --output-path relatorio.json`."}
    return {"checado": False, "disponivel": True,
            "motivo": "Lighthouse CLI disponível, mas a execução automática não está habilitada nesta fase — "
                      "rode manualmente e anexe o relatório à revisão de prontidão."}


# --------------------------------------------------------------------------- relatório
def build_readiness_report(site: dict, contexto: dict) -> tuple[str, bool, list[str]]:
    pendencias: list[str] = []

    n_artigos = contexto["n_artigos"]
    min_artigos = contexto["min_artigos"]
    if n_artigos < min_artigos:
        pendencias.append(f"Apenas {n_artigos} artigo(s) otimizado(s) em `{READY_ARTICLES_DIR.relative_to(ROOT)}` "
                           f"— recomendado ter pelo menos {min_artigos} antes de aplicar ao AdSense.")

    faltantes = [p["slug"].strip("/") for p in site.get("compliance", {}).get("paginas_obrigatorias", [])
                 if p["slug"].strip("/") not in contexto["paginas_geradas"]]
    if faltantes:
        pendencias.append(f"Páginas legais não geradas: {', '.join(faltantes)}.")

    if contexto["duplicados"]:
        pendencias.append(f"{len(contexto['duplicados'])} par(es) de artigos com alta similaridade de conteúdo "
                           "— revisar antes de publicar todos.")

    for nome in ("robots.txt", "sitemap.xml", "ads.txt"):
        if nome not in contexto["arquivos_tecnicos"]:
            pendencias.append(f"Arquivo técnico '{nome}' não foi gerado.")

    ads_txt_placeholder_pendente = "pub-0000000000000000" in site.get("compliance", {}).get("ads_txt_placeholder", "")
    if ads_txt_placeholder_pendente:
        pendencias.append("ads.txt ainda usa o Publisher ID placeholder — atualizar com o pub-id real após a "
                           "aprovação no AdSense (nunca antes: o AdSense é quem gera esse dado).")

    if contexto["https"]["checado"] and not contexto["https"]["ok"]:
        pendencias.append(f"HTTPS não confirmado: {contexto['https']['motivo']}")

    pronto = not pendencias
    hoje = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    L = [
        f"# Relatório de prontidão para AdSense — {site['site_id']}",
        "",
        f"- **Gerado em:** {now_iso()}",
        f"- **Domínio:** {site['dominio']}",
        f"- **Status:** {'✅ PRONTO PARA APLICAR' if pronto else '⛔ PENDÊNCIAS ENCONTRADAS'}",
        "",
        "## Resumo",
        "",
        f"| Artigos otimizados | Mínimo recomendado | Páginas legais | Arquivos técnicos | Pares duplicados | HTTPS |",
        f"|---|---|---|---|---|---|",
        f"| {n_artigos} | {min_artigos} | {len(contexto['paginas_geradas'])}/{len(site.get('compliance', {}).get('paginas_obrigatorias', []))} "
        f"| {len(contexto['arquivos_tecnicos'])}/3 | {len(contexto['duplicados'])} "
        f"| {'✅' if contexto['https']['ok'] else ('não verificado' if not contexto['https']['checado'] else '⛔')} |",
        "",
    ]
    if contexto["duplicados"]:
        L += ["## Pares de artigos com alta similaridade", "", "| Artigo A | Artigo B | Similaridade |", "|---|---|---|"]
        L += [f"| {d['artigo_a']} | {d['artigo_b']} | {d['similaridade']:.0%} |" for d in contexto["duplicados"]]
        L.append("")
    L += [
        "## Performance (Lighthouse)",
        "",
        f"- {contexto['lighthouse']['motivo']}",
        "",
        "## Pendências", "",
    ]
    L += [f"- [ ] {p}" for p in pendencias] if pendencias else ["- Nenhuma. O site atende aos critérios automatizados deste agente."]
    L += [
        "",
        "## Lembrete importante",
        "",
        "Este relatório não substitui a leitura humana das páginas legais geradas (elas contêm "
        "placeholders `[PREENCHER]` que precisam de dados reais) nem a decisão final de aplicar ao "
        "AdSense, que exige aprovação humana explícita (gate `aprovacao_candidatura_adsense`).",
    ]
    return "\n".join(L) + "\n", pronto, pendencias


# --------------------------------------------------------------------------- entrypoint
def run(context: dict) -> dict:
    log = context["logger"]
    site_id = context["site_id"]
    site = context.get("site") or load_site(site_id)
    min_artigos = context.get("min_artigos") or site.get("compliance", {}).get("min_artigos_adsense", MIN_ARTIGOS_PADRAO)

    paginas_geradas = write_legal_pages(site_id, site, log)
    arquivos_tecnicos = write_technical_files(site_id, site)

    artigos = list_ready_articles()
    duplicados = check_duplicate_content(artigos)
    https = check_https(site["dominio"])
    lighthouse = check_lighthouse(site["dominio"])

    contexto = {
        "n_artigos": len(artigos), "min_artigos": min_artigos, "paginas_geradas": paginas_geradas,
        "arquivos_tecnicos": arquivos_tecnicos, "duplicados": duplicados, "https": https, "lighthouse": lighthouse,
    }
    relatorio_md, pronto, pendencias = build_readiness_report(site, contexto)

    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    report_path = COMPLIANCE_DIR / f"relatorio_prontidao_{date_str}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(relatorio_md, encoding="utf-8")

    pendencias_humanas = list(pendencias)
    pendencias_humanas.append("Revisar todas as páginas legais geradas e substituir os placeholders "
                               "`[PREENCHER]`/`[...]` por dados reais antes de publicar.")
    if pronto:
        pendencias_humanas.append("Critérios automatizados atendidos — decisão de aplicar ao AdSense ainda exige "
                                   "aprovação humana explícita (gate 'aprovacao_candidatura_adsense').")

    output = {
        "agent": AGENT_NAME,
        "schema_version": SCHEMA_VERSION,
        "site_id": site_id,
        "gerado_em": now_iso(),
        "status": "ok",  # este agente sempre "ok": a decisão de aplicar é do humano, não um bloqueio de pipeline
        "pronto_para_aplicar": pronto,
        "paginas_legais": paginas_geradas,
        "arquivos_tecnicos": arquivos_tecnicos,
        "n_artigos_otimizados": len(artigos),
        "min_artigos_recomendado": min_artigos,
        "conteudo_duplicado": duplicados,
        "https": https,
        "lighthouse": lighthouse,
        "relatorio_prontidao": str(report_path.relative_to(ROOT)),
        "pendencias_humanas": pendencias_humanas,
    }
    log.info(f"[{AGENT_NAME}] pronto={pronto} artigos={len(artigos)}/{min_artigos} paginas={len(paginas_geradas)} "
             f"→ {report_path.relative_to(ROOT)}")
    return output


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 06 — compliance de plataforma / prontidão AdSense")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    parser.add_argument("--min-artigos", type=int, dest="min_artigos", help="mínimo de artigos recomendado (default: 15)")
    args = parser.parse_args()

    load_env_file()
    run_id = f"{now_iso().replace(':', '').replace('+0000', 'Z')}-{AGENT_NAME}"
    output = run({"site_id": args.site, "min_artigos": args.min_artigos, "logger": get_logger(run_id)})
    return 0 if output["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
