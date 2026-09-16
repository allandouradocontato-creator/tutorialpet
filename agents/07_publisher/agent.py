"""Agente 07 — Publisher.

Pega um artigo otimizado pelo agente 05 (data/seo_onpage/otimizados/) e "publica" — nesta
fase, só em MODO SIMULAÇÃO: gera o HTML final (meta tags + JSON-LD do agente 05 incluídos)
pronto para upload manual e abertura no navegador, em data/publisher/simulado/{slug}.html.

O MODO REAL (WordPress REST API / Ghost Admin API) está estruturado mas desligado —
ver MODO_REAL_HABILITADO abaixo e prompt.md para o que cada conector vai precisar.

Este agente nunca gera nada (nem em modo simulação) sem:
  1. o gate humano 'aprovacao_publicacao' registrado (aprovado ou simulado em dry-run);
  2. as páginas legais e os arquivos técnicos do agente 06 presentes no disco.

Uso isolado:
    python agents/07_publisher/agent.py --site pets-tutores-iniciantes \
        --slug como-cortar-unha-de-cachorro --run-dir data/runs/<run_id>
"""
from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_env_file, load_publishing_schedule, load_site  # noqa: E402
from core.io import normalize_term, now_iso, read_json, write_json  # noqa: E402
from core.log import get_logger  # noqa: E402
from core.markdown import MarkdownError, read_markdown, write_markdown  # noqa: E402

AGENT_NAME = "07_publisher"
SCHEMA_VERSION = "1.0"

OTIMIZADOS_DIR = ROOT / "data" / "seo_onpage" / "otimizados"
SIMULADO_DIR = ROOT / "data" / "publisher" / "simulado"
PUBLISHER_DIR = ROOT / "data" / "publisher"
LEGAL_DIR = ROOT / "data" / "platform_compliance" / "paginas_legais"
TECH_DIR = ROOT / "data" / "platform_compliance" / "arquivos_tecnicos"

# Nunca True nesta fase. Ligar isso exige credenciais reais configuradas (ver prompt.md) e
# confirmação explícita do operador — não é uma flag de linha de comando "liga sozinho".
MODO_REAL_HABILITADO = False

WEEKDAY_MAP = {"segunda": 0, "terca": 1, "quarta": 2, "quinta": 3, "sexta": 4, "sabado": 5, "domingo": 6}


# --------------------------------------------------------------------------- gates
def check_publication_gate(context: dict) -> tuple[bool, str]:
    """Confere o gate 'aprovacao_publicacao' — via state.json de uma rodada do orchestrator
    (context['run_dir'], preenchido automaticamente no pipeline) ou, em uso isolado, via um
    arquivo de aprovação avulso passado em context['aprovacao_manual']."""
    gate_id = "aprovacao_publicacao"
    run_dir = context.get("run_dir")
    if run_dir:
        state_path = Path(run_dir) / "state.json"
        if not state_path.exists():
            return False, f"run_dir informado mas sem state.json ({state_path})."
        status = read_json(state_path).get("gates", {}).get(gate_id)
        if status in ("aprovado", "simulado"):
            return True, f"gate '{gate_id}' = {status} (registrado em {state_path.relative_to(ROOT)})"
        return False, f"gate '{gate_id}' ainda não aprovado (status atual: {status or 'pendente'})."

    manual_path = context.get("aprovacao_manual")
    if not manual_path:
        return False, ("nenhum registro do gate 'aprovacao_publicacao' encontrado — rode via orchestrator.py "
                        "ou passe --aprovacao-manual com um arquivo de aprovação preenchido.")
    path = Path(manual_path) if Path(manual_path).is_absolute() else ROOT / manual_path
    if not path.exists():
        return False, f"arquivo de aprovação manual não encontrado: {manual_path}"
    decision = read_json(path)
    if decision.get("status") == "aprovado" and decision.get("revisor", "").strip():
        return True, f"aprovado manualmente por {decision['revisor']} ({manual_path})"
    return False, f"arquivo de aprovação manual pendente ou incompleto: {manual_path}"


def check_compliance_criticas(site_id: str, site: dict) -> tuple[bool, list[str]]:
    """Checagem direta no disco (não depende do JSON de saída do agente 06) — mesmos
    diretórios que o agente 06 escreve. Só bloqueia por ausência de páginas/arquivos
    obrigatórios; não considera aqui o mínimo de artigos (isso é sobre a candidatura ao
    AdSense como um todo, não sobre a segurança de publicar um artigo específico)."""
    problemas = []
    legal_dir = LEGAL_DIR / site_id
    for pagina in site.get("compliance", {}).get("paginas_obrigatorias", []):
        slug = pagina["slug"].strip("/")
        if not (legal_dir / f"{slug}.md").exists():
            problemas.append(f"página legal obrigatória ausente: {slug} (rode o agente 06)")
    tech_dir = TECH_DIR / site_id
    for nome in ("robots.txt", "sitemap.xml", "ads.txt"):
        if not (tech_dir / nome).exists():
            problemas.append(f"arquivo técnico obrigatório ausente: {nome} (rode o agente 06)")
    return not problemas, problemas


