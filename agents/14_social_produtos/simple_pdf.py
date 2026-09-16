"""Gerador mínimo de PDF, sem dependências externas — no espírito do conversor Markdown→HTML
do agente 07 (agents/07_publisher/agent.py): cobre só o necessário para montar um e-book
simples (texto corrido, títulos, quebra de página automática), não é uma biblioteca de PDF
completa.

Usa fonte padrão Helvetica (Base-14, sempre disponível em leitores de PDF) e codificação
WinAnsi (cp1252), que cobre os acentos do português.
"""
from __future__ import annotations

from pathlib import Path

PAGE_WIDTH, PAGE_HEIGHT = 595, 842  # A4 em pontos
MARGIN = 56
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN

FONT_SIZES = {"titulo_capa": 26, "h1": 18, "h2": 14, "corpo": 11, "citacao": 10}
LEADING_FACTOR = 1.4  # espaçamento entre linhas, proporcional ao tamanho da fonte


def _escape(text: str) -> str:
    return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def _wrap(text: str, size: int, max_width: float = CONTENT_WIDTH) -> list[str]:
    """Quebra de linha aproximada: Helvetica tem largura média ~0.5*size por caractere —
    suficiente pra não estourar a margem, sem precisar das métricas exatas da fonte."""
    max_chars = max(10, int(max_width / (size * 0.5)))
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            if len(current) + 1 + len(word) <= max_chars:
                current += " " + word
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


class SimplePDF:
    """Documento PDF de fluxo simples: adiciona blocos de texto que quebram de página
    automaticamente quando não cabem mais na página atual."""

    def __init__(self):
        self.pages: list[list[tuple[str, int, bool]]] = [[]]  # cada página: [(linha, size, bold), ...]
        self._y = PAGE_HEIGHT - MARGIN

    def _ensure_space(self, needed: float) -> None:
        if self._y - needed < MARGIN:
            self.pages.append([])
            self._y = PAGE_HEIGHT - MARGIN

    def _add_line(self, text: str, size: int, bold: bool) -> None:
        leading = size * LEADING_FACTOR
        self._ensure_space(leading)
        self.pages[-1].append((text, size, bold))
        self._y -= leading

    def add_paragraph(self, text: str, style: str = "corpo") -> None:
        size = FONT_SIZES[style]
        for line in _wrap(text, size):
            self._add_line(line, size, bold=False)
        self._ensure_space(size * LEADING_FACTOR * 0.5)  # respiro entre parágrafos
        self._y -= size * LEADING_FACTOR * 0.5

    def add_heading(self, text: str, style: str = "h1") -> None:
        self._ensure_space(FONT_SIZES[style] * LEADING_FACTOR * 1.5)
        size = FONT_SIZES[style]
        for line in _wrap(text, size):
            self._add_line(line, size, bold=True)

    def new_page(self) -> None:
        self.pages.append([])
        self._y = PAGE_HEIGHT - MARGIN

    def add_cover(self, titulo: str, subtitulo: str = "") -> None:
        if self.pages[-1]:
            self.new_page()
        self._y = PAGE_HEIGHT / 2 + 60
        for line in _wrap(titulo, FONT_SIZES["titulo_capa"]):
            self._add_line(line, FONT_SIZES["titulo_capa"], bold=True)
        if subtitulo:
            self._y -= 20
            for line in _wrap(subtitulo, FONT_SIZES["h2"]):
                self._add_line(line, FONT_SIZES["h2"], bold=False)
        self.new_page()

    def save(self, path: Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        objects: list[bytes] = []

        def add_object(body: bytes) -> int:
            objects.append(body)
            return len(objects)  # objetos PDF são 1-indexados

        font_regular_id = add_object(
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
        )
        font_bold_id = add_object(
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
        )

        pages_kids_ids: list[int] = []
        page_content_pairs: list[tuple[int, int]] = []

        # Gera páginas e conteúdos primeiro; o objeto /Pages entra por último, quando os ids das
        # páginas já são conhecidos (evita ter que pré-calcular numeração de objetos).
        for page_blocks in self.pages:
            content_lines = ["BT", f"/F1 {FONT_SIZES['corpo']} Tf"]
            y = PAGE_HEIGHT - MARGIN
            last_font_key = None
            for text, size, bold in page_blocks:
                font_key = ("F2" if bold else "F1", size)
                if font_key != last_font_key:
                    content_lines.append(f"/{font_key[0]} {font_key[1]} Tf")
                    last_font_key = font_key
                content_lines.append(f"1 0 0 1 {MARGIN} {y:.2f} Tm ({_escape(text)}) Tj")
                y -= size * LEADING_FACTOR
            content_lines.append("ET")
            stream = "\n".join(content_lines).encode("cp1252", errors="replace")
            content_id = add_object(
                b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream"
            )
            page_id_placeholder = add_object(b"")  # preenchido no próximo passo
            page_content_pairs.append((page_id_placeholder, content_id))
            pages_kids_ids.append(page_id_placeholder)

        pages_id = add_object(b"")  # preenchido abaixo

        for page_id, content_id in page_content_pairs:
            objects[page_id - 1] = (
                f"<< /Type /Page /Parent {pages_id} 0 R /Resources << /Font << /F1 {font_regular_id} 0 R "
                f"/F2 {font_bold_id} 0 R >> >> /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
                f"/Contents {content_id} 0 R >>"
            ).encode()

        kids_refs = " ".join(f"{pid} 0 R" for pid in pages_kids_ids)
        objects[pages_id - 1] = (
            f"<< /Type /Pages /Kids [{kids_refs}] /Count {len(pages_kids_ids)} >>".encode()
        )

        catalog_id = add_object(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode())

        out = bytearray(b"%PDF-1.4\n")
        offsets = [0]
        for i, obj in enumerate(objects, 1):
            offsets.append(len(out))
            out += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
        xref_offset = len(out)
        out += f"xref\n0 {len(objects) + 1}\n".encode()
        out += b"0000000000 65535 f \n"
        for off in offsets[1:]:
            out += f"{off:010d} 00000 n \n".encode()
        out += (
            f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF"
        ).encode()

        path.write_bytes(bytes(out))
        return path
