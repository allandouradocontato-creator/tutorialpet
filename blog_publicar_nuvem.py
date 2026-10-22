"""Publica um artigo no blog na nuvem: editor de qualidade -> SEO -> capa -> site/build.

Uso: python blog_publicar_nuvem.py <pasta_media> [slug indice]
Sem slug/indice, publica TODAS as linhas de config/blog_aprovados.txt ainda não publicadas ("<slug> <indice_da_foto>").
A linha é escrita pelo Publicador (Claude) depois de revisar o pacote e escolher a foto (só animal).
Entrada: rascunho em data/content_writer/rascunhos/<slug>.md (main) + fotos candidatas em
<pasta_media>/pacotes/<slug>/imagens_candidatas/ (branch media).
"""
from __future__ import annotations

import json
import os
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


# --- Portão de raça em camadas (Allan, 22/10/2026): 1) Gemini, 2) Cloudflare llava+llama, 3) título da foto na fonte
# confirma quando só o juiz fraco (CF) reprova, 4) sem foto do banco que passe: gera a foto da raça por IA grátis. ---
_VER: dict[str, bool] = {}   # stem da foto -> passou no portão de raça


def _fonte_cita_raca(cand: Path, stem: str, raca: str) -> bool:
    try:
        lista = json.loads((cand / "candidatos.json").read_text(encoding="utf-8"))
        c = next((x for x in lista if str(x.get("indice")) == str(stem)), None)
        if not c or c.get("fonte") != "pexels":
            return False
        sys.path.insert(0, str(ROOT / "scripts"))
        from gerar_foto_ia import EN
        url = (c.get("url_pagina") or "").lower()
        nomes = {raca.lower().replace(" ", "-"), EN.get(raca.lower(), raca).lower().split(" (")[0].replace(" ", "-")}
        return any(n and n in url for n in nomes)
    except Exception:  # noqa: BLE001
        return False


def raca_ok(cand: Path, stem: str, especie: str, raca: str) -> bool:
    if str(stem) in _VER:
        return _VER[str(stem)]
    from core.coerencia import verificar_imagens
    f = cand / f"{stem}.jpg"
    ok, motivo = verificar_imagens([f.read_bytes()], especie, raca, primeira_obrigatoria=True)
    if not ok and "[cf]" in motivo and motivo.startswith("raça errada") and _fonte_cita_raca(cand, str(stem), raca):
        ok, motivo = True, motivo + " | confirmada pelo título da foto na fonte"
    ok = ok and "não verificada" not in motivo
    print(f"[coerencia] capa {f.name}: {'ok' if ok else 'REPROVADA'} - {motivo}")
    _VER[str(stem)] = ok
    return ok


def plano_b_ia(cand: Path, slug: str, especie: str, raca: str) -> str | None:
    """Nenhuma foto do banco passou: gera a foto da raça por IA grátis (CF FLUX) e passa pelo MESMO portão."""
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from gerar_foto_ia import gerar
        manifesto = json.loads((cand / "candidatos.json").read_text(encoding="utf-8"))
        prox = max([int(c["indice"]) for c in manifesto] + [-1]) + 1
        for v in range(3):
            dest = cand / f"{prox}.jpg"
            ok, msg = gerar(raca, dest, v)
            print(f"[plano B IA] {raca} variacao {v}: {msg}")
            if not ok:
                dest.unlink(missing_ok=True)
                continue
            if raca_ok(cand, str(prox), especie, raca):
                manifesto.append({"fonte": "ia", "id": 0, "url_download": "", "url_pagina": "", "fotografo": "IA", "fotografo_url": "",
                                  "largura": 1024, "altura": 1024, "query": f"ia: {raca}", "indice": prox,
                                  "arquivo": str(dest.relative_to(ROOT))})
                (cand / "candidatos.json").write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"[plano B IA] foto gerada {prox}.jpg passou no portão de raça")
                return str(prox)
            _VER.pop(str(prox), None)
            dest.unlink(missing_ok=True)
    except Exception as exc:  # noqa: BLE001
        print("[plano B IA] falhou:", str(exc)[:120])
    return None


