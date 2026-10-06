"""Fábrica Tutorial Pet na nuvem (GitHub Actions): artigo -> roteiro -> vídeo -> pacote.

Roda sem o PC do Allan. Saída em <saida>/pacotes/<slug>/ : artigo.md, roteiro.json, video.mp4, legenda.txt, manifest.json
Nada é publicado aqui: o pacote fica 'aguardando_revisao' (portão de qualidade do Claude) e depois é agendado no Metricool.
Uso: python fabrica_nuvem.py <pasta_saida>
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RASC = ROOT / "data" / "content_writer" / "rascunhos"


def run(cmd: list[str], env_extra: dict | None = None) -> None:
    import os
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", **(env_extra or {})}
    print("$", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT, env=env)
    if r.returncode != 0:
        raise SystemExit(f"falhou ({r.returncode}): {' '.join(cmd)}")


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit("uso: python fabrica_nuvem.py <pasta_saida>")
    saida = Path(sys.argv[1])
    antes = {p.name for p in RASC.glob("*.md")} if RASC.exists() else set()
    run([sys.executable, "rotina_diaria.py"], {"WRITER_MODE": "llm"})
    novos = [p for p in RASC.glob("*.md") if p.name not in antes]
    if not novos:
        print("nenhum artigo novo produzido")
        return 1
    artigo = max(novos, key=lambda p: p.stat().st_mtime)
    slug = artigo.stem
    roteiro = ROOT / "data" / "social" / "roteiros" / f"{slug}.json"
    if not roteiro.exists():
        raise SystemExit(f"roteiro não gerado: {roteiro}")
    run([sys.executable, "agents/17_video/montar_video6.py", str(roteiro)])
    video = ROOT / "data" / "social" / "videos" / f"{slug}_v2.mp4"
    legenda = ROOT / "data" / "social" / "videos" / f"{slug}_v2.legenda.txt"
    if not video.exists():
        raise SystemExit("vídeo não gerado")
    pkg = saida / "pacotes" / slug
    pkg.mkdir(parents=True, exist_ok=True)
    shutil.copy(artigo, pkg / "artigo.md")
    shutil.copy(roteiro, pkg / "roteiro.json")
    shutil.copy(video, pkg / "video.mp4")
    shutil.copy(legenda, pkg / "legenda.txt")
    (pkg / "manifest.json").write_text(json.dumps({
        "slug": slug, "status": "aguardando_revisao",
        "criado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "artigo_url_futura": f"https://tutorialpet.com.br/{slug}",
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PACOTE PRONTO:", pkg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
