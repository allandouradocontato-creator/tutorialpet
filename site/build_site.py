"""Monta o site estático final em site/build/, pronto para deploy.

Este script fica FORA de agents/ e de orchestrator.py de propósito: é uma ferramenta de
montagem de site, não um agente do pipeline de produção. Reaproveita a função pura de
conversão Markdown→HTML do agente 07 (agents/07_publisher/agent.py, markdown_to_html_body
— importada, não copiada nem modificada), mas usa seu PRÓPRIO template de página: sem a
faixa de "prévia/simulação" do agente 07 (que não faz sentido num site pronto para
deploy), com navegação real (início, pilar, rodapé com páginas legais) e URLs/meta tags
apontando para o domínio real do site.

Uso:
    python site/build_site.py --site pets-tutores-iniciantes
"""
from __future__ import annotations

import argparse
import html as html_lib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.config import load_env_file, load_site  # noqa: E402
from core.markdown import MarkdownError, read_markdown  # noqa: E402

OTIMIZADOS_DIR = ROOT / "data" / "seo_onpage" / "otimizados"
LEGAL_DIR = ROOT / "data" / "platform_compliance" / "paginas_legais"
TECH_DIR = ROOT / "data" / "platform_compliance" / "arquivos_tecnicos"
BUILD_DIR = ROOT / "site" / "build"

LEGAL_PAGES_ORDER = ["sobre", "contato", "politica-de-privacidade", "termos"]
LEGAL_PAGES_TITULOS = {"sobre": "Sobre", "contato": "Contato",
                        "politica-de-privacidade": "Política de Privacidade", "termos": "Termos de Uso"}


