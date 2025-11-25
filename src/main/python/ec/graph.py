import sys
from collections import defaultdict
from collections import deque
from collections.abc import Callable
from collections.abc import Iterator
from queue import PriorityQueue
from typing import TypeVar

T = TypeVar("T")


def bfs_path(
    start: T,
    is_end: Callable[[T], bool],
    adjacent: Callable[[T], Iterator[T]],
) -> tuple[int, list[T]]:
    q: deque[tuple[int, T]] = deque()
    q.append((0, start))
    seen: set[T] = set()
    seen.add(start)
    parent: dict[T, T] = {}
    while len(q) != 0:
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
    msg = "unsolvable"
    raise RuntimeError(msg)


def bfs(
    start: T,
    is_end: Callable[[T], bool],
    adjacent: Callable[[T], Iterator[T]],
) -> int:
    return bfs_with_cost(start, is_end, adjacent, lambda _, __: 1)


def bfs_with_cost(
    start: T,
    is_end: Callable[[T], bool],
    adjacent: Callable[[T], Iterator[T]],
    cost: Callable[[T, T], int],
) -> int:
    q: deque[tuple[int, T]] = deque()
    q.append((0, start))
    seen: set[T] = set()
    seen.add(start)
    while len(q) != 0:
        distance, node = q.popleft()
        if is_end(node):
            return distance
        for n in adjacent(node):
            if n in seen:
                continue
            seen.add(n)
            q.append((distance + cost(node, n), n))
    msg = "unsolvable"
    raise RuntimeError(msg)


def bfs_full(
    start: T,
    is_end: Callable[[T], bool],
    adjacent: Callable[[T], Iterator[T]],
) -> dict[T, int]:
    q: deque[tuple[int, T]] = deque()
    q.append((0, start))
    seen: set[T] = set()
    seen.add(start)
    parent: dict[T, T] = {}
    dists = defaultdict[T, int](int)
    while len(q) != 0:
        distance, node = q.popleft()
        if is_end(node):
            dists[node] = distance
        for n in adjacent(node):
            if n in seen:
                continue
            seen.add(n)
            parent[n] = node
            q.append((distance + 1, n))
    return dists


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


def prim(
    start: T, adjacent: Callable[[T], Iterator[tuple[T, int]]]
) -> tuple[int, set[T]]:
    q = PriorityQueue[tuple[int, T]]()
    q.put((0, start))
    seen = set[T]()
    total = 0
    while not q.empty():
        distance, node = q.get()
        if node in seen:
            continue
        total += distance
        seen.add(node)
        for n, d in adjacent(node):
            if n in seen:
                continue
            q.put((d, n))
    return total, seen


def connected_components(
    nodes: set[T], adjacent: Callable[[T], Iterator[T]]
) -> list[set[T]]:
    components = list[set[T]]()
    todo = set(nodes)
    while len(todo) != 0:
        node = todo.pop()
        component = {node}
        q = deque[T]([node])
        while len(q) != 0:
            node = q.popleft()
            for n in adjacent(node):
                if n not in component:
                    q.append(n)
                component.add(n)
        components.append(component)
    return components
