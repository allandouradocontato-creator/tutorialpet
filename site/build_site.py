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

from core.config import load_env_file, load_site, load_yaml  # noqa: E402
from core.markdown import MarkdownError, read_markdown  # noqa: E402
from core.theme import BASE_CSS, GOOGLE_FONT_HEAD, PILAR_VISUAL, PILAR_VISUAL_PADRAO  # noqa: E402

# Google Analytics 4 (propriedade tutorialpet.com.br, criada em 06/10/2026)
GA_ID = "G-HP7ZXLFBXH"
GA_TAG = (
    f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
    "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
    f"gtag('js',new Date());gtag('config','{GA_ID}');</script>"
)

OTIMIZADOS_DIR = ROOT / "data" / "seo_onpage" / "otimizados"
LEGAL_DIR = ROOT / "data" / "platform_compliance" / "paginas_legais"
TECH_DIR = ROOT / "data" / "platform_compliance" / "arquivos_tecnicos"
BUILD_DIR = ROOT / "site" / "build"
PRODUTOS_PATH = ROOT / "config" / "produtos_relacionados.yaml"

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


# CSS unificado em core/theme.py (paleta de marca + tipografia), compartilhado com o
# agente 07 — antes cada um tinha sua própria cópia quase idêntica, que podia divergir
# sem ninguém perceber.
CSS = BASE_CSS


def render_header(site_nome: str, pilares: dict[str, str]) -> str:
    links = "".join(f'<a href="/#{key}">{html_lib.escape(nome)}</a>' for key, nome in pilares.items())
    return f"""<header class="site">
<a href="/" class="brand">{html_lib.escape(site_nome)}</a>
<nav>{links}</nav>
</header>"""


def render_footer() -> str:
    links = "".join(
        f'<a href="/{slug}">{LEGAL_PAGES_TITULOS[slug]}</a>' for slug in LEGAL_PAGES_ORDER
    )
    ano = datetime.now(timezone.utc).year
    return (f'<footer class="site">{links}<p>© {ano} Tutorial Pet — conteúdo informativo, '
            f'não substitui orientação veterinária profissional.</p></footer>')


