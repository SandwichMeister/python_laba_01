"""Ошибки программы."""


class ToolkitError(Exception):
    """Общая ошибка ввода."""


# калькулятор


class CalculatorError(ToolkitError):
    """Ошибка калькулятора."""


class EmptyExpressionError(CalculatorError):
    """Пустое выражение."""


class InvalidCharacterError(CalculatorError):
    """Недопустимый символ."""


class InvalidNumberError(CalculatorError):
    """Неверное число."""


class MissingOperandError(CalculatorError):
    """Пропущено число."""


class MissingOperatorError(CalculatorError):
    """Пропущен знак."""


class ConsecutiveOperatorsError(CalculatorError):
    """Два знака подряд."""


class ParenthesisError(CalculatorError):
    """Непарные скобки."""


class DivisionByZeroError(CalculatorError):
    """Деление на ноль."""


# --- конвертер ---


class ConverterError(ToolkitError):
    """Ошибка конвертера."""


class UnknownUnitError(ConverterError):
    """Неизвестная единица."""


class IncompatibleUnitsError(ConverterError):
    """Единицы из разных групп."""


class BelowAbsoluteZeroError(ConverterError):
    """Температура ниже абсолютного нуля."""
