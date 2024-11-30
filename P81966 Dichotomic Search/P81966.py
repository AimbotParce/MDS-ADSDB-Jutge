from typing import Any, TypeVar

T = TypeVar("T", bound=Any)


def position(x: T, v: list[T], left: int = 0, right: int = -1) -> int:
    """
    Search `x` in a sorted sub-vector `v[left:right]` and return its position
    inside said sub-vector. The "real" position of `x` would be `left + i`,
    where `i` is the result of this function. Whenever `x` is not present in the
    sub-vector `v[left:right]`, or `left` and `right` have improper values, `-1`
    will be returned.

    If `x` can be found in more than one position on the list, this function
    will return one of them, which might not be the first appearance.

    Parameters
    ----
    x : T(Any)
        Value to search.
    v : list[T(Any)]
        Vector in which `x` should be searched.
    left : int
        Left limit (included) of the sub-vector in which to search `x`. Must
        satisfy 0 <= left <= len(v).
    right : int
        Right limit (included) of the sub-vector in which to search `x`.
        Must satisfy -1 <= right < len(v).
    """
    if left < 0 or left > len(v) or right < -1 or right >= len(v):
        return -1
    if right == -1:  # For some reason, statement says that right can be -1.
        right = len(v) - 1
    if left > right:
        return -1
    if left == right:
        if v[left] == x:
            return 0
        else:
            return -1
    midpoint = (right - left) // 2
    if x > v[midpoint + left]:
        return position(x=x, v=v, left=left + midpoint + 1, right=right) + midpoint + 1
    else:
        return position(x=x, v=v, left=left, right=left + midpoint)


if __name__ == "__main__":
    example_vector = sorted([5, 12, 6, 7, 2, 4, 7, 21, 67, 2, 51, 34, 5, 1, 345, 17, 3, 524, 17, 35, 42, 51])
    for j, value in enumerate(example_vector):
        pos = position(x=value, v=example_vector)
        print(f"v[{j}] = {value} -> Found v[{pos}] = {example_vector[pos]}")
        assert example_vector[pos] == value, f"Value {value} was not found correctly"
