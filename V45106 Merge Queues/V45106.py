from typing import Generic, Iterator, TypeVar, Union

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

    def merge(self, other: "LinkedQueue[T]") -> None:
        """Merge queues 'self' and 'other' as follows. If 'self' is e_1, e_2, ..., e_n
        and 'other' is o_1, o_2, ..., o_m, after executing self.merge(other) the
        queue 'self' contains the sequence e_1,o_1,e_2,o_2,...e_n,o_n,o_n+1,...,o_m if
        n <= m, and the sequence e_1,o_1,e_2,o_2,...e_m,o_m,e_m+1,...,e_n if
        n > m, and in both cases the queue other is empty.
        """
        if self.is_empty():
            self._head = other._head
            self._tail = other._tail
            self._size = other._size
        else:
            other_size = other._size  # Save the size of other to update the size of self later
            current = self._head  # Current will always be the last element "added" of this queue
            for _ in range(min(self._size - 1, other._size)):
                temp = current._next  # Next element to add from self
                current._next = other._head  # Add the first element of other
                other._head = other._head._next  # Update other
                other._size -= 1  # Update other size
                current._next._next = temp  # Add the next element of self
                current = temp  # Update current
            if other._size > 0:
                # If there are elements left in other, add them to the end of self
                current._next = other._head
                self._tail = other._tail
            # If there are elements left in self, we don't need to do anything
            self._size += other_size  # Update the size of self
        other._size = 0
        other._head = None
        other._tail = None


if __name__ == "__main__":
    import sys

    v: list[LinkedQueue[int]] = []
    for line in sys.stdin:
        line = line.strip()
        # if not line:
        #     break
        v.append(LinkedQueue())
        for e in line.split():
            v[-1].enqueue(int(e))

    print(f"v[0]: {v[0]}")
    print(f"v[1]: {v[1]}")
    v[0].merge(v[1])
    print("After calling v[0].merge(v[1])")
    print(f"v[0]: {v[0]}")
    print(f"v[1]: {v[1]}")
