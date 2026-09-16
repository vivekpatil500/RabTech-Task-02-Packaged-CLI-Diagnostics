"""Configuration loading and validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ConfigError(ValueError):
    """Raised when diagnostics configuration is invalid."""


DEFAULT_CONFIG = {
    "min_python": "3.9",
    "min_free_disk_gb": 1,
    "required_env": ["PATH"],
    "developer_tools": ["python", "git", "pip"],
}


def _validate_version(value: Any) -> str:
    if not isinstance(value, str) or len(value.split(".")) < 2:
        raise ConfigError("min_python must be a version string such as '3.9'")
    parts = value.split(".")
    if not all(part.isdigit() for part in parts):
        raise ConfigError("min_python must contain numeric version parts")
    return value


def load_config(path: str | None) -> dict:
    """Load and validate a JSON configuration file."""
    if path is None:
        return dict(DEFAULT_CONFIG)

    config_path = Path(path)
    if not config_path.is_file():
        raise ConfigError(f"Configuration file not found: {config_path}")

    try:
        with config_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Malformed JSON configuration: {exc.msg}") from exc
    except OSError as exc:
        raise ConfigError(f"Unable to read configuration: {exc}") from exc

    if not isinstance(data, dict):
        raise ConfigError("Configuration root must be a JSON object")

    merged = dict(DEFAULT_CONFIG)
    merged.update(data)

    _validate_version(merged["min_python"])

    if not isinstance(merged["min_free_disk_gb"], (int, float)) or merged["min_free_disk_gb"] < 0:
        raise ConfigError("min_free_disk_gb must be a non-negative number")

    for key in ("required_env", "developer_tools"):
        if not isinstance(merged[key], list) or not all(isinstance(x, str) and x for x in merged[key]):
            raise ConfigError(f"{key} must be a list of non-empty strings")

    return merged
