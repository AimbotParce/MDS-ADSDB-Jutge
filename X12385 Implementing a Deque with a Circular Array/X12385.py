import sys
from typing import Any, Callable, Generic, Iterable, ParamSpec, Protocol, TypeVar, Union

from yogi import scan


class Empty(Exception):
    """Error attempting to access an element from an empty container"""

    pass


T = TypeVar("T")  # type of elements stored in a Deque
P = ParamSpec("P")
R = TypeVar("R")


def _resize_check(previous, current):
    if previous != current:
        print(f"resized from {previous} to {current}")


def check_resize(method: Callable[P, R]) -> Callable[P, R]:  # pyright: ignore
    def wrapper(self: "ArrayDeque", *args: P.args, **kwargs: P.kwargs) -> R:
        previous = sys.getsizeof(self._data)
        res = method(self, *args, **kwargs)
        current = sys.getsizeof(self._data)
        _resize_check(previous, current)
        return res

    return wrapper


class ArrayDeque(Generic[T]):
    "Deque implementation using a Python list as underlying storage."

    DEFAULT_CAPACITY = 10  # moderate capacity for all new queues

    def __init__(self, data: Iterable[T] = None) -> None:
        """Create an empty queue."""
        self._data: list[T] = [None] * self.DEFAULT_CAPACITY
        self._size: int = 0
        self._front: int = 0
        if data is not None:
            for d in data:
                self.add_last(d)

    def _resize(self, cap):  # we assume cap >= len(self)
        """Resize to a new list of capacity >= len(self)."""
        old = self._data  # keep track of existing list
        self._data = [None] * cap  # allocate list with new capacity
        walk = self._front
        for k in range(self._size):  # only consider existing elements
            self._data[k] = old[walk]  # intentionally shift indices
            walk = (1 + walk) % len(old)  # use old size as modulus
        self._front = 0  # front has been realigned

    # ---- Length methods ----

    def __len__(self) -> int:
        "Return the number of elements in the queue."
        return self._size

    def is_empty(self) -> bool:
        "Return True if the queue is empty."
        return self._size == 0

    # ---- Peek methods ----

    def first(self) -> T:
        """
        Return (but do not remove) the element at the front of the queue.
        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty("Queue is empty")
        return self._data[self._front]

    def last(self) -> T:
        """
        Return (but do not remove) the element at the front of the queue.
        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty("Queue is empty")
        return self._data[(self._front + self._size - 1) % len(self._data)]

    # ---- Update methods ----

    @check_resize
    def delete_first(self):
        """
        Remove and return the first element of the queue.
        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty("Queue is empty")
        answer = self._data[self._front]
        self._data[self._front] = None  # help garbage collection
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        if 0 < self._size < len(self._data) // 4:
            self._resize(len(self._data) // 2)
        return answer

    @check_resize
    def delete_last(self):
        """
        Remove and return the last element of the queue.
        Raise Empty exception if the queue is empty.
        """
        if self.is_empty():
            raise Empty("Queue is empty")
        last = (self._front + self._size - 1) % len(self._data)
        answer = self._data[last]
        self._data[last] = None
        self._size -= 1
        if 0 < self._size < len(self._data) // 4:
            self._resize(len(self._data) // 2)
        return answer

    @check_resize
    def add_last(self, e):
        """Add an element to the back of queue."""
        if self._size == len(self._data):
            self._resize(2 * len(self._data))  # double the array size
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1

    @check_resize
    def add_first(self, e):
        """Add an element to the front of queue."""
        if self._size == len(self._data):
            self._resize(2 * len(self._data))  # double the array size
        self._front = (self._front - 1) % len(self._data)
        self._data[self._front] = e
        self._size += 1


if __name__ == "__main__":
    n = scan(int)
    while n is not None:
        s = ArrayDeque()

        print(f"len {len(s)}")
        if s.is_empty():
            print("deque empty")

        for i in range(n // 2):
            s.add_first(i)
            print(f"{i} added to the front")

        for i in range(n // 2, n):
            s.add_last(i)

            print(f"{i} added to the back")

        print(f"len {len(s)}")
        try:
            print(f"first {s.first()}")
        except:
            print("first error: deque empty")

        try:
            print(f"last {s.last()}")
        except:
            print("last error: deque empty")

        for _ in range(n // 2):

            try:
                e = s.delete_last()
                print(f"{e} deleted from the back")
            except Empty:
                print("delete last error: deque empty")

        print(f"len {len(s)}")
        try:
            print(f"first {s.first()}")
        except:
            print("first error: deque empty")

        try:
            print(f"last {s.last()}")
        except:
            print("last error: deque empty")

        for _ in range(n // 2 + 1):
            try:
                e = s.delete_first()

                print(f"{e} deleted from the front")
            except Empty:
                print("delete first error: deque empty")

        try:
            e = s.delete_last()
            print(f"{e} deleted from the back")
        except Empty:
            print("delete last error: deque empty")

        print(f"len {len(s)}")
        try:
            print(f"first {s.first()}")
        except Empty:
            print("first error: deque empty")

        try:
            print(f"last {s.last()}")
        except:
            print("last error: deque empty")

        print()

        n = scan(int)
