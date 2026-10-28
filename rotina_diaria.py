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


def hoje_fortaleza() -> str:
    """Data do DIA EDITORIAL (America/Fortaleza). O runner do GitHub roda em UTC: uma rodada de reserva depois das
    21h de Fortaleza caia no 'dia seguinte' e o rodizio de pilares recomecava no meio do dia (28/10/2026)."""
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("America/Fortaleza")).strftime("%Y-%m-%d")
    except Exception:  # sem tzdata: UTC-3 fixo (Fortaleza nao tem horario de verao)
        from datetime import timedelta, timezone
        return datetime.now(timezone(timedelta(hours=-3))).strftime("%Y-%m-%d")


def _ritmo_cfg() -> dict:
    try:
        return yaml.safe_load((ROOT / "config" / "ritmo_blog.yaml").read_text(encoding="utf-8")) or {}
    except Exception:  # noqa: BLE001
        return {}


def escolher_proximo(fila: dict, hoje: str | None = None) -> dict | None:
    """RODIZIO DE PILARES (ritmo fixo de 3 artigos/dia, config/ritmo_blog.yaml). Regras, nesta ordem:
    1) NUNCA repetir no mesmo dia um pilar que ainda tem alternativa: os pilares ja usados HOJE ficam bloqueados.
    2) Na virada de dia, o 1o artigo nao repete o pilar do ultimo artigo do dia anterior (nem os do dia anterior,
       se houver alternativa).
    3) Entre os livres, vence o pilar usado ha mais tempo (nunca usado vem primeiro); empate = ordem da fila.
    4) Se so sobrar pilar ja usado hoje (mais de 5 producoes no dia, p.ex. disparos manuais), escolhe o pilar MENOS
       usado hoje e avisa; nunca cai cegamente em pendentes[0].
    A fila guarda so a DATA (dia de Fortaleza) da producao; entradas sem data (rascunho que ja existia) nao contam."""
    hoje = hoje or hoje_fortaleza()
    pendentes = [t for t in fila["temas"] if t.get("status") == "pendente"]
    if not pendentes:
        return None
    usados = [t for t in fila["temas"] if t.get("status") != "pendente" and t.get("data") and t.get("pilar")]
    usos_hoje: dict[str, int] = {}
    ultimo_uso: dict[str, str] = {}
    for t in usados:
        d = str(t["data"])
        ultimo_uso[t["pilar"]] = max(ultimo_uso.get(t["pilar"], ""), d)
        if d == hoje:
            usos_hoje[t["pilar"]] = usos_hoje.get(t["pilar"], 0) + 1
    # Regra 2: se ainda nao ha producao hoje, a referencia e o dia mais recente anterior a hoje.
    anteriores = [str(t["data"]) for t in usados if str(t["data"]) < hoje]
    dia_ref = max(anteriores) if (not usos_hoje and anteriores) else None
    bloqueados = set(usos_hoje) | ({t["pilar"] for t in usados if str(t["data"]) == dia_ref} if dia_ref else set())

    prioritarios = set(_ritmo_cfg().get("pilares_prioritarios") or [])

    def chave(t: dict) -> tuple:
        # series prioritarias (adocao, utilidade_publica) primeiro; o bloqueio de "ja usado hoje" garante 1/dia
        return (0 if t.get("pilar") in prioritarios else 1, ultimo_uso.get(t.get("pilar"), ""), pendentes.index(t))

    livres = [t for t in pendentes if t.get("pilar") not in bloqueados]
    if not livres and dia_ref:      # regra 2 sem alternativa: relaxa so a virada de dia, mantem o bloqueio de hoje
        livres = [t for t in pendentes if t.get("pilar") not in usos_hoje]
    if livres:
        return min(livres, key=chave)
    log(f"AVISO: so ha pendentes de pilares ja usados hoje ({hoje}): {usos_hoje}; escolhendo o menos usado hoje. "
        "Repor a fila com os outros pilares.")
    return min(pendentes, key=lambda t: (usos_hoje.get(t.get("pilar"), 0), ultimo_uso.get(t.get("pilar"), ""), pendentes.index(t)))


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
        "Distribua os temas entre TODOS os pilares permitidos (no minimo 1 por pilar; nunca mais de 2 do mesmo pilar), "
        "porque a fabrica alterna os pilares e nao publica dois seguidos do mesmo. "
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
    proximo = escolher_proximo(fila)
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
    # trava de seguranca: pilar desconhecido pelo escritor derrubava a rodada inteira (15/10/2026, 'saude_basica')
    _validos = {"alimentacao", "comportamento", "cuidados_diarios", "primeiros_passos_filhotes", "produtos_compras", "adocao", "utilidade_publica", "pauta_especifica"}
    if proximo.get("pilar") not in _validos:
        log(f"AVISO: pilar '{proximo.get('pilar')}' invalido; usando cuidados_diarios")
        proximo["pilar"] = "cuidados_diarios"
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
    proximo["data"] = hoje_fortaleza()
    salvar_fila(fila)
    log("PRONTO PARA REVISÃO — nada foi publicado.")
    return 0


if __name__ == "__main__":
    rc = main()
    (ROOT / "logs").mkdir(exist_ok=True)
    (ROOT / "logs" / f"rotina_{datetime.now().strftime('%Y%m%d')}.txt").write_text("\n".join(LOG_LINES), encoding="utf-8")
    sys.exit(rc)
