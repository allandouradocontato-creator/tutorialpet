"""Escritor com LLM + rodízio de vozes (Agente 03, modo WRITER_MODE=llm)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.llm import gerar_texto  # noqa: E402

VOZES_PATH = ROOT / "config" / "vozes_cronistas.yaml"
ESTADO_PATH = ROOT / "data" / "content_writer" / "estado_rotacao.json"

SISTEMA = """Você escreve artigos de blog em português do Brasil para a marca Tutorial Pet (todos os tutores de cães e gatos: de quem está chegando com o primeiro pet a quem já tem vários; filhote, adulto e idoso).
LINHA EDITORIAL (07/10/2026): não escreva só para iniciantes. Escolha o leitor pelo tema (iniciante, experiente, família com crianças, tutor de idoso, multi-pet) e não use "tutor de primeira viagem" no título nem repita isso no texto, salvo quando o tema for mesmo de chegada do pet.
REGRAS INEGOCIÁVEIS:
- Texto 100% original. Nunca copie nem parafraseie de perto nenhuma fonte.
- Nunca diga que é veterinário nem alegue credencial. Fale como tutor experiente aconselhando um amigo.
- Nunca invente estudo, estatística, pesquisa, depoimento ou nome de pessoa/autor.
- Em qualquer tema de saúde ou segurança, oriente a procurar um médico-veterinário.
- Não imite nem cite pessoas reais. Use apenas o estilo descrito.
- Sem venda direta, sem urgência artificial.
Formato: Markdown. Comece com "# Título". Depois introdução curta, seções "## ..." com subtítulos "### ..." quando fizer sentido,
um "Exemplo prático:" concreto por seção principal, seção "## Perguntas frequentes" com 3 a 5 perguntas (pergunta em negrito e resposta curta),
e "## Para fechar" com conclusão e convite suave para continuar lendo o blog. Entre 900 e 1200 palavras (não passe de 1300).
- Números práticos (horas, idades, quantidades) devem vir com "em média" ou "costuma" e a lembrança de confirmar com o médico-veterinário do pet.
PRIMEIRA LINHA da resposta, obrigatória: META: <descrição única do artigo para o Google, 120 a 150 caracteres, sem aspas>. Depois uma linha em branco e o artigo.
Se o tema for sensível, escreva exatamente a linha [[AVISO_SAUDE]] logo após a introdução."""


def carregar_vozes() -> dict:
    return yaml.safe_load(VOZES_PATH.read_text(encoding="utf-8"))


def escolher_voz(vozes: dict) -> dict:
    lista = vozes["vozes"]
    ultimo = -1
    if ESTADO_PATH.exists():
        try:
            ultimo = json.loads(ESTADO_PATH.read_text(encoding="utf-8")).get("ultimo_indice", -1)
        except json.JSONDecodeError:
            ultimo = -1
    idx = (ultimo + 1) % len(lista)
    ESTADO_PATH.parent.mkdir(parents=True, exist_ok=True)
    ESTADO_PATH.write_text(json.dumps({"ultimo_indice": idx, "ultima_voz": lista[idx]["id"]}), encoding="utf-8")
    return lista[idx]


def _bloco_links_internos() -> str:
    """Lista dos artigos JÁ NO AR para o texto linkar (SEO interno + leitor navega para outro comportamento/tema)."""
    import re
    build = ROOT / "site" / "build"
    itens = []
    for md in sorted((ROOT / "data" / "content_writer" / "rascunhos").glob("*.md")):
        if (build / f"{md.stem}.html").exists():
            m = re.search(r"^titulo:\s*['\"]?(.+?)['\"]?\s*$", md.read_text(encoding="utf-8"), re.M)
            itens.append(f"- /{md.stem} — {m.group(1) if m else md.stem}")
    if not itens:
        return ""
    return ("\n\nLINKS INTERNOS (obrigatório): inclua de 3 a 4 links em Markdown no formato [texto âncora natural](/slug) para os artigos abaixo "
            "mais ligados ao assunto, no meio do texto. Use SOMENTE slugs desta lista, sem inventar:\n" + "\n".join(itens) + "\n")


def escrever_corpo(pauta: dict, site: dict, sensivel: bool) -> tuple[str, dict]:
    vozes = carregar_vozes()
    voz = escolher_voz(vozes)
    aviso = (site.get("compliance", {}).get("aviso_saude") or "").strip()
    prompt = (
        f"Escreva o artigo.\nTítulo: {pauta['titulo']}\nTermo de busca: {pauta['termo_origem']}\n"
        f"Gancho/ângulo: {pauta.get('angulo_gancho', '')}\nPilar: {pauta.get('pilar', '')}\n"
        f"Tema sensível (saúde/segurança): {'sim' if sensivel else 'não'}\n\n"
        f"VOZ DESTE ARTIGO — coluna \"{voz['coluna']}\": {voz['estilo']}\n"
        "Mantenha essa voz do começo ao fim, sem citar o nome da coluna no texto."
    )
    prompt += _bloco_links_internos()
    corpo = gerar_texto(prompt, sistema=SISTEMA, temperatura=0.9)
    voz = dict(voz)
    if corpo.lstrip().upper().startswith("META:"):
        primeira, _, resto = corpo.lstrip().partition("\n")
        meta = primeira.split(":", 1)[1].strip().strip('"')
        if 60 <= len(meta) <= 160:
            voz["meta"] = meta
        corpo = resto.lstrip("\n")
    if "[[AVISO_SAUDE]]" in corpo:
        corpo = corpo.replace("[[AVISO_SAUDE]]", f"> {aviso}" if aviso else "")
    elif sensivel and aviso:
        partes = corpo.split("\n\n", 2)
        corpo = "\n\n".join(partes[:2] + [f"> {aviso}"] + partes[2:])
    return corpo.strip() + "\n", voz
