import sys
from collections import deque
from typing import Iterable, TextIO

# The mapping of opening-to-closing characters. The pairs are in the form of
# "opening": "closing".
mapping = {"[": "]", "(": ")"}
# This means, "[" can only be closed with "]", and "(" can only be closed by ")"


def checkParenthesis(line: str) -> bool:
    opener_stack: deque[str] = deque()
    for char in line:
        expected_closer = mapping.get(char)
        # This is the closer that we're expecting to find further down the line
        if expected_closer is not None:
            # Store it in the stack, so we can check it later
            opener_stack.append(expected_closer)
        else:
            # If it's not an opener, it can be either a closer or an illegal
            # character. Pop the last expected closer from the stack, if it
            # matches the current character, we're good. Otherwise, it's either
            # an illegal character or a mismatched closer. If the stack is empty,
            # it cannot be okay.
            if len(opener_stack) == 0 or char != opener_stack.pop():
                return False

    # If we've ended, we only need to check whether we haven't left any unclosed scopes.
    return len(opener_stack) == 0


def generateCases(input_buffer: TextIO) -> Iterable[str]:
    """
    Given an open file buffer, yield the lines on it as strings.
    """
    for line in input_buffer:
        line = line.strip()
        if not line:
            return  # If the line is empty, we're done with the file

        yield from line.split()  # Split the line by whitespace and yield each part


if __name__ == "__main__":
    for case in generateCases(input_buffer=sys.stdin):
        if checkParenthesis(case):
            print(f"{case} is correct")
        else:
            print(f"{case} is incorrect")
