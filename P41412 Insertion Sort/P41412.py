from typing import Any

# def stringify(v: list[Any], query: int, head: int):
#     ln1 = []
#     ln2 = []
#     for j, val in enumerate(v):
#         vstr = str(val)
#         l = len(vstr)
#         ln1.append(vstr)
#         if j == query:
#             ln2.append(l * "~")
#         elif j == head:
#             ln2.append(l * "^")
#         else:
#             ln2.append(l * " ")
#     return "[" + ", ".join(ln1) + "]\n " + "  ".join(ln2) + " "


def insertion_sort(v: list[Any]) -> None:
    """
    Sort vector `v` in place using the Insertion Sort algorithm.
    """
    for i in range(1, len(v)):
        # No need to sort the first one, as it is already sorted.
        key = v[i]
        j = i - 1
        # print(stringify(v, i, j), "\n")
        while j >= 0 and key < v[j]:
            v[j + 1] = v[j]
            j -= 1
            # print(stringify(v, i, j), "\n")
        v[j + 1] = key


if __name__ == "__main__":
    example_vector = [5, 12, 6, 7, 2, 4, 7, 21, 67, 2, 51, 34, 5, 1, 0, 1, 345, 17, 3, 524, 17, 35, 42, 51]
    sorted_vector = sorted(example_vector)
    insertion_sort(example_vector)
    assert example_vector == sorted_vector, "Vector wasn't sorted correctly"
