"""Agente 14 — Distribuição & Produtos Derivados.

Pós-lançamento, chamado separadamente (nunca faz parte do fluxo principal 1→13 do
orchestrator, igual aos agentes 08/09/10): agrupa artigos já otimizados em e-books por
pilar, gera legendas de redes sociais e sugere (sem nunca inserir sozinho) onde um CTA de
produto relacionado faria sentido.

TRAVA DE ATIVAÇÃO — a primeira coisa que este agente confere, antes de qualquer outra
lógica: só gera output real quando (1) monetizacao.status_adsense do site é "aprovado" E
(2) o site já tem pelo menos o mínimo de artigos otimizados configurado. Mesmo padrão do
agente 09 (config/sites/<site>.yaml), reaproveitado aqui — sem importar o agente 09, só
repetindo a mesma ideia de checagem.

Uso isolado:
    python agents/14_social_produtos/agent.py --site pets-tutores-iniciantes
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_env_file, load_publishing_schedule, load_site, load_yaml  # noqa: E402
from core.io import normalize_term, now_iso, slugify  # noqa: E402
from core.log import get_logger  # noqa: E402
from core.markdown import MarkdownError, read_markdown, write_markdown  # noqa: E402
from simple_pdf import SimplePDF  # noqa: E402

AGENT_NAME = "14_social_produtos"
SCHEMA_VERSION = "1.0"

OTIMIZADOS_DIR = ROOT / "data" / "seo_onpage" / "otimizados"
SOCIAL_DIR = ROOT / "data" / "social_produtos"
EBOOKS_DIR = SOCIAL_DIR / "ebooks"
CTA_DIR = SOCIAL_DIR / "sugestoes_cta"
STATUS_QUE_ATIVA = "aprovado"


# --------------------------------------------------------------------------- trava de ativação
def check_ativacao(site: dict, site_id: str, schedule_cfg: dict, n_artigos: int) -> tuple[bool, list[str]]:
    """Mesma lógica de trava do agente 09 (status_adsense == 'aprovado'), somada à checagem
    de volume mínimo de catálogo. As duas precisam ser verdadeiras."""
    motivos = []
    status_adsense = (site.get("monetizacao") or {}).get("status_adsense", "nao_aplicado")
    if status_adsense != STATUS_QUE_ATIVA:
        motivos.append(f"status_adsense = '{status_adsense}' (precisa ser 'aprovado') em "
                        f"config/sites/{site_id}.yaml → monetizacao.status_adsense.")
    minimo = schedule_cfg.get("minimo_artigos_para_distribuicao", 15)
    if n_artigos < minimo:
        motivos.append(f"{n_artigos} artigo(s) otimizado(s) em data/seo_onpage/otimizados/, abaixo do "
                        f"mínimo configurado ({minimo}) em config/publishing_schedule.yaml → "
                        "minimo_artigos_para_distribuicao.")
    return (not motivos), motivos


# --------------------------------------------------------------------------- leitura de artigos
def load_optimized_articles() -> list[tuple[dict, str, Path]]:
    artigos = []
    if not OTIMIZADOS_DIR.exists():
        return artigos
    for path in sorted(OTIMIZADOS_DIR.glob("*.md")):
        try:
            fm, body = read_markdown(path)
        except MarkdownError:
            continue
        artigos.append((fm, body, path))
    return artigos


# --------------------------------------------------------------------------- gerador de e-books
def markdown_to_pdf_blocks(doc: SimplePDF, body: str) -> None:
    """Reorganiza o corpo do artigo em blocos de PDF, sem reescrever ou resumir nada — cada
    linha de texto do artigo original é preservada, só convertida de Markdown para blocos de
    parágrafo/heading."""
    lines = body.split("\n")
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue
        header = re.match(r"^(#{1,6})\s+(.*)", stripped)
        if header:
            style = "h1" if len(header.group(1)) <= 2 else "h2"
            doc.add_heading(header.group(2), style)
            i += 1
            continue
        if stripped.startswith(">"):
            quote_parts = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_parts.append(lines[i].strip().lstrip(">").strip())
                i += 1
            doc.add_paragraph("Aviso: " + " ".join(quote_parts), "citacao")
            continue
        if stripped.startswith("- "):
            while i < len(lines) and lines[i].strip().startswith("- "):
                doc.add_paragraph("• " + lines[i].strip()[2:], "corpo")
                i += 1
            continue
        paragraph = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,6})\s+", lines[i].strip()) \
                and not lines[i].strip().startswith((">", "- ")):
            paragraph.append(lines[i].strip())
            i += 1
        texto = re.sub(r"\*\*(.+?)\*\*", r"\1", " ".join(paragraph))
        doc.add_paragraph(texto, "corpo")


def build_ebook(pilar_key: str, pilar_titulo: str, artigos: list[tuple[dict, str, Path]]) -> Path:
    doc = SimplePDF()
    doc.add_cover(pilar_titulo, f"{len(artigos)} artigo(s) — coletânea gerada automaticamente")

    doc.add_heading("Sumário", "h1")
    for fm, _, _ in artigos:
        doc.add_paragraph(fm.get("titulo", fm.get("slug", "?")))
    doc.new_page()

    for fm, body, _ in artigos:
        doc.add_heading(fm.get("titulo", fm.get("slug", "?")), "h1")
        markdown_to_pdf_blocks(doc, body)
        doc.new_page()

    out_path = EBOOKS_DIR / f"{pilar_key}.pdf"
    doc.save(out_path)
    return out_path


def generate_ebooks(artigos: list[tuple[dict, str, Path]], site: dict) -> dict[str, str]:
    pilares_nomes = site.get("pilares", {})
    por_pilar: dict[str, list] = {}
    for item in artigos:
        pilar = item[0].get("pilar") or "outros"
        por_pilar.setdefault(pilar, []).append(item)

    gerados = {}
    for pilar_key, itens in por_pilar.items():
        titulo = pilares_nomes.get(pilar_key, pilar_key.replace("_", " ").title())
        path = build_ebook(pilar_key, titulo, itens)
        gerados[pilar_key] = str(path.relative_to(ROOT))
    return gerados


# --------------------------------------------------------------------------- calendário social
def first_paragraph(body: str) -> str:
    for bloco in body.split("\n\n"):
        texto = bloco.strip()
        if texto and not texto.startswith(("#", ">", "-")):
            return re.sub(r"\*\*(.+?)\*\*", r"\1", texto)
    return ""


def build_social_caption(fm: dict, body: str, dominio: str) -> str:
    gancho = first_paragraph(body)
    resumo = fm.get("meta_description", "")
    link = f"{dominio.rstrip('/')}/{fm.get('slug', '')}" if dominio else "[LINK_DO_ARTIGO]"
    hashtag_pilar = "#" + re.sub(r"[^a-z0-9]", "", normalize_term(fm.get("pilar", "pets")))
    return (
        f"🐾 {gancho}\n\n"
        f"{resumo}\n\n"
        f"📖 Artigo completo: {link}\n\n"
        f"#dicasdepet #tutordeprimeiraviagem {hashtag_pilar}"
    )


def generate_social_calendar(artigos: list[tuple[dict, str, Path]], site: dict) -> str:
    dominio = site.get("dominio", "")
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = SOCIAL_DIR / f"calendario_social_{date_str}.md"

    L = [f"# Calendário de conteúdo social — {site['site_id']}", "", f"Gerado em: {now_iso()}", "",
         "Legendas para revisão e postagem manual (Instagram/Facebook) — nenhuma publicação "
         "automática é feita por este agente.", ""]
    for fm, body, _ in artigos:
        L += [f"## {fm.get('titulo', fm.get('slug'))}", "", "```", build_social_caption(fm, body, dominio), "```", ""]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(L), encoding="utf-8")
    return str(out_path.relative_to(ROOT))


# --------------------------------------------------------------------------- sugestões de CTA
def load_produtos_relacionados() -> list[dict]:
    raw = load_yaml(ROOT / "config" / "produtos_relacionados.yaml")
    return raw.get("produtos") or []


def find_matching_products(fm: dict, produtos: list[dict]) -> list[dict]:
    alvo = normalize_term(f"{fm.get('termo_origem', '')} {fm.get('titulo', '')} {fm.get('pilar', '')}")
    encontrados = []
    for produto in produtos:
        palavras = [normalize_term(p) for p in produto.get("palavras_chave", [])]
        if any(p in alvo for p in palavras):
            encontrados.append(produto)
    return encontrados


def generate_cta_suggestions(artigos: list[tuple[dict, str, Path]], produtos: list[dict]) -> list[str]:
    if not produtos:
        return []
    gerados = []
    for fm, body, _ in artigos:
        matches = find_matching_products(fm, produtos)
        if not matches:
            continue
        slug = fm.get("slug") or "artigo"
        front_matter = {
            "slug": slug, "titulo_artigo": fm.get("titulo"), "gerado_em": now_iso(),
            "status": "sugestao_nao_aplicada",
        }
        corpo = [f"## Produtos relacionados encontrados para \"{fm.get('titulo')}\"", ""]
        for produto in matches:
            corpo += [
                f"### {produto.get('nome', '(sem nome)')}", "",
                produto.get("descricao", ""), "",
                f"- Link: {produto.get('link', '[PREENCHER_LINK_REAL_DO_PRODUTO]')}",
                "- Onde um CTA discreto faria sentido: perto da conclusão do artigo, ou logo "
                "após a seção que menciona o tópico relacionado.",
                "",
            ]
        corpo.append("*Esta é só uma sugestão — nenhum CTA foi inserido no artigo. A decisão e "
                     "a edição do texto continuam sempre humanas.*")
        path = write_markdown(CTA_DIR / f"{slug}.md", front_matter, "\n".join(corpo))
        gerados.append(str(path.relative_to(ROOT)))
    return gerados


# --------------------------------------------------------------------------- relatório de bloqueio
def render_blocked_report(site_id: str, motivos: list[str], n_artigos: int) -> str:
    L = [
        f"# Agente 14 — aguardando requisitos ({site_id})", "",
        f"- **Gerado em:** {now_iso()}",
        f"- **Status:** ⛔ aguardando_requisitos",
        f"- **Artigos otimizados atualmente:** {n_artigos}",
        "",
        "## O que falta para ativar", "",
    ]
    L += [f"- [ ] {m}" for m in motivos]
    L += [
        "",
        "## O que este agente fará quando ativado", "",
        "- E-book em PDF por pilar, agrupando os artigos já otimizados (sem reescrever nada).",
        "- Calendário de legendas para redes sociais, uma por artigo (revisão e postagem manuais).",
        "- Sugestões de CTA para produtos cadastrados em `config/produtos_relacionados.yaml` "
        "(nunca inseridas automaticamente).",
        "",
        "Nenhum desses três itens é gerado enquanto as pendências acima não forem resolvidas.",
    ]
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- entrypoint
def run(context: dict) -> dict:
    log = context["logger"]
    site_id = context["site_id"]
    site = context.get("site") or load_site(site_id)
    schedule_cfg = load_publishing_schedule(site_id)

    artigos = load_optimized_articles()
    ativo, motivos = check_ativacao(site, site_id, schedule_cfg, len(artigos))

    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    SOCIAL_DIR.mkdir(parents=True, exist_ok=True)

    if not ativo:
        relatorio_md = render_blocked_report(site_id, motivos, len(artigos))
        out_path = SOCIAL_DIR / f"relatorio_{date_str}.md"
        out_path.write_text(relatorio_md, encoding="utf-8")
        log.warning(f"[{AGENT_NAME}] modo aguardando_requisitos: {'; '.join(motivos)}")
        output = {
            "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "site_id": site_id, "gerado_em": now_iso(),
            "status": "aguardando_requisitos", "n_artigos_otimizados": len(artigos),
            "relatorio": str(out_path.relative_to(ROOT)), "pendencias_humanas": motivos,
        }
        return output

    ebooks = generate_ebooks(artigos, site)
    calendario = generate_social_calendar(artigos, site)
    produtos = load_produtos_relacionados()
    sugestoes = generate_cta_suggestions(artigos, produtos)

    pendencias = [f"{len(ebooks)} e-book(s) gerado(s) em {EBOOKS_DIR.relative_to(ROOT)} — revisar antes de distribuir.",
                  f"Calendário social em {calendario} — revisar e postar manualmente."]
    if sugestoes:
        pendencias.append(f"{len(sugestoes)} sugestão(ões) de CTA de produto geradas — revisar antes de aplicar "
                           "qualquer alteração nos artigos.")
    elif not produtos:
        pendencias.append("config/produtos_relacionados.yaml está vazio — cadastre produtos para receber "
                           "sugestões de CTA.")

    output = {
        "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "site_id": site_id, "gerado_em": now_iso(),
        "status": "ok", "n_artigos_otimizados": len(artigos), "ebooks": ebooks,
        "calendario_social": calendario, "sugestoes_cta": sugestoes, "pendencias_humanas": pendencias,
    }
    log.info(f"[{AGENT_NAME}] ativo=True ebooks={len(ebooks)} calendario={calendario} sugestoes_cta={len(sugestoes)}")
    return output


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 14 — distribuição e produtos derivados (pós-lançamento)")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    args = parser.parse_args()

    load_env_file()
    run_id = f"{now_iso().replace(':', '').replace('+0000', 'Z')}-{AGENT_NAME}"
    output = run({"site_id": args.site, "logger": get_logger(run_id)})
    return 0 if output["status"] in ("ok", "aguardando_requisitos") else 2


if __name__ == "__main__":
    sys.exit(main())
