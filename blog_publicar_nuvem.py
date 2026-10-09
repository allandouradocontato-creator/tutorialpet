"""Publica um artigo no blog na nuvem: editor de qualidade -> SEO -> capa -> site/build.

Uso: python blog_publicar_nuvem.py <pasta_media> [slug indice]
Sem slug/indice, publica TODAS as linhas de config/blog_aprovados.txt ainda não publicadas ("<slug> <indice_da_foto>").
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


def preparar(slug: str, indice: str, media: Path | None) -> None:
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


def ja_publicado(slug: str) -> bool:
    pagina = ROOT / "site" / "build" / f"{slug}.html"
    return pagina.exists() and f"imagens/{slug}.jpg" in pagina.read_text(encoding="utf-8")


def main() -> int:
    media = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if len(sys.argv) >= 4:
        fila = [(sys.argv[2], sys.argv[3])]
    else:
        # TODAS as linhas ainda não publicadas (antes só a última: com 2 artigos por dia o outro se perdia)
        linhas = [l.split() for l in (ROOT / "config" / "blog_aprovados.txt").read_text(encoding="utf-8").splitlines()
                  if l.strip() and not l.lstrip().startswith("#")]
        fila = [(l[0], l[1]) for l in linhas if len(l) >= 2 and not ja_publicado(l[0])]
        if not linhas:
            raise SystemExit("config/blog_aprovados.txt vazio ou sem 'slug indice'")
        if not fila:
            print("nada pendente: todos os artigos aprovados já estão no site")
            return 0
    erros = []
    for slug, indice in fila:
        try:
            preparar(slug, indice, media)
        except SystemExit as e:
            erros.append(f"{slug}: {e}")
            print("ERRO:", slug, e, flush=True)
    run([sys.executable, "site/build_site.py", "--site", SITE])
    for slug, _ in fila:
        if not any(e.startswith(slug + ":") for e in erros):
            if not ja_publicado(slug):
                erros.append(f"{slug}: página gerada sem a imagem de capa; não publicar")
            else:
                print("ARTIGO PRONTO NO SITE:", ROOT / "site" / "build" / f"{slug}.html")
    if erros:
        print("FALHAS:\n" + "\n".join(erros))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
