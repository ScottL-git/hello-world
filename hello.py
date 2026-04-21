"""Simple hello CLI module and pytest tests."""

from __future__ import annotations

import argparse

import pytest


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


def test_main_prints_greeting_for_valid_name_flag(capsys):
    exit_code = main(["--name", "Alice"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "Hello, Alice\n"
    assert captured.err == ""


def test_main_supports_uppercase_flag(capsys):
    exit_code = main(["--name", "Alice", "--uppercase"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "HELLO, ALICE\n"
    assert captured.err == ""


@pytest.mark.parametrize("invalid_name", ["", "   "])
def test_main_rejects_empty_or_whitespace_name(invalid_name, capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--name", invalid_name])

    captured = capsys.readouterr()
    assert exc_info.value.code == 2
    assert "name must be a non-empty string" in captured.err


def test_main_requires_name_argument(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main([])

    captured = capsys.readouterr()
    assert exc_info.value.code == 2
    assert "the following arguments are required: --name" in captured.err


if __name__ == "__main__":
    raise SystemExit(main())
