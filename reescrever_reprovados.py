"""Reescreve sozinho os artigos reprovados pelo editor de qualidade (agente 04).

Criado em 22/10/2026 (padrão "fábrica que não para"): artigo reprovado não pode ficar parado
esperando alguém, nem ser reaprovado sem mudança. Fluxo por slug de config/blog_reprovados.txt
("<slug> <tentativas>"):
  1. lê os bloqueios do editor (legibilidade etc.);
  2. pede ao LLM só a reescrita do CORPO (fatos, títulos e assinatura preservados);
  3. roda o editor de novo; se aprovar, tira o slug de blog_reprovados.txt e, se o pacote de vídeo
     estiver aprovado na branch media, já grava "<slug> 0" em blog_aprovados.txt (o publicar_blog
     confere a coerência da foto e troca a capa se preciso);
  4. se reprovar, soma 1 tentativa; com 3 tentativas fica "pendência humana" (o saude.yml avisa).

Uso: python reescrever_reprovados.py [pasta_media] [--dry]
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core.llm import LLMError, gerar_texto  # noqa: E402
from core.markdown import read_markdown, write_markdown  # noqa: E402

SITE = "pets-tutores-iniciantes"
REPROV = ROOT / "config" / "blog_reprovados.txt"
APROV = ROOT / "config" / "blog_aprovados.txt"
RASC = ROOT / "data" / "content_writer" / "rascunhos"
REJ = ROOT / "data" / "quality_editor" / "reprovados"
MAX_TENTATIVAS = 3
MAX_POR_RODADA = 2   # economia de tempo/crédito: 2 artigos por rodada da fábrica

SISTEMA = (
    "Você é redator sênior do blog Tutorial Pet (pt-BR, tutores de cães e gatos). "
    "Reescreva SOMENTE o corpo do artigo em Markdown, tornando-o fácil de ler, sem inventar fatos, números, marcas ou fontes novas. "
    "Mantenha todos os títulos (##), a ordem das seções, os avisos de saúde existentes e os links existentes. "
    "Não use a palavra 'cão' (use 'cachorro' ou 'pet'). Sem alegação médica nem promessa de cura; em saúde, orientar procurar veterinário. "
    "Devolva apenas o Markdown do corpo, sem explicações e sem bloco de código."
)


def ler_lista() -> dict[str, int]:
    out: dict[str, int] = {}
    if REPROV.exists():
        for l in REPROV.read_text(encoding="utf-8").splitlines():
            t = l.split()
            if t and not t[0].startswith("#"):
                out[t[0]] = int(t[1]) if len(t) > 1 and t[1].isdigit() else 0
    return out


def gravar_lista(d: dict[str, int]) -> None:
    cab = [l for l in (REPROV.read_text(encoding="utf-8").splitlines() if REPROV.exists() else []) if l.startswith("#")]
    REPROV.write_text("\n".join(cab + [f"{s} {n}" for s, n in d.items()]) + "\n", encoding="utf-8")


def bloqueios(slug: str) -> str:
    """Texto com os bloqueios do editor (do arquivo de reprovados; se faltar, roda o editor)."""
    arq = REJ / f"{slug}.md"
    if not arq.exists():
        subprocess.run([sys.executable, "agents/04_quality_editor/agent.py", "--site", SITE, "--slug", slug],
                       cwd=ROOT, capture_output=True)
    if not arq.exists():
        return "legibilidade: frases acima de 35 palavras e parágrafos acima de 130 palavras."
    fm, _ = read_markdown(arq)
    linhas = []
    for c in fm.get("checagens_qualidade", []):
        if c.get("severidade") == "bloqueante":
            linhas.append(f"- [{c.get('checagem')}] {c.get('descricao')}")
            for t in (c.get("trechos") or [])[:5]:
                linhas.append(f"    trecho: {t}")
    return "\n".join(linhas) or "legibilidade."


def editor_aprova(slug: str) -> bool:
    r = subprocess.run([sys.executable, "agents/04_quality_editor/agent.py", "--site", SITE, "--slug", slug],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0


def pacote_aprovado(media: Path | None, slug: str) -> bool:
    if not media:
        return False
    m = media / "pacotes" / slug / "manifest.json"
    if not m.exists():
        return False
    try:
        return json.loads(m.read_text(encoding="utf-8")).get("status") == "aprovado" and \
            (media / "pacotes" / slug / "imagens_candidatas").exists()
    except Exception:  # noqa: BLE001
        return False


def reescrever(slug: str, tentativa: int) -> bool:
    arq = RASC / f"{slug}.md"
    if not arq.exists():
        print(f"[reescrita] sem rascunho: {slug}")
        return False
    fm, corpo = read_markdown(arq)
    pedido = (
        f"O editor de qualidade reprovou este artigo (tentativa {tentativa + 1} de {MAX_TENTATIVAS}). Bloqueios:\n"
        f"{bloqueios(slug)}\n\n"
        "Regras de reescrita: frases com no máximo 22 palavras; parágrafos com no máximo 80 palavras; "
        "transforme qualquer tabela com células longas em lista curta (uma ideia por item, até 20 palavras); "
        "divida listas aninhadas longas em itens curtos; preserve todos os fatos.\n\n"
        f"CORPO ATUAL:\n{corpo}"
    )
    try:
        novo = gerar_texto(pedido, sistema=SISTEMA, temperatura=0.4, max_tokens=7000).strip()
    except LLMError as exc:
        print(f"[reescrita] LLM indisponível ({slug}): {str(exc)[:120]}")
        return False
    novo = re.sub(r"^```(?:markdown|md)?\s*|\s*```$", "", novo).strip()
    if len(novo) < 0.6 * len(corpo.strip()) or novo.count("\n## ") + novo.startswith("## ") < max(2, corpo.count("\n## ") // 2):
        print(f"[reescrita] resultado suspeito (curto ou sem seções): {slug}; descartado")
        return False
    backup = arq.with_suffix(".md.bak")
    backup.write_text(arq.read_text(encoding="utf-8"), encoding="utf-8")
    fm = {**fm, "status": "rascunho_pendente_revisao", "reescrito_automatico": tentativa + 1}
    write_markdown(arq, fm, novo)
    if editor_aprova(slug):
        backup.unlink(missing_ok=True)
        return True
    arq.write_text(backup.read_text(encoding="utf-8"), encoding="utf-8")   # volta ao original se não melhorou
    backup.unlink(missing_ok=True)
    return False


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    media = Path(args[0]) if args else None
    dry = "--dry" in sys.argv
    lista = ler_lista()
    pend = [s for s, n in lista.items() if n < MAX_TENTATIVAS]
    humanos = [s for s, n in lista.items() if n >= MAX_TENTATIVAS]
    if humanos:
        print("PENDENCIA HUMANA (3 tentativas esgotadas):", humanos)
    print(f"reprovados na fila de reescrita: {pend}")
    if dry:
        for s in pend:
            print("---", s, "\n", bloqueios(s))
        return 0
    feitos = 0
    for slug in pend[:MAX_POR_RODADA]:
        ok = reescrever(slug, lista[slug])
        if ok:
            print(f"[reescrita] APROVADO pelo editor: {slug}")
            del lista[slug]
            if pacote_aprovado(media, slug):
                linhas = APROV.read_text(encoding="utf-8").splitlines() if APROV.exists() else []
                if not any(l.split() and l.split()[0] == slug for l in linhas):
                    APROV.write_text("\n".join(linhas + [f"{slug} 0"]) + "\n", encoding="utf-8")
                    print(f"[reescrita] {slug} 0 gravado em blog_aprovados.txt (publicar_blog dispara)")
            feitos += 1
        else:
            lista[slug] = lista[slug] + 1
    gravar_lista(lista)
    print(f"reescritos e aprovados nesta rodada: {feitos}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
