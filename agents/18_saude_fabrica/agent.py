"""Agente 18 — Saúde da Fábrica (orquestrador de verificação).

Roda DEPOIS da produção diária e diz, sem rodeio, se o pacote do dia está bom. Existe porque a
fábrica antes ficava "verde" mesmo quebrada (passos com `|| true`). Aqui toda falha crítica vira
código de saída 1, relatório em data/saude/ e (no workflow) um alerta aberto no GitHub.

Só LÊ arquivos; nunca altera artigo, vídeo ou fila.

Uso:
    python agents/18_saude_fabrica/agent.py <pasta_saida_com_pacotes> [--slug SLUG] [--max-idade-h 36]
Saída: data/saude/ultimo.json e data/saude/ultimo.md. Código 0 = sem críticos; 1 = há crítico.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

SAIDA_DIR = ROOT / "data" / "saude"
ARQUIVOS_OBRIGATORIOS = ["artigo.md", "roteiro.json", "video.mp4", "legenda.txt", "manifest.json"]
CHAVES_ROTEIRO = ["titulo_video", "gancho_3s", "cenas", "chamada_final", "legenda", "slug"]
VIDEO_MIN_S, VIDEO_MAX_S = 8.0, 75.0
COMECO_ARTIGO_CHARS = 700  # regra do Allan: link do produto bem visível no começo


def _item(nivel: str, nome: str, detalhe: str = "") -> dict:
    return {"nivel": nivel, "nome": nome, "detalhe": detalhe}


def links_dos_produtos() -> list[str]:
    path = ROOT / "config" / "produtos_relacionados.yaml"
    if not path.exists():
        return []
    dados = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return [p["link"] for p in dados.get("produtos", []) if p.get("link", "").startswith("http")]


def achar_pacote(saida: Path, slug: str | None) -> Path | None:
    base = saida / "pacotes"
    if not base.exists():
        return None
    if slug:
        p = base / slug
        return p if p.exists() else None
    candidatos = [p for p in base.iterdir() if (p / "manifest.json").exists()]
    if not candidatos:
        return None

    def criado(p: Path) -> str:
        try:
            return json.loads((p / "manifest.json").read_text(encoding="utf-8")).get("criado_em", "")
        except (ValueError, OSError):
            return ""

    return max(candidatos, key=criado)


def duracao_e_audio(video: Path) -> tuple[float | None, bool]:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
             "-of", "json", str(video)], capture_output=True, text=True, timeout=60)
        dados = json.loads(out.stdout or "{}")
        dur = float(dados.get("format", {}).get("duration", 0)) or None
        audio = any(s.get("codec_type") == "audio" for s in dados.get("streams", []))
        return dur, audio
    except (OSError, ValueError, subprocess.SubprocessError):
        return None, False


def checar_pacote(pkg: Path, max_idade_h: float) -> list[dict]:
    r: list[dict] = []
    for nome in ARQUIVOS_OBRIGATORIOS:
        f = pkg / nome
        if not f.exists():
            r.append(_item("critico", f"arquivo {nome}", "não existe"))
        elif f.stat().st_size == 0:
            r.append(_item("critico", f"arquivo {nome}", "está vazio"))
        else:
            r.append(_item("ok", f"arquivo {nome}", f"{f.stat().st_size} bytes"))

    # manifest: idade do pacote (pega o caso "a rodada de hoje não produziu nada, sobrou o de ontem")
    try:
        manifest = json.loads((pkg / "manifest.json").read_text(encoding="utf-8"))
        criado = datetime.fromisoformat(manifest["criado_em"])
        idade = datetime.now(timezone.utc) - criado
        if idade > timedelta(hours=max_idade_h):
            r.append(_item("critico", "pacote é de hoje", f"último pacote tem {idade.total_seconds()/3600:.0f} h"))
        else:
            r.append(_item("ok", "pacote é de hoje", f"criado há {idade.total_seconds()/3600:.1f} h"))
    except (OSError, ValueError, KeyError):
        manifest = {}
        r.append(_item("critico", "manifest.json legível", "inválido ou sem criado_em"))

    # roteiro
    try:
        roteiro = json.loads((pkg / "roteiro.json").read_text(encoding="utf-8"))
        faltam = [k for k in CHAVES_ROTEIRO if not roteiro.get(k)]
        if faltam:
            r.append(_item("critico", "roteiro completo", "faltam: " + ", ".join(faltam)))
        elif len(roteiro["cenas"]) < 3:
            r.append(_item("aviso", "roteiro completo", f"só {len(roteiro['cenas'])} cenas"))
        else:
            r.append(_item("ok", "roteiro completo", f"{len(roteiro['cenas'])} cenas"))
    except (OSError, ValueError):
        r.append(_item("critico", "roteiro legível", "JSON inválido"))

    # vídeo
    video = pkg / "video.mp4"
    if video.exists() and video.stat().st_size > 0:
        dur, audio = duracao_e_audio(video)
        if dur is None:
            r.append(_item("critico", "vídeo abre", "ffprobe não conseguiu ler"))
        elif not (VIDEO_MIN_S <= dur <= VIDEO_MAX_S):
            r.append(_item("critico", "duração do vídeo", f"{dur:.1f}s fora de {VIDEO_MIN_S:.0f}-{VIDEO_MAX_S:.0f}s"))
        else:
            r.append(_item("ok", "duração do vídeo", f"{dur:.1f}s"))
        r.append(_item("ok" if audio else "critico", "vídeo tem áudio", "" if audio else "sem faixa de áudio (narração)"))

    # legenda: precisa de link do produto E link do artigo (regra de cross-promoção)
    leg_path = pkg / "legenda.txt"
    if leg_path.exists():
        legenda = leg_path.read_text(encoding="utf-8")
        produtos = links_dos_produtos()
        if not produtos:
            r.append(_item("aviso", "link do produto na legenda", "nenhum produto cadastrado em produtos_relacionados.yaml"))
        elif not any(l in legenda for l in produtos):
            r.append(_item("critico", "link do produto na legenda", "legenda sem o link do produto"))
        else:
            r.append(_item("ok", "link do produto na legenda"))
        url_artigo = manifest.get("artigo_url_futura", "")
        if url_artigo and url_artigo not in legenda:
            r.append(_item("critico", "link do artigo na legenda", url_artigo))
        elif url_artigo:
            r.append(_item("ok", "link do artigo na legenda"))

    # artigo: link do produto bem no começo (regra do Allan). Aviso, não bloqueio, até a regra entrar no escritor.
    art = pkg / "artigo.md"
    if art.exists():
        texto = art.read_text(encoding="utf-8")
        produtos = links_dos_produtos()
        if produtos and not any(l in texto[:COMECO_ARTIGO_CHARS] for l in produtos):
            r.append(_item("aviso", "link do produto no começo do artigo",
                           f"não aparece nos primeiros {COMECO_ARTIGO_CHARS} caracteres"))
        elif produtos:
            r.append(_item("ok", "link do produto no começo do artigo"))
    return r


def checar_ambiente() -> list[dict]:
    r: list[dict] = []
    modo = os.environ.get("WRITER_MODE", "")
    if modo == "llm":
        r.append(_item("ok" if os.environ.get("GEMINI_API_KEY") else "critico", "GEMINI_API_KEY presente",
                       "" if os.environ.get("GEMINI_API_KEY") else "secret ausente no repositório"))
    r.append(_item("ok" if os.environ.get("PEXELS_API_KEY") else "aviso", "PEXELS_API_KEY presente",
                   "" if os.environ.get("PEXELS_API_KEY") else "sem fotos do Pexels (cai no fundo liso)"))
    return r


def checar_fila() -> list[dict]:
    path = ROOT / "config" / "fila_temas.yaml"
    try:
        temas = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("temas", [])
    except (OSError, yaml.YAMLError):
        return [_item("critico", "fila de temas legível", str(path))]
    pendentes = sum(1 for t in temas if t.get("status") == "pendente")
    if pendentes == 0:
        return [_item("critico", "fila de temas", "nenhum tema pendente: amanhã a fábrica não tem o que produzir")]
    if pendentes < 5:
        return [_item("aviso", "fila de temas", f"só {pendentes} pendentes (ideal ≥ 5; rode o agente 19)")]
    return [_item("ok", "fila de temas", f"{pendentes} pendentes")]


def relatorio_md(itens: list[dict], pkg: Path | None) -> str:
    icone = {"ok": "OK ", "aviso": "AVISO", "critico": "FALHA"}
    linhas = [f"# Saúde da fábrica — {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC",
              f"Pacote avaliado: `{pkg.name if pkg else 'NENHUM'}`", ""]
    for nivel in ("critico", "aviso", "ok"):
        for i in (x for x in itens if x["nivel"] == nivel):
            det = f" — {i['detalhe']}" if i["detalhe"] else ""
            linhas.append(f"- **{icone[nivel]}** {i['nome']}{det}")
    return "\n".join(linhas) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("saida", help="pasta que contém pacotes/<slug>/")
    ap.add_argument("--slug")
    ap.add_argument("--max-idade-h", type=float, default=36.0)
    args = ap.parse_args()

    itens: list[dict] = []
    pkg = achar_pacote(Path(args.saida), args.slug)
    if pkg is None:
        itens.append(_item("critico", "pacote do dia", f"nenhum pacote encontrado em {args.saida}/pacotes"))
    else:
        itens += checar_pacote(pkg, args.max_idade_h)
    itens += checar_ambiente() + checar_fila()

    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    criticos = [i for i in itens if i["nivel"] == "critico"]
    (SAIDA_DIR / "ultimo.json").write_text(json.dumps(
        {"quando": datetime.now(timezone.utc).isoformat(timespec="seconds"),
         "pacote": pkg.name if pkg else None, "ok": not criticos, "itens": itens},
        ensure_ascii=False, indent=2), encoding="utf-8")
    md = relatorio_md(itens, pkg)
    (SAIDA_DIR / "ultimo.md").write_text(md, encoding="utf-8")
    print(md)
    return 1 if criticos else 0


if __name__ == "__main__":
    sys.exit(main())
