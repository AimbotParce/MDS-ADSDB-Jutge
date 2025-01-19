import sys
from typing import Generator, Generic, Iterator, Literal, Optional, Self, TextIO, TypeVar

from yogi import scan

T = TypeVar("T")


class BTNode(Generic[T]):
    __slots__ = ("val", "left", "right")

    def __init__(self, val: T, left: "BTNode[T]" = None, right: "BTNode[T]" = None):
        self.val = val
        self.left = left
        self.right = right


class BST(Generic[T]):
    def __init__(self, root: BTNode[T] = None):
        "Create a binary tree from a root node. If root is None, the tree is empty."
        self.root = root

    @property
    def is_empty(self) -> bool:
        return self.root is None

    @property
    def left(self) -> Optional[Self]:
        "Return the left subtree of the tree. If the tree is empty, return an empty tree."
        if self.is_empty:
            return self.__class__(None)
        return self.__class__(self.root.left)

    @property
    def right(self) -> Optional[Self]:
        "Return the right subtree of the tree. If the tree is empty, return an empty tree."
        if self.is_empty:
            return self.__class__(None)
        return self.__class__(self.root.right)

    @property
    def val(self) -> T:
        "Return the value of the root node. If the tree is empty, return None."
        if self.is_empty:
            return None
        return self.root.val

    def _search(self, node: BTNode, value: T) -> bool:
        if node is None:
            return False
        elif value == node.val:
            return True
        elif value < node.val:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

    def __contains__(self, val: T) -> bool:
        "Check if a value is in the tree"
        return self._search(self.root, val)


def _readNodesPreOrder(tokens: Iterator[T]) -> BTNode[T]:
    "Read a binary tree from pre-order traversal"
    val = next(tokens)
    if val == -1 or val is None:
        return None
    return BTNode(val, _readNodesPreOrder(tokens), _readNodesPreOrder(tokens))


def readTreePreOrder(tokens: Iterator[T]) -> BST[T]:
    "Read a binary tree from pre-order traversal"
    return BST(_readNodesPreOrder(tokens))


def yieldTokens(io: TextIO) -> Generator[int, None, None]:
    "Yield integer tokens from a file-like object. Break on empty line."
    for line in io:
        line = line.strip()
        if not line:
            return
        yield from map(int, line.split())


if __name__ == "__main__":
    n = scan(int)  # The number of elements, ignored as per the statement
    tree = readTreePreOrder(yieldTokens(sys.stdin))

    while (val := scan(int)) is not None:
        if val in tree:
            print(val, 1)
        else:
            print(val, 0)
