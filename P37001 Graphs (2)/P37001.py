import sys
from collections import deque
from typing import *


def tokenGenerator(input_buffer: TextIO) -> Generator[str, None, None]:
    for line in input_buffer:
        if line.strip() == "":
            continue
        yield from line.strip().split()


def generateNodes(tokens: Iterable[str]) -> List[str]:
    n = int(next(tokens))
    nodes = [next(tokens) for _ in range(n)]
    return nodes


def generateEdges(tokens: Iterable[str]) -> List[Tuple[str, str]]:
    n = int(next(tokens))
    edges = [(next(tokens), next(tokens)) for _ in range(n)]
    return edges


def getAdjacencyList(nodes: List[str], edges: List[Tuple[str, str]]) -> Dict[str, deque[str]]:
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
    tokens = tokenGenerator(sys.stdin)
    nodes = generateNodes(tokens)
    next(sys.stdin)  # Read one empty line because yes
    edges = generateEdges(tokens)
    next(sys.stdin)  # Read one empty line because yes

    adj_list = getAdjacencyList(nodes, edges)
    source, target = next(tokens), next(tokens)
    if searchBFS(adj_list, source, target):
        print("yes")
    else:
        print("no")
