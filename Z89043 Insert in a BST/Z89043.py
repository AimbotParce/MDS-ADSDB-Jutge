import sys
from collections import deque
from typing import Generator, Generic, Optional, Self, TextIO, TypeVar

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


class BST(BTree[T]):
    def __contains__(self, val: T) -> bool:
        "Check if a value is in the tree"
        if self.is_empty:
            return False
        if self.root.val == val:
            return True
        if val < self.root.val:
            return val in self.left
        return val in self.right

    def insert(self, val: T) -> None:
        "Insert a value into the tree"
        if self.is_empty:
            self.root = BTNode(val)
            return
        elif self.root.val == val:
            return
        elif val < self.root.val:
            if self.left.is_empty:
                self.root.left = BTNode(val)
            else:
                self.left.insert(val)
        else:
            if self.right.is_empty:
                self.root.right = BTNode(val)
            else:
                self.right.insert(val)


def yieldTokens(io: TextIO) -> Generator[int, None, None]:
    "Yield integer tokens from a file-like object. Break on empty line."
    for line in io:
        line = line.strip()
        if not line:
            break
        for token in line.split():
            yield int(token)


def printPreOrder(tree: BTree[T]) -> None:
    if tree.is_empty:
        print()
        return

    values = deque[T]()
    stack = deque[BTree[T]]()
    stack.append(tree)

    while stack:
        node = stack.pop()
        values.append(node.val)

        if not node.right.is_empty:
            stack.append(node.right)
        if not node.left.is_empty:
            stack.append(node.left)

    print(" ".join(map(str, values)))


if __name__ == "__main__":
    tree = BST()
    for token in yieldTokens(sys.stdin):
        tree.insert(token)

    print("Pre-order traversal: ", end="")
    printPreOrder(tree)
