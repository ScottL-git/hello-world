import pytest

from hello import main


def test_main_prints_greeting_for_valid_name(capsys):
    exit_code = main(["Alice"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "Hello, Alice\n"
    assert captured.err == ""


@pytest.mark.parametrize("invalid_name", ["", "   "])
def test_main_rejects_empty_or_whitespace_name(invalid_name, capsys):
    with pytest.raises(SystemExit) as exc_info:
        main([invalid_name])

    captured = capsys.readouterr()
    assert exc_info.value.code == 2
    assert "name must be a non-empty string" in captured.err


def test_main_requires_name_argument(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main([])

    captured = capsys.readouterr()
    assert exc_info.value.code == 2
    assert "the following arguments are required: name" in captured.err
