import sys
from collections import defaultdict
from collections import deque
from collections.abc import Iterator
from queue import PriorityQueue
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


def dijkstra(
    start: T,
    is_end: Callable[[T], bool],
    adjacent: Callable[[T], Iterator[T]],
    get_cost: Callable[[T, T], int],
) -> tuple[int, dict[T, int], list[T]]:
    q: PriorityQueue[tuple[int, T]] = PriorityQueue()
    q.put((0, start))
    best: defaultdict[T, int] = defaultdict(lambda: sys.maxsize)
    best[start] = 0
    parent: dict[T, T] = {}
    path = []
    while not q.empty():
        cost, node = q.get()
        if is_end(node):
            path = [node]
            curr = node
            while curr in parent:
                curr = parent[curr]
                path.append(curr)
            break
        best_cost = best[node]
        for n in adjacent(node):
            new_cost = best_cost + get_cost(node, n)
            if new_cost < best[n]:
                best[n] = new_cost
                parent[n] = node
                q.put((new_cost, n))
    return cost, best, path
