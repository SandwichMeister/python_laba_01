"""Тесты конвертера."""
import pytest

from toolkit.converter import convert
from toolkit.errors import BelowAbsoluteZeroError, IncompatibleUnitsError, UnknownUnitError

# позитивные


def test_convert_length_and_mass():
    assert convert(1000, "mm", "m") == pytest.approx(1)
    assert convert(1.5, "kg", "g") == pytest.approx(1500)


def test_convert_temperature():
    assert convert(0, "c", "f") == pytest.approx(32)
    assert convert(-273.15, "c", "k") == pytest.approx(0, abs=1e-9)


def test_convert_case_and_result_type():
    assert convert(1, "KG", "G") == pytest.approx(1000)
    assert isinstance(convert(1, "m", "m"), float)


# негативные


def test_convert_below_absolute_zero():
    with pytest.raises(BelowAbsoluteZeroError):
        convert(-274, "c", "k")
    with pytest.raises(BelowAbsoluteZeroError):
        convert(-1, "k", "c")


def test_convert_unit_errors():
    with pytest.raises(IncompatibleUnitsError):
        convert(1, "kg", "m")
    with pytest.raises(UnknownUnitError):
        convert(1, "mile", "m")
