#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 19
#

import sys
from collections import defaultdict
from collections.abc import Iterator
from functools import cache
from math import ceil

from ec.common import Direction
from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.graph import dijkstra

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
7,7,2
12,0,4
15,5,3
24,1,6
28,5,5
40,8,2
"""
TEST2 = """\
7,7,2
7,1,3
12,0,4
15,5,3
24,1,6
28,5,5
40,3,3
40,8,2
"""

Position = tuple[int, int]


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input_data: InputData) -> Output1:
        def adjacent(pos: Position) -> Iterator[Position]:
            for d in (Direction.RIGHT_AND_UP, Direction.RIGHT_AND_DOWN):
                nx, ny = pos[0] + d.x, pos[1] + d.y
                passage = passages.get(nx)
                if (
                    nx <= w
                    and 0 <= ny <= h
                    and (
                        passage is None
                        or passage[0] <= ny <= passage[0] + passage[1]
                    )
                ):
                    yield (nx, ny)

        w, h = 0, 0
        passages = dict[int, tuple[int, int]]()
        for line in input_data:
            x, y, dy = map(int, line.split(","))
            passages[x] = (y, dy)
            h = max(h, y + dy)
            w = max(w, x)
        w, h = w + 1, h + 1
        cost, _, _ = dijkstra(
            start=(0, 0),
            is_end=lambda pos: pos[0] == w,
            adjacent=adjacent,
            get_cost=lambda pos, nxt: 1 if pos[1] < nxt[1] else 0,
        )
        return cost

    def part_2(self, input_data: InputData) -> Output2:
        def adjacent(pos: Position) -> Iterator[Position]:
            for d in (Direction.RIGHT_AND_UP, Direction.RIGHT_AND_DOWN):
                nx, ny = pos[0] + d.x, pos[1] + d.y
                pp = passages.get(nx)
                if (
                    nx <= w
                    and 0 <= ny <= h
                    and (
                        pp is None
                        or any(p[0] <= ny <= p[0] + p[1] for p in pp)
                    )
                ):
                    yield (nx, ny)

        w, h = 0, 0
        passages = defaultdict[int, set[tuple[int, int]]](set)
        for line in input_data:
            x, y, dy = map(int, line.split(","))
            passages[x].add((y, dy))
            h = max(h, y + dy)
            w = max(w, x)
        w, h = w + 1, h + 1
        cost, _, _ = dijkstra(
            start=(0, 0),
            is_end=lambda pos: pos[0] == w,
            adjacent=adjacent,
            get_cost=lambda pos, nxt: 1 if pos[1] < nxt[1] else 0,
        )
        return cost

    def part_3(self, input_data: InputData) -> Output3:
        @cache
        def gap_ys(x: int) -> set[int]:
            cx = comp_x[x]
            return {
                y
                for py, dy in passages[x]
                for y in range(py, py + dy + 1)
                if (cx + y) & 1 != 0
            }

        def adjacent(pos: Position) -> Iterator[Position]:
            x, y = pos
            cx = comp_x[x]
            nx = x + 1
            ncx = comp_x[nx]
            if nx <= w:
                for ny in gap_ys(nx):
                    if abs(ny - y) <= ncx - cx:
                        yield (nx, ny)

        def get_cost(pos: Position, nxt: Position) -> int:
            dx, dy = comp_x[nxt[0]] - comp_x[pos[0]], nxt[1] - pos[1]
            return dy + ceil((dx - dy) / 2)

        w = 0
        passages = defaultdict[int, set[tuple[int, int]]](set)
        xs = set[int]()
        xs.add(0)
        for line in input_data:
            x, y, dy = map(int, line.split(","))
            xs.add(x)
            x = len(sorted(xs)) - 1
            passages[x].add((y, dy))
            w = max(w, x)
        w = w + 1
        xs.add(max(xs) + 1)
        for y, dy in passages[w - 1]:
            passages[w].add((y, dy))
        comp_x = sorted(xs)
        cost, _, _ = dijkstra(
            start=(0, 0),
            is_end=lambda pos: pos[0] == w,
            adjacent=adjacent,
            get_cost=get_cost,
        )
        return cost

    @ec_samples(
        (
            ("part_1", TEST1, 24),
            ("part_2", TEST2, 22),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 19)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
