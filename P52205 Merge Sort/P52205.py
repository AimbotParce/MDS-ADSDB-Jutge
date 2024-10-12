from collections import deque
from typing import Any


def mergesort(v: list[Any], left: int = 0, right: int = -1) -> None:
    """
    Sort vector `v` "in place" using the Merge Sort algorithm.

    Parameters
    ----
    v : list[Any]
        Vector to sort. All of its elements must support comparison.
    left : int
        Left limit (included) of the sub-vector to sort. Must satisfy
        0 <= left <= len(v).
    right : int
        Right limit (included) of the sub-vector to sort. Must satisfy
        -1 <= right < len(v).
    """

    if left < 0 or left > len(v) or right < -1 or right >= len(v):
        raise ValueError("0 <= left <= len(v) and -1 <= right < len(v)")
    if right == -1:
        right = len(v) - 1
    if left > right:
        return ValueError("left must be lower than right unless right is -1")

    if left < right:
        midpoint = (left + right) // 2
        mergesort(v=v, left=left, right=midpoint)
        mergesort(v=v, left=midpoint + 1, right=right)
        merge(v=v, left=left, mid=midpoint, right=right)

    # If left == right, it means we've finished.


def merge(v: list[Any], left: int, mid: int, right: int):
    """
    Perform an in-place merge of the two sub-vectors `v[left:mid]` and
    `v[mid:right]`.

    Parameters
    ----
    v : list[Any]
        Vector from which the sub-vectors to merge are. All of its elements must
        support comparison.
    left : int
        Left limit (included) of the first sub-vector to merge.
    mid : int
        Right limit (included) of the first sub-vector to merge. It also is the
        left limit (not included) of the second sub-vector to merge.
    right : int
        Right limit (included) of the second sub-vector to merge.

    These variables must satisfy 0 <= left <= mid < right < len(v)
    """
    if not 0 <= left <= mid < right < len(v):
        raise ValueError("Parameters must satisfy 0 <= left <= mid < right < len(v)")

    # We'll simplify our lives by using two "reading" queues and one "writing"
    # pointer. Start by populating the left and right queues
    left_q = deque(v[left : mid + 1])
    right_q = deque(v[mid + 1 : right + 1])

    writing = left
    while len(left_q) > 0 and len(right_q) > 0:
        if left_q[0] < right_q[0]:
            v[writing] = left_q.popleft()
        else:
            v[writing] = right_q.popleft()
        writing += 1  # By definition, it's impossible that this overflows the
        # section we are merging (left <= writing <= right always).

    for i in range(writing, writing + len(left_q)):
        # We've finished the right queue, the left out elements of the left one
        # must be greater than everything already in the merged vector. If
        # nothing is left in the left queue, then the code will never reach this.
        v[i] = left_q.popleft()

    for i in range(writing, writing + len(right_q)):
        # Same with the right queue. Both blocks of code cannot be executed,
        # because we don't break the while loop until at least one of them is
        # completely empty.
        v[i] = right_q.popleft()


if __name__ == "__main__":
    example_vector = [5, 12, 6, 7, 2, 4, 7, 21, 67, 2, 51, 34, 5, 1, 0, 1, 345, 17, 3, 524, 17, 35, 42, 51]
    sorted_vector = sorted(example_vector)
    mergesort(example_vector)
    assert example_vector == sorted_vector, "Vector wasn't sorted correctly"
