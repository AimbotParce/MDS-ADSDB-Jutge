import sys
from typing import Iterable, TextIO

import yogi


def generateCases() -> Iterable[list[int]]:
    """
    Given an open file buffer, yield the lists on it defined as:
    <n> <n elements> <m> <m elements>
    of type int.
    """
    while True:
        # Read the first integer of the line
        length = yogi.scan(int)
        if length is None:
            # If we reached the end of the file, break the loop
            break
        # Read that amount of elements from the text
        yield list(yogi.scan(float) for _ in range(length))


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


for case in generateCases():
    print("YES" if hasSumOfRest(case) else "NO")
