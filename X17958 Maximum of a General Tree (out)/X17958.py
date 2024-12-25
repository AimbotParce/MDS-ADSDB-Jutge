from collections import deque
from typing import Generator, Generic, Iterator, Optional, TypeVar

from yogi import scan

T = TypeVar("T")
NT = TypeVar("NT")


class Tree(Generic[T]):
    # ------------------- nested _Node class ---------------------
    class _Node(Generic[NT]):
        __slots__ = "_element", "_children"

        def __init__(self, element: NT, children: list["Tree._Node[NT]"] = []):
            self._element = element
            self._children = children

    # ------------------- public methods --------------------
    # Constructor
    def __init__(self, *rest) -> None:
        n = len(rest)  # rest is the list of arguments
        if n == 0:  # rest is the empty list
            self._root = None
        elif n == 1:  # rest is a list containing a single node
            self._root = rest[0]
        else:  # rest is a list containing the root element
            # and a possibly empty list of subtrees
            children = []
            for i in range(len(rest[1])):
                children.append(rest[1][i]._root)
            self._root = self._Node(rest[0], children)

    # Checks whether the tree is empty.
    def is_empty(self) -> bool:
        return self._root == None

    # Returns the element stored in the root node
    def root_element(self) -> T:
        return self._root._element

    # Returns the list of subtrees
    def subtrees(self) -> Generator["Tree[T]", None, None]:
        for child in self._root._children:
            yield Tree(child)


# Reads a tree
def readTree() -> Tree[int]:
    element = scan(int)
    if element is None:
        return Tree[int]()
    n = scan(int)
    subtrees = [None] * n
    for i in range(n):
        subtrees[i] = readTree()
    return Tree(element, subtrees)


# Prints a tree in pre-order
def printPreorder(t, depth=0):
    if not t.is_empty():
        print(" " * 2 * depth, end="")
        print(t.root_element())
        for st in t.subtrees():
            printPreorder(st, depth + 1)


def maxim(t: Tree[T]) -> Optional[T]:
    if t.is_empty():
        return None

    current_max = t.root_element()
    trees = deque(t.subtrees())
    while trees:
        current_tree = trees.popleft()
        current_max = max(current_max, current_tree.root_element())
        trees.extend(current_tree.subtrees())
    return current_max


if __name__ == "__main__":
    t = readTree()
    print(maxim(t))
