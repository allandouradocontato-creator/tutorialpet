"""Agente 15 — Visual (geração de imagem por IA).

Gera uma imagem de capa por artigo (ilustração estilizada, não foto de banco) via API de
geração de imagem da OpenAI, e anota o resultado no front-matter do artigo já otimizado
(campo `imagem_capa`) para que `site/build_site.py` a use na home e na página do artigo,
e para preencher o campo `image` que faltava no JSON-LD (ganho de SEO, não só estético).

TRAVA: sem OPENAI_API_KEY configurada, o agente roda em modo "aguardando_credenciais" —
gera só um relatório do que falta, sem chamar a API nem gastar nada. Mesmo padrão de trava
dos agentes 09/14.

Uso:
    python agents/15_visual/agent.py --site pets-tutores-iniciantes
    python agents/15_visual/agent.py --site pets-tutores-iniciantes --slug <slug>  # só 1
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
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

AGENT_NAME = "15_visual"
SCHEMA_VERSION = "1.0"

OTIMIZADOS_DIR = ROOT / "data" / "seo_onpage" / "otimizados"
VISUAL_DIR = ROOT / "data" / "visual"
API_URL = "https://api.openai.com/v1/images/generations"


def load_visual_settings() -> dict:
    return load_yaml(CONFIG_DIR / "visual_settings.yaml")


def check_credenciais() -> tuple[bool, str]:
    chave = os.environ.get("OPENAI_API_KEY", "").strip()
    if not chave:
        return False, "OPENAI_API_KEY não configurada em .env — nenhuma chamada de API foi feita."
    return True, "OPENAI_API_KEY configurada."


def build_prompt(termo_origem: str, titulo: str, settings: dict) -> str:
    return f"{settings['prefixo_estilo'].strip()} Cena específica: {termo_origem} — referente ao artigo \"{titulo}\"."


def call_openai_images_api(prompt: str, settings: dict, api_key: str) -> bytes:
    """Chamada mínima via urllib (sem dependência de `requests`, que não está instalada
    neste ambiente) — POST simples com corpo JSON, resposta em base64 (b64_json)."""
    body = json.dumps({
        "model": settings["modelo"], "prompt": prompt, "size": settings["tamanho"],
        "quality": settings["qualidade"], "n": 1,
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL, data=body, method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    b64 = payload["data"][0]["b64_json"]
    return base64.b64decode(b64)


def generate_image_for_article(fm: dict, settings: dict, api_key: str, log) -> dict:
    slug = fm["slug"]
    prompt = build_prompt(fm.get("termo_origem", fm["titulo"]), fm["titulo"], settings)
    image_bytes = call_openai_images_api(prompt, settings, api_key)

    out_dir = ROOT / settings["diretorio_saida"]
    out_dir.mkdir(parents=True, exist_ok=True)
    image_path = out_dir / f"{slug}.png"
    image_path.write_bytes(image_bytes)

    manifest = {
        "slug": slug, "prompt": prompt, "modelo": settings["modelo"], "qualidade": settings["qualidade"],
        "tamanho": settings["tamanho"], "custo_estimado_usd": settings["custo_estimado_por_imagem_usd"],
        "gerado_em": now_iso(), "arquivo": str(image_path.relative_to(ROOT)),
    }
    (out_dir / f"{slug}.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info(f"[{AGENT_NAME}] imagem gerada para '{slug}' → {image_path.relative_to(ROOT)} "
             f"(~US$ {settings['custo_estimado_por_imagem_usd']:.3f})")
    return manifest


def update_article_with_image(path: Path, fm: dict, body: str, manifest: dict) -> None:
    """Anota o artigo já otimizado com a imagem gerada — aditivo, não mexe em nenhum outro
    campo (título, meta description, corpo continuam intactos)."""
    novo_fm = {**fm, "imagem_capa": f"imagens/{manifest['slug']}.png", "imagem_gerada_em": manifest["gerado_em"],
               "imagem_modelo": manifest["modelo"]}
    write_markdown(path, novo_fm, body)
    return novo_fm


def update_jsonld_image(fm: dict, dominio: str) -> None:
    jsonld_path = ROOT / fm.get("dados_estruturados_arquivo", "")
    if not jsonld_path.exists():
        return
    data = json.loads(jsonld_path.read_text(encoding="utf-8"))
    url_imagem = f"{dominio.rstrip('/')}/imagens/{fm['slug']}.png"
    if "article" in data:
        data["article"]["image"] = url_imagem
    jsonld_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# --------------------------------------------------------------------------- relatório
def render_blocked_report(motivo: str, n_artigos: int, n_ja_geradas: int) -> str:
    return (
        f"# Agente 15 — aguardando credenciais\n\n"
        f"- **Gerado em:** {now_iso()}\n"
        f"- **Status:** ⛔ aguardando_credenciais\n"
        f"- **Motivo:** {motivo}\n"
        f"- **Artigos no catálogo:** {n_artigos}\n"
        f"- **Imagens já geradas anteriormente:** {n_ja_geradas}\n\n"
        "## Como destravar\n\n"
        "1. Gere uma chave em platform.openai.com (Settings → API keys).\n"
        "2. Adicione `OPENAI_API_KEY=<sua chave>` no arquivo `.env` na raiz do projeto "
        "(nunca no `.env.example`, e nunca cole a chave direto no chat).\n"
        "3. Rode este agente de novo.\n\n"
        "Nenhuma chamada de API foi feita nem nenhum custo gerado até este ponto.\n"
    )


def render_run_report(resultados: list[dict], erros: list[dict]) -> str:
    custo_total = sum(r["custo_estimado_usd"] for r in resultados)
    L = [
        "# Agente 15 — relatório de geração de imagens", "", f"- **Gerado em:** {now_iso()}",
        f"- **Imagens geradas nesta rodada:** {len(resultados)}", f"- **Falhas:** {len(erros)}",
        f"- **Custo estimado desta rodada:** US$ {custo_total:.3f}", "",
        "## Imagens geradas", "", "| Artigo | Arquivo | Custo estimado |", "|---|---|---|",
    ]
    L += [f"| {r['slug']} | {r['arquivo']} | US$ {r['custo_estimado_usd']:.3f} |" for r in resultados]
    if erros:
        L += ["", "## Falhas", ""] + [f"- **{e['slug']}**: {e['erro']}" for e in erros]
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- entrypoint
def run(context: dict) -> dict:
    log = context["logger"]
    site_id = context["site_id"]
    site = context.get("site") or load_site(site_id)
    settings = load_visual_settings()

    artigos = []
    for path in sorted(OTIMIZADOS_DIR.glob("*.md")):
        try:
            fm, body = read_markdown(path)
        except MarkdownError:
            continue
        if context.get("slug") and fm.get("slug") != context["slug"]:
            continue
        artigos.append((path, fm, body))

    ja_geradas = sum(1 for _, fm, _ in artigos if fm.get("imagem_capa"))
    ok_credenciais, motivo = check_credenciais()

    VISUAL_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")

    if not ok_credenciais:
        relatorio_md = render_blocked_report(motivo, len(artigos), ja_geradas)
        out_path = VISUAL_DIR / f"relatorio_{date_str}.md"
        out_path.write_text(relatorio_md, encoding="utf-8")
        log.warning(f"[{AGENT_NAME}] modo aguardando_credenciais: {motivo}")
        return {
            "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "site_id": site_id, "gerado_em": now_iso(),
            "status": "aguardando_credenciais", "n_artigos": len(artigos), "n_ja_geradas": ja_geradas,
            "relatorio": str(out_path.relative_to(ROOT)), "pendencias_humanas": [motivo],
        }

    api_key = os.environ["OPENAI_API_KEY"]
    pendentes = [(p, fm, body) for p, fm, body in artigos if not fm.get("imagem_capa") or context.get("forcar")]
    resultados, erros = [], []
    for path, fm, body in pendentes:
        try:
            manifest = generate_image_for_article(fm, settings, api_key, log)
            update_article_with_image(path, fm, body, manifest)
            fm_atualizado = {**fm, "imagem_capa": f"imagens/{fm['slug']}.png"}
            update_jsonld_image(fm_atualizado, site["dominio"])
            resultados.append(manifest)
        except (urllib.error.URLError, KeyError, ValueError, OSError) as ex:
            erros.append({"slug": fm["slug"], "erro": str(ex)})
            log.error(f"[{AGENT_NAME}] falha ao gerar imagem para '{fm['slug']}': {ex}")

    relatorio_md = render_run_report(resultados, erros)
    out_path = VISUAL_DIR / f"relatorio_{date_str}.md"
    out_path.write_text(relatorio_md, encoding="utf-8")

    pendencias = [f"{len(resultados)} imagem(ns) gerada(s) — rode `python site/build_site.py --site {site_id}` "
                  "para publicá-las no site."]
    if erros:
        pendencias += [f"[erro] {e['slug']}: {e['erro']}" for e in erros]

    output = {
        "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "site_id": site_id, "gerado_em": now_iso(),
        "status": "ok", "n_geradas": len(resultados), "n_erros": len(erros),
        "custo_estimado_usd": sum(r["custo_estimado_usd"] for r in resultados),
        "relatorio": str(out_path.relative_to(ROOT)), "pendencias_humanas": pendencias,
    }
    log.info(f"[{AGENT_NAME}] geradas={len(resultados)} erros={len(erros)} "
             f"custo≈US${output['custo_estimado_usd']:.3f} → {out_path.relative_to(ROOT)}")
    return output


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 15 — geração de imagem de capa por IA")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    parser.add_argument("--slug", help="gerar/regenerar só este artigo")
    parser.add_argument("--forcar", action="store_true", help="regenerar mesmo artigos que já têm imagem_capa")
    args = parser.parse_args()

    load_env_file()
    run_id = f"{now_iso().replace(':', '').replace('+0000', 'Z')}-{AGENT_NAME}"
    output = run({"site_id": args.site, "slug": args.slug, "forcar": args.forcar, "logger": get_logger(run_id)})
    return 0 if output["status"] in ("ok", "aguardando_credenciais") else 2


if __name__ == "__main__":
    sys.exit(main())
