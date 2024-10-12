import pathlib
import re
import sys
from collections import deque
from typing import Callable, Iterable, Literal, TextIO, TypeAlias, Union

Number: TypeAlias = Union[int, float]
Operator: TypeAlias = Literal["+", "-", "*"]
Token: TypeAlias = Union[Number, Operator]
Operation: TypeAlias = Callable[[Number, Number], Number]


def readSplitLines(input_buffer: TextIO) -> Iterable[list[str]]:
    """
    Given an open file buffer, yield the lines on it as lists of elements.
    """
    for line in input_buffer:
        line = line.strip()
        line = re.sub(" +", " ", line)  # This will remove duplicate whitespaces from the line
        yield line.split(" ")  # And split the line into tokens


def parseToken(token: str) -> Token:
    """
    Convert a string token into either a number or an operand (+, - or * are
    supported)
    """
    if token.isnumeric():
        return int(token)
    elif token.replace(".", "", 1).isnumeric():
        return float(token)
    elif token in ["+", "-", "*"]:
        return token
    else:
        raise ValueError(f"Token {token} cannot be interpreted as numeric or operand")


operations: dict[Operator, Operation] = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
}


def operate(operation: Iterable[Token]):
    number_stack: deque[Number] = deque()  # A stack registry of all the numbers we're
    # encountering in the computation
    for token in operation:
        if isinstance(token, str) and token in operations:
            # Pop first the B, because some operations are not commutable (e.g. subtraction)
            if not len(number_stack) >= 2:
                raise ValueError("Operation cannot continue, operator requires at least 2 numbers")
            regB = number_stack.pop()
            regA = number_stack.pop()
            result = operations[token](regA, regB)
            number_stack.append(result)
        else:
            number_stack.append(token)

    if not len(number_stack) == 1:
        raise ValueError("Operation is not finished, missing operators")
    return number_stack.pop()


if __name__ == "__main__":
    # input_file = pathlib.Path(__file__).parent / "demo_input.txt"
    # input_buffer = input_file.open()

    for line in readSplitLines(input_buffer=sys.stdin):
        tokens = map(parseToken, line)
        print(operate(tokens))
