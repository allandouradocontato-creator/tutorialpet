"""Agente 04 — Quality Editor.

Recebe um rascunho do agente 03 e faz uma revisão de qualidade determinística antes de
liberar para SEO/publicação. Não reescreve o texto — sinaliza problemas para revisão
humana (ou reenvio ao agente 03). Ver prompt.md para o significado de cada checagem e
seus limites (isto é um filtro heurístico, não uma checagem factual real).

Uso isolado:
    python agents/04_quality_editor/agent.py --site pets-tutores-iniciantes \
        --slug como-cortar-unha-de-cachorro
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_env_file, load_site  # noqa: E402
from core.io import now_iso  # noqa: E402
from core.log import get_logger  # noqa: E402
from core.markdown import MarkdownError, read_markdown, write_markdown  # noqa: E402

AGENT_NAME = "04_quality_editor"
SCHEMA_VERSION = "1.0"
DRAFTS_DIR = ROOT / "data" / "content_writer" / "rascunhos"
APPROVED_DIR = ROOT / "data" / "quality_editor" / "aprovados"
REJECTED_DIR = ROOT / "data" / "quality_editor" / "reprovados"

SENTENCE_MAX_WORDS = 35
PARAGRAPH_MAX_WORDS = 130
LEGIBILIDADE_PROPORCAO_BLOQUEANTE = 0.25  # >25% das frases longas demais barra a aprovação

# --------------------------------------------------------------------------- listas heurísticas
# "Clichês de artigo gerado em massa": frases de recheio comuns em conteúdo raso/genérico.
CLICHE_PATTERNS = [
    r"em um mundo cada vez mais", r"e[ ]?importante ressaltar que", r"vale a pena ressaltar",
    r"sem sombra de duvida", r"nos dias de hoje", r"cada vez mais comum", r"de suma importancia",
    r"^em suma,", r"nao e novidade que", r"convem destacar", r"podemos concluir que",
    r"gostariamos de destacar", r"desvendar os segredos", r"neste artigo,? vamos explorar",
    r"ao longo deste artigo",
]

# Alegações que colocam em risco a segurança do pet ou contradizem o consenso veterinário básico —
# checagem de PLAUSIBILIDADE, não uma checagem factual real contra fontes específicas.
DANGEROUS_CLAIM_PATTERNS = [
    r"nao precisa d[eo] veterinari", r"dispensa (a )?consulta veterinaria", r"cura garantida",
    r"substitu[ai] a vacina", r"remedio caseiro cura", r"pode dar (qualquer )?remedio human",
    r"nao tem contraindicaca", r"sem risco nenhum", r"de acordo com estudos", r"pesquisas comprovam",
    r"cientificamente comprovado",
]

# Vocabulário técnico/formal que destoa da persona "caloroso, prático, não-técnico".
JARGON_PATTERNS = [
    r"\boutrossim\b", r"\bsupracitad[oa]\b", r"\bdestarte\b", r"\bdoravante\b", r"\bconcomitantemente\b",
    r"\betiologia\b", r"\bsintomatologia\b", r"\bposologia\b", r"\banamnese\b", r"\bin loco\b",
]

# Alegações de credencial profissional — proibidas pela persona editorial (regra do agente 03).
CREDENTIAL_CLAIM_PATTERNS = [
    r"sou veterinari[ao]", r"como veterinari[ao]", r"meu crmv", r"minha clinica veterinaria",
    r"atendo como veterinari[ao]", r"sou medic[ao] veterinari[ao]", r"formad[ao] em (medicina )?veterinaria",
    r"\bprescrevo\b", r"\breceito\b",
]

# Palavras que, aparecendo pouco antes de uma alegação de credencial, indicam que a frase é uma
# NEGAÇÃO da credencial (disclaimer de segurança — o projeto exige isso, ex.: "não sou
# veterinário de verdade"), não uma alegação real. Ex.: "sou veterinari[ao]" por si só bate como
# substring dentro de "não sou veterinário", então o match cru precisa ser filtrado por contexto.
NEGATION_WORDS = {"nao", "nunca", "jamais"}
NEGATION_WINDOW = 5  # nº de palavras antes do match onde a negação ainda "conta"


def _norm(text: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", text.lower()) if not unicodedata.combining(c))


def _find_matches(patterns: list[str], text_norm: str) -> list[str]:
    found = []
    for pat in patterns:
        m = re.search(pat, text_norm, flags=re.MULTILINE)
        if m:
            found.append(m.group(0))
    return found


def _has_negation_before(text_norm: str, match_start: int, window: int = NEGATION_WINDOW) -> bool:
    """True se alguma das últimas `window` palavras antes de match_start for uma negação
    ("não", "nunca", "jamais") — usado só para alegação de credencial, onde negar a frase
    inverte completamente o sentido (disclaimer vs. alegação real)."""
    palavras_antes = re.findall(r"[a-z0-9]+", text_norm[:match_start])
    return any(p in NEGATION_WORDS for p in palavras_antes[-window:])


def _find_unnegated_matches(patterns: list[str], text_norm: str) -> list[str]:
    """Como _find_matches, mas ignora ocorrências claramente negadas pouco antes (ver
    _has_negation_before) — evita marcar um disclaimer de segurança como se fosse a alegação
    que ele nega."""
    found = []
    for pat in patterns:
        for m in re.finditer(pat, text_norm, flags=re.MULTILINE):
            if not _has_negation_before(text_norm, m.start()):
                found.append(m.group(0))
                break  # uma ocorrência não-negada já basta pra sinalizar o padrão
    return found


def _strip_markdown(body: str) -> str:
    """Remove marcações estruturais (headers, blockquote, ênfase) para deixar só a prosa."""
    text = re.sub(r"^#{1,6}\s*", "", body, flags=re.MULTILINE)
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"^-\s+", "", text, flags=re.MULTILINE)
    return text


def _paragraphs(body_plain: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", body_plain) if p.strip()]


def _sentences(paragraph: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", paragraph) if s.strip()]


def add_problem(problemas: list[dict], checagem: str, severidade: str, descricao: str, trechos: list[str] | None = None) -> None:
    problemas.append({"checagem": checagem, "severidade": severidade, "descricao": descricao, "trechos": trechos or []})


# --------------------------------------------------------------------------- checagens
def check_originalidade(body_norm: str, problemas: list[dict]) -> None:
    hits = _find_matches(CLICHE_PATTERNS, body_norm)
    if not hits:
        return
    severidade = "bloqueante" if len(hits) >= 3 else "aviso"
    add_problem(problemas, "originalidade", severidade,
                f"{len(hits)} trecho(s) com clichê típico de conteúdo genérico/gerado em massa.", hits)


def check_precisao_sensivel(body_norm: str, sensivel: bool, aviso_saude_esperado: str, problemas: list[dict]) -> None:
    if not sensivel:
        return
    hits = _find_matches(DANGEROUS_CLAIM_PATTERNS, body_norm)
    if hits:
        add_problem(problemas, "precisao_factual", "bloqueante",
                    "Tópico sensível (YMYL) contém afirmação implausível/arriscada — reescrever e reforçar "
                    "orientação para consulta veterinária.", hits)
    if aviso_saude_esperado and _norm(aviso_saude_esperado) not in body_norm:
        add_problem(problemas, "aviso_saude_ausente", "bloqueante",
                    "Artigo é YMYL (aviso_saude_aplicavel: true) mas o texto do aviso de saúde do site não "
                    "foi encontrado no corpo do artigo.")


def check_tom(body_norm: str, problemas: list[dict]) -> None:
    hits = _find_matches(JARGON_PATTERNS, body_norm)
    if not hits:
        return
    severidade = "bloqueante" if len(hits) >= 2 else "aviso"
    add_problem(problemas, "tom_persona", severidade,
                f"{len(hits)} termo(s) técnico(s)/formal(is) destoando da persona caloroso/não-técnico.", hits)


def check_legibilidade(body_plain: str, problemas: list[dict]) -> None:
    long_sentences, long_paragraphs, total_sentences = [], [], 0
    for paragraph in _paragraphs(body_plain):
        p_words = len(paragraph.split())
        if p_words > PARAGRAPH_MAX_WORDS:
            long_paragraphs.append(f"{p_words} palavras: \"{paragraph[:80]}...\"")
        for sentence in _sentences(paragraph):
            total_sentences += 1
            n = len(sentence.split())
            if n > SENTENCE_MAX_WORDS:
                long_sentences.append(f"{n} palavras: \"{sentence[:80]}...\"")
    if not long_sentences and not long_paragraphs:
        return
    proporcao = len(long_sentences) / total_sentences if total_sentences else 0
    severidade = "bloqueante" if proporcao > LEGIBILIDADE_PROPORCAO_BLOQUEANTE or len(long_paragraphs) >= 2 else "aviso"
    add_problem(problemas, "legibilidade", severidade,
                f"{len(long_sentences)}/{total_sentences} frases acima de {SENTENCE_MAX_WORDS} palavras e "
                f"{len(long_paragraphs)} parágrafo(s) acima de {PARAGRAPH_MAX_WORDS} palavras — simplificar.",
                long_sentences[:5] + long_paragraphs[:2])


def check_autoria_e_credencial(front_matter: dict, body_norm: str, problemas: list[dict]) -> None:
    autor = (front_matter.get("autor") or "").strip()
    if autor:
        add_problem(problemas, "autor_preenchido", "bloqueante",
                    f"Campo 'autor' não está em branco ('{autor}') — só um humano pode preenchê-lo, com uma "
                    "pessoa real cadastrada em /sobre.")
    hits = _find_unnegated_matches(CREDENTIAL_CLAIM_PATTERNS, body_norm)
    if hits:
        add_problem(problemas, "alegacao_credencial", "bloqueante",
                    "Texto alega credencial veterinária real, o que é proibido pela persona editorial.", hits)


# --------------------------------------------------------------------------- entrypoint
def resolve_draft_path(context: dict) -> Path | None:
    prev = context.get("input")
    if isinstance(prev, dict) and prev.get("arquivo"):
        return ROOT / prev["arquivo"]
    if context.get("arquivo"):
        return ROOT / context["arquivo"]
    if context.get("slug"):
        return DRAFTS_DIR / f"{context['slug']}.md"
    return None


def run(context: dict) -> dict:
    log = context["logger"]
    site_id = context["site_id"]
    site = context.get("site") or load_site(site_id)

    draft_path = resolve_draft_path(context)
    if not draft_path or not draft_path.exists():
        log.warning(f"[{AGENT_NAME}] nenhum rascunho encontrado ({draft_path})")
        return {
            "agent": AGENT_NAME, "status": "sem_rascunho",
            "mensagem": f"Rascunho não encontrado: {draft_path}. Rode o agente 03 antes deste.",
        }

    try:
        front_matter, body = read_markdown(draft_path)
    except MarkdownError as ex:
        log.error(f"[{AGENT_NAME}] {draft_path}: {ex}")
        return {"agent": AGENT_NAME, "status": "erro_formato", "mensagem": str(ex)}

    sensivel = bool(front_matter.get("aviso_saude_aplicavel"))
    body_plain = _strip_markdown(body)
    body_norm = _norm(body_plain)
    aviso_saude = site.get("compliance", {}).get("aviso_saude", "")

    problemas: list[dict] = []
    check_originalidade(body_norm, problemas)
    check_precisao_sensivel(body_norm, sensivel, aviso_saude, problemas)
    check_tom(body_norm, problemas)
    check_legibilidade(body_plain, problemas)
    check_autoria_e_credencial(front_matter, body_norm, problemas)

    aprovado = not any(p["severidade"] == "bloqueante" for p in problemas)
    slug = front_matter.get("slug") or draft_path.stem

    novo_front_matter = {
        **front_matter,
        "status": "aprovado_qualidade" if aprovado else "reprovado_qualidade",
        "revisado_por_agente_04": True,
        "revisado_em": now_iso(),
        "checagens_qualidade": problemas,
    }
    out_dir = APPROVED_DIR if aprovado else REJECTED_DIR
    out_path = write_markdown(out_dir / f"{slug}.md", novo_front_matter, body)

    bloqueantes = [p for p in problemas if p["severidade"] == "bloqueante"]
    avisos = [p for p in problemas if p["severidade"] == "aviso"]
    pendencias = []
    if not aprovado:
        pendencias.append(f"Revisar {len(bloqueantes)} problema(s) bloqueante(s) e reenviar (ajustar manualmente "
                           "ou regerar com o agente 03), depois rodar o agente 04 de novo.")
        pendencias += [f"[{p['checagem']}] {p['descricao']}" for p in bloqueantes]
    else:
        pendencias.append("Aprovado na revisão de qualidade — seguir para o agente 05 (SEO on-page).")
    if avisos:
        pendencias += [f"[aviso/{p['checagem']}] {p['descricao']}" for p in avisos]

    output = {
        "agent": AGENT_NAME,
        "schema_version": SCHEMA_VERSION,
        "site_id": site_id,
        "gerado_em": now_iso(),
        "status": "ok" if aprovado else "reprovado_qualidade",
        "aprovado": aprovado,
        "arquivo": str(out_path.relative_to(ROOT)),
        "slug": slug,
        "titulo": front_matter.get("titulo"),
        "termo_origem": front_matter.get("termo_origem"),
        "pilar": front_matter.get("pilar"),
        "sensivel_ymyl": sensivel,
        "checagens": problemas,
        "pendencias_humanas": pendencias,
    }
    log.info(f"[{AGENT_NAME}] {slug}: {'aprovado' if aprovado else 'reprovado'} "
             f"({len(bloqueantes)} bloqueante(s), {len(avisos)} aviso(s)) → {out_path.relative_to(ROOT)}")
    return output


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 04 — revisão de qualidade (uso isolado)")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--slug", help="slug do rascunho em data/content_writer/rascunhos/")
    group.add_argument("--arquivo", help="caminho do .md a revisar, relativo à raiz do projeto")
    args = parser.parse_args()

    load_env_file()
    run_id = f"{now_iso().replace(':', '').replace('+0000', 'Z')}-{AGENT_NAME}"
    output = run({"site_id": args.site, "slug": args.slug, "arquivo": args.arquivo, "logger": get_logger(run_id)})
    return 0 if output["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