def preparar(slug: str, indice: str, media: Path | None) -> None:
    _VER.clear()   # o cache do portão de raça vale só para este artigo (índices 0,1,2 se repetem entre artigos)
    if not (ROOT / "data" / "content_writer" / "rascunhos" / f"{slug}.md").exists():
        raise SystemExit(f"rascunho não encontrado: {slug}")
    cand = ROOT / "data" / "visual" / "candidatos" / slug
    if media:
        origem = media / "pacotes" / slug / "imagens_candidatas"
        if origem.exists():
            shutil.copytree(origem, cand, dirs_exist_ok=True)
    if not (cand / "candidatos.json").exists():
        # 22/10 (Juiz): sem candidatas = buscar agora com consultas do tema (Pexels), nunca travar o artigo
        if os.environ.get("PEXELS_API_KEY"):
            run([sys.executable, "blog_imagens_nuvem.py", slug])
        if not (cand / "candidatos.json").exists():
            raise SystemExit(f"sem fotos candidatas para {slug}")
    # coerência de raça/espécie da capa (regra do Allan, 15/10/2026): dentro da produção do artigo
    especie = raca = ""
    try:
        from core.coerencia import detectar
        especie, raca = detectar(slug)
        if especie or raca:
            fotos = sorted(cand.glob("*.jpg"), key=lambda f: (f.stem != str(indice), f.stem))
            for f in fotos:
                if raca_ok(cand, f.stem, especie, raca):
                    if f.stem != str(indice):
                        print(f"[coerencia] trocando a capa {indice} pela {f.stem}")
                        indice = f.stem
                    break
            else:
                if raca:
                    ia = plano_b_ia(cand, slug, especie, raca)
                    if not ia:
                        raise SystemExit(f"coerência: nenhuma foto candidata mostra a raça '{raca}' ({slug}); não publica com raça errada")
                    indice = ia
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print("[coerencia] não verificada:", str(exc)[:100])
    # capa coerente com o tema, bonita, nao agressiva e nunca repetida (Allan, 22/10/2026)
    try:
        from core.capa import escolher
        idx, motivo = escolher(slug)
        if idx is None and "candidata" in motivo and os.environ.get("PEXELS_API_KEY"):
            print(f"[capa] {motivo}; buscando fotos novas com consultas do tema")
            shutil.rmtree(cand, ignore_errors=True)
            run([sys.executable, "blog_imagens_nuvem.py", slug])
            idx, motivo = escolher(slug)
        if idx is None:
            if motivo.startswith("visao indisponivel"):
                print("[capa] nao verificada:", motivo)
            else:
                with open(ROOT / "config" / "capas_pendentes.txt", "a", encoding="utf-8") as fh:
                    fh.write(f"{slug}\n")
                raise SystemExit(f"capa: {motivo}; nao publica com foto que nao mostra o tema")
        else:
            print(f"[capa] escolhida {idx}: {motivo}")
            indice = str(idx)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print("[capa] checagem nao feita:", str(exc)[:100])
    if raca:   # a escolha de capa por tema não pode passar por cima do portão de raça
        if not raca_ok(cand, str(indice), especie, raca):
            boas = [k for k, v in _VER.items() if v]
            if not boas:
                raise SystemExit(f"coerência: a capa escolhida não mostra a raça '{raca}' ({slug}); não publica com raça errada")
            print(f"[coerencia] capa {indice} reprovada no portão final; usando {boas[0]}")
            indice = boas[0]
    py = sys.executable
    run([py, "agents/04_quality_editor/agent.py", "--site", SITE, "--slug", slug])   # rc!=0 = reprovado: não publica
    run([py, "agents/05_seo_onpage/agent.py", "--site", SITE, "--slug", slug])
    run([py, "agents/15_visual/agent.py", "--site", SITE, "--selecionar", slug, str(indice)])
    try:  # ate 2 fotos no meio do artigo (Allan, 22/10/2026), das candidatas que tambem mostram o tema
        from core.capa import escolher as _esc
        extras = [i for i in getattr(_esc, "bons", []) if str(i) != str(indice) and (not raca or raca_ok(cand, str(i), especie, raca))][:2]
        if extras:
            run([py, "scripts/add_imagens_corpo.py", slug, ",".join(map(str, extras))])
    except Exception as exc:  # noqa: BLE001
        print("[corpo] sem fotos extras:", str(exc)[:100])


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
