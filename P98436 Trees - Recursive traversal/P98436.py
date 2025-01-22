import sys
from collections import deque
from typing import Generator, Generic, Iterator, Literal, Optional, TextIO, TypeVar

T = TypeVar("T")


class BTNode(Generic[T]):
    __slots__ = ("val", "left", "right")

    def __init__(self, val: T, left: "BTNode[T]" = None, right: "BTNode[T]" = None):
        self.val = val
        self.left = left
        self.right = right


class BTree(Generic[T]):
    def __init__(self, root: BTNode[T] = None):
        "Create a binary tree from a root node. If root is None, the tree is empty."
        self.root = root

    @property
    def is_empty(self) -> bool:
        return self.root is None

    @property
    def left(self) -> Optional["BTree[T]"]:
        "Return the left subtree of the tree. If the tree is empty, return an empty tree."
        if self.is_empty:
            return BTree(None)
        return BTree(self.root.left)

    @property
    def right(self) -> Optional["BTree[T]"]:
        "Return the right subtree of the tree. If the tree is empty, return an empty tree."
        if self.is_empty:
            return BTree(None)
        return BTree(self.root.right)

    @property
    def val(self) -> T:
        "Return the value of the root node. If the tree is empty, return None."
        if self.is_empty:
            return None
        return self.root.val

    def __repr__(self) -> str:
        return f"BTree({self.root})"

    def __str__(self) -> str:
        return str(self.root)

    def __contains__(self, val: T) -> bool:
        "Check if a value is in the tree"
        if self.is_empty:
            return False
        if self.root.val == val:
            return True
        return val in self.left or val in self.right


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
    if tree.is_empty:
        return

    printInOrder(tree.left, path=path + "l")

    lines = ""
    if path:
        last = path[0]
        for c in path[1:]:
            if c != last:
                lines += " │"
            else:
                lines += "  "
            last = c
        lines += " ┌" if path[-1] == "l" else " └"

    print(lines + ">" + str(tree.val))
    printInOrder(tree.right, path=path + "r")


def yieldTokens(io: TextIO) -> Generator[int, None, None]:
    "Yield integer tokens from a file-like object. Break on empty line."
    for line in io:
        line = line.strip()
        if not line:
            break
        for token in line.split():
            yield int(token)


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
    print(f"pos: {postOrder(tree)}")
    print(f"ino: {inOrder(tree)}")
