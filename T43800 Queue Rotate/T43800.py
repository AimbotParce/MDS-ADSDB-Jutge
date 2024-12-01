from typing import Generic, Iterator, TypeVar, Union

from yogi import scan

T = TypeVar("T")  # type of the elements in the queue
NT = TypeVar("NT")  # type of the elements in the queue


class Empty(Exception):
    """Error attempting to access an element from an empty container"""

    pass


class LinkedQueue(Generic[T]):
    """FIFO queue implementation using a singly linked list for storage."""

    # -------------------------- nested _Node class -------------
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

    def rotate(self) -> T:
        """Move element at the front to the back of the queue and return it
        Raise Empty exception if the queue is empty .
        """
        if self.is_empty():
            raise Empty("Queue is empty")
        self._tail._next = self._head
        self._tail = self._head
        self._head = self._head._next
        self._tail._next = None
        return self._tail._element


if __name__ == "__main__":
    q = LinkedQueue[int]()
    e = scan(int)
    while e is not None:
        q.enqueue(e)
        e = scan(int)
    print(q)
    print(f"rotate returns: {q.rotate()}")
    print(q)
