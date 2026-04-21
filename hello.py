"""Simple hello CLI module."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Create and configure the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Print a personalized greeting.")
    parser.add_argument("name", help="Name to greet")
    return parser


def validate_name(value: str, parser: argparse.ArgumentParser) -> str:
    """Validate that the provided name is non-empty after trimming."""
    name = value.strip()
    if not name:
        parser.error("name must be a non-empty string")
    return name


def main(argv: list[str] | None = None) -> int:
    """Run the hello CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    name = validate_name(args.name, parser)
    print(f"Hello, {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