def page_shell(title: str, meta_description: str, canonical: str, og_type: str, body_html: str,
               extra_head: str = "", og_image: str = "") -> str:
    og_image_tag = f'<meta property="og:image" content="{html_lib.escape(og_image)}">' if og_image else ""
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
{og_image_tag}
{GOOGLE_FONT_HEAD}
{GA_TAG}
{extra_head}
<style>{CSS}</style>
</head>
<body>
{body_html}
</body>
</html>
"""


def load_produto_destaque(fm: dict) -> dict | None:
    """Escolhe o produto cadastrado em config/produtos_relacionados.yaml que mais combina com o
    artigo (por palavras-chave); empate ou nenhuma palavra casando cai no primeiro produto."""
    try:
        cfg = load_yaml(PRODUTOS_PATH) or {}
    except Exception:
        return None
    produtos = [p for p in (cfg.get("produtos") or []) if p.get("link")]
    if not produtos:
        return None
    texto = " ".join(str(fm.get(k, "")) for k in ("slug", "titulo", "titulo_seo", "meta_description")).lower()
    return max(produtos, key=lambda p: sum(1 for kw in (p.get("palavras_chave") or []) if str(kw).lower() in texto))


def render_produto_topo(produto: dict | None) -> str:
    """Faixa do produto, usada NO COMEÇO e no fim de todo artigo (regra de 05/10/2026)."""
    if not produto:
        return ""
    chamada = produto.get("chamada_topo") or f"Conheça {produto['nome']}"
    botao = produto.get("botao_topo") or "Conhecer"
    return (f'<aside class="produto-topo"><p class="produto-topo-texto">🐾 {html_lib.escape(chamada)}</p>'
            f'<a class="btn" rel="noopener" href="{html_lib.escape(produto["link"])}">{html_lib.escape(botao)}</a></aside>')


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

    jsonld_scripts = jsonld_scripts.replace(
        '{"@type": "Person", "name": "PREENCHER_APOS_APROVACAO_HUMANA"}',
        '{"@type": "Organization", "name": "Tutorial Pet"}')

    autor = (fm.get("autor") or "").strip()
    byline = (f'<p class="byline">Por {html_lib.escape(autor)}</p>' if autor
              else (f'<p class="byline">Por {html_lib.escape((fm.get("assinatura") or "Equipe Tutorial Pet").strip())}</p>'))

    breadcrumb = (f'<div class="breadcrumb"><a href="/">Início</a> &gt; '
                  f'<a href="/#{pilar_key}">{html_lib.escape(pilar_titulo)}</a> &gt; {html_lib.escape(fm["titulo"])}</div>')

    imagem_capa = fm.get("imagem_capa")
    og_image = f"{dominio}/{imagem_capa}" if imagem_capa else ""
    hero_img = ""
    if imagem_capa:
        hero_img = f'<img class="hero-img" src="/{imagem_capa}" alt="{html_lib.escape(fm["titulo"])}">'
        fotografo, fonte_url = fm.get("imagem_fotografo"), fm.get("imagem_fotografo_url")
        if fotografo and fonte_url:
            fonte_nome = (fm.get("imagem_fonte") or "").capitalize()
            hero_img += (f'<p class="image-credit">Foto: <a href="{html_lib.escape(fonte_url)}">'
                         f'{html_lib.escape(fotografo)}</a> via {html_lib.escape(fonte_nome)}</p>')

    body_html = md_to_html(body)
    produto_faixa = render_produto_topo(load_produto_destaque(fm))
    cta = (f'<div class="cta-box"><p>Gostou deste guia? Tem mais conteúdo sobre '
           f'{html_lib.escape(pilar_titulo.lower())} esperando por você.</p>'
           f'<a class="btn" href="/#{pilar_key}">Ver mais sobre {html_lib.escape(pilar_titulo)}</a></div>')
    main = f"""{render_header(site["nome"], pilares)}
{breadcrumb}
<main class="article">
{produto_faixa}
{hero_img}
{byline}
{body_html}
{produto_faixa}
{cta}
</main>
{render_footer()}"""
    return page_shell(titulo_seo, fm.get("meta_description", ""), canonical, "article", main, jsonld_scripts,
                       og_image=og_image)


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
        visual = PILAR_VISUAL.get(pilar_key, PILAR_VISUAL_PADRAO)
        cards = "".join(
            f'<div class="card"><a class="card-link" href="/{fm["slug"]}">'
            + (f'<img class="card-cover" src="/{fm["imagem_capa"]}" alt="{html_lib.escape(fm["titulo"])}">'
               if fm.get("imagem_capa") else
               f'<div class="card-cover" style="background:{visual["bg"]}">{visual["emoji"]}</div>')
            + f'<div class="card-body"><div class="card-title">{html_lib.escape(fm["titulo"])}</div></div>'
            f'</a></div>'
            for fm in itens
        )
        sections.append(
            f'<section class="pilar-section" id="{pilar_key}">'
            f'<h2>{html_lib.escape(titulo)} <span class="pilar-tag">{len(itens)} artigo(s)</span></h2>'
            f'<div class="card-grid">{cards}</div></section>'
        )

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

    n_imagens = 0
    imagens_src = ROOT / "data" / "visual" / "imagens"
    if imagens_src.exists():
        imagens_dst = BUILD_DIR / "imagens"
        imagens_dst.mkdir(parents=True, exist_ok=True)
        for fm, _, _ in artigos:
            imagem_capa = fm.get("imagem_capa")
            if not imagem_capa:
                continue
            nome_arquivo = Path(imagem_capa).name
            origem = imagens_src / nome_arquivo
            if origem.exists():
                (imagens_dst / nome_arquivo).write_bytes(origem.read_bytes())
                n_imagens += 1

    (BUILD_DIR / "index.html").write_text(build_home_page(site, pilares, artigos_por_pilar), encoding="utf-8")
    (BUILD_DIR / "sitemap.xml").write_text(build_sitemap(site, [fm for fm, _, _ in artigos]), encoding="utf-8")
    (BUILD_DIR / "robots.txt").write_text(build_robots(site), encoding="utf-8")

    ads_txt_src = TECH_DIR / site_id / "ads.txt"
    if ads_txt_src.exists():
        (BUILD_DIR / "ads.txt").write_text(ads_txt_src.read_text(encoding="utf-8"), encoding="utf-8")

    (BUILD_DIR / "vercel.json").write_text(json.dumps({"cleanUrls": True, "trailingSlash": False}, indent=2),
                                            encoding="utf-8")

    return {
        "n_artigos": len(artigos), "n_paginas_legais": len(legal_gerados), "n_imagens": n_imagens,
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
    print(f"  Imagens publicadas: {resultado['n_imagens']}")
    print(f"  Arquivos: {', '.join(resultado['arquivos_gerados'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
