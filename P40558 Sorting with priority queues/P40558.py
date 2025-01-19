import math
import re
import sys
from collections import deque
from typing import *

T = TypeVar("T")


class Heap(Generic[T]):
    def __init__(self, initial: Iterable[T] = None):
        self._vector: List[T] = [None]
        for value in initial if initial else []:
            self._vector.append(value)

        for i in range((len(self._vector) - 1) // 2, 0, -1):
            self._percolateDown(i)

    def __len__(self):
        return len(self._vector) - 1

    def __str__(self) -> str:
        if self.isEmpty():
            return ""
        queue = deque[Union[int, None]]([1, None])
        levels: list[list[str]] = []
        current_level: list[str] = []
        while queue:
            i = queue.popleft()
            if i == None:
                if not current_level:
                    # We've finished
                    break
                levels.append(current_level)
                queue.append(None)
                current_level = []
                continue
            left = self._left(i)
            right = self._right(i)
            if left < len(self._vector):
                queue.append(left)
            if right < len(self._vector):
                queue.append(right)
            current_level.append(str(self._vector[i]))

        return ">".join(",".join(l) for l in levels)

    def _checkHeapProperty(self):
        "Check that the heap property is correctly maintained."
        for i in range(1, len(self._vector)):
            if self._left(i) < len(self._vector) and not self._vector[i] >= self._vector[self._left(i)]:
                return False
            if self._right(i) < len(self._vector) and not self._vector[i] >= self._vector[self._right(i)]:
                return False
        return True

    def isEmpty(self):
        return len(self) == 0

    @staticmethod
    def _left(i: int):
        return 2 * i

    @staticmethod
    def _right(i: int):
        return 2 * i + 1

    @staticmethod
    def _parent(i: int):
        return i // 2

    def _max(self, *indices: int) -> int:
        "Out of the provided indices, return which of them has the maximum key"
        largest = None
        largest_value = None
        for i in indices:
            if 0 < i < len(self._vector):
                if largest is None:
                    largest = i
                    largest_value = self._vector[i]
                elif (value := self._vector[i]) > largest_value:
                    largest = i
                    largest_value = value

        if largest is None:
            raise ValueError("All the provided values are outside the vector.")
        return largest

    def _percolateDown(self, i: int):
        """Percolate down the max-heap condition on index i, supposing that its
        children trees are max-heaps"""
        if i > (len(self._vector) - 1) // 2:  # The right half of the vector is necessarily correct already.
            return
        largest = self._max(i, self._left(i), self._right(i))  # Get the max index
        if largest != i:
            self._vector[i], self._vector[largest] = self._vector[largest], self._vector[i]  # Swap them
            self._percolateDown(largest)

    def _percolateUp(self, i: int):
        """
        Percolate up the max-heap condition on index i, supposing that the rest
        of the tree is actually a max-heap
        """
        if i <= 1:  # In the base case, no need to do anything.
            return
        parent = self._parent(i)
        if self._max(i, parent) == i:
            self._vector[i], self._vector[parent] = self._vector[parent], self._vector[i]  # Swap them
            self._percolateUp(parent)

    def insert(self, value: T) -> None:
        "Append a new element to the queue"
        self._vector.append(value)
        self._percolateUp(len(self._vector) - 1)

    def maximum(self) -> T:
        "Returns the element with the highest priority"
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self._vector[1]

    def extractMax(self) -> T:
        "Pops the element with the highest priority"
        if self.isEmpty():
            raise IndexError("Queue is empty")
        res = self._vector[1]
        self._vector[1] = self._vector[-1]
        self._vector.pop()
        self._percolateDown(1)
        return res


def heapSort(array: list[T], desc: bool = False) -> list[T]:
    "Use a heap to sort the array"
    heap = Heap(array)
    sorted_array = [None] * len(array)
    if desc:
        for i in range(len(array)):
            sorted_array[i] = heap.extractMax()
    else:
        for i in range(len(array) - 1, -1, -1):
            sorted_array[i] = heap.extractMax()

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
    print(" ".join(map(str, sorted[::-1])))
