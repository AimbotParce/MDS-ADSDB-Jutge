import sys
from typing import Any, Callable, ParamSpec, Protocol, TypeVar

from yogi import scan

T = TypeVar("T", bound=Any)

P = ParamSpec("P")
R = TypeVar("R")


class Empty(Exception):
    """Error attempting to access an element from an empty container"""

    pass


class Full(Exception):
    """Error attempting to add an element to a full container"""

    pass


class Stack(Protocol[T]):
    _data: list[T]

    def __init__(self, maxlen: int = 0) -> None: ...
    def __len__(self) -> int: ...
    def is_empty(self) -> bool: ...

    def push(self, e: T) -> None: ...
    def top(self) -> T: ...
    def pop(self) -> T: ...

    @staticmethod
    def _resize_check(previous, current):
        if previous != current:
            print(f"resized from {previous} to {current}")

    @staticmethod
    def check_resize(method: Callable[P, R]) -> Callable[P, R]:  # pyright: ignore
        def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> R:
            previous = sys.getsizeof(self._data)
            res = method(self, *args, **kwargs)
            current = sys.getsizeof(self._data)
            Stack._resize_check(previous, current)
            return res

        return wrapper


class DynamicArrayStack(Stack):
    """LIFO Stack implementation using a Python list as underlying storage."""

    def __init__(self):
        """
        Create an empty stack without a maximum.
        """
        self._data = []

    def __len__(self):
        """Return the number of elements in the stack."""
        return len(self._data)

    def is_empty(self):
        """Return True if the stack is empty."""
        return len(self._data) == 0

    @Stack.check_resize
    def push(self, e):
        """Add element e to the top of the stack."""
        self._data.append(e)

    def top(self):
        """Return (but do not remove) the element at the top of the stack.

        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data[-1]

    @Stack.check_resize
    def pop(self):
        """Remove and return the element from the top of the stack (i.e., LIFO).

        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty("Stack is empty")
        else:
            val = self._data.pop()
        return val


class FixedArrayStack(Stack):

    def __init__(self, maxlen: int):
        """
        Create an empty stack with a fixed maximum capacity.
        """
        if maxlen < 0:
            raise ValueError("maxlen must be positive")
        self._data = [None] * maxlen
        self._maxlen = maxlen
        self._index = 0

    def __len__(self):
        """Return the number of elements in the stack."""
        return self._index

    def is_empty(self):
        """Return True if the stack is empty."""
        return len(self) == 0

    @Stack.check_resize
    def push(self, e):
        """Add element e to the top of the stack."""
        if len(self) == self._maxlen:
            raise Full("Maxlen was already reached")
        self._data[self._index] = e
        self._index += 1

    def top(self):
        """Return (but do not remove) the element at the top of the stack.

        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data[self._index - 1]

    @Stack.check_resize
    def pop(self):
        """Remove and return the element from the top of the stack (i.e., LIFO).

        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty("Stack is empty")
        else:
            self._index -= 1
            val = self._data[self._index]  # No need to remove the element, it will
            # be overridden on the next push operation.
        return val


def ArrayStack(maxlen: int = 0) -> Stack:
    """
    Create a stack using python lists. If maxlen is >= 0, a fixed memory will be
    allocated for the stack. Otherwise, a dynamic list will be used.
    """
    if maxlen >= 0:
        return FixedArrayStack(maxlen=maxlen)
    else:
        return DynamicArrayStack()


if __name__ == "__main__":
    n = scan(int)
    while n is not None:
        # s = ArrayStack()  # COMMENT THIS LINE IN YOUR ANSWER, AND UNCOMMENT NEXT LINE
        s = ArrayStack(n)
        # DO NOT MODIFY ANY OTHER PART OF THE PART OF THE __main__ FUNCTION
        print(f"len {len(s)}")
        if s.is_empty():
            print("stack empty")

        # pushing elements
        for i in range(n + 1):
            try:
                s.push(i)
                print(f"{i} pushed")
            except Full:
                print("push error: stack full")

        # using accessors
        print(f"len {len(s)}")
        try:
            print(f"top {s.top()}")
        except:
            print("top error: stack empty")

        # popping elements
        for _ in range(n // 4):
            try:
                e = s.pop()
                print(f"{e} popped")
            except Empty:
                print("pop error: stack empty")

        # using accessors
        print(f"len {len(s)}")
        try:
            print(f"top {s.top()}")
        except:
            print("top error: stack empty")

        # popping elements
        for _ in range(2 + 3 * (n // 4)):
            try:
                e = s.pop()
                print(f"{e} popped")
            except Empty:
                print("pop error: stack empty")

        print(f"len {len(s)}")
        try:
            print(f"top {s.top()}")
        except Empty:
            print("top error: stack empty")

        print()

        n = scan(int)
