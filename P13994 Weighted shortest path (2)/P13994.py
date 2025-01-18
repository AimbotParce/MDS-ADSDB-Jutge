from collections import deque
from typing import *

from yogi import scan

T = TypeVar("T")


class _HeapNode(Generic[T]):
    __slots__ = "_key", "_value"

    def __init__(self, key: float, value: T) -> None:
        self._key = key
        self._value = value

    def __str__(self) -> str:
        return "{}({})".format(str(self._value), str(self._key))

    def __gt__(self, other: Self):
        if not isinstance(other, _HeapNode):
            raise TypeError("Other must be a Heap Node")
        return self._key > other._key

    def __ge__(self, other: Self):
        if not isinstance(other, _HeapNode):
            raise TypeError("Other must be a Heap Node")
        return self._key >= other._key

    def __lt__(self, other: Self):
        if not isinstance(other, _HeapNode):
            raise TypeError("Other must be a Heap Node")
        return self._key < other._key

    def __le__(self, other: Self):
        if not isinstance(other, _HeapNode):
            raise TypeError("Other must be a Heap Node")
        return self._key <= other._key


class PriorityQueue(Generic[T]):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, initial: Iterable[Tuple[T, float]] = None): ...

    def __init__(self, initial: Iterable[Tuple[T, float]] = None):
        self._vector: List[_HeapNode] = [None]
        self._map: dict[T, int] = {}
        for value, priority in initial if initial else []:
            self._map[value] = len(self._vector)
            self._vector.append(_HeapNode(priority, value))

        for i in range((len(self._vector) - 1) // 2, 0, -1):
            self._percolateDown(i)

    def __len__(self):
        return len(self._vector) - 1

    def __str__(self) -> str:
        if self.isEmpty():
            return ""
        queue = deque[Union[int, None]]([1, None])
        levels: list[list[str]] = []
        current_level: list[str] = []
        while queue:
            i = queue.popleft()
            if i == None:
                if not current_level:
                    # We've finished
                    break
                levels.append(current_level)
                queue.append(None)
                current_level = []
                continue
            left = self._left(i)
            right = self._right(i)
            if left < len(self._vector):
                queue.append(left)
            if right < len(self._vector):
                queue.append(right)
            current_level.append(str(self._vector[i]))

        return "<".join(",".join(l) for l in levels)

    def _checkHeapProperty(self):
        "Check that the heap property is correctly maintained."
        for i in range(1, len(self._vector)):
            if self._left(i) < len(self._vector) and not self._vector[i] <= self._vector[self._left(i)]:
                return False
            if self._right(i) < len(self._vector) and not self._vector[i] <= self._vector[self._right(i)]:
                return False
        return True

    def isEmpty(self):
        return len(self) == 0

    @staticmethod
    def _left(i: int):
        return 2 * i

    @staticmethod
    def _right(i: int):
        return 2 * i + 1

    @staticmethod
    def _parent(i: int):
        return i // 2

    def _min(self, *indices: int) -> int:
        "Out of the provided indices, return which of them has the maximum key"
        smallest = None
        smallest_value = None
        for i in indices:
            if 0 < i < len(self._vector):
                if smallest is None:
                    smallest = i
                    smallest_value = self._vector[i]
                elif (value := self._vector[i]) < smallest_value:
                    smallest = i
                    smallest_value = value

        if smallest is None:
            raise ValueError("All the provided values are outside the vector.")
        return smallest

    def _percolateDown(self, i: int):
        """Percolate down the min-heap condition on index i, supposing that its
        children trees are min-heaps"""
        if i > (len(self._vector) - 1) // 2:  # The right half of the vector is necessarily correct already.
            return
        smallest = self._min(i, self._left(i), self._right(i))  # Get the max index
        if smallest != i:
            self._map[self._vector[i]._value] = smallest
            self._map[self._vector[smallest]._value] = i
            self._vector[i], self._vector[smallest] = self._vector[smallest], self._vector[i]  # Swap them
            self._percolateDown(smallest)

    def _percolateUp(self, i: int):
        """
        Percolate up the min-heap condition on index i, supposing that the rest
        of the tree is actually a min-heap
        """
        if i <= 1:  # In the base case, no need to do anything.
            return
        parent = self._parent(i)
        if self._min(i, parent) == i:
            self._map[self._vector[i]._value] = parent
            self._map[self._vector[parent]._value] = i
            self._vector[i], self._vector[parent] = self._vector[parent], self._vector[i]  # Swap them
            self._percolateUp(parent)

    def insert(self, priority: float, value: T) -> None:
        "Append a new element to the queue"
        node = _HeapNode(priority, value)
        self._map[value] = len(self._vector)
        self._vector.append(node)
        self._percolateUp(len(self._vector) - 1)

    def peek(self) -> T:
        "Returns the element with the highest priority"
        if self.isEmpty():
            raise IndexError("Queue is empty")
        return self._vector[1]._value

    def pop(self) -> T:
        "Pops the element with the lowest priority value"
        if self.isEmpty():
            raise IndexError("Queue is empty")
        res = self._vector[1]._value
        del self._map[res]
        self._map[self._vector[-1]._value] = 1
        self._vector[1] = self._vector[-1]
        self._vector.pop()
        self._percolateDown(1)
        return res

    def _update(self, i: int, priority: float) -> None:
        "Increase the priority of element in position i"
        if self.isEmpty():
            raise IndexError("Queue is empty")
        if not 0 < i < len(self._vector):
            raise IndexError("Index out of bounds")

        node = self._vector[i]
        if node._key > priority:
            # We're decreasing the priority, we must percolate up
            node._key = priority
            self._percolateUp(i)
        elif node._key < priority:
            # We're increasing the priority, this is not supported yet
            raise NotImplementedError

    def update(self, value: T, priority: float):
        if not value in self._map:
            raise ValueError("Value not found in map")
        self._update(self._map[value], priority=priority)


def dijkstra(adjacency_list: dict[int, deque[tuple[int, float]]], start: int, end: int) -> tuple[list[int], float]:
    queue: list[tuple[int, float]] = [None] * len(adjacency_list)
    distance: dict[int, float] = {}
    parenthood: dict[int, int] = {}
    for node in adjacency_list:
        if node != start:
            distance[node] = float("inf")
            queue[node] = (node, float("inf"))
        else:
            distance[node] = 0
            queue[node] = (node, 0)
        parenthood[node] = None
    priority = PriorityQueue(queue)

    visited = set[int]()
    while end not in visited:
        current_node = priority.pop()
        current_distance = distance[current_node]
        visited.add(current_node)
        if current_distance == float("inf"):
            # Break early
            break
        for other, edge_weight in adjacency_list[current_node]:
            if current_distance + edge_weight < distance[other]:
                priority.update(other, current_distance + edge_weight)
                distance[other] = current_distance + edge_weight
                parenthood[other] = current_node

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parenthood[current]

    return list(reversed(path)), distance[end]


def readCase(num_vertices: int, num_edges: int):
    adjacency_list = {i: deque[int]() for i in range(num_vertices)}
    for _ in range(num_edges):
        edge_from, edge_to, edge_weight = scan(int), scan(int), scan(int)
        adjacency_list[edge_from].append((edge_to, edge_weight))
    node_from, node_to = scan(int), scan(int)
    return adjacency_list, node_from, node_to


if __name__ == "__main__":
    while (num_vertices := scan(int)) is not None:
        num_edges = scan(int)
        adjacency_list, start, end = readCase(num_vertices, num_edges)
        path, dist = dijkstra(adjacency_list, start, end)
        if dist == float("inf"):
            print(f"no path from {start} to {end}")
        else:
            p = " ".join(str(e) for e in path)
            print(p)
