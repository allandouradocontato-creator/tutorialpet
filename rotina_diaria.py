"""Rotina diária do Tutorial Pet (roda sozinha pelo Agendador de Tarefas do Windows).

Faz, em ordem:
 1. Mantém a fila de temas (config/fila_temas.yaml). Se tiver menos de 3 pendentes, pede ao Gemini 8 temas novos
    do nicho (sem repetir o que já existe) — pesquisa de pauta.
 2. Pega o próximo tema e escreve o artigo com a voz da vez (Agente 03, WRITER_MODE=llm).
 3. Gera o roteiro de vídeo a partir do artigo (cenas, narração, legenda com link do produto NO COMEÇO).
 4. Grava um relatório em logs/rotina_AAAAMMDD.txt.

NÃO publica nada: blog, Facebook e Instagram só saem depois da revisão (portão humano/Claude).
Uso manual: python rotina_diaria.py [--dry]
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from core.config import load_env_file, load_site  # noqa: E402
from core.io import slugify  # noqa: E402
from core.llm import LLMError, gerar_texto  # noqa: E402

FILA = ROOT / "config" / "fila_temas.yaml"
RASCUNHOS = ROOT / "data" / "content_writer" / "rascunhos"
SITE_ID = "pets-tutores-iniciantes"
LOG_LINES: list[str] = []


def log(msg: str) -> None:
    linha = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(linha)
    LOG_LINES.append(linha)


def carregar_fila() -> dict:
    if FILA.exists():
        return yaml.safe_load(FILA.read_text(encoding="utf-8")) or {"temas": []}
    return {"temas": []}


def salvar_fila(fila: dict) -> None:
    FILA.write_text(yaml.safe_dump(fila, allow_unicode=True, sort_keys=False), encoding="utf-8")


def slugs_existentes() -> set[str]:
    return {p.stem for p in RASCUNHOS.glob("*.md")}


def repor_fila(fila: dict) -> None:
    pendentes = [t for t in fila["temas"] if t.get("status") == "pendente"]
    if len(pendentes) >= 3:
        return
    site = load_site(SITE_ID)
    pilares = list((site.get("pilares") or {}).keys())
    ja = sorted(slugs_existentes() | {slugify(t["termo"]) for t in fila["temas"]})
    prompt = (
        f"Nicho: {site['nicho']}. Público: tutores de primeira viagem no Brasil.\n"
        f"Pilares permitidos: {', '.join(pilares)}.\n"
        f"Já existem estes artigos (slugs), NÃO repita nem faça variações próximas: {', '.join(ja)}.\n"
        "Sugira 8 novos temas com demanda real de busca no Google Brasil (perguntas que tutores iniciantes fazem). "
        "Responda SOMENTE JSON: [{\"termo\": str, \"pilar\": str}]"
    )
    txt = gerar_texto(prompt, sistema="Você é pesquisador de pautas de SEO para blog de pets em pt-BR.", temperatura=0.7)
    txt = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    novos = json.loads(txt[txt.find("["): txt.rfind("]") + 1])
    adicionados = 0
    for n in novos:
        termo = (n.get("termo") or "").strip()
        pilar = n.get("pilar") if n.get("pilar") in pilares else (pilares[0] if pilares else "comportamento")
        if termo and slugify(termo) not in set(ja):
            fila["temas"].append({"termo": termo, "pilar": pilar, "status": "pendente"})
            adicionados += 1
    log(f"fila reposta: +{adicionados} temas novos")


def rodar(cmd: list[str], extra_env: dict | None = None) -> tuple[int, str]:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", **(extra_env or {})}
    r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout + r.stderr)[-1500:]


def main() -> int:
    load_env_file()
    dry = "--dry" in sys.argv
    fila = carregar_fila()
    try:
        repor_fila(fila)
    except (LLMError, ValueError) as exc:
        log(f"AVISO: não consegui repor a fila ({exc})")
    # Pula tema "pendente" que já tem rascunho pronto (evita reescrever o mesmo artigo todo dia)
    existentes = slugs_existentes()
    for t in fila["temas"]:
        if t.get("status") == "pendente" and slugify(t["termo"]) in existentes:
            t["status"] = "rascunho_pronto"
            log(f"tema já tinha rascunho, marcado como pronto: {t['termo']}")
    proximo = next((t for t in fila["temas"] if t.get("status") == "pendente"), None)
    if not proximo:
        log("ERRO: fila vazia e sem como repor. Nada produzido.")
        salvar_fila(fila)
        return 1
    log(f"tema do dia: {proximo['termo']} [{proximo['pilar']}]")
    if dry:
        log("dry-run: parando antes de escrever")
        salvar_fila(fila)
        return 0

    py = sys.executable
    code, out = rodar([py, "agents/03_content_writer/agent.py", "--site", SITE_ID,
                       "--termo", proximo["termo"], "--pilar", proximo["pilar"]], {"WRITER_MODE": "llm"})
    slug = slugify(proximo["termo"])
    arquivo = RASCUNHOS / f"{slug}.md"
    log("saída do escritor (fim): " + " | ".join(out.strip().splitlines()[-6:])[:600])
    if code != 0 or not arquivo.exists():
        proximo["status"] = "erro"
        proximo["erro"] = out[-300:]
        log(f"ERRO ao escrever o artigo: {out[-300:]}")
        salvar_fila(fila)
        return 1
    log(f"artigo escrito: {arquivo.name}")

    code, out = rodar([py, "agents/03_content_writer/roteiro_video.py", str(arquivo)])
    roteiro = ROOT / "data" / "social" / "roteiros" / f"{slug}.json"
    log("roteiro de vídeo pronto" if code == 0 and roteiro.exists() else f"AVISO roteiro falhou: {out[-300:]}")

    proximo["status"] = "rascunho_pronto"
    proximo["data"] = datetime.now().strftime("%Y-%m-%d")
    salvar_fila(fila)
    log("PRONTO PARA REVISÃO — nada foi publicado.")
    return 0


if __name__ == "__main__":
    rc = main()
    (ROOT / "logs").mkdir(exist_ok=True)
    (ROOT / "logs" / f"rotina_{datetime.now().strftime('%Y%m%d')}.txt").write_text("\n".join(LOG_LINES), encoding="utf-8")
    sys.exit(rc)
