from collections.abc import Callable


def binary_search(
    predicate: Callable[[int], bool],
    min_index: int = 0,
    max_index: int | None = None,
) -> int:
    """Search the maximum index such that the predicate is True."""
    # Set Left
    left = min_index
    if not predicate(left):
        raise AssertionError

    # Set Right
    if max_index is not None:
        right = max_index
        if predicate(right):
            raise AssertionError
    else:
        diff = 1
        right = left + diff
        while predicate(right):
            left = right
            diff *= 2
            right = left + diff

    # Bisect
    while (diff := (right - left)) > 1:
        mid = left + diff // 2
        if predicate(mid):
            left = mid
        else:
            right = mid

    return left
