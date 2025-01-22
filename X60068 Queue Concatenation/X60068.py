from typing import Callable, Generic, Iterator, TypeVar, Union

T = TypeVar("T")  # type of the elements in the queue
NT = TypeVar("NT")  # type of the elements in the queue


class Empty(Exception):
    """Error attempting to access an element from an empty container"""

    pass


class LinkedQueue(Generic[T]):
    """FIFO queue implementation using a singly linked list for storage."""

    class _Node(Generic[NT]):
        """Lightweight, nonpublic class for storing a singly linked node."""

        __slots__ = "_element", "_next"  # streamline memory usage

        def __init__(self, element: NT, next: Union["LinkedQueue._Node[NT]", None]) -> None:
            self._element = element
            self._next = next

    def __init__(self) -> None:
        """Create an empty queue."""
        self._head: Union[LinkedQueue._Node[T], None] = None
        self._tail: Union[LinkedQueue._Node[T], None] = None
        self._size: int = 0

    def __iter__(self) -> Iterator[T]:
        """Return an iterator of the elements in the queue."""
        current = self._head
        while current is not None:
            yield current._element
            current = current._next

    def __str__(self):
        """Return a string representation of the queue."""
        return " ".join(str(item) for item in self)

    # ---- Length methods ----

    def __len__(self) -> int:
        """Return the number of elements in the queue."""
        return self._size

    def is_empty(self) -> bool:
        """Return True if the queue is empty."""
        return self._size == 0

    # ---- Peek methods ----

    def first(self) -> T:
        """Return (but do not remove) the element at the front of the queue. Raise Empty exception if the queue is empty."""
        if self.is_empty():
            raise Empty("Queue is empty")
        return self._head._element

    def last(self) -> T:
        """Return (but do not remove) the element at the back of the queue. Raise Empty exception if the queue is empty."""
        if self.is_empty():
            raise Empty("Queue is empty")
        return self._tail._element

    # ---- Update methods ----

    def dequeue(self) -> T:
        """Remove and return the first element of the queue (i.e., FIFO). Raise Empty exception if the queue is empty."""
        if self.is_empty():
            raise Empty("Queue is empty")
        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        if self.is_empty():
            self._tail = None
        return answer

    def enqueue(self, e: T) -> None:
        """Add an element to the back of queue."""
        newest = self._Node(e, None)
        if self.is_empty():
            self._head = newest
        else:
            self._tail._next = newest
        self._tail = newest
        self._size += 1

    def concatenate(self, q: "LinkedQueue[T]") -> None:
        """Concatenate this queue with another queue."""
        if not isinstance(q, LinkedQueue):
            raise ValueError("q must be an instance of LinkedQueue")
        if q.is_empty():
            return
        if self.is_empty():
            self._head = q._head
            self._tail = q._tail
        else:
            self._tail._next = q._head
            self._tail = q._tail
        self._size += q._size
        q._head = None
        q._tail = None
        q._size = 0


if __name__ == "__main__":
    import sys
    from typing import Protocol, TextIO

    class Operation(Protocol):
        def __call__(self, q_pool: list[LinkedQueue[int]], q: int, *args: str) -> None: ...

    # I'll let each operation choose how to parse its arguments.
    # I will only enforce that the first argument is the queue index (int)

    def enqueue(q_pool: list[LinkedQueue[int]], q: int, e: str) -> None:
        q_pool[q].enqueue(int(e))
        print(f"queue {q}: {e} enqueued")

    def dequeue(q_pool: list[LinkedQueue[int]], q: int) -> None:
        e = q_pool[q].dequeue()
        print(f"queue {q}: {e} dequeued")

    def first(q_pool: list[LinkedQueue[int]], q: int) -> None:
        e = q_pool[q].first()
        print(f"queue {q} first element: {e}")

    def last(q_pool: list[LinkedQueue[int]], q: int) -> None:
        e = q_pool[q].last()
        print(f"queue {q} last element: {e}")

    def concatenate(q_pool: list[LinkedQueue[int]], q1: int, q2: str) -> None:
        q_pool[q1].concatenate(q_pool[int(q2)])
        print(f"queues {q1} and {q2} concatenated")
        print(f"queue {q1}: {str(q_pool[q1])}")
        print(f"queue {int(q2)}: {str(q_pool[int(q2)])}")

    def len_(q_pool: list[LinkedQueue[int]], q: int) -> None:
        l = len(q_pool[q])
        print(f"queue {q} has {l} element(s)")

    def is_empty(q_pool: list[LinkedQueue[int]], q: int) -> None:
        empty = q_pool[q].is_empty()
        if empty:
            print(f"queue {q} is empty ")
        else:
            print(f"queue {q} is not empty ")

    def print_(q_pool: list[LinkedQueue[int]], q: int) -> None:
        print(f"queue {q}: {str(q_pool[q])}")

    operations: dict[str, Operation] = {
        "enqueue": enqueue,
        "dequeue": dequeue,
        "first": first,
        "last": last,
        "concatenate": concatenate,
        "len": len_,
        "is_empty": is_empty,
        "print": print_,
    }

    def operationsGenerator(
        available_operations: dict[str, Operation], input_buffer: TextIO
    ) -> Iterator[tuple[Operation, int, tuple[str]]]:
        """
        Generate operations from the input buffer, in the form of (operation, queue, args).
        Queue is an integer referring to the index of the queue in the pool, starting by 1.
        """
        while True:
            command = input_buffer.readline().strip()
            if not command:
                break
            queue, operation, *args = command.split()
            yield available_operations[operation], int(queue), args

    class ListFrom1(list[T]):
        def __getitem__(self, item) -> T:
            return super().__getitem__(item - 1)

    pool_count = int(sys.stdin.readline())
    queue_pool: ListFrom1[LinkedQueue[int]] = ListFrom1(LinkedQueue[int]() for _ in range(pool_count))
    for operation, queue, args in operationsGenerator(available_operations=operations, input_buffer=sys.stdin):
        operation(queue_pool, queue, *args)
