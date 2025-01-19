import heapq

from yogi import scan

if __name__ == "__main__":
    heap: list[int] = []
    current_max: int = -float("inf")
    current_sum: int = 0
    while (instruction := scan(str)) is not None:
        if instruction == "number":
            new_number = scan(int)
            current_max = max(current_max, new_number)
            current_sum += new_number
            heapq.heappush(heap, new_number)
        elif instruction == "delete":
            if len(heap) > 0:
                elem = heapq.heappop(heap)
                current_sum -= elem
                if len(heap) == 0:
                    current_max = -float("inf")  # reset the current max
        if not heap:
            print("no elements")
        else:
            print(f"minimum: {heap[0]}, maximum: {current_max}, average: {current_sum/len(heap):.4f}")
