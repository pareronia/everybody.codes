#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 12
#

import sys
from collections import deque
from collections.abc import Callable
from collections.abc import Iterator
from typing import TypeVar

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.common import log

T = TypeVar("T")
Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
989601
857782
746543
766789
"""
TEST2 = """\
9589233445
9679121695
8469121876
8352919876
7342914327
7234193437
6789193538
6781219648
5691219769
5443329859
"""
TEST3 = """\
5411
3362
5235
3112
"""
TEST4 = """\
41951111131882511179
32112222211518122215
31223333322115122219
31234444432147511128
91223333322176121892
61112222211166431583
14661111166111111746
11111119142122222177
41222118881233333219
71222127839122222196
56111126279711111517
"""


def flood_fill(
    start: T,
    adjacent: Callable[[T], Iterator[T]],
) -> set[T]:
    q: deque[T] = deque()
    q.append(start)
    seen: set[T] = set()
    seen.add(start)
    while len(q) != 0:
        node = q.popleft()
        for n in adjacent(node):
            if n in seen:
                continue
            seen.add(n)
            q.append(n)
    return seen


class Solution(SolutionBase[Output1, Output2, Output3]):
    def adjacent(
        self,
        grid: tuple[str, ...],
        cell: tuple[int, int],
        seen: set[tuple[int, int]] | None = None,
    ) -> Iterator[tuple[int, int]]:
        for dr, dc in {(0, 1), (0, -1), (1, 0), (-1, 0)}:
            r, c = cell
            rr, cc = r + dr, c + dc
            if (
                0 <= rr < len(grid)
                and 0 <= cc < len(grid[0])
                and grid[r][c] >= grid[rr][cc]
                and not (seen is not None and (r, c) in seen)
            ):
                yield (rr, cc)

    def part_1(self, input_data: InputData) -> Output1:
        return len(flood_fill((0, 0), lambda x: self.adjacent(input_data, x)))

    def part_2(self, input_data: InputData) -> Output2:
        return len(
            flood_fill((0, 0), lambda x: self.adjacent(input_data, x))
            | flood_fill(
                (len(input_data) - 1, len(input_data[0]) - 1),
                lambda x: self.adjacent(input_data, x),
            )
        )

    def part_3(self, input_data: InputData) -> Output3:
        first = [
            (
                (r, c),
                len(
                    flood_fill((r, c), lambda x: self.adjacent(input_data, x))
                ),
            )
            for r in range(len(input_data))
            for c in range(len(input_data[0]))
        ]
        log("first")
        first.sort(key=lambda x: x[1])
        seen = flood_fill(first[-1][0], lambda x: self.adjacent(input_data, x))
        second = [
            (
                (r, c),
                len(
                    seen
                    | flood_fill(
                        (r, c), lambda x: self.adjacent(input_data, x, seen)
                    )
                ),
            )
            for r in range(len(input_data))
            for c in range(len(input_data[0]))
            if (r, c) not in seen
        ]
        log("second")
        second.sort(key=lambda x: x[1])
        seen |= flood_fill(
            second[-1][0], lambda x: self.adjacent(input_data, x, seen)
        )
        third = [
            (
                (r, c),
                len(
                    seen
                    | flood_fill(
                        (r, c), lambda x: self.adjacent(input_data, x, seen)
                    )
                ),
            )
            for r in range(len(input_data))
            for c in range(len(input_data[0]))
            if (r, c) not in seen
        ]
        log("third")
        third.sort(key=lambda x: x[1])
        seen |= flood_fill(
            third[-1][0], lambda x: self.adjacent(input_data, x, seen)
        )
        return len(seen)

    @ec_samples(
        (
            ("part_1", TEST1, 16),
            ("part_2", TEST2, 58),
            ("part_3", TEST3, 14),
            ("part_3", TEST4, 136),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 12)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
