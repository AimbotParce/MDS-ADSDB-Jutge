"This implementation was provided in class. Not my solution."

import heapq

from yogi import scan

if __name__ == "__main__":
    n = scan(int)
    while n is not None:
        m = scan(int)
        grau = [0] * n
        G = [[] for _ in range(n)]
        for i in range(m):
            x = scan(int)
            y = scan(int)
            G[x].append(y)
            grau[y] += 1

        q = []
        for i in range(n):
            if grau[i] == 0:
                q.append(i)
        heapq.heapify(q)  # O(n)
        # min priority queue (to obtain the lexicographically smallest
        # topological order). To compute just a topological order, not
        # necessarily the smallest one, a FIFO queue can be used.

        counter = 0
        while len(q) > 0:
            x = heapq.heappop(q)  # O(log n)
            print(" " if counter > 0 else "", x, sep="", end="")
            counter += 1
            for i in G[x]:
                grau[i] -= 1
                if grau[i] == 0:
                    heapq.heappush(q, i)  # O(log n)
        print()
        if counter != n:
            print("Cycle Found")
        n = scan(int)
