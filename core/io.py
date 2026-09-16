"""Leitura/escrita de JSON e helpers de texto."""
from __future__ import annotations

import json
import os
import re
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))


def normalize_term(text: str) -> str:
    return " ".join(strip_accents(str(text)).lower().split())


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", normalize_term(text)).strip("-")


def write_json(path: Path, data: Any) -> Path:
    """Escrita atômica: evita JSON truncado se o processo for interrompido."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, path)
    return path


def read_json(path: Path) -> Any:
    with Path(path).open(encoding="utf-8") as fh:
        return json.load(fh)
