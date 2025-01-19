import heapq

from yogi import scan


def printStats(min_heap: list[int]):
    if not min_heap:
        print("no elements")
        return
    min_ = min_heap[0]
    max_ = max(min_heap)
    mean_ = sum(heap) / len(heap)
    print(f"minimum: {min_}, maximum: {max_}, average: {mean_:.4f}")


if __name__ == "__main__":
    heap: list[int] = []
    while (instruction := scan(str)) is not None:
        if instruction == "number":
            heapq.heappush(heap, scan(int))
        elif instruction == "delete":
            if len(heap) > 0:
                heapq.heappop(heap)
        printStats(heap)
