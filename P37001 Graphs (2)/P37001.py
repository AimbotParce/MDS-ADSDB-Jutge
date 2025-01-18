import sys
from collections import deque
from typing import *

from yogi import scan


def generateNodes() -> List[str]:
    n = scan(int)
    nodes = [scan(str) for _ in range(n)]
    return nodes


def generateEdges() -> Generator[Tuple[str, str], None, None]:
    n = scan(int)
    yield from list((scan(str), scan(str)) for _ in range(n))


def getAdjacencyList(nodes: Iterable[str], edges: Iterable[Tuple[str, str]]) -> Dict[str, deque[str]]:
    adj_list = {node: deque[str]() for node in nodes}
    for u, v in edges:
        adj_list[u].append(v)
    return adj_list


def searchBFS(adj_list: Dict[str, deque[str]], start: str, target: str) -> List[str]:
    visited = set[str]()
    queue = deque[str]([start])
    while queue:
        node = queue.popleft()
        if node == target:
            return True
        visited.add(node)
        for other in adj_list[node]:
            if other not in visited:
                queue.append(other)

    return False


if __name__ == "__main__":
    nodes = generateNodes()
    edges = generateEdges()

    adj_list = getAdjacencyList(nodes, edges)
    source, target = scan(int), scan(int)
    if searchBFS(adj_list, source, target):
        print("yes")
    else:
        print("no")
