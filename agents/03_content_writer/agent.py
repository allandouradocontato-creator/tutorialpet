"""Agente 03 — Content Writer.

Recebe UMA pauta (selecionada no gate humano 'aprovacao_pauta', a partir da saída do
agente 02) e escreve o rascunho completo do artigo: título, meta description, introdução
com abertura variável, H2/H3 com desenvolvimento prático, FAQ e conclusão com CTA suave.

A prosa dos blocos de conteúdo (agents/03_content_writer/content_blocks.py) é original,
escrita para este projeto — este agente NUNCA copia, resume ou parafraseia fontes
externas, e nunca alega credencial veterinária. Ver prompt.md para as regras completas.

Uso isolado (sem passar pelo agente 02, útil para testes):
    python agents/03_content_writer/agent.py --site pets-tutores-iniciantes \
        --termo "como cortar unha de cachorro" --pilar cuidados_diarios
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_env_file, load_site  # noqa: E402
from core.io import normalize_term, now_iso, slugify  # noqa: E402
from core.log import get_logger  # noqa: E402
from content_blocks import CONTENT_BLOCKS  # noqa: E402

AGENT_NAME = "03_content_writer"
SCHEMA_VERSION = "1.0"
DRAFTS_DIR = ROOT / "data" / "content_writer" / "rascunhos"

OPENING_STRUCTURES = ["preview_lista", "pergunta_retorica", "direto_ao_topico"]
CTA_PADRAO = (
    "Guarda essa dica, testa com calma no ritmo do seu pet e ajusta o que for preciso — "
    "cada bichinho é um caso. Continue por aqui: temos outros guias parecidos que podem ajudar "
    "no seu dia a dia como tutor."
)


def _pick_index(seed: str, n: int) -> int:
    """Escolha determinística: o mesmo termo sempre cai no mesmo índice, mas termos
    diferentes tendem a variar — evita repetir sempre a mesma estrutura de abertura."""
    return int(hashlib.md5(normalize_term(seed).encode("utf-8")).hexdigest(), 16) % n


# --------------------------------------------------------------------------- FAQ
FAQ_MIN, FAQ_MAX = 3, 5


def answer_for_manual_question(pilar_key: str, sensivel: bool) -> str:
    generic = {
        "alimentacao": "Isso costuma variar conforme o pet e a fase de vida, mas os pontos acima já te dão uma "
                       "boa base para observar a rotina alimentar e ajustar aos poucos.",
        "comportamento": "Cada pet reage de um jeito, então observe o padrão específico do seu antes de aplicar "
                          "qualquer ajuste — o que funciona para um pode não funcionar para outro.",
        "cuidados_diarios": "A resposta muda um pouco conforme o porte e a pelagem do pet, mas os passos acima "
                             "cobrem a maior parte dos casos do dia a dia.",
        "primeiros_passos_filhotes": "Cada filhote se adapta em um ritmo próprio — use os pontos acima como guia, "
                                      "mas sem pressa de 'bater' um prazo específico.",
        "produtos_compras": "A escolha ideal depende do porte e da rotina do seu pet específico — use os "
                             "critérios acima para comparar as opções disponíveis para o seu caso.",
    }.get(pilar_key, "Isso pode variar de pet para pet — use os pontos acima como ponto de partida e ajuste "
                      "conforme a resposta do seu bichinho.")
    if sensivel:
        generic += " Como esse tema envolve a saúde do animal, o ideal é confirmar com um médico-veterinário o " \
                   "que é mais adequado para o seu caso."
    return generic


def build_faq(pauta: dict, blocks: dict) -> list[dict]:
    faq: list[dict] = []
    seen = set()
    for q in pauta.get("perguntas_relacionadas", []):
        key = normalize_term(q)
        if key in seen:
            continue
        faq.append({"pergunta": q, "resposta": answer_for_manual_question(pauta.get("pilar"), pauta.get("sensivel_ymyl", False))})
        seen.add(key)
    for item in blocks["faq_banco"]:
        if len(faq) >= FAQ_MAX:
            break
        key = normalize_term(item["pergunta"])
        if key not in seen:
            faq.append(item)
            seen.add(key)
    return faq[:FAQ_MAX]


# --------------------------------------------------------------------------- meta description
def build_meta_description(pauta: dict, limit: int = 155) -> str:
    base = re.sub(r"\s+", " ", f"{pauta['titulo']}. {pauta['angulo_gancho']}").strip()
    if len(base) <= limit:
        return base
    truncated = base[: limit - 3].rsplit(" ", 1)[0]
    return truncated + "..."


# --------------------------------------------------------------------------- corpo do artigo
def render_article_body(pauta: dict, site: dict, blocks: dict, faq: list[dict], opening_idx: int, sensivel: bool) -> str:
    term = pauta["termo_origem"]
    style = OPENING_STRUCTURES[opening_idx]
    L = [f"# {pauta['titulo']}", "", pauta["angulo_gancho"], ""]

    if style == "preview_lista":
        L += ["Neste guia você vai encontrar:", ""]
        L += [f"- {h2['titulo']}" for h2 in blocks["h2"]]
        L += [""]
    elif style == "pergunta_retorica":
        L += [f'Mas afinal, por onde começar quando o assunto é "{term}"? Vamos por partes, sem complicação.', ""]
    # "direto_ao_topico": sem parágrafo extra, o texto já segue direto para o primeiro H2

    if sensivel:
        aviso = site.get("compliance", {}).get("aviso_saude", "").strip()
        if aviso:
            L += [f"> {aviso}", ""]

    for h2 in blocks["h2"]:
        L += [f"## {h2['titulo']}", ""]
        for paragrafo in h2["paragrafos"]:
            L += [paragrafo, ""]
        for h3 in h2.get("h3", []):
            L += [f"### {h3['titulo']}", "", h3["texto"], ""]
        if h2.get("exemplo"):
            L += [f"**Exemplo prático:** {h2['exemplo']}", ""]

    L += ["## Perguntas frequentes", ""]
    for item in faq:
        L += [f"**{item['pergunta']}**", "", item["resposta"], ""]

    L += ["## Para fechar", "", blocks.get("conclusao", ""), "", CTA_PADRAO]
    return "\n".join(L) + "\n"


def render_front_matter(fm: dict) -> str:
    return "---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + "---\n\n"


# --------------------------------------------------------------------------- entrypoint
def resolve_pauta(context: dict) -> dict | None:
    """A pauta pode vir do gate 'aprovacao_pauta' (pipeline normal) ou, em uso isolado,
    de context['input'] (quando já é um dict de pauta) ou dos argumentos de CLI."""
    pauta = context.get("pauta_selecionada")
    if pauta:
        return pauta
    candidate = context.get("input")
    if isinstance(candidate, dict) and "termo_origem" in candidate:
        return candidate
    return None


def run(context: dict) -> dict:
    log = context["logger"]
    site_id = context["site_id"]
    site = context.get("site") or load_site(site_id)

    pauta = resolve_pauta(context)
    if not pauta:
        log.warning(f"[{AGENT_NAME}] nenhuma pauta selecionada — não há o que escrever")
        return {
            "agent": AGENT_NAME, "status": "sem_pauta_selecionada",
            "mensagem": "Nenhuma pauta foi selecionada no gate 'aprovacao_pauta' (campo 'pauta_id_selecionada').",
        }

    sensivel = bool(pauta.get("sensivel_ymyl"))
    pilar_key = pauta.get("pilar") if pauta.get("pilar") in CONTENT_BLOCKS else "pauta_especifica"
    blocks = CONTENT_BLOCKS[pilar_key]

    faq = build_faq(pauta, blocks)
    meta_description = build_meta_description(pauta)
    opening_idx = _pick_index(pauta["termo_origem"] + "#estrutura", len(OPENING_STRUCTURES))
    body_md = render_article_body(pauta, site, blocks, faq, opening_idx, sensivel)

    slug = slugify(pauta["termo_origem"])
    front_matter = {
        "titulo": pauta["titulo"],
        "meta_description": meta_description,
        "data": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "status": "rascunho_pendente_revisao",
        "slug": slug,
        "termo_origem": pauta["termo_origem"],
        "pilar": pauta.get("pilar"),
        "intencao_busca": pauta.get("intencao_busca"),
        "autor": "",  # preencher com uma pessoa real cadastrada em /sobre — nunca um nome fictício
        "site_id": site_id,
        "gerado_em": now_iso(),
        "aviso_saude_aplicavel": sensivel,
        "estrutura_abertura": OPENING_STRUCTURES[opening_idx],
    }
    full_md = render_front_matter(front_matter) + body_md

    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DRAFTS_DIR / f"{slug}.md"
    if context.get("dry_run"):
        log.info(f"[{AGENT_NAME}] dry-run: rascunho seria salvo em {out_path.relative_to(ROOT)} (gravando mesmo assim, é um rascunho local, não uma publicação)")
    out_path.write_text(full_md, encoding="utf-8")

    pendencias = [
        "Revisão editorial completa pelo agente 04 antes de aprovar a publicação.",
        "Preencher o campo 'autor' no front-matter com uma pessoa real cadastrada em /sobre.",
    ]
    if sensivel:
        pendencias.append("Conteúdo classificado como YMYL: reforçar o aviso de saúde e a revisão editorial.")

    output = {
        "agent": AGENT_NAME,
        "schema_version": SCHEMA_VERSION,
        "site_id": site_id,
        "gerado_em": now_iso(),
        "status": "ok",
        "arquivo": str(out_path.relative_to(ROOT)),
        "titulo": pauta["titulo"],
        "slug": slug,
        "termo_origem": pauta["termo_origem"],
        "pilar": pauta.get("pilar"),
        "sensivel_ymyl": sensivel,
        "estrutura_abertura": OPENING_STRUCTURES[opening_idx],
        "contagem_palavras": len(full_md.split()),
        "pendencias_humanas": pendencias,
    }
    log.info(f"[{AGENT_NAME}] artigo gerado: {out_path.relative_to(ROOT)} ({output['contagem_palavras']} palavras, "
              f"abertura={output['estrutura_abertura']})")
    return output


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 03 — redator de artigos (uso isolado)")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    parser.add_argument("--termo", required=True, help="termo_origem da pauta")
    parser.add_argument("--titulo", help="título do artigo (default: gerado a partir do termo)")
    parser.add_argument("--pilar", default="pauta_especifica", choices=list(CONTENT_BLOCKS))
    parser.add_argument("--intencao", default="informacional", choices=["informacional", "transacional", "navegacional"])
    parser.add_argument("--sensivel", action="store_true", help="marca a pauta como YMYL")
    args = parser.parse_args()

    load_env_file()
    pauta = {
        "termo_origem": args.termo,
        "titulo": args.titulo or f"{args.termo[:1].upper()}{args.termo[1:]}: guia prático",
        "angulo_gancho": "Vamos direto ao ponto, com um passo a passo simples de aplicar hoje mesmo.",
        "intencao_busca": args.intencao,
        "pilar": args.pilar,
        "sensivel_ymyl": args.sensivel,
        "perguntas_relacionadas": [],
    }
    run_id = f"{now_iso().replace(':', '').replace('+0000', 'Z')}-{AGENT_NAME}"
    output = run({"site_id": args.site, "pauta_selecionada": pauta, "logger": get_logger(run_id)})
    return 0 if output["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
