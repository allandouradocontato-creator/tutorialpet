"""Carregamento de configuração (.env, YAML de sites e filtros)."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
SITES_DIR = CONFIG_DIR / "sites"

SITE_REQUIRED_KEYS = ("site_id", "nicho", "idioma", "google_ads", "termos_semente", "persona_editorial", "compliance")


class ConfigError(RuntimeError):
    pass


def load_env_file(path: Path = ROOT / ".env") -> None:
    """Carrega KEY=VALUE de um .env sem sobrescrever variáveis já definidas no ambiente."""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and value and not os.environ.get(key):
            os.environ[key] = value


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ConfigError(f"Arquivo de configuração não encontrado: {path}")
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def deep_merge(base: dict, override: dict) -> dict:
    merged = dict(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_site(site_id: str) -> dict[str, Any]:
    site = load_yaml(SITES_DIR / f"{site_id}.yaml")
    missing = [k for k in SITE_REQUIRED_KEYS if k not in site]
    if missing:
        raise ConfigError(f"Site '{site_id}' sem chaves obrigatórias: {', '.join(missing)}")
    if site["site_id"] != site_id:
        raise ConfigError(f"site_id no YAML ({site['site_id']}) difere do nome do arquivo ({site_id})")
    return site


def load_keyword_filters(site_id: str) -> dict[str, Any]:
    raw = load_yaml(CONFIG_DIR / "keyword_filters.yaml")
    return deep_merge(raw.get("default", {}), (raw.get("sites") or {}).get(site_id, {}))


def load_publishing_schedule(site_id: str) -> dict[str, Any]:
    raw = load_yaml(CONFIG_DIR / "publishing_schedule.yaml")
    return deep_merge(raw.get("default", {}), (raw.get("sites") or {}).get(site_id, {}))
