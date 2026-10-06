"""Конвертер величин."""
from toolkit.errors import BelowAbsoluteZeroError, IncompatibleUnitsError, UnknownUnitError

# коэффициенты к базовой единице группы (длина - мм, масса - г)
LENGTH = {"mm": 1.0, "cm": 10.0, "m": 1000.0, "km": 1_000_000.0}
MASS = {"g": 1.0, "kg": 1000.0}
TEMPERATURE = ("c", "f", "k")

EPS = 1e-9  # допуск на погрешность float при проверке абсолютного нуля


def get_group(unit: str) -> str:
    """Находит группу единицы."""
    if unit in LENGTH:
        return "length"
    if unit in MASS:
        return "mass"
    if unit in TEMPERATURE:
        return "temperature"
    raise UnknownUnitError(f"неизвестная единица: {unit!r}")


def to_kelvin(value: float, unit: str) -> float:
    if unit == "c":
        return value + 273.15
    if unit == "f":
        return (value - 32) * 5 / 9 + 273.15
    return value


def from_kelvin(kelvin: float, unit: str) -> float:
    if unit == "c":
        return kelvin - 273.15
    if unit == "f":
        return (kelvin - 273.15) * 9 / 5 + 32
    return kelvin


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    kelvin = to_kelvin(value, from_unit)
    if kelvin < -EPS:
        raise BelowAbsoluteZeroError(f"температура ниже абсолютного нуля: {value} {from_unit}")
    if from_unit == to_unit:
        return float(value)
    return from_kelvin(max(kelvin, 0.0), to_unit)


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Переводит значение из одной единицы в другую."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    group = get_group(from_unit)
    if group != get_group(to_unit):
        raise IncompatibleUnitsError(f"несовместимые единицы: {from_unit} и {to_unit}")

    if group == "temperature":
        return convert_temperature(value, from_unit, to_unit)

    table = LENGTH if group == "length" else MASS
    return float(value * table[from_unit] / table[to_unit])
