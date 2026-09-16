"""Logging: texto legível + JSON Lines por execução em /logs."""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone

from core.config import ROOT

LOGS_DIR = ROOT / "logs"


class JsonLinesFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        entry = {
            "ts": datetime.fromtimestamp(record.created, timezone.utc).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            entry["exc"] = self.formatException(record.exc_info)
        return json.dumps(entry, ensure_ascii=False)


def get_logger(run_id: str, name: str = "blog_factory") -> logging.Logger:
    """Um logger por run_id, gravando logs/<run_id>.log e logs/<run_id>.jsonl."""
    logger = logging.getLogger(f"{name}.{run_id}")
    if logger.handlers:
        return logger
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    text = logging.FileHandler(LOGS_DIR / f"{run_id}.log", encoding="utf-8")
    text.setLevel(logging.DEBUG)
    text.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s"))

    jsonl = logging.FileHandler(LOGS_DIR / f"{run_id}.jsonl", encoding="utf-8")
    jsonl.setLevel(logging.DEBUG)
    jsonl.setFormatter(JsonLinesFormatter())

    console = logging.StreamHandler(sys.stderr)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    for handler in (text, jsonl, console):
        logger.addHandler(handler)
    return logger