def load_agent07_markdown_converter():
    """Importa agents/07_publisher/agent.py só para reaproveitar markdown_to_html_body —
    não instancia nem chama nada que dependa do gate de aprovação do agente 07."""
    path = ROOT / "agents" / "07_publisher" / "agent.py"
    spec = importlib.util.spec_from_file_location("agent_07_publisher_reuso", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.markdown_to_html_body


CSS = """
:root { color-scheme: light; }
body { margin: 0; font-family: -apple-system, Segoe UI, Roboto, Arial, sans-serif; background: #fafaf7; color: #262220; }
header.site { background: #2f4538; color: #fff; padding: 14px 20px; }
header.site a { color: #fff; text-decoration: none; font-weight: 600; }
header.site nav { margin-top: 6px; font-size: 14px; }
header.site nav a { margin-right: 14px; opacity: 0.9; }
.breadcrumb { max-width: 760px; margin: 16px auto 0; padding: 0 20px; font-size: 13px; color: #6b645f; }
.breadcrumb a { color: #2f4538; }
main.article, main.legal { max-width: 760px; margin: 0 auto; padding: 16px 20px 48px; }
main.home { max-width: 960px; margin: 0 auto; padding: 24px 20px 48px; }
h1 { font-size: 1.9rem; line-height: 1.25; }
h2 { font-size: 1.35rem; margin-top: 2em; }
h3 { font-size: 1.1rem; margin-top: 1.4em; }
p { line-height: 1.7; font-size: 1.05rem; }
blockquote { border-left: 4px solid #d99a2b; background: #fff8ec; margin: 1.5em 0; padding: 0.8em 1.2em; font-size: 0.98rem; }
ul { line-height: 1.7; }
.byline { font-size: 0.9rem; color: #6b645f; margin-top: -0.5em; }
.pilar-section { margin-top: 2.5em; }
.pilar-section h2 { border-bottom: 2px solid #e5e0d8; padding-bottom: 6px; }
.pilar-section ul { list-style: none; padding: 0; }
.pilar-section li { padding: 8px 0; border-bottom: 1px solid #efece5; }
.pilar-section a { color: #2f4538; text-decoration: none; font-size: 1.05rem; }
.pilar-section a:hover { text-decoration: underline; }
footer.site { max-width: 960px; margin: 32px auto 0; padding: 20px 20px 40px; font-size: 0.85rem; color: #6b645f; border-top: 1px solid #e5e0d8; }
footer.site a { color: #6b645f; margin-right: 12px; }
.hero { padding: 40px 0 10px; }
.hero p { font-size: 1.1rem; color: #4a453f; }
"""


def render_header(site_nome: str, pilares: dict[str, str]) -> str:
    links = "".join(f'<a href="/#{key}">{html_lib.escape(nome)}</a>' for key, nome in pilares.items())
    return f"""<header class="site">
<a href="/">{html_lib.escape(site_nome)}</a>
<nav>{links}</nav>
</header>"""


def render_footer() -> str:
    links = "".join(
        f'<a href="/{slug}">{LEGAL_PAGES_TITULOS[slug]}</a>' for slug in LEGAL_PAGES_ORDER
    )
    ano = datetime.now(timezone.utc).year
    return (f'<footer class="site">{links}<p>© {ano} Tutor de Primeira Viagem — conteúdo informativo, '
            f'não substitui orientação veterinária profissional.</p></footer>')


def page_shell(title: str, meta_description: str, canonical: str, og_type: str, body_html: str,
               extra_head: str = "") -> str:
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_lib.escape(title)}</title>
<meta name="description" content="{html_lib.escape(meta_description)}">
<link rel="canonical" href="{html_lib.escape(canonical)}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html_lib.escape(title)}">
<meta property="og:description" content="{html_lib.escape(meta_description)}">
<meta property="og:url" content="{html_lib.escape(canonical)}">
<meta property="og:locale" content="pt_BR">
{extra_head}
<style>{CSS}</style>
</head>
<body>
{body_html}
</body>
</html>
"""


def build_article_page(fm: dict, body: str, structured_data: dict, site: dict, pilares: dict,
                        md_to_html) -> str:
    dominio = site["dominio"].rstrip("/")
    slug = fm["slug"]
    pilar_key = fm.get("pilar", "")
    pilar_titulo = pilares.get(pilar_key, pilar_key.replace("_", " ").title())
    canonical = f"{dominio}/{slug}"
    titulo_seo = fm.get("titulo_seo") or fm["titulo"]

    jsonld_scripts = "\n".join(
        f'<script type="application/ld+json">{json.dumps(v, ensure_ascii=False)}</script>'
        for v in structured_data.values()
    )

    autor = (fm.get("autor") or "").strip()
    byline = (f'<p class="byline">Por {html_lib.escape(autor)}</p>' if autor
              else '<p class="byline">Autoria: [PREENCHER — pessoa real cadastrada em /sobre antes de publicar]</p>')

    breadcrumb = (f'<div class="breadcrumb"><a href="/">Início</a> &gt; '
                  f'<a href="/#{pilar_key}">{html_lib.escape(pilar_titulo)}</a> &gt; {html_lib.escape(fm["titulo"])}</div>')

    body_html = md_to_html(body)
    main = f"""{render_header(site["nome"], pilares)}
{breadcrumb}
<main class="article">
{byline}
{body_html}
</main>
{render_footer()}"""
    return page_shell(titulo_seo, fm.get("meta_description", ""), canonical, "article", main, jsonld_scripts)


def build_legal_page(slug: str, fm: dict, body: str, site: dict, pilares: dict, md_to_html) -> str:
    dominio = site["dominio"].rstrip("/")
    canonical = f"{dominio}/{slug}"
    body_html = md_to_html(body)
    main = f"""{render_header(site["nome"], pilares)}
<main class="legal">
{body_html}
</main>
{render_footer()}"""
    return page_shell(fm.get("titulo", slug), site["nicho"][:150], canonical, "website", main)


def build_home_page(site: dict, pilares: dict, artigos_por_pilar: dict) -> str:
    dominio = site["dominio"].rstrip("/")
    sections = []
    for pilar_key, titulo in pilares.items():
        itens = artigos_por_pilar.get(pilar_key, [])
        if not itens:
            continue
        links = "".join(
            f'<li><a href="/{fm["slug"]}">{html_lib.escape(fm["titulo"])}</a></li>' for fm in itens
        )
        sections.append(f'<section class="pilar-section" id="{pilar_key}"><h2>{html_lib.escape(titulo)}</h2><ul>{links}</ul></section>')

    main = f"""{render_header(site["nome"], pilares)}
