"""Machine and developer-environment checks."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def _version_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def check_python(min_version: str) -> dict:
    current = ".".join(map(str, sys.version_info[:3]))
    passed = sys.version_info[:2] >= _version_tuple(min_version)[:2]
    return {
        "name": "python_version",
        "status": "PASS" if passed else "FAIL",
        "value": current,
        "message": f"Python {current} (minimum {min_version})",
    }


def check_disk(path: str, minimum_gb: float) -> dict:
    target = Path(path)
    try:
        usage = shutil.disk_usage(target)
    except OSError as exc:
        return {
            "name": "disk_space",
            "status": "FAIL",
            "value": None,
            "message": f"Unable to inspect {target}: {exc}",
        }

    free_gb = usage.free / (1024 ** 3)
    passed = free_gb >= minimum_gb
    return {
        "name": "disk_space",
        "status": "PASS" if passed else "FAIL",
        "value": round(free_gb, 2),
        "message": f"{free_gb:.2f} GB free (minimum {minimum_gb} GB)",
    }


def check_environment(required: list[str]) -> dict:
    missing = [name for name in required if not os.environ.get(name)]
    passed = not missing
    return {
        "name": "environment_variables",
        "status": "PASS" if passed else "FAIL",
        "value": {"checked": required, "missing": missing},
        "message": "All required environment variables are set."
        if passed else f"Missing: {', '.join(missing)}",
    }


def check_developer_tools(tools: list[str]) -> dict:
    missing = [tool for tool in tools if shutil.which(tool) is None]
    passed = not missing
    return {
        "name": "developer_tools",
        "status": "PASS" if passed else "FAIL",
        "value": {"checked": tools, "missing": missing},
        "message": "All configured developer tools were found on PATH."
        if passed else f"Missing: {', '.join(missing)}",
    }


def run_diagnostics(config: dict, path: str) -> dict:
    checks = [
        check_python(config["min_python"]),
        check_disk(path, config["min_free_disk_gb"]),
        check_environment(config["required_env"]),
        check_developer_tools(config["developer_tools"]),
    ]

    failed = [item for item in checks if item["status"] == "FAIL"]
    return {
        "tool": "rabtech-cli-diagnostics",
        "version": "1.0.0",
        "path": str(Path(path).resolve()),
        "checks": checks,
        "overall_status": "HEALTHY" if not failed else "UNHEALTHY",
        "exit_code": 0 if not failed else 1,
    }