# --------------------------------------------------------------------------- resolução do artigo
def resolve_article(context: dict) -> Path | None:
    outputs = context.get("outputs") or {}
    seo_output_path = outputs.get("05_seo_onpage")
    if seo_output_path:
        seo_output = read_json(ROOT / seo_output_path)
        if seo_output.get("arquivo"):
            return ROOT / seo_output["arquivo"]
    if context.get("arquivo"):
        return ROOT / context["arquivo"]
    if context.get("slug"):
        return OTIMIZADOS_DIR / f"{context['slug']}.md"
    return None


# --------------------------------------------------------------------------- cadência/calendário
def list_ready_articles_meta() -> list[dict]:
    articles = []
    for path in sorted(OTIMIZADOS_DIR.glob("*.md")):
        try:
            fm, _ = read_markdown(path)
        except MarkdownError:
            continue
        articles.append({
            "slug": fm.get("slug") or path.stem,
            "sensivel_ymyl": bool(fm.get("aviso_saude_aplicavel")),
            "mtime": path.stat().st_mtime,
        })
    return articles


def _next_preferred_weekday(d: date, preferred: set[int]) -> date:
    if not preferred:
        return d
    for offset in range(7):
        if (d + timedelta(days=offset)).weekday() in preferred:
            return d + timedelta(days=offset)
    return d  # nunca deveria chegar aqui se `preferred` não é vazio


def build_calendar(articles_meta: list[dict], schedule_cfg: dict, data_inicio: date) -> list[dict]:
    if schedule_cfg.get("priorizar_nao_sensiveis_primeiro", True):
        ordenados = sorted(articles_meta, key=lambda a: (a["sensivel_ymyl"], a["mtime"]))
    else:
        ordenados = sorted(articles_meta, key=lambda a: a["mtime"])

    minimo = schedule_cfg.get("artigos_por_semana_min", 3)
    maximo = schedule_cfg.get("artigos_por_semana_max", 5)
    por_semana = max(1, round((minimo + maximo) / 2))
    intervalo_dias = 7 / por_semana

    preferidos_raw = schedule_cfg.get("dias_preferidos") or []
    preferidos = {WEEKDAY_MAP[normalize_term(d)] for d in preferidos_raw if normalize_term(d) in WEEKDAY_MAP}

    calendario = []
    for i, artigo in enumerate(ordenados):
        data_base = data_inicio + timedelta(days=round(i * intervalo_dias))
        data_sugerida = _next_preferred_weekday(data_base, preferidos)
        calendario.append({
            "ordem": i + 1, "slug": artigo["slug"], "sensivel_ymyl": artigo["sensivel_ymyl"],
            "data_sugerida": data_sugerida.isoformat(),
        })
    return calendario


def load_or_init_calendar_anchor(site_id: str, schedule_cfg: dict) -> date:
    """A data de início do calendário fica fixa entre execuções (persistida no próprio
    calendário salvo) para não empurrar as datas sugeridas a cada vez que o agente roda."""
    existing_path = PUBLISHER_DIR / f"calendario_publicacao_{site_id}.json"
    if existing_path.exists():
        anchor = read_json(existing_path).get("data_inicio")
        if anchor:
            return date.fromisoformat(anchor)
    return schedule_cfg.get("data_inicio") or datetime.now(timezone.utc).date()


def write_calendar(site_id: str, calendario: list[dict], data_inicio: date, schedule_cfg: dict) -> None:
    payload = {
        "site_id": site_id, "gerado_em": now_iso(), "data_inicio": data_inicio.isoformat(),
        "artigos_por_semana": f"{schedule_cfg.get('artigos_por_semana_min', 3)}-{schedule_cfg.get('artigos_por_semana_max', 5)}",
        "calendario": calendario,
    }
    write_json(PUBLISHER_DIR / f"calendario_publicacao_{site_id}.json", payload)

    linhas = [f"# Calendário de publicação sugerido — {site_id}", "", f"Gerado em: {now_iso()}", "",
              "| Ordem | Artigo | YMYL | Data sugerida |", "|---|---|---|---|"]
    linhas += [f"| {c['ordem']} | {c['slug']} | {'⚠️' if c['sensivel_ymyl'] else ''} | {c['data_sugerida']} |"
               for c in calendario]
    linhas.append("\n*Sugestão de ritmo, não um bloqueio: publicar fora dessa data não impede o agente 07 de gerar "
                   "a prévia. Ajuste manualmente `config/publishing_schedule.yaml` para mudar a cadência.*")
    (PUBLISHER_DIR / f"calendario_publicacao_{site_id}.md").write_text("\n".join(linhas), encoding="utf-8")


