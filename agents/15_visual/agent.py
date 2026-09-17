"""Agente 15 — Visual (banco de imagens: Pexels e/ou Pixabay).

Decisão revista: geração por IA (OpenAI) foi trocada por busca em banco de imagens, para
não depender de billing/chave da OpenAI e ter imagem publicável no mesmo dia. Cada artigo
recebe uma foto real de animal (nunca ilustração gerada) — mas a regra mais importante do
projeto continua valendo: a foto tem que mostrar SÓ o animal, nunca uma pessoa/tutor
visível (personas do site são 100% fictícias; uma foto de pessoa real associada a uma
autoria fictícia seria inconsistente com essa regra).

Como nenhuma busca automática garante sozinha "sem pessoa na imagem" com 100% de certeza,
o fluxo é em duas etapas, com revisão humana (ou do operador do agente) no meio:

  1. `--fetch-candidatos`: baixa algumas fotos candidatas por artigo (não publica nada).
  2. Revisão visual dos candidatos baixados em data/visual/candidatos/<slug>/.
  3. `--selecionar <slug> <indice>`: promove o candidato aprovado para a imagem oficial do
     artigo, grava a atribuição (foto + fotógrafo + banco) e anota o front-matter.

TRAVA: sem PEXELS_API_KEY nem PIXABAY_API_KEY configuradas, o agente roda em modo
"aguardando_credenciais" — nenhuma chamada de API é feita. Mesmo padrão dos agentes 09/14.

Uso:
    python agents/15_visual/agent.py --site pets-tutores-iniciantes --fetch-candidatos
    python agents/15_visual/agent.py --site pets-tutores-iniciantes --selecionar <slug> 0
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import CONFIG_DIR, load_env_file, load_site, load_yaml  # noqa: E402
from core.io import now_iso  # noqa: E402
from core.log import get_logger  # noqa: E402
from core.markdown import MarkdownError, read_markdown, write_markdown  # noqa: E402
from stock_queries import queries_for  # noqa: E402

AGENT_NAME = "15_visual"
SCHEMA_VERSION = "1.0"

OTIMIZADOS_DIR = ROOT / "data" / "seo_onpage" / "otimizados"
VISUAL_DIR = ROOT / "data" / "visual"
CANDIDATOS_DIR = VISUAL_DIR / "candidatos"
IMAGENS_DIR = VISUAL_DIR / "imagens"
PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"
PIXABAY_SEARCH_URL = "https://pixabay.com/api/"


def load_visual_settings() -> dict:
    return load_yaml(CONFIG_DIR / "visual_settings.yaml")


def check_credenciais() -> tuple[bool, str, dict]:
    chaves = {"pexels": os.environ.get("PEXELS_API_KEY", "").strip(),
              "pixabay": os.environ.get("PIXABAY_API_KEY", "").strip()}
    if not chaves["pexels"] and not chaves["pixabay"]:
        return False, "Nem PEXELS_API_KEY nem PIXABAY_API_KEY estão configuradas em .env.", chaves
    disponiveis = [k for k, v in chaves.items() if v]
    return True, f"Configurada(s): {', '.join(disponiveis)}.", chaves


# --------------------------------------------------------------------------- busca
def search_pexels(query: str, api_key: str, per_page: int = 5) -> list[dict]:
    url = f"{PEXELS_SEARCH_URL}?{urllib.parse.urlencode({'query': query, 'per_page': per_page, 'orientation': 'landscape'})}"
    req = urllib.request.Request(url, headers={"Authorization": api_key})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return [{
        "fonte": "pexels", "id": p["id"], "url_download": p["src"]["large"],
        "url_pagina": p["url"], "fotografo": p["photographer"], "fotografo_url": p["photographer_url"],
    } for p in data.get("photos", [])]


def search_pixabay(query: str, api_key: str, per_page: int = 5) -> list[dict]:
    params = {"key": api_key, "q": query, "image_type": "photo", "safesearch": "true",
              "orientation": "horizontal", "per_page": max(per_page, 3)}
    url = f"{PIXABAY_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return [{
        "fonte": "pixabay", "id": h["id"], "url_download": h["largeImageURL"],
        "url_pagina": h["pageURL"], "fotografo": h["user"], "fotografo_url": f"https://pixabay.com/users/{h['user']}-{h['user_id']}/",
    } for h in data.get("hits", [])[:per_page]]


def search_candidates(query: str, chaves: dict, per_page: int) -> list[dict]:
    resultados = []
    if chaves.get("pexels"):
        try:
            resultados += search_pexels(query, chaves["pexels"], per_page)
        except (urllib.error.URLError, KeyError, ValueError) as ex:
            resultados.append({"erro": f"pexels: {ex}"})
    if chaves.get("pixabay") and len(resultados) < per_page:
        try:
            resultados += search_pixabay(query, chaves["pixabay"], per_page - len(resultados))
        except (urllib.error.URLError, KeyError, ValueError) as ex:
            resultados.append({"erro": f"pixabay: {ex}"})
    return resultados


# --------------------------------------------------------------------------- etapa 1: candidatos
def fetch_candidates_for_article(slug: str, chaves: dict, settings: dict, log) -> dict:
    out_dir = CANDIDATOS_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    candidatos_final: list[dict] = []

    for query in queries_for(slug):
        candidatos = search_candidates(query, chaves, settings.get("candidatos_por_busca", 5))
        for c in candidatos:
            if "erro" in c:
                continue
            candidatos_final.append({**c, "query": query})
        if len(candidatos_final) >= settings.get("candidatos_por_busca", 5):
            break

    manifest = []
    for i, c in enumerate(candidatos_final):
        try:
            with urllib.request.urlopen(c["url_download"], timeout=30) as resp:
                img_bytes = resp.read()
        except urllib.error.URLError as ex:
            log.error(f"[{AGENT_NAME}] falha ao baixar candidato {i} de '{slug}': {ex}")
            continue
        arquivo = out_dir / f"{i}.jpg"
        arquivo.write_bytes(img_bytes)
        manifest.append({**c, "indice": i, "arquivo": str(arquivo.relative_to(ROOT))})

    (out_dir / "candidatos.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info(f"[{AGENT_NAME}] {len(manifest)} candidato(s) baixado(s) para '{slug}' → {out_dir.relative_to(ROOT)}")
    return {"slug": slug, "n_candidatos": len(manifest), "diretorio": str(out_dir.relative_to(ROOT))}


# --------------------------------------------------------------------------- etapa 2: seleção
def select_candidate(slug: str, indice: int, site: dict, log) -> dict:
    candidatos_path = CANDIDATOS_DIR / slug / "candidatos.json"
    if not candidatos_path.exists():
        raise FileNotFoundError(f"nenhum candidato baixado para '{slug}' — rode --fetch-candidatos primeiro")
    candidatos = json.loads(candidatos_path.read_text(encoding="utf-8"))
    escolhido = next((c for c in candidatos if c["indice"] == indice), None)
    if not escolhido:
        raise ValueError(f"índice {indice} não existe entre os candidatos de '{slug}'")

    IMAGENS_DIR.mkdir(parents=True, exist_ok=True)
    origem = ROOT / escolhido["arquivo"]
    destino = IMAGENS_DIR / f"{slug}.jpg"
    destino.write_bytes(origem.read_bytes())

    manifest = {
        "slug": slug, "arquivo": str(destino.relative_to(ROOT)), "fonte": escolhido["fonte"],
        "fotografo": escolhido["fotografo"], "fotografo_url": escolhido["fotografo_url"],
        "url_pagina": escolhido["url_pagina"], "query": escolhido["query"], "selecionado_em": now_iso(),
    }
    (IMAGENS_DIR / f"{slug}.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    article_path = OTIMIZADOS_DIR / f"{slug}.md"
    fm, body = read_markdown(article_path)
    novo_fm = {
        **fm, "imagem_capa": f"imagens/{slug}.jpg", "imagem_fonte": manifest["fonte"],
        "imagem_fotografo": manifest["fotografo"], "imagem_fotografo_url": manifest["fotografo_url"],
        "imagem_url_pagina": manifest["url_pagina"], "imagem_selecionada_em": manifest["selecionado_em"],
    }
    write_markdown(article_path, novo_fm, body)

    jsonld_path = ROOT / fm.get("dados_estruturados_arquivo", "")
    if jsonld_path.exists():
        data = json.loads(jsonld_path.read_text(encoding="utf-8"))
        if "article" in data:
            data["article"]["image"] = f"{site['dominio'].rstrip('/')}/imagens/{slug}.jpg"
        jsonld_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    log.info(f"[{AGENT_NAME}] '{slug}' → imagem de {manifest['fonte']} (foto de {manifest['fotografo']}) selecionada")
    return manifest


# --------------------------------------------------------------------------- relatórios
def render_blocked_report(motivo: str, n_artigos: int) -> str:
    return (
        f"# Agente 15 — aguardando credenciais\n\n- **Gerado em:** {now_iso()}\n"
        f"- **Status:** ⛔ aguardando_credenciais\n- **Motivo:** {motivo}\n"
        f"- **Artigos no catálogo:** {n_artigos}\n\n## Como destravar\n\n"
        "1. Crie uma conta gratuita em pexels.com/api (ou pixabay.com/api/docs) — aprovação é instantânea.\n"
        "2. Adicione `PEXELS_API_KEY=<chave>` e/ou `PIXABAY_API_KEY=<chave>` no `.env` "
        "(nunca no `.env.example`, e nunca cole a chave direto no chat).\n"
        "3. Rode este agente de novo com `--fetch-candidatos`.\n\n"
        "Nenhuma chamada de API foi feita até este ponto.\n"
    )


def render_candidates_report(resultados: list[dict]) -> str:
    L = ["# Agente 15 — candidatos baixados para revisão", "", f"- **Gerado em:** {now_iso()}", "",
         "| Artigo | Candidatos | Pasta |", "|---|---|---|"]
    L += [f"| {r['slug']} | {r['n_candidatos']} | {r['diretorio']} |" for r in resultados]
    L += ["", "## Próximo passo", "",
          "Revise as imagens em cada pasta e confirme que mostram SÓ o animal (sem pessoa visível), depois rode:",
          "```", "python agents/15_visual/agent.py --site <site_id> --selecionar <slug> <indice>", "```"]
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- entrypoint
def run(context: dict) -> dict:
    log = context["logger"]
    site_id = context["site_id"]
    site = context.get("site") or load_site(site_id)
    settings = load_visual_settings()
    VISUAL_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")

    artigos = []
    for path in sorted(OTIMIZADOS_DIR.glob("*.md")):
        try:
            fm, _ = read_markdown(path)
        except MarkdownError:
            continue
        artigos.append(fm)

    if context.get("selecionar"):
        slug, indice = context["selecionar"]
        manifest = select_candidate(slug, indice, site, log)
        return {"agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "site_id": site_id, "gerado_em": now_iso(),
                "status": "ok", "acao": "selecionar", "manifest": manifest,
                "pendencias_humanas": [f"Rode `python site/build_site.py --site {site_id}` para publicar a imagem."]}

    ok_credenciais, motivo, chaves = check_credenciais()
    if not ok_credenciais:
        relatorio_md = render_blocked_report(motivo, len(artigos))
        out_path = VISUAL_DIR / f"relatorio_{date_str}.md"
        out_path.write_text(relatorio_md, encoding="utf-8")
        log.warning(f"[{AGENT_NAME}] modo aguardando_credenciais: {motivo}")
        return {"agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "site_id": site_id, "gerado_em": now_iso(),
                "status": "aguardando_credenciais", "n_artigos": len(artigos),
                "relatorio": str(out_path.relative_to(ROOT)), "pendencias_humanas": [motivo]}

    alvo = [fm for fm in artigos if not context.get("slug") or fm["slug"] == context["slug"]]
    if not context.get("forcar"):
        alvo = [fm for fm in alvo if not fm.get("imagem_capa")]

    resultados = [fetch_candidates_for_article(fm["slug"], chaves, settings, log) for fm in alvo]
    relatorio_md = render_candidates_report(resultados)
    out_path = VISUAL_DIR / f"relatorio_{date_str}.md"
    out_path.write_text(relatorio_md, encoding="utf-8")

    output = {
        "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "site_id": site_id, "gerado_em": now_iso(),
        "status": "ok", "acao": "fetch_candidatos", "n_artigos_processados": len(resultados),
        "relatorio": str(out_path.relative_to(ROOT)),
        "pendencias_humanas": ["Revisar candidatos e rodar --selecionar para cada artigo."],
    }
    log.info(f"[{AGENT_NAME}] candidatos buscados para {len(resultados)} artigo(s) → {out_path.relative_to(ROOT)}")
    return output


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 15 — imagem de capa via banco de imagens")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    parser.add_argument("--fetch-candidatos", action="store_true", help="baixa candidatos para revisão")
    parser.add_argument("--selecionar", nargs=2, metavar=("SLUG", "INDICE"), help="promove um candidato revisado")
    parser.add_argument("--slug", help="restringe a um artigo (com --fetch-candidatos)")
    parser.add_argument("--forcar", action="store_true", help="busca de novo mesmo quem já tem imagem_capa")
    args = parser.parse_args()

    load_env_file()
    run_id = f"{now_iso().replace(':', '').replace('+0000', 'Z')}-{AGENT_NAME}"
    context = {"site_id": args.site, "slug": args.slug, "forcar": args.forcar, "logger": get_logger(run_id)}
    if args.selecionar:
        context["selecionar"] = (args.selecionar[0], int(args.selecionar[1]))
    output = run(context)
    return 0 if output["status"] in ("ok", "aguardando_credenciais") else 2


if __name__ == "__main__":
    sys.exit(main())
