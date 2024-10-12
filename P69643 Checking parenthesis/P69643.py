from collections import deque

import yogi

# The list of "opening" and "closing" characters. Each opening character must be
# in the same position in the "openers" list as their closing character is in
# the "closers" one.
openers = "[("
closers = "])"
# This means, "[" can only be closed with "]", and "(" can only be closed by ")"


def checkParenthesis(line: str) -> bool:
    opener_stack: deque[str] = deque()
    for char in line:
        # Check if the character is an opening or closing character, and find
        # which "id" is it. This will allow us to identify which character is
        # needed to close the current scope (the latest opening character in the
        # stack).
        opener_pos = openers.find(char)
        closer_pos = closers.find(char)
        if opener_pos != -1:
            # If we encountered an opener, add one level to the stack
            opener_stack.append(opener_pos)
        elif closer_pos != opener_stack.pop():
            # If we encountered a closer, check if it's the one that we were
            # expecting. Otherwise, break early, this is incorrect.
            return False
        elif opener_pos == -1 and closer_pos == -1:
            # If it is neither, then we've found an illegal character.
            raise ValueError(f"Encountered illegal character: {char}")
        # It can't be both at the same time, because we've constructed the
        # openers and closers list such that they are mutually exclusive.

    # If we've ended, we only need to check whether we haven't left any unclosed scopes.
    return len(opener_stack) == 0


if __name__ == "__main__":
    # input_file = pathlib.Path(__file__).parent / "demo_input.txt"
    # input_buffer = input_file.open()

    for case in yogi.tokens(str):
        if checkParenthesis(case):
            print(f"{case} is correct")
        else:
            print(f"{case} is incorrect")