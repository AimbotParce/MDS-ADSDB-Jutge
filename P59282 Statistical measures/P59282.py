import math
import re
import sys
from collections import deque
from typing import *

T = TypeVar("T")


class Heap(Generic[T]):
    @overload
    def __init__(self, initial: Iterable[T] = None, type: Literal["min", "max"] = "max"): ...
    @overload
    def __init__(self, type: Literal["min", "max"] = "max"): ...
    @overload
    def __init__(self, initial: Iterable[T] = None): ...
    @overload
    def __init__(self): ...

    def __init__(self, initial: Iterable[T] = None, type: Literal["min", "max"] = "max"):
        self._vector: List[T] = [None]
        self._type = type
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

        cmp = "<" if self._type == "min" else ">"

        return cmp.join(",".join(l) for l in levels)

    def _checkHeapProperty(self):
        "Check that the heap property is correctly maintained."
        if self._type == "max":
            for i in range(1, len(self._vector)):
                if self._left(i) < len(self._vector) and not self._vector[i] >= self._vector[self._left(i)]:
                    return False
                if self._right(i) < len(self._vector) and not self._vector[i] >= self._vector[self._right(i)]:
                    return False
        else:
            for i in range(1, len(self._vector)):
                if self._left(i) < len(self._vector) and not self._vector[i] <= self._vector[self._left(i)]:
                    return False
                if self._right(i) < len(self._vector) and not self._vector[i] <= self._vector[self._right(i)]:
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

    def _min(self, *indices: int) -> int:
        "Out of the provided indices, return which of them has the maximum key"
        smallest = None
        smallest_value = None
        for i in indices:
            if 0 < i < len(self._vector):
                if smallest is None:
                    smallest = i
                    smallest_value = self._vector[i]
                elif (value := self._vector[i]) < smallest_value:
                    smallest = i
                    smallest_value = value

        if smallest is None:
            raise ValueError("All the provided values are outside the vector.")
        return smallest

    def _percolateDown(self, i: int):
        """Percolate down the max-heap condition on index i, supposing that its
        children trees are max-heaps"""
        if i > (len(self._vector) - 1) // 2:  # The right half of the vector is necessarily correct already.
            return
        if self._type == "max":
            new_root = self._max(i, self._left(i), self._right(i))  # Get the max index
        else:
            new_root = self._min(i, self._left(i), self._right(i))  # Get the min index
        if new_root != i:
            self._vector[i], self._vector[new_root] = self._vector[new_root], self._vector[i]  # Swap them
            self._percolateDown(new_root)

    def _percolateUp(self, i: int):
        """
        Percolate up the max-heap condition on index i, supposing that the rest
        of the tree is actually a max-heap
        """
        if i <= 1:  # In the base case, no need to do anything.
            return
        parent = self._parent(i)
        if self._type == "max" and self._max(i, parent) == i:
            self._vector[i], self._vector[parent] = self._vector[parent], self._vector[i]
            self._percolateUp(parent)
        elif self._type == "min" and self._min(i, parent) == i:
            self._vector[i], self._vector[parent] = self._vector[parent], self._vector[i]  # Swap them
            self._percolateUp(parent)

    def insert(self, value: T) -> None:
        "Append a new element to the queue"
        self._vector.append(value)
        self._percolateUp(len(self._vector) - 1)

    def maximum(self) -> T:
        "Returns the element with the highest key"
        if self._type == "min":
            raise ValueError("This is a min-heap")
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self._vector[1]

    def minimum(self) -> T:
        "Returns the element with the lowest key"
        if self._type == "max":
            raise ValueError("This is a max-heap")
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self._vector[1]

    def extractMax(self) -> T:
        "Pops the element with the highest key"
        if self._type == "min":
            raise ValueError("This is a min-heap")
        if self.isEmpty():
            raise IndexError("Queue is empty")
        res = self._vector[1]
        self._vector[1] = self._vector[-1]
        self._vector.pop()
        self._percolateDown(1)
        return res

    def extractMin(self) -> T:
        "Pops the element with the lowest key"
        if self._type == "max":
            raise ValueError("This is a max-heap")
        if self.isEmpty():
            raise IndexError("Queue is empty")
        res = self._vector[1]
        self._vector[1] = self._vector[-1]
        self._vector.pop()
        self._percolateDown(1)
        return res

    @property
    def vector(self):
        return self._vector[1:]


def printStats(vector: list[int]):
    if not vector:
        print("no elements")
        return
    s = 0
    min_ = math.inf
    max_ = -math.inf
    for i in vector:
        s += i
        min_ = min(min_, i)
        max_ = max(max_, i)
    mean = s / len(vector)
    print(f"minimum: {min_}, maximum: {max_}, average: {mean:.4f}")


if __name__ == "__main__":
    heap = Heap(type="min")
    for line in sys.stdin:
        if line.strip() == "":
            break
        instruction, *args = line.strip().split()
        if instruction == "number":
            heap.insert(int(args[0]))
        elif instruction == "delete":
            try:
                heap.extractMin()
            except IndexError:
                pass
        printStats(heap.vector)
