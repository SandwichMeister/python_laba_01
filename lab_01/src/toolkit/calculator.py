"""Ядро калькулятора"""
from toolkit.errors import (
    CalculatorError,
    ConsecutiveOperatorsError,
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    InvalidNumberError,
    MissingOperandError,
    MissingOperatorError,
    ParenthesisError,
)

Token = float | str

# "neg" - унарный минус перед скобкой
PRIO = {"+": 1, "-": 1, "*": 2, "/": 2, "//": 2, "%": 2, "neg": 3}

def is_op(token: object) -> bool:
    return token in ['+',"-","*","/","//","%","neg"]

def is_number(token: object) -> bool:
    return isinstance(token, (int, float))

def read_number(expr: str) -> tuple[float, str]:
    """Читает число из начала строки."""
    num = ""
    while expr and expr[0] in "0123456789.":
        num += expr[0]
        expr = expr[1:]
    try:
        return float(num), expr
    except ValueError:
        raise InvalidNumberError(f"неверное число: {num!r}") from None


def tokenize(expr: str) -> list[Token]:
    """Делит строку на числа (float), знаки и скобки."""
    tokens: list[Token] = []
    while expr:
        tok = expr[0]

        # пробелы между токенами игнорируем
        if tok == " ":
            expr = expr[1:]
            continue

        # обработка унарного знака
        if tok in "-+" and (not tokens or is_op(tokens[-1]) or tokens[-1] == "("):
            expr = expr[1:].lstrip()
            if not expr:
                raise MissingOperandError("после унарного знака ожидается число или скобка")
            if expr[0] in "0123456789.":
                # знак перед числом приклеиваем к числу
                sign = -1 if tok == "-" else 1
                num, expr = read_number(expr)
                tokens.append(sign * num)
            elif tok == "-":
                # минус перед скобкой
                tokens.append("neg")
            # унарный плюс перед скобкой ничего не меняет, пропускаем его
            continue

        #обработка чисел
        if tok in "0123456789.":
            num, expr = read_number(expr)
            tokens.append(num)
            continue

        # знак // состоит из двух символов
        if expr[:2] == "//":
            tokens.append("//")
            expr = expr[2:]
            continue

        if is_op(tok) or tok in "()":
            tokens.append(tok)
        else:
            raise InvalidCharacterError(f"недопустимый символ: {tok!r}")

        expr = expr[1:]

    return tokens

def validate(tokens: list[Token]) -> None:
    """Проверяет корректность выражения"""
    if not tokens:
        raise EmptyExpressionError("пустое выражение")

    depth = 0            # сколько скобок открыто и ещё не закрыто
    need_operand = True  # чего ждём дальше: операнд [число или "("] / оператор [или ")"]
    prev = None
    for tok in tokens:
        if need_operand:
            if is_number(tok):
                need_operand = False
            elif tok == "(":
                depth += 1
            elif tok == "neg":
                pass  # после унарного минуса всё ещё ждём операнд
            elif is_op(tok) and is_op(prev) and prev != "neg":
                raise ConsecutiveOperatorsError(f"два оператора подряд: {prev}{tok}")
            else:
                raise MissingOperandError(f"пропущен операнд перед {tok!r}")
        else:
            if is_op(tok):
                need_operand = True
            elif tok == ")":
                if depth == 0:
                    raise ParenthesisError("лишняя закрывающая скобка")
                depth -= 1
            else:
                raise MissingOperatorError(f"пропущен оператор перед {tok!r}")
        prev = tok

    if need_operand:
        raise MissingOperandError("пропущен операнд в конце выражения")
    if depth > 0:
        raise ParenthesisError("не закрыта скобка")


def trans_polish(tokens: list[Token]) -> list[Token]:
    """Переводит выражение в RPN."""
    res: list[Token] = []
    stack: list[Token] = []
    for tok in tokens:
        if is_number(tok):
            res.append(tok)

        elif tok == "neg":
            # ждём операнд, ничего не выталкиваем
            stack.append(tok)

        elif is_op(tok):
            while stack and is_op(stack[-1]) and PRIO[stack[-1]] >= PRIO[tok]:
                res.append(stack.pop())
            stack.append(tok)

        elif tok == "(":
            stack.append(tok)
        elif tok == ")":
            while stack and stack[-1] != "(":
                res.append(stack.pop())
            if stack and stack[-1] == "(":
                stack.pop()

    while stack:
        res.append(stack.pop())

    return res

def calc_polish(rpn_expr: list[Token]) -> float:
    """Считает выражение в RPN."""
    stack: list[float] = []
    for tok in rpn_expr:
        if is_number(tok):
            stack.append(tok)
        elif tok == "neg":
            # унарный минус берёт одно число и меняет ему знак
            stack.append(-stack.pop())
        elif is_op(tok):
            op1 = stack.pop()
            op2 = stack.pop()
            match tok:
                case "+":
                    res = op1 + op2
                case "-":
                    res = op2 - op1
                case "*":
                    res = op1 * op2
                case "/":
                    if op1 != 0:
                        res = op2 / op1
                    else:
                        raise DivisionByZeroError("деление на ноль")
                case "//":
                    # деление нацело, округляет вниз: -7 // 2 = -4
                    if op1 != 0:
                        res = op2 // op1
                    else:
                        raise DivisionByZeroError("деление на ноль")
                case "%":
                    # остаток, знак как у делителя: -7 % 2 = 1
                    if op1 != 0:
                        res = op2 % op1
                    else:
                        raise DivisionByZeroError("деление на ноль")

                case _: #unknown operation
                    raise CalculatorError(f"неизвестный оператор: {tok!r}")
            #push result
            stack.append(res)
    if stack:
        return stack.pop()
    raise CalculatorError("некорректное выражение")

def calculate(expr: str) -> float:
    """Считает выражение из строки."""
    tokens = tokenize(expr)
    validate(tokens)
    rpn_expr = trans_polish(tokens)
    return calc_polish(rpn_expr)
