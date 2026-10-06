"""Тесты калькулятора."""
import pytest

from toolkit.calculator import calculate, tokenize
from toolkit.errors import (
    ConsecutiveOperatorsError,
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    InvalidNumberError,
    MissingOperandError,
    ParenthesisError,
)

# --- позитивные ---


def test_calc_basic():
    assert calculate("2+3*4") == 14
    assert calculate("10 / 4") == 2.5
    assert calculate("8-2-1") == 5


def test_calc_parentheses():
    assert calculate("(1+2)*3") == 9
    assert calculate("2.5 * (4 - 2)") == 5


def test_calc_unary_sign():
    assert calculate("-2 * -3") == 6
    assert calculate("1+-2") == -1
    assert calculate("-(1+2)+1") == -2


def test_calc_floor_division_and_remainder():
    assert calculate("7//2") == 3
    assert calculate("7%2") == 1
    assert calculate("-7//2") == -4
    assert calculate("7%-2") == -1


def test_tokenize():
    assert tokenize("-2*-3") == [-2.0, "*", -3.0]
    assert tokenize("-(1)") == ["neg", "(", 1.0, ")"]


# --- негативные ---


def test_calc_empty_expression():
    with pytest.raises(EmptyExpressionError):
        calculate("")


def test_calc_division_by_zero():
    with pytest.raises(DivisionByZeroError):
        calculate("1/0")
    with pytest.raises(DivisionByZeroError):
        calculate("7%0")


def test_calc_invalid_input():
    with pytest.raises(InvalidCharacterError):
        calculate("2+a")
    with pytest.raises(InvalidNumberError):
        calculate("1..2+3")


def test_calc_operator_errors():
    with pytest.raises(ConsecutiveOperatorsError):
        calculate("2*/3")
    with pytest.raises(MissingOperandError):
        calculate("2+")


def test_calc_parenthesis_errors():
    with pytest.raises(ParenthesisError):
        calculate("(1+2")
    with pytest.raises(ParenthesisError):
        calculate("1+2)")
