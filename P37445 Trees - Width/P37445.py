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
        for token in line.split():
            yield int(token)


def width(tree: BTree[T]) -> int:
    "Return the width of a binary tree"

    levels = deque[BTree | None]([tree, None])  # None marks the end of a level
    max_width = 0
    current_width = 0
    while levels:
        node = levels.popleft()
        if node is None:
            max_width = max(max_width, current_width)
            current_width = 0
            if levels:
                levels.append(None)
        elif not node.is_empty:
            current_width += 1
            levels.append(node.left)
            levels.append(node.right)

    return max_width


if __name__ == "__main__":
    generator = yieldTokens(sys.stdin)
    n_trees = next(generator)

    for _ in range(n_trees):
        tree = readTreePreOrder(yieldTokens(sys.stdin))
        # printInOrder(tree)
        print(width(tree))
