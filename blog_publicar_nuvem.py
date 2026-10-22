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
REPROVADOS = ROOT / "config" / "blog_reprovados.txt"   # "<slug> <tentativas_de_reescrita>"; a fábrica reescreve e tira daqui


def ler_reprovados() -> dict[str, int]:
    if not REPROVADOS.exists():
        return {}
    out = {}
    for l in REPROVADOS.read_text(encoding="utf-8").splitlines():
        t = l.split()
        if t and not t[0].startswith("#"):
            out[t[0]] = int(t[1]) if len(t) > 1 and t[1].isdigit() else 0
    return out


def registrar_reprovados(slugs: set[str]) -> None:
    atual = ler_reprovados()
    novos = [s for s in sorted(slugs) if s not in atual]
    if novos:
        with REPROVADOS.open("a", encoding="utf-8") as f:
            for s in novos:
                f.write(f"{s} 0\n")
        print(f"registrados em blog_reprovados.txt (a fábrica reescreve): {novos}")


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
    # coerência de raça/espécie da capa (regra do Allan, 15/10/2026): dentro da produção do artigo
    try:
        from core.coerencia import detectar, verificar_imagens
        especie, raca = detectar(slug)
        if especie or raca:
            fotos = sorted(cand.glob("*.jpg"), key=lambda f: (f.stem != str(indice), f.stem))
            for f in fotos:
                ok_c, motivo = verificar_imagens([f.read_bytes()], especie, raca, primeira_obrigatoria=True)
                print(f"[coerencia] capa {f.name}: {'ok' if ok_c else 'REPROVADA'} - {motivo}")
                if ok_c and "não verificada" not in motivo:
                    if f.stem != str(indice):
                        print(f"[coerencia] trocando a capa {indice} pela {f.stem}")
                        indice = f.stem
                    break
            else:
                if raca:
                    raise SystemExit(f"coerência: nenhuma foto candidata mostra a raça '{raca}' ({slug}); não publica com raça errada")
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print("[coerencia] não verificada:", str(exc)[:100])
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
        reprov = ler_reprovados()
        for l in linhas:
            if l and l[0] in reprov:
                print(f"ignorado (reprovado, aguardando reescrita automática): {l[0]}")
        fila = [(l[0], l[1]) for l in linhas if len(l) >= 2 and l[0] not in reprov and not ja_publicado(l[0])]
        if not linhas:
            raise SystemExit("config/blog_aprovados.txt vazio ou sem 'slug indice'")
        if not fila:
            print("nada pendente: todos os artigos aprovados já estão no site")
            return 0
    erros = []
    publicados = []
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
                publicados.append(slug)
    # 21/10: slug reprovado (editor, coerência ou capa) tirado de blog_aprovados.txt aqui mesmo,
    # para não ficar travando toda rodada futura até alguém limpar a mão (era a causa do #23/#24 vermelho).
    if erros and len(sys.argv) < 4:
        aprovados_path = ROOT / "config" / "blog_aprovados.txt"
        reprovados_slugs = {e.split(":", 1)[0] for e in erros}
        registrar_reprovados({e.split(":", 1)[0] for e in erros if "04_quality_editor" in e})
        linhas_novas = [l for l in aprovados_path.read_text(encoding="utf-8").splitlines()
                         if l.split()[0] not in reprovados_slugs if l.strip()]
        aprovados_path.write_text("\n".join(linhas_novas) + ("\n" if linhas_novas else ""), encoding="utf-8")
        print(f"removidos de blog_aprovados.txt (reprovados): {sorted(reprovados_slugs)}")
    if erros:
        print("FALHAS:\n" + "\n".join(erros))
    # 21/10 (decisão V02 do Vigia): sair 0 quando publicou >=1, mesmo com reprovados no lote,
    # para o job não ficar vermelho por causa de UM slug ruim enquanto os outros foram ao ar.
    if publicados:
        return 0
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