<main class="home">
<div class="hero"><h1>{html_lib.escape(site["nome"])}</h1><p>{html_lib.escape(site["nicho"])}</p></div>
{''.join(sections)}
</main>
{render_footer()}"""
    return page_shell(site["nome"], site["nicho"][:155], f"{dominio}/", "website", main)


def build_sitemap(site: dict, artigos: list[dict]) -> str:
    dominio = site["dominio"].rstrip("/")
    urls = [f"{dominio}/"] + [f"{dominio}/{slug}" for slug in LEGAL_PAGES_ORDER] + \
           [f"{dominio}/{fm['slug']}" for fm in artigos]
    entries = "\n".join(f"  <url>\n    <loc>{u}</loc>\n  </url>" for u in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n"
    )


def build_robots(site: dict) -> str:
    dominio = site["dominio"].rstrip("/")
    return f"User-agent: *\nAllow: /\n\nSitemap: {dominio}/sitemap.xml\n"


def run(site_id: str) -> dict:
    site = load_site(site_id)
    md_to_html = load_agent07_markdown_converter()
    pilares = site.get("pilares", {})

    artigos = []
    for path in sorted(OTIMIZADOS_DIR.glob("*.md")):
        try:
            fm, body = read_markdown(path)
        except MarkdownError:
            continue
        jsonld_path = ROOT / fm.get("dados_estruturados_arquivo", "")
        structured_data = json.loads(jsonld_path.read_text(encoding="utf-8")) if jsonld_path.exists() else {}
        artigos.append((fm, body, structured_data))

    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    artigos_por_pilar: dict[str, list[dict]] = {}
    for fm, body, structured_data in artigos:
        pilar_key = fm.get("pilar", "outros")
        artigos_por_pilar.setdefault(pilar_key, []).append(fm)
        html_out = build_article_page(fm, body, structured_data, site, pilares, md_to_html)
        (BUILD_DIR / f"{fm['slug']}.html").write_text(html_out, encoding="utf-8")

    legal_gerados = []
    legal_dir = LEGAL_DIR / site_id
    for slug in LEGAL_PAGES_ORDER:
        legal_path = legal_dir / f"{slug}.md"
        if not legal_path.exists():
            continue
        fm, body = read_markdown(legal_path)
        html_out = build_legal_page(slug, fm, body, site, pilares, md_to_html)
        (BUILD_DIR / f"{slug}.html").write_text(html_out, encoding="utf-8")
        legal_gerados.append(slug)

    (BUILD_DIR / "index.html").write_text(build_home_page(site, pilares, artigos_por_pilar), encoding="utf-8")
    (BUILD_DIR / "sitemap.xml").write_text(build_sitemap(site, [fm for fm, _, _ in artigos]), encoding="utf-8")
    (BUILD_DIR / "robots.txt").write_text(build_robots(site), encoding="utf-8")

    ads_txt_src = TECH_DIR / site_id / "ads.txt"
    if ads_txt_src.exists():
        (BUILD_DIR / "ads.txt").write_text(ads_txt_src.read_text(encoding="utf-8"), encoding="utf-8")

    (BUILD_DIR / "vercel.json").write_text(json.dumps({"cleanUrls": True, "trailingSlash": False}, indent=2),
                                            encoding="utf-8")

    return {
        "n_artigos": len(artigos), "n_paginas_legais": len(legal_gerados),
        "arquivos_gerados": sorted(p.name for p in BUILD_DIR.iterdir()),
        "build_dir": str(BUILD_DIR.relative_to(ROOT)),
    }


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Monta o site estático final em site/build/")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    args = parser.parse_args()

    load_env_file()
    resultado = run(args.site)
    print(f"Site montado em {resultado['build_dir']}")
    print(f"  Artigos: {resultado['n_artigos']}")
    print(f"  Páginas legais: {resultado['n_paginas_legais']}")
    print(f"  Arquivos: {', '.join(resultado['arquivos_gerados'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
