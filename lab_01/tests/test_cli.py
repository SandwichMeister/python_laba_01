"""Тесты командной строки."""
import subprocess
import sys

from toolkit.cli import main

# --- позитивные ---


def test_cli_help(capsys):
    assert main(["--help"]) == 0
    assert "usage" in capsys.readouterr().out


def test_cli_success(capsys):
    assert main(["calc", "2+3*4"]) == 0
    assert capsys.readouterr().out.strip() == "14"


# негативные


def test_cli_errors(capsys):
    assert main(["calc", "1/0"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "деление на ноль" in captured.err


def test_cli_real_run_error():
    result = subprocess.run(
        [sys.executable, "-m", "toolkit", "convert", "abc", "--from", "m", "--to", "cm"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "неверное числовое значение" in result.stderr
