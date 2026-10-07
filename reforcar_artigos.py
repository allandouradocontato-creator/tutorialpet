"""Reescreve os artigos antigos do blog com profundidade, rigor técnico, links internos e assinatura da equipe.

Uso:
    python reforcar_artigos.py --lote 4            # reescreve até 4 artigos ainda sem 'revisao_profunda'
    python reforcar_artigos.py --slug <slug>       # reescreve um específico
    python reforcar_artigos.py --dry               # só lista quem entraria
Cada artigo só é gravado se passar no Curador do Blog (agente 24); se não passar após 2 tentativas, o antigo fica como está.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "agents" / "03_content_writer"))
RASC = ROOT / "data" / "content_writer" / "rascunhos"

spec = importlib.util.spec_from_file_location("curador", ROOT / "agents" / "24_curador_blog" / "agent.py")
curador = importlib.util.module_from_spec(spec)
spec.loader.exec_module(curador)

EXTRA = """
REFORÇO DE QUALIDADE (este artigo precisa passar na revisão do Google AdSense):
- Assinatura da equipe: nenhuma voz de personagem, nenhum nome de pessoa, nenhuma "coluna". Tom: claro, acolhedor e direto, de equipe que pesquisa e explica.
- Profundidade e rigor técnico: explique o PORQUÊ (comportamento ou fisiologia do animal) antes de cada recomendação, dê passos numerados, erros comuns, sinais de alerta e quando procurar o médico-veterinário. Sem inventar estudo, número exato ou estatística.
- Facilidade de leitura: parágrafos de até 4 linhas, listas, negrito nas ideias-chave, frases curtas.
- Entre 1000 e 1300 palavras. Seções obrigatórias: introdução, pelo menos 4 seções "##", "## Perguntas frequentes" (3 a 5, pergunta inteira em negrito terminando em "?"), "## Para fechar".
- LINKS INTERNOS: inclua de 3 a 4 links em Markdown no formato [texto âncora natural](/slug) para artigos da lista abaixo, escolhendo os mais ligados ao assunto, no meio do texto (não só no fim). Use SOMENTE slugs da lista, sem inventar.
- O título "# ..." deve ser o termo de busca de forma natural, até 70 caracteres, sem nome de personagem.
"""


def titulo_limpo(fm: dict) -> str:
    return re.sub(r"\s*[:\-–]\s*(a|o)\s+[A-ZÀ-Ú].*$", "", str(fm.get("titulo") or "")).strip() or str(fm.get("termo_origem"))


def precisa(fm: dict) -> bool:
    return not fm.get("revisao_profunda")


def reescrever(path: Path, slugs_info: list[tuple[str, str]], site: dict) -> bool:
    from core.llm import gerar_texto
    from escritor_llm import SISTEMA
    fm, _ = curador.ler(path)
    slug = path.stem
    sensivel = bool(fm.get("aviso_saude_aplicavel")) or bool(curador.SAUDE.search(str(fm.get("termo_origem"))))
    aviso = (site.get("compliance", {}).get("aviso_saude") or "").strip()
    lista = "\n".join(f"- /{s} — {t}" for s, t in slugs_info if s != slug)
    base = (f"Escreva o artigo.\nTermo de busca: {fm.get('termo_origem')}\nTítulo de referência (limpe nomes de personagem): {titulo_limpo(fm)}\n"
            f"Pilar: {fm.get('pilar', '')}\nTema sensível (saúde/segurança): {'sim' if sensivel else 'não'}\n\n"
            f"ARTIGOS DO SITE PARA LINKAR:\n{lista}\n")
    erros = ""
    for tentativa in (1, 2):
        corpo = gerar_texto(base + erros, sistema=SISTEMA + EXTRA, temperatura=0.6, max_tokens=8000)
        meta = ""
        if corpo.lstrip().upper().startswith("META:"):
            primeira, _, resto = corpo.lstrip().partition("\n")
            meta = primeira.split(":", 1)[1].strip().strip('"')
            corpo = resto.lstrip("\n")
        if "[[AVISO_SAUDE]]" in corpo:
            corpo = corpo.replace("[[AVISO_SAUDE]]", f"> {aviso}" if aviso else "")
        elif sensivel and aviso and aviso not in corpo:
            partes = corpo.split("\n\n", 2)
            corpo = "\n\n".join(partes[:2] + [f"> {aviso}"] + partes[2:])
        corpo = corpo.strip() + "\n"
        h1 = re.match(r"#\s+(.+)", corpo)
        novo = {k: fm[k] for k in ("data", "status", "slug", "termo_origem", "pilar", "intencao_busca", "site_id", "gerado_em", "aviso_saude_aplicavel") if k in fm}
        novo.update({"titulo": h1.group(1).strip() if h1 else titulo_limpo(fm),
                     "meta_description": meta if 60 <= len(meta) <= 160 else fm.get("meta_description", ""),
                     "autor": "", "atualizado_em": f"{datetime.now():%Y-%m-%d}", "revisao_profunda": True})
        probs = curador.auditar(slug, novo, corpo, curador.todos_slugs())
        bloq = [m for n, m in probs if n == "bloqueante"]
        if not bloq:
            texto = "---\n" + yaml.safe_dump(novo, allow_unicode=True, sort_keys=False, width=1000) + "---\n\n" + corpo
            path.write_text(texto, encoding="utf-8")
            print(f"OK   {slug} ({len(corpo.split())} palavras)", flush=True)
            return True
        erros = "\nA versão anterior foi REPROVADA por: " + "; ".join(bloq) + ". Corrija tudo isso na nova versão."
        print(f"RETRY {slug}: {bloq}", flush=True)
    print(f"FALHOU {slug}: mantido o texto antigo", flush=True)
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lote", type=int, default=4)
    ap.add_argument("--slug")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    arquivos = sorted(RASC.glob("*.md"), key=lambda p: len(p.read_text(encoding="utf-8")))
    infos = []
    for p in arquivos:
        fm, _ = curador.ler(p)
        infos.append((p.stem, titulo_limpo(fm)))
    alvos = [RASC / f"{a.slug}.md"] if a.slug else [p for p in arquivos if precisa(curador.ler(p)[0])][: a.lote]
    print("alvos:", [p.stem for p in alvos], flush=True)
    if a.dry:
        return 0
    from core.config import load_env_file
    load_env_file()
    site = yaml.safe_load((ROOT / "config" / "sites" / "pets-tutores-iniciantes.yaml").read_text(encoding="utf-8")) or {}
    feitos = sum(reescrever(p, infos, site) for p in alvos)
    print(f"reescritos: {feitos}/{len(alvos)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
