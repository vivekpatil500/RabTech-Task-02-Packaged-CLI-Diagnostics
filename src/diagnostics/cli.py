"""Command-line interface."""

from __future__ import annotations

import argparse
import sys

from .checks import run_diagnostics
from .config import ConfigError, load_config
from .reporter import to_json, to_text, write_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rabtech-diagnostics",
        description="Inspect a machine and produce a deterministic developer-environment health report.",
    )
    parser.add_argument(
        "--config",
        help="Path to a JSON diagnostics configuration file.",
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Disk path to inspect (default: current directory).",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Report format (default: text).",
    )
    parser.add_argument(
        "--output",
        help="Optional path to save the report.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = load_config(args.config)
    except ConfigError as exc:
        print(f"CONFIG ERROR: {exc}", file=sys.stderr)
        return 2

    report = run_diagnostics(config, args.path)
    content = to_json(report) if args.format == "json" else to_text(report)
    print(content)
    try:
        write_report(content, args.output)
    except OSError as exc:
        print(f"OUTPUT ERROR: {exc}", file=sys.stderr)
        return 2
    return report["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
