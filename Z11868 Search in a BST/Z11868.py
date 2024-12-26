import sys
from typing import Generator, Generic, Iterator, Literal, TextIO, TypeVar

T = TypeVar("T")


class BTNode(Generic[T]):
    __slots__ = ("val", "left", "right")

    def __init__(self, val: T, left: "BTNode[T]" = None, right: "BTNode[T]" = None):
        self.val = val
        self.left = left
        self.right = right


class BTree(Generic[T]):
    def __init__(self, root: BTNode[T] = None):
        self.root = root

    @property
    def left(self) -> "BTree[T]":
        return BTree(self.root.left)

    @property
    def right(self) -> "BTree[T]":
        return BTree(self.root.right)

    @property
    def val(self) -> T:
        return self.root.val

    def __repr__(self) -> str:
        return f"BTree({self.root})"

    def __str__(self) -> str:
        return str(self.root)

    def __contains__(self, val: T) -> bool:
        if self.root is None:
            return False
        if self.root.val == val:
            return True
        if val < self.root.val:
            return val in self.left
        return val in self.right


def yieldTokens(io: TextIO) -> Generator[int, None, None]:
    "Yield integer tokens from a file-like object. Break on empty line."
    for line in io:
        line = line.strip()
        if not line:
            break
        for token in line.split():
            yield int(token)


def _readNodesPreOrder(tokens: Iterator[T]) -> BTNode[T]:
    "Read a binary tree from pre-order traversal"
    val = next(tokens)
    if val == -1 or val is None:
        return None
    return BTNode(val, _readNodesPreOrder(tokens), _readNodesPreOrder(tokens))


def readTreePreOrder(tokens: Iterator[T]) -> BTree[T]:
    "Read a binary tree from pre-order traversal"
    return BTree(_readNodesPreOrder(tokens))


def printInOrder(tree: BTree[T], path: str = "") -> None:
    "Print in-order traversal of a binary tree"
    if tree is None:
        return

    printInOrder(tree.left, path=path + "l")

    lines = ""
    if path:
        last = path[0]
        for c in path[1:]:
            if c != last:
                lines += " |"
            else:
                lines += "  "
            last = c
        lines += " ┌" if path[-1] == "l" else " └"

    print(lines + ">" + str(tree.val))
    printInOrder(tree.right, path=path + "r")


if __name__ == "__main__":
    tree = readTreePreOrder(yieldTokens(sys.stdin))
    # Read an empty line because yes....
    next(sys.stdin)

    for val in yieldTokens(sys.stdin):
        if val in tree:
            print(val, 1)
        else:
            print(val, 0)
