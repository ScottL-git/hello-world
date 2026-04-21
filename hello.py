"""Simple hello CLI module."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Create and configure the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Print a personalized greeting.")
    parser.add_argument("--name", required=True, help="Name to greet")
    parser.add_argument(
        "--uppercase",
        action="store_true",
        help="Print the greeting in uppercase",
    )
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

    greeting = f"Hello, {name}"
    if args.uppercase:
        greeting = greeting.upper()

    print(greeting)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
