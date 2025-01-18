import math
import re
import sys
from collections import deque
from typing import *

T = TypeVar("T")


class _HeapNode(Generic[T]):
    __slots__ = "_key", "_value"

    def __init__(self, key: float, value: T) -> None:
        self._key = key
        self._value = value

    def __str__(self) -> str:
        return "{}({})".format(str(self._value), str(self._key))

    def __gt__(self, other: Self):
        if not isinstance(other, _HeapNode):
            raise TypeError("Other must be a Heap Node")
        return self._key > other._key

    def __ge__(self, other: Self):
        if not isinstance(other, _HeapNode):
            raise TypeError("Other must be a Heap Node")
        return self._key >= other._key

    def __lt__(self, other: Self):
        if not isinstance(other, _HeapNode):
            raise TypeError("Other must be a Heap Node")
        return self._key < other._key

    def __le__(self, other: Self):
        if not isinstance(other, _HeapNode):
            raise TypeError("Other must be a Heap Node")
        return self._key <= other._key


class PriorityQueue(Generic[T]):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, initial: Iterable[Tuple[T, float]] = None): ...

    def __init__(self, initial: Iterable[Tuple[T, float]] = None):
        self._vector: List[_HeapNode] = [None]
        for value, priority in initial if initial else []:
            self._vector.append(_HeapNode(priority, value))

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

    def insert(self, priority: float, value: T) -> None:
        "Append a new element to the queue"
        node = _HeapNode(priority, value)
        self._vector.append(node)
        self._percolateUp(len(self._vector) - 1)

    def maximum(self) -> T:
        "Returns the element with the highest priority"
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self._vector[1]._value

    def extractMax(self) -> T:
        "Pops the element with the highest priority"
        if self.isEmpty():
            raise IndexError("Queue is empty")
        res = self._vector[1]._value
        self._vector[1] = self._vector[-1]
        self._vector.pop()
        self._percolateDown(1)
        return res

    def increasePriority(self, i: int, priority: float) -> None:
        "Increase the priority of element in position i"
        if self.isEmpty():
            raise IndexError("Queue is empty")
        if not 0 < i < len(self._vector):
            raise IndexError("Index out of bounds")

        node = self._vector[i]
        if node._key > priority:
            raise ValueError("New priority value cannot be lower than the old one")
        node._key = priority
        self._percolateUp(i)


EntersEvent: TypeAlias = tuple[Literal["ENTERS"], str, float, int]
LeavesEvent: TypeAlias = tuple[Literal["LEAVES"], int]
Event: TypeAlias = Union[EntersEvent, LeavesEvent]


def tokenGenerator(input_buffer: TextIO) -> Generator[str, None, None]:
    for line in input_buffer:
        line = line.strip()
        if not line:
            return
        yield from line.split()


def listenEvents(input_buffer: TextIO) -> Iterable[Event]:
    """
    Given an open file buffer, yield the events on the log, which satisfy the
    following structure:

    ```
    <EVENT> <data1> <data2> ...
    ```

    The possible events are:
    - `ENTERS <name> <priority> <queue_number>`
    - `LEAVES <queue_number>`

    For instance,

    ```
    ENTERS Melissa 42 3
    LEAVES 4
    ```

    Yields
    ------
    The parsed events in the form of tuples, the first element of which is the
    event type, and the rest of which is its data.
    """
    tokens = tokenGenerator(input_buffer)
    for event_type in tokens:  # Read a single element of the text
        if event_type == "ENTERS":
            yield (event_type, next(tokens), float(next(tokens)), int(next(tokens)))
        elif event_type == "LEAVES":
            yield (event_type, int(next(tokens)))


def readHeader(input_buffer: TextIO) -> list[PriorityQueue[str]]:
    """
    Read the initial configuration of the queues. It must follow the structure
    ```
    <num_queues>
    Q1Person1 Q1Person1Priority Q1Person2 Q1Person2Priority ...
    Q2Person1 Q2Person1Priority Q2Person2 Q2Person2Priority ...
    ...
    QNPerson1 ...
    ```

    Returns
    -------
    initial_configuration : list[PriorityQueue[str]]
        The initial configuration of the queues.
    """
    num_queues = int(input_buffer.readline().strip())
    if num_queues is None:
        raise ValueError(f"Could not read num_queues: {num_queues}")
    initial_configuration: list[PriorityQueue[str]] = []
    for _ in range(num_queues):
        line = input_buffer.readline()
        line = line.strip()
        line = re.sub(" +", " ", line)  # This will remove duplicate whitespaces from the line
        if line == "":
            queue_configuration = []
        else:
            queue_configuration = line.split()  # And split the line into tokens
        queue_configuration = map(lambda t: (t[0], float(t[1])), batched(queue_configuration, 2))
        initial_configuration.append(PriorityQueue(queue_configuration))

    # Before continuing, there's an empty line that we need to skip
    input_buffer.readline()

    return initial_configuration


def batched(iterable: Iterable[T], n: int) -> Generator[Tuple[T, ...], None, None]:
    iterable = iter(iterable)

    if n < 1:
        raise ValueError("N cannot be lower than 1")
    for first in iterable:
        yield tuple([first, *(next(iterable) for _ in range(n - 1))])


class QueueManager:
    def __init__(self, initial_configuration: list[PriorityQueue[str]]):
        self.queues = initial_configuration

    def enqueue(self, name: str, priority: int, queue_number: int) -> None:
        if self._checkQueueNumber(queue_number):
            self.queues[queue_number - 1].insert(priority=priority, value=name)

    def dequeue(self, queue_number: int) -> str:
        if self._checkQueueNumber(queue_number) and len(self.queues[queue_number - 1]) > 0:
            return self.queues[queue_number - 1].extractMax()

    def _checkQueueNumber(self, queue_number: int):
        return 0 < queue_number <= len(self.queues)

    def getContents(self) -> list[list[str]]:
        return list(list(q.extractMax() for _ in range(len(q))) for q in self.queues)


def printPreOrder(queue: PriorityQueue, j: int = 1) -> None:
    "Small helper function I did to see properly how the heap was structured."
    if queue.isEmpty() or j >= len(queue._vector):
        return

    depth = int(math.log2(j))

    print(depth * "| " + str(queue._vector[j]))
    printPreOrder(queue, queue._left(j))
    printPreOrder(queue, queue._right(j))


if __name__ == "__main__":
    # input_file = pathlib.Path(__file__).parent / "demo_input.txt"
    # io = input_file.open()
    io = sys.stdin
    queues = readHeader(io)
    manager = QueueManager(queues)
    print("DEPARTS")
    print("-------")
    for event in listenEvents(io):
        if event[0] == "ENTERS":
            manager.enqueue(*event[1:])
        elif event[0] == "LEAVES":
            person = manager.dequeue(*event[1:])
            if person is not None:
                print(person)
        else:
            raise ValueError(f"Unknown event type {event[0]}")

    print("")
    print("FINAL CONTENTS")
    print("--------------")
    for j, queue_content in enumerate(manager.getContents(), start=1):
        if len(queue_content) == 0:
            print(f"queue {j}:")
        else:
            print(f"queue {j}:", " ".join(queue_content))
