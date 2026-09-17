"""Checagens de texto compartilhadas entre agentes de revisão (04_quality_editor,
10_policy_guardian, ...) — extraída depois de um mesmo bug (falso positivo de "alegação de
credencial" por não reconhecer negação) aparecer duplicado em dois agentes que tinham cada
um sua própria cópia da lógica. Manter isso num só lugar evita o bug se repetir num terceiro.
"""
from __future__ import annotations

import re

# Palavras que, aparecendo pouco antes de um padrão como "sou veterinário", indicam que a
# frase é uma NEGAÇÃO da alegação (disclaimer de segurança — ex.: "não sou veterinário de
# verdade"), não a alegação em si. Sem isso, a busca por substring bate igual nos dois casos.
NEGATION_WORDS = {"nao", "nunca", "jamais"}
NEGATION_WINDOW = 5  # nº de palavras antes do match onde a negação ainda "conta"


def has_negation_before(text_norm: str, match_start: int, window: int = NEGATION_WINDOW) -> bool:
    """True se alguma das últimas `window` palavras antes de `match_start` for uma negação.
    `text_norm` já deve estar normalizado (minúsculo, sem acento) pelo chamador."""
    palavras_antes = re.findall(r"[a-z0-9]+", text_norm[:match_start])
    return any(p in NEGATION_WORDS for p in palavras_antes[-window:])


def find_unnegated_matches(patterns: list[str], text_norm: str) -> list[str]:
    """Busca cada regex de `patterns` em `text_norm` e ignora ocorrências claramente negadas
    pouco antes (ver has_negation_before) — evita marcar um disclaimer de segurança como se
    fosse a alegação que ele nega. Retorna um match por padrão que bateu sem negação."""
    found = []
    for pat in patterns:
        for m in re.finditer(pat, text_norm, flags=re.MULTILINE):
            if not has_negation_before(text_norm, m.start()):
                found.append(m.group(0))
                break  # uma ocorrência não-negada já basta pra sinalizar o padrão
    return found
