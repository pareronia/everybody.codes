from collections import deque
from collections.abc import Iterator
from typing import Callable
from typing import TypeVar

T = TypeVar("T")


def bfs(
    start: T,
    is_end: Callable[[T], bool],
    adjacent: Callable[[T], Iterator[T]],
) -> tuple[int, list[T]]:
    q: deque[tuple[int, T]] = deque()
    q.append((0, start))
    seen: set[T] = set()
    seen.add(start)
    parent: dict[T, T] = {}
    while not len(q) == 0:
        distance, node = q.popleft()
        if is_end(node):
            path = [node]
            curr = node
            while curr in parent:
                curr = parent[curr]
                path.append(curr)
            return distance, path
        for n in adjacent(node):
            if n in seen:
                continue
            seen.add(n)
            parent[n] = node
            q.append((distance + 1, n))
    raise RuntimeError("unsolvable")
