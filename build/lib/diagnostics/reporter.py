"""Report formatting and file output."""

from __future__ import annotations

import json
from pathlib import Path


def to_json(report: dict) -> str:
    return json.dumps(report, indent=2)


def to_text(report: dict) -> str:
    lines = [
        "Developer Environment Health Report",
        "===================================",
        f"Path            : {report['path']}",
        "",
    ]
    for item in report["checks"]:
        lines.append(f"{item['name']:<18}: {item['status']}")
        lines.append(f"  {item['message']}")
    lines.extend([
        "",
        f"Overall Status   : {report['overall_status']}",
        f"Exit Code        : {report['exit_code']}",
    ])
    return "\n".join(lines)


def write_report(content: str, output: str | None) -> None:
    if not output:
        return
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content + "\n", encoding="utf-8")
