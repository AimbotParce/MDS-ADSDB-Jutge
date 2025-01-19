import heapq
import math
import re
import sys
from collections import deque
from typing import *

T = TypeVar("T")


def heapSort(array: list[T], desc: bool = False) -> list[T]:
    "Use a heap to sort the array"
    heap = array.copy()
    heapq.heapify(heap)

    sorted_array = [None] * len(array)
    if desc:
        for i in range(len(array) - 1, -1, -1):
            sorted_array[i] = heapq.heappop(heap)
    else:
        for i in range(len(array)):
            sorted_array[i] = heapq.heappop(heap)

    return sorted_array


def yieldCases(input_buffer: TextIO) -> Generator[List[int], None, None]:
    for line in input_buffer:
        if line.strip() == "":
            return
        yield list(map(int, line.split()))


if __name__ == "__main__":
    case = next(yieldCases(sys.stdin))
    sorted = heapSort(case)
    print(" ".join(map(str, sorted)))
    print(" ".join(map(str, reversed(sorted))))
