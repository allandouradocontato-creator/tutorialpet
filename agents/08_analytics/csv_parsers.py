"""Parsers tolerantes para exports reais de CSV do Google Search Console e do Google
Analytics 4 (GA4). Os dois exports variam de formato conforme o relatório exportado e a
localidade da conta, então em vez de exigir um cabeçalho exato, procuramos a linha que
mais parece um cabeçalho de dados (por sinônimos de coluna) e ignoramos linhas de
metadados que o GA4 costuma incluir no topo do arquivo.

Isto cobre os formatos mais comuns encontrados na prática — não é garantido cobrir toda
variação de exportação do Google (que muda com frequência).
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

import sys
AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT,):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
from core.io import normalize_term  # noqa: E402

# --------------------------------------------------------------------------- sinônimos de coluna
GSC_SYNONYMS = {
    "pagina": ["top pages", "top queries", "page", "query", "pages", "queries"],
    "cliques": ["clicks"],
    "impressoes": ["impressions"],
    "ctr": ["ctr"],
    "posicao_media": ["position", "average position", "posicao media"],
}
GA_SYNONYMS = {
    "pagina": ["page path and screen class", "page path", "landing page", "page", "pagina"],
    "visualizacoes": ["views", "pageviews", "screen page views"],
    "usuarios": ["users", "active users", "total users"],
    "engajamento_medio_seg": ["average engagement time per active user", "avg. engagement time per user",
                              "user engagement duration per active user"],
}


def _to_float(raw: str) -> float:
    text = raw.strip().replace("%", "").replace(" ", "")
    if not text:
        return 0.0
    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return 0.0


def _find_header(rows: list[list[str]], synonyms: dict[str, list[str]]) -> tuple[int, dict[str, int]] | None:
    synonyms_norm = {campo: {normalize_term(s) for s in lista} for campo, lista in synonyms.items()}
    for idx, row in enumerate(rows):
        cells_norm = [normalize_term(c) for c in row]
        mapping = {}
        for campo, opcoes in synonyms_norm.items():
            for col_idx, cell in enumerate(cells_norm):
                if cell in opcoes:
                    mapping[campo] = col_idx
                    break
        if "pagina" in mapping and len(mapping) >= 2:
            return idx, mapping
    return None


def _read_rows(path: Path) -> list[list[str]]:
    with Path(path).open(encoding="utf-8-sig", newline="") as fh:
        sample = fh.read(4096)
        fh.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        return list(csv.reader(fh, dialect=dialect))


class CsvFormatError(RuntimeError):
    pass


def parse_gsc_csv(path: Path) -> list[dict]:
    """Espera um export do Search Console (aba 'Páginas' ou 'Consultas' do relatório de
    Desempenho, exportado como CSV): colunas como 'Top pages'/'Top queries', 'Clicks',
    'Impressions', 'CTR', 'Position'."""
    rows = _read_rows(path)
    found = _find_header(rows, GSC_SYNONYMS)
    if not found:
        raise CsvFormatError(f"não foi possível identificar as colunas esperadas do Search Console em {path}")
    header_idx, mapping = found
    resultado = []
    for row in rows[header_idx + 1:]:
        if not row or not any(c.strip() for c in row):
            continue
        try:
            resultado.append({
                "pagina": row[mapping["pagina"]].strip(),
                "cliques": int(_to_float(row[mapping["cliques"]])) if "cliques" in mapping else 0,
                "impressoes": int(_to_float(row[mapping["impressoes"]])) if "impressoes" in mapping else 0,
                "ctr": _to_float(row[mapping["ctr"]]) / 100 if "ctr" in mapping else 0.0,
                "posicao_media": _to_float(row[mapping["posicao_media"]]) if "posicao_media" in mapping else 0.0,
            })
        except IndexError:
            continue
    return resultado


def parse_ga_csv(path: Path) -> list[dict]:
    """Espera um export do GA4 (ex.: relatório 'Páginas e telas'), tolerando linhas de
    metadados no topo do arquivo antes do cabeçalho real da tabela."""
    rows = _read_rows(path)
    found = _find_header(rows, GA_SYNONYMS)
    if not found:
        raise CsvFormatError(f"não foi possível identificar as colunas esperadas do GA4 em {path}")
    header_idx, mapping = found
    resultado = []
    for row in rows[header_idx + 1:]:
        if not row or not any(c.strip() for c in row) or row[0].strip().startswith("#"):
            continue
        try:
            resultado.append({
                "pagina": row[mapping["pagina"]].strip(),
                "visualizacoes": int(_to_float(row[mapping["visualizacoes"]])) if "visualizacoes" in mapping else 0,
                "usuarios": int(_to_float(row[mapping["usuarios"]])) if "usuarios" in mapping else 0,
                "engajamento_medio_seg": _to_float(row[mapping["engajamento_medio_seg"]]) if "engajamento_medio_seg" in mapping else 0.0,
            })
        except IndexError:
            continue
    return resultado
