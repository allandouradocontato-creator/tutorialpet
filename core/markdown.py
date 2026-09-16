"""Leitura/escrita de artigos em Markdown com front-matter YAML.

Usado pelos agentes 04 e 05 em diante — o agente 03 mantém sua própria função local de
escrita (não foi tocado nesta fase).
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

FRONT_MATTER_RE = re.compile(r"\A---\r?\n(.*?\r?\n)---\r?\n?(.*)\Z", re.DOTALL)


class MarkdownError(RuntimeError):
    pass


def parse_front_matter(text: str) -> tuple[dict, str]:
    """Retorna (front_matter, corpo). Levanta MarkdownError se não houver front-matter válido."""
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise MarkdownError("arquivo sem front-matter YAML válido (esperado '---' no início e no fim do bloco)")
    front_matter = yaml.safe_load(match.group(1)) or {}
    if not isinstance(front_matter, dict):
        raise MarkdownError("front-matter não é um mapeamento YAML válido")
    return front_matter, match.group(2)


def read_markdown(path: Path) -> tuple[dict, str]:
    return parse_front_matter(Path(path).read_text(encoding="utf-8"))


def render_markdown(front_matter: dict, body: str) -> str:
    header = yaml.safe_dump(front_matter, allow_unicode=True, sort_keys=False)
    return f"---\n{header}---\n\n{body.lstrip(chr(10))}"


def write_markdown(path: Path, front_matter: dict, body: str) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(front_matter, body), encoding="utf-8")
    return path


def strip_markdown_plain(body: str) -> str:
    """Remove marcação estrutural (headers, blockquote, ênfase, listas) para comparação de
    texto puro — usado por checagens de legibilidade/duplicidade em agentes downstream."""
    text = re.sub(r"^#{1,6}\s*", "", body, flags=re.MULTILINE)
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"^-\s+", "", text, flags=re.MULTILINE)
    return text
