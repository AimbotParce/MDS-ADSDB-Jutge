import logging as log
import pathlib
from typing import Iterable, TextIO

import yogi


def generateCases(input_buffer: TextIO) -> Iterable[list[int]]:
    """
    Given an open file buffer, yield the lists on it defined as:
    <n> <n elements> <m> <m elements>
    of type int.
    """
    input_buffer.seek(0)  # Reset read pointer
    reader = yogi.Yogi(input_buffer)
    tokens_generator = reader.tokens(int)
    for length in tokens_generator:  # Read a single element of the text
        # This element will be considered to be the length of the next case.
        current_case = list(next(tokens_generator) for _ in range(length))
        # Read that amount of elements from the text
        yield current_case


def hasSumOfRest(numbers: list[int]) -> bool:
    """
    Check whether a list of integers contains at least one element which is
    equal to the sum of the rest.
    """
    sum_total = sum(numbers)  # Same as total=0; for n in numbers: total+=1

    for num in numbers:
        # Run over all the numbers and compute the sum of all the others, to compare it.
        others_sum = sum_total - num
        if others_sum == num:
            # If we found one number that is equal to the sum of the others, break early.
            return True

    # If we found nothing, return False.
    return False


if __name__ == "__main__":
    log.basicConfig(level=log.INFO, format="%(msg)s")

    input_file = pathlib.Path(__file__).parent / "demo_input.txt"
    input_buffer = input_file.open()

    for case in generateCases(input_buffer=input_buffer):
        log.info("YES" if hasSumOfRest(case) else "NO")