# --------------------------------------------------------------------------- markdown → HTML
def _inline_md(text: str) -> str:
    escaped = html_lib.escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)


def markdown_to_html_body(body: str) -> str:
    """Conversor mínimo, propositalmente limitado ao subconjunto de Markdown que o próprio
    pipeline gera (headers, parágrafos, **negrito**, blockquote, listas '- item') — não é
    um parser CommonMark completo."""
    lines = body.split("\n")
    out: list[str] = []
    in_list = False
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            if in_list:
                out.append("</ul>")
                in_list = False
            i += 1
            continue
        header = re.match(r"^(#{1,6})\s+(.*)", stripped)
        if header:
            if in_list:
                out.append("</ul>")
                in_list = False
            level = len(header.group(1))
            out.append(f"<h{level}>{_inline_md(header.group(2))}</h{level}>")
            i += 1
            continue
        if stripped.startswith(">"):
            if in_list:
                out.append("</ul>")
                in_list = False
            quote_parts = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_parts.append(_inline_md(lines[i].strip().lstrip(">").strip()))
                i += 1
            out.append(f"<blockquote><p>{' '.join(quote_parts)}</p></blockquote>")
            continue
        if stripped.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_inline_md(stripped[2:])}</li>")
            i += 1
            continue
        paragraph = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,6})\s+", lines[i].strip()) \
                and not lines[i].strip().startswith((">", "- ")):
            paragraph.append(lines[i].strip())
            i += 1
        if in_list:
            out.append("</ul>")
            in_list = False
        out.append(f"<p>{_inline_md(' '.join(paragraph))}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


# --------------------------------------------------------------------------- HTML final
PREVIEW_CSS = """
:root { color-scheme: light; }
body { margin: 0; font-family: -apple-system, Segoe UI, Roboto, Arial, sans-serif; background: #fafaf7; color: #262220; }
.preview-banner { background: #fff3cd; color: #6b5300; padding: 10px 16px; font-size: 13px; text-align: center; border-bottom: 1px solid #e8d68a; }
main { max-width: 720px; margin: 0 auto; padding: 32px 20px 64px; }
h1 { font-size: 1.9rem; line-height: 1.25; margin-bottom: 0.3em; }
h2 { font-size: 1.35rem; margin-top: 2em; }
h3 { font-size: 1.1rem; margin-top: 1.4em; }
p { line-height: 1.7; font-size: 1.05rem; }
blockquote { border-left: 4px solid #d99a2b; background: #fff8ec; margin: 1.5em 0; padding: 0.8em 1.2em; font-size: 0.98rem; }
ul { line-height: 1.7; }
footer { max-width: 720px; margin: 0 auto; padding: 0 20px 48px; font-size: 0.85rem; color: #6b645f; border-top: 1px solid #e5e0d8; padding-top: 16px; }
"""


def is_placeholder_domain(dominio: str) -> bool:
    return any(m in dominio.lower() for m in ("seu-dominio", "example.com", "localhost"))


def build_preview_html(front_matter: dict, body: str, structured_data: dict, site: dict, calendario_entry: dict | None) -> str:
    titulo_seo = front_matter.get("titulo_seo") or front_matter["titulo"]
    meta_description = front_matter.get("meta_description", "")
    dominio = site.get("dominio", "").rstrip("/")
    url = f"{dominio}/{front_matter.get('slug', '')}" if dominio else ""
    idioma = site.get("idioma", "pt-BR")

    jsonld_scripts = "\n".join(
        f'<script type="application/ld+json">{json.dumps(v, ensure_ascii=False)}</script>'
        for v in structured_data.values()
    )
    canonical_tag = f'<link rel="canonical" href="{html_lib.escape(url)}">' if dominio and not is_placeholder_domain(dominio) else \
        "<!-- domínio ainda é um placeholder (config/sites/<site>.yaml → dominio) — atualizar antes do upload real -->"

    banner_bits = ["PRÉVIA — MODO SIMULAÇÃO — este artigo ainda não foi publicado de verdade."]
    if calendario_entry:
        banner_bits.append(f"Data sugerida no calendário: {calendario_entry['data_sugerida']}.")
    if not (front_matter.get("autor") or "").strip():
        banner_bits.append("Campo 'autor' ainda em branco — preencher antes de publicar de verdade.")

    body_html = markdown_to_html_body(body)

    return f"""<!doctype html>
<html lang="{idioma}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_lib.escape(titulo_seo)}</title>
<meta name="description" content="{html_lib.escape(meta_description)}">
{canonical_tag}
<meta property="og:type" content="article">
<meta property="og:title" content="{html_lib.escape(front_matter['titulo'])}">
<meta property="og:description" content="{html_lib.escape(meta_description)}">
<meta property="og:url" content="{html_lib.escape(url)}">
<meta property="og:locale" content="{idioma.replace('-', '_')}">
{jsonld_scripts}
<style>{PREVIEW_CSS}</style>
<!--
front-matter original (referência para quem for publicar manualmente):
{yaml_dump_for_comment(front_matter)}
-->
</head>
<body>
<div class="preview-banner">{html_lib.escape(' '.join(banner_bits))}</div>
<main>
<article>
{body_html}
</article>
</main>
<footer>Gerado pelo agente 07_publisher em modo simulação — {now_iso()}.</footer>
</body>
</html>
"""


def yaml_dump_for_comment(front_matter: dict) -> str:
    import yaml
    return yaml.safe_dump(front_matter, allow_unicode=True, sort_keys=False).strip()


# --------------------------------------------------------------------------- modo real (desabilitado)
def publish_wordpress(article: dict, credentials: dict) -> dict:
    """Estrutura do conector WordPress REST API. NÃO faz nenhuma chamada de rede — só existe
    para documentar o formato esperado quando MODO_REAL_HABILITADO for ligado manualmente.
    Ver prompt.md para as credenciais e o endpoint exatos."""
    return {"conector": "wordpress", "habilitado": False,
            "motivo": "modo real desabilitado nesta fase (MODO_REAL_HABILITADO=False em agent.py)"}


def publish_ghost(article: dict, credentials: dict) -> dict:
    """Estrutura do conector Ghost Admin API. NÃO faz nenhuma chamada de rede — mesma lógica
    de publish_wordpress(). Ver prompt.md."""
    return {"conector": "ghost", "habilitado": False,
            "motivo": "modo real desabilitado nesta fase (MODO_REAL_HABILITADO=False em agent.py)"}


# --------------------------------------------------------------------------- entrypoint
def run(context: dict) -> dict:
    log = context["logger"]
    site_id = context["site_id"]
    site = context.get("site") or load_site(site_id)

    gate_ok, gate_motivo = check_publication_gate(context)
    if not gate_ok:
        log.warning(f"[{AGENT_NAME}] gate 'aprovacao_publicacao' não confirmado: {gate_motivo}")
        return {"agent": AGENT_NAME, "status": "gate_nao_aprovado", "mensagem": gate_motivo}
    log.info(f"[{AGENT_NAME}] gate 'aprovacao_publicacao' ok: {gate_motivo}")

    compliance_ok, problemas_compliance = check_compliance_criticas(site_id, site)
    if not compliance_ok:
        log.warning(f"[{AGENT_NAME}] pendências críticas de compliance: {problemas_compliance}")
        return {
            "agent": AGENT_NAME, "status": "compliance_pendente",
            "mensagem": "Pendências críticas de compliance impedem a publicação, mesmo em modo simulação.",
            "pendencias_humanas": [f"[compliance] {p}" for p in problemas_compliance] + ["Rodar o agente 06 e resolver as pendências antes de publicar."],
        }

    path = resolve_article(context)
    if not path or not path.exists():
        log.warning(f"[{AGENT_NAME}] artigo otimizado não encontrado ({path})")
        return {"agent": AGENT_NAME, "status": "sem_artigo_otimizado",
                "mensagem": f"Artigo otimizado não encontrado: {path}. Rode o agente 05 antes deste."}

    try:
        front_matter, body = read_markdown(path)
    except MarkdownError as ex:
        log.error(f"[{AGENT_NAME}] {path}: {ex}")
        return {"agent": AGENT_NAME, "status": "erro_formato", "mensagem": str(ex)}

    if front_matter.get("status") != "otimizado_seo":
        log.warning(f"[{AGENT_NAME}] artigo com status '{front_matter.get('status')}' — esperado 'otimizado_seo'")
        return {"agent": AGENT_NAME, "status": "artigo_nao_otimizado",
                "mensagem": "O artigo referenciado não está marcado como otimizado pelo agente 05."}

    structured_data = {}
    jsonld_rel = front_matter.get("dados_estruturados_arquivo")
    if jsonld_rel and (ROOT / jsonld_rel).exists():
        structured_data = json.loads((ROOT / jsonld_rel).read_text(encoding="utf-8"))

    schedule_cfg = load_publishing_schedule(site_id)
    data_inicio = load_or_init_calendar_anchor(site_id, schedule_cfg)
    calendario = build_calendar(list_ready_articles_meta(), schedule_cfg, data_inicio)
    write_calendar(site_id, calendario, data_inicio, schedule_cfg)
    slug = front_matter.get("slug") or path.stem
    entrada = next((c for c in calendario if c["slug"] == slug), None)

    html_out = build_preview_html(front_matter, body, structured_data, site, entrada)
    SIMULADO_DIR.mkdir(parents=True, exist_ok=True)
    out_path = SIMULADO_DIR / f"{slug}.html"
    out_path.write_text(html_out, encoding="utf-8")

    modo_real_pedido = bool(context.get("modo_real"))
    if modo_real_pedido:
        log.warning(f"[{AGENT_NAME}] modo real foi solicitado mas está desabilitado nesta fase "
                     "(MODO_REAL_HABILITADO=False) — nada foi enviado para nenhuma plataforma.")

    novo_front_matter = {**front_matter, "status": "publicado_simulado", "publicado_em": now_iso(),
                          "modo_publicacao": "simulacao", "arquivo_preview": str(out_path.relative_to(ROOT)),
                          "data_sugerida_calendario": entrada["data_sugerida"] if entrada else None}
    write_markdown(SIMULADO_DIR / f"{slug}.md", novo_front_matter, body)

    pendencias = [
        f"Abrir {out_path.relative_to(ROOT)} no navegador para conferir a prévia antes de qualquer publicação real.",
        "Modo real (WordPress/Ghost) está desabilitado nesta fase — ver prompt.md para os requisitos de configuração.",
    ]
    if entrada:
        pendencias.append(f"Calendário sugerido: publicar em {entrada['data_sugerida']} "
                           f"(posição {entrada['ordem']} de {len(calendario)} artigo(s) pronto(s)).")
    if front_matter.get("aviso_saude_aplicavel"):
        pendencias.append("Artigo é YMYL — o calendário já prioriza publicá-lo depois dos posts não sensíveis.")
    if modo_real_pedido:
        pendencias.append("Modo real foi pedido nesta rodada, mas foi ignorado por segurança — nada foi publicado de verdade.")

    output = {
        "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "site_id": site_id, "gerado_em": now_iso(),
        "status": "ok", "modo": "simulacao", "modo_real_habilitado": MODO_REAL_HABILITADO,
        "slug": slug, "titulo": front_matter.get("titulo"),
        "arquivo_preview": str(out_path.relative_to(ROOT)),
        "calendario_arquivo": str((PUBLISHER_DIR / f"calendario_publicacao_{site_id}.md").relative_to(ROOT)),
        "data_sugerida": entrada["data_sugerida"] if entrada else None,
        "posicao_calendario": entrada["ordem"] if entrada else None,
        "sensivel_ymyl": bool(front_matter.get("aviso_saude_aplicavel")),
        "pendencias_humanas": pendencias,
    }
    log.info(f"[{AGENT_NAME}] {slug}: prévia gerada em modo simulação → {out_path.relative_to(ROOT)} "
             f"(data sugerida: {output['data_sugerida']})")
    return output


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 07 — publicação em modo simulação (uso isolado)")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--slug", help="slug do artigo em data/seo_onpage/otimizados/")
    group.add_argument("--arquivo", help="caminho do .md a publicar, relativo à raiz do projeto")
    parser.add_argument("--run-dir", help="pasta de uma rodada do orchestrator (para checar o gate 'aprovacao_publicacao')")
    parser.add_argument("--aprovacao-manual", help="caminho para um JSON de aprovação avulso (uso sem orchestrator)")
    parser.add_argument("--modo-real", action="store_true", help="pedido de modo real — será recusado (desabilitado nesta fase)")
    args = parser.parse_args()

    load_env_file()
    run_id = f"{now_iso().replace(':', '').replace('+0000', 'Z')}-{AGENT_NAME}"
    output = run({
        "site_id": args.site, "slug": args.slug, "arquivo": args.arquivo,
        "run_dir": Path(args.run_dir) if args.run_dir else None,
        "aprovacao_manual": args.aprovacao_manual, "modo_real": args.modo_real,
        "logger": get_logger(run_id),
    })
    return 0 if output["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
