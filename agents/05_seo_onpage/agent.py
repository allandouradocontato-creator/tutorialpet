"""Agente 05 — SEO On-page.

Recebe um artigo aprovado pelo agente 04 (data/quality_editor/aprovados/{slug}.md) e
otimiza os elementos técnicos de SEO — título de página, meta description, estrutura de
headings, slug, dados estruturados (JSON-LD) — sem reescrever a prosa do artigo e sem
keyword stuffing. Também identifica oportunidades de link interno, mas NUNCA insere um
link para uma página que talvez ainda não exista: isso vira uma sugestão para um humano
(ou o agente 07) aplicar quando o artigo-irmão já estiver publicado.

Uso isolado:
    python agents/05_seo_onpage/agent.py --site pets-tutores-iniciantes \
        --slug como-cortar-unha-de-cachorro
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_env_file, load_site  # noqa: E402
from core.io import normalize_term, now_iso, slugify  # noqa: E402
from core.log import get_logger  # noqa: E402
from core.markdown import MarkdownError, read_markdown, write_markdown  # noqa: E402

AGENT_NAME = "05_seo_onpage"
SCHEMA_VERSION = "1.0"
APPROVED_DIR = ROOT / "data" / "quality_editor" / "aprovados"
OUT_DIR = ROOT / "data" / "seo_onpage" / "otimizados"

TITLE_SEO_MAX = 60          # tamanho recomendado para a tag <title> nos resultados de busca
META_DESCRIPTION_MAX = 155
KEYWORD_DENSITY_MAX = 0.025  # acima disso soa "forçado" (keyword stuffing)
STOPWORDS = {"de", "da", "do", "para", "com", "em", "a", "o", "e", "que", "como", "no", "na", "os", "as", "um", "uma"}


# --------------------------------------------------------------------------- título/slug
def build_titulo_seo(titulo: str, limit: int = TITLE_SEO_MAX) -> tuple[str, bool]:
    """Trunca o título original em um limite de página de busca sem cortar palavra ao meio.
    O H1/título editorial do artigo NUNCA é alterado — isto é só a tag <title>."""
    if len(titulo) <= limit:
        return titulo, False
    truncated = titulo[:limit].rsplit(" ", 1)[0].rstrip(" -:—")
    return truncated, True


def validate_slug(slug: str, termo_origem: str) -> list[str]:
    problemas = []
    if slug != slugify(slug):
        problemas.append(f"slug '{slug}' contém caracteres fora do padrão (esperado: minúsculas, hífen).")
    if len(slug) > 75:
        problemas.append(f"slug com {len(slug)} caracteres — recomendado manter abaixo de 75.")
    termo_slug = slugify(termo_origem)
    if termo_slug not in slug and slug not in termo_slug:
        problemas.append("slug não reflete claramente o termo de origem da pauta.")
    return problemas


# --------------------------------------------------------------------------- meta description
def keyword_leads_description(meta_description: str, termo_origem: str, janela: int = 60) -> bool:
    return normalize_term(termo_origem) in normalize_term(meta_description[:janela])


def rebuild_meta_description(titulo: str, termo_origem: str, corpo_intro: str, limit: int = META_DESCRIPTION_MAX) -> str:
    """Recompõe a meta description começando pelo termo-alvo, sem inventar conteúdo novo —
    reaproveita a primeira frase do corpo do artigo como complemento."""
    base = re.sub(r"\s+", " ", f"{titulo}. {corpo_intro}").strip()
    if len(base) <= limit:
        return base
    return base[: limit - 3].rsplit(" ", 1)[0] + "..."


# --------------------------------------------------------------------------- headings
def extract_headings(body: str) -> list[tuple[int, str]]:
    headings = []
    for line in body.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            headings.append((len(m.group(1)), m.group(2).strip()))
    return headings


def check_heading_structure(headings: list[tuple[int, str]], problemas: list[str]) -> None:
    h1s = [h for h in headings if h[0] == 1]
    if len(h1s) != 1:
        problemas.append(f"esperado exatamente 1 H1 no artigo, encontrado(s) {len(h1s)}.")
    previous = 1
    for level, text in headings:
        if level > previous + 1:
            problemas.append(f"heading '{text}' pula de H{previous} para H{level} (hierarquia quebrada).")
        previous = level


def check_keyword_in_headings(headings: list[tuple[int, str]], termo_origem: str, problemas: list[str]) -> None:
    term_words = {w for w in normalize_term(termo_origem).split() if len(w) >= 4 and w not in STOPWORDS}
    if not term_words:
        return
    h2_text = normalize_term(" ".join(h[1] for h in headings if h[0] == 2))
    if not (term_words & set(h2_text.split())):
        problemas.append("nenhum H2 contém uma palavra-chave central do termo de origem — considerar ajuste manual.")


# --------------------------------------------------------------------------- densidade de palavra-chave
def strip_markdown_for_count(body: str) -> str:
    text = re.sub(r"^#{1,6}\s*", "", body, flags=re.MULTILINE)
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    return re.sub(r"[*_`]", "", text)


def keyword_density(body_plain: str, termo_origem: str) -> float:
    words = normalize_term(body_plain).split()
    if not words:
        return 0.0
    term_norm = normalize_term(termo_origem)
    n_words_term = len(term_norm.split())
    occurrences = 0
    for i in range(len(words) - n_words_term + 1):
        if " ".join(words[i:i + n_words_term]) == term_norm:
            occurrences += 1
    return round((occurrences * n_words_term) / len(words), 4)


# --------------------------------------------------------------------------- links internos (sugestões)
def suggest_internal_links(site: dict, pilar: str, termo_origem: str, max_sugestoes: int = 3) -> list[dict]:
    """Sugere artigos-irmãos do mesmo pilar como candidatos a link interno. Não insere nenhum
    link no corpo do texto: um link para uma página que ainda não existe é pior para SEO e
    para o usuário do que nenhum link. Cabe a um humano (ou ao agente 07) aplicar isso depois
    de confirmar que o artigo de destino já foi publicado."""
    sugestoes = []
    for seed in site.get("termos_semente", []):
        if seed.get("pilar") != pilar or normalize_term(seed["termo"]) == normalize_term(termo_origem):
            continue
        sugestoes.append({
            "termo_relacionado": seed["termo"],
            "slug_provavel": slugify(seed["termo"]),
            "ancora_sugerida": seed["termo"],
            "aplicar_somente_se": "o artigo de destino já estiver publicado no site",
        })
    return sugestoes[:max_sugestoes]


# --------------------------------------------------------------------------- dados estruturados
def extract_faq_pairs(body: str) -> list[tuple[str, str]]:
    faq_section = re.search(r"^## Perguntas frequentes\s*\n(.*?)(?=\n## |\Z)", body, flags=re.MULTILINE | re.DOTALL)
    if not faq_section:
        return []
    pairs = re.findall(r"\*\*(.+?)\*\*\s*\n+(.+?)(?=\n\*\*|\Z)", faq_section.group(1), flags=re.DOTALL)
    return [(q.strip(), a.strip().replace("\n", " ")) for q, a in pairs]


def build_structured_data(front_matter: dict, body: str, site: dict) -> dict:
    dominio = site.get("dominio", "").rstrip("/")
    url = f"{dominio}/{front_matter['slug']}" if dominio else None
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": front_matter["titulo"],
        "description": front_matter["meta_description"],
        "datePublished": front_matter.get("data"),
        "inLanguage": site.get("idioma", "pt-BR"),
        "author": ({"@type": "Person", "name": front_matter["autor"]} if front_matter.get("autor") else {"@type": "Organization", "name": "Equipe Tutorial Pet"}),
        **({"url": url, "mainEntityOfPage": {"@type": "WebPage", "@id": url}} if url else {}),
    }
    faq_pairs = extract_faq_pairs(body)
    if not faq_pairs:
        return {"article": article}
    faq_page = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq_pairs
        ],
    }
    return {"article": article, "faq": faq_page}


# --------------------------------------------------------------------------- entrypoint
def resolve_approved_path(context: dict) -> Path | None:
    prev = context.get("input")
    if isinstance(prev, dict) and prev.get("arquivo") and prev.get("agent") == "04_quality_editor":
        return ROOT / prev["arquivo"]
    if context.get("arquivo"):
        return ROOT / context["arquivo"]
    if context.get("slug"):
        return APPROVED_DIR / f"{context['slug']}.md"
    return None


def run(context: dict) -> dict:
    log = context["logger"]
    site_id = context["site_id"]
    site = context.get("site") or load_site(site_id)

    path = resolve_approved_path(context)
    if not path or not path.exists():
        log.warning(f"[{AGENT_NAME}] artigo aprovado não encontrado ({path})")
        return {
            "agent": AGENT_NAME, "status": "sem_artigo_aprovado",
            "mensagem": f"Artigo aprovado não encontrado: {path}. Rode o agente 04 antes deste.",
        }
    try:
        front_matter, body = read_markdown(path)
    except MarkdownError as ex:
        log.error(f"[{AGENT_NAME}] {path}: {ex}")
        return {"agent": AGENT_NAME, "status": "erro_formato", "mensagem": str(ex)}

    if front_matter.get("status") != "aprovado_qualidade":
        log.warning(f"[{AGENT_NAME}] artigo com status '{front_matter.get('status')}' — esperado 'aprovado_qualidade'")
        return {"agent": AGENT_NAME, "status": "artigo_nao_aprovado",
                "mensagem": "O artigo referenciado não está marcado como aprovado pelo agente 04."}

    termo_origem = front_matter.get("termo_origem", "")
    titulo = front_matter["titulo"]
    slug = front_matter.get("slug") or slugify(termo_origem)

    problemas: list[str] = []
    titulo_seo, titulo_truncado = build_titulo_seo(titulo)
    if titulo_truncado:
        problemas.append(f"título original ({len(titulo)} caracteres) excede o recomendado para <title> — "
                          f"gerado 'titulo_seo' truncado para uso na tag de página, H1 do artigo mantido intacto.")

    meta_description = front_matter.get("meta_description", "")
    if len(meta_description) > META_DESCRIPTION_MAX or not keyword_leads_description(meta_description, termo_origem):
        primeiro_paragrafo = next((p for p in body.split("\n\n") if p.strip() and not p.strip().startswith("#")), "")
        meta_description = rebuild_meta_description(titulo, termo_origem, primeiro_paragrafo)
        problemas.append("meta description recomposta para não ultrapassar 155 caracteres e/ou para trazer o "
                          "termo-alvo mais perto do início.")

    headings = extract_headings(body)
    check_heading_structure(headings, problemas)
    check_keyword_in_headings(headings, termo_origem, problemas)

    body_plain = strip_markdown_for_count(body)
    densidade = keyword_density(body_plain, termo_origem)
    if densidade > KEYWORD_DENSITY_MAX:
        problemas.append(f"densidade de palavra-chave em {densidade:.2%} — acima de {KEYWORD_DENSITY_MAX:.1%}, "
                          "risco de keyword stuffing; considerar variar a redação em revisão manual.")

    slug_problemas = validate_slug(slug, termo_origem)
    problemas += slug_problemas

    sugestoes_links = suggest_internal_links(site, front_matter.get("pilar", ""), termo_origem)
    structured_data = build_structured_data({**front_matter, "meta_description": meta_description}, body, site)

    jsonld_path = OUT_DIR / f"{slug}.jsonld.json"
    jsonld_path.parent.mkdir(parents=True, exist_ok=True)
    jsonld_path.write_text(json.dumps(structured_data, ensure_ascii=False, indent=2), encoding="utf-8")

    novo_front_matter = {
        **front_matter,
        "status": "otimizado_seo",
        "meta_description": meta_description,
        "titulo_seo": titulo_seo,
        "keyword_density": densidade,
        "otimizado_por_agente_05": True,
        "otimizado_em": now_iso(),
        "checagens_seo": problemas,
        "sugestoes_links_internos": sugestoes_links,
        "dados_estruturados_arquivo": str(jsonld_path.relative_to(ROOT)),
    }
    out_path = write_markdown(OUT_DIR / f"{slug}.md", novo_front_matter, body)

    pendencias = ["Seguir para o agente 06 (platform compliance) e depois para a aprovação final de publicação."]
    if problemas:
        pendencias += [f"[seo] {p}" for p in problemas]
    if sugestoes_links:
        pendencias.append(f"{len(sugestoes_links)} sugestão(ões) de link interno registrada(s) — aplicar manualmente "
                           "assim que os artigos-irmãos estiverem publicados (ver 'sugestoes_links_internos').")

    output = {
        "agent": AGENT_NAME,
        "schema_version": SCHEMA_VERSION,
        "site_id": site_id,
        "gerado_em": now_iso(),
        "status": "ok",
        "arquivo": str(out_path.relative_to(ROOT)),
        "dados_estruturados_arquivo": str(jsonld_path.relative_to(ROOT)),
        "slug": slug,
        "titulo": titulo,
        "titulo_seo": titulo_seo,
        "termo_origem": termo_origem,
        "pilar": front_matter.get("pilar"),
        "sensivel_ymyl": bool(front_matter.get("aviso_saude_aplicavel")),
        "keyword_density": densidade,
        "checagens": problemas,
        "sugestoes_links_internos": sugestoes_links,
        "pendencias_humanas": pendencias,
    }
    log.info(f"[{AGENT_NAME}] {slug}: otimizado ({len(problemas)} observação(ões), "
             f"densidade={densidade:.2%}) → {out_path.relative_to(ROOT)}")
    return output


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 05 — otimização SEO on-page (uso isolado)")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--slug", help="slug do artigo em data/quality_editor/aprovados/")
    group.add_argument("--arquivo", help="caminho do .md a otimizar, relativo à raiz do projeto")
    args = parser.parse_args()

    load_env_file()
    run_id = f"{now_iso().replace(':', '').replace('+0000', 'Z')}-{AGENT_NAME}"
    output = run({"site_id": args.site, "slug": args.slug, "arquivo": args.arquivo, "logger": get_logger(run_id)})
    return 0 if output["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
