"""Работа с командной строкой."""
import sys

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError

EXIT_OK = 0
EXIT_USER_ERROR = 2

HELP = """\
usage: python -m toolkit calc "EXPRESSION"
       python -m toolkit convert VALUE --from UNIT --to UNIT
       python -m toolkit --help

Консольный набор утилит: калькулятор и конвертер величин.

команды:
  calc EXPRESSION                    вычислить выражение, например "2+3*4"
  convert VALUE --from UNIT --to UNIT
                                     перевести величину в другую единицу

операции:
  + - * /                            сложение, вычитание, умножение, деление
  // %                               деление нацело и остаток
  ( )                                скобки

единицы:
  длина: mm, cm, m, km
  масса: g, kg
  температура: c, f, k

опции:
  -h, --help                         показать эту справку"""


def format_number(value: float) -> str:
    """Убирает .0 у целых чисел."""
    if value.is_integer():
        return str(int(value))
    return str(value)


def run_calc(args: list[str]) -> float:
    """Команда calc."""
    if len(args) != 1:
        raise ToolkitError('calc ожидает одно выражение в кавычках, например: calc "2 + 3"')
    return calculate(args[0])


def run_convert(args: list[str]) -> float:
    """Команда convert."""
    value_text = None
    units = {"--from": None, "--to": None}

    i = 0
    while i < len(args):
        arg = args[i]
        if arg in units:
            if i + 1 >= len(args):
                raise ToolkitError(f"после {arg} нужно указать единицу")
            units[arg] = args[i + 1]
            i += 2
        elif value_text is None:
            value_text = arg
            i += 1
        else:
            raise ToolkitError(f"лишний аргумент: {arg!r}")

    if value_text is None:
        raise ToolkitError("convert: не указано значение")
    if units["--from"] is None or units["--to"] is None:
        raise ToolkitError("convert: нужно указать --from и --to")

    try:
        value = float(value_text)
    except ValueError:
        raise ToolkitError(f"неверное числовое значение: {value_text!r}") from None
    return convert(value, units["--from"], units["--to"])


def run(argv: list[str]) -> float:
    """Выбирает команду для запуска."""
    if not argv:
        raise ToolkitError("не указана команда (подробнее: --help)")
    command, args = argv[0], argv[1:]
    if command == "calc":
        return run_calc(args)
    if command == "convert":
        return run_convert(args)
    raise ToolkitError(f"неизвестная команда: {command!r} (доступны calc и convert)")


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if "-h" in argv or "--help" in argv:
        print(HELP)
        return EXIT_OK

    try:
        result = run(argv)
    except ToolkitError as err:
        print(f"ошибка: {err}", file=sys.stderr)
        return EXIT_USER_ERROR

    print(format_number(result))
    return EXIT_OK