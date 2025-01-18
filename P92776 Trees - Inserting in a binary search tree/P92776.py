import sys
from typing import Generator, Generic, Iterator, Literal, Optional, Self, TextIO, TypeVar

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


def printPreOrder(tree: BTree) -> None:
    if tree.is_empty:
        return
    print(tree.val)
    printPreOrder(tree.left)
    printPreOrder(tree.right)


if __name__ == "__main__":
    tree = BST[int]()
    for val in yieldTokens(sys.stdin):
        tree.insert(val)

    printPreOrder(tree)
