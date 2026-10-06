"""Publica um artigo no blog na nuvem: editor de qualidade -> SEO -> capa -> site/build.

Uso: python blog_publicar_nuvem.py <pasta_media> [slug indice]
Sem slug/indice, lê a ÚLTIMA linha de config/blog_aprovados.txt ("<slug> <indice_da_foto>").
A linha é escrita pelo Publicador (Claude) depois de revisar o pacote e escolher a foto (só animal).
Entrada: rascunho em data/content_writer/rascunhos/<slug>.md (main) + fotos candidatas em
<pasta_media>/pacotes/<slug>/imagens_candidatas/ (branch media).
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "pets-tutores-iniciantes"


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    if r.returncode != 0:
        raise SystemExit(f"falhou ({r.returncode}): {' '.join(cmd)}")


def main() -> int:
    media = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if len(sys.argv) >= 4:
        slug, indice = sys.argv[2], sys.argv[3]
    else:
        linhas = [l.split() for l in (ROOT / "config" / "blog_aprovados.txt").read_text(encoding="utf-8").splitlines()
                  if l.strip() and not l.lstrip().startswith("#")]
        if not linhas or len(linhas[-1]) < 2:
            raise SystemExit("config/blog_aprovados.txt vazio ou sem 'slug indice'")
        slug, indice = linhas[-1][0], linhas[-1][1]
    if not (ROOT / "data" / "content_writer" / "rascunhos" / f"{slug}.md").exists():
        raise SystemExit(f"rascunho não encontrado: {slug}")
    cand = ROOT / "data" / "visual" / "candidatos" / slug
    if media:
        origem = media / "pacotes" / slug / "imagens_candidatas"
        if origem.exists():
            shutil.copytree(origem, cand, dirs_exist_ok=True)
    if not (cand / "candidatos.json").exists():
        raise SystemExit(f"sem fotos candidatas para {slug}")
    py = sys.executable
    run([py, "agents/04_quality_editor/agent.py", "--site", SITE, "--slug", slug])   # rc!=0 = reprovado: não publica
    run([py, "agents/05_seo_onpage/agent.py", "--site", SITE, "--slug", slug])
    run([py, "agents/15_visual/agent.py", "--site", SITE, "--selecionar", slug, str(indice)])
    run([py, "site/build_site.py", "--site", SITE])
    pagina = ROOT / "site" / "build" / f"{slug}.html"
    if not pagina.exists() or f"imagens/{slug}.jpg" not in pagina.read_text(encoding="utf-8"):
        raise SystemExit("página gerada sem a imagem de capa; não publicar")
    print("ARTIGO PRONTO NO SITE:", pagina)
    return 0


if __name__ == "__main__":
    sys.exit(main())
