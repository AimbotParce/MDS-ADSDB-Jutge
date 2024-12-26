import sys
from collections import deque
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
        return BTree(self.root.left) if self.root is not None else None

    @property
    def right(self) -> "BTree[T]":
        return BTree(self.root.right) if self.root is not None else None

    @property
    def val(self) -> T:
        return self.root.val if self.root is not None else None

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


def _inOrder(tree: BTree[T], curr: deque[str]) -> str:
    "Compute an in-order representation of a tree"
    if tree is None or tree.root is None:
        return

    _inOrder(tree.left, curr)
    curr.append(str(tree.val))
    _inOrder(tree.right, curr)


def inOrder(tree: BTree[T]) -> str:
    "Compute an in-order representation of a tree"
    curr = deque()
    _inOrder(tree, curr)
    return " ".join(curr)


def _postOrder(tree: BTree[T], curr: deque[str]) -> str:
    "Compute a post-order representation of a tree"
    if tree is None or tree.root is None:
        return

    _postOrder(tree.left, curr)
    _postOrder(tree.right, curr)
    curr.append(str(tree.val))


def postOrder(tree: BTree[T]) -> str:
    "Compute a post-order representation of a tree"
    curr = deque()
    _postOrder(tree, curr)
    return " ".join(curr)


if __name__ == "__main__":
    tree = readTreePreOrder(yieldTokens(sys.stdin))
    print("pos:", postOrder(tree))
    print("ino:", inOrder(tree))
