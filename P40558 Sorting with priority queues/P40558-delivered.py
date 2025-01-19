import heapq
from typing import *

from yogi import scan

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


if __name__ == "__main__":
    case: list[int] = []
    while (num := scan(int)) is not None:
        case.append(num)
    print(" ".join(map(str, heapSort(case))))
    print(" ".join(map(str, heapSort(case, desc=True))))
