#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 15
#

import sys
from collections.abc import Iterator
from functools import reduce

from ec.common import Direction
from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.graph import bfs

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
#####.#####
#.........#
#.######.##
#.........#
###.#.#####
#H.......H#
###########
"""
TEST2 = """\
##########.##########
#...................#
#.###.##.###.##.#.#.#
#..A#.#..~~~....#A#.#
#.#...#.~~~~~...#.#.#
#.#.#.#.~~~~~.#.#.#.#
#...#.#.B~~~B.#.#...#
#...#....BBB..#....##
#C............#....C#
#####################
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, input: tuple[str, ...], start: tuple[int, int]) -> int:
        h = len(input)
        w = len(input[0])
        complete = reduce(
            lambda agg, h: agg | 1 << (ord(h) - ord("A")),
            filter(
                lambda v: v.isalpha(),
                (input[r][c] for r in range(h) for c in range(w)),
            ),
            0,
        )

        def is_end(node: tuple[int, int, int]) -> bool:
            r, c, herbs = node
            return herbs == complete and (r, c) == start

        def adjacent(
            node: tuple[int, int, int]
        ) -> Iterator[tuple[int, int, int]]:
            r, c, herbs = node
            for d in Direction.capitals():
                n_r, n_c = r + d.y, c + d.x
                if 0 <= n_r < h and 0 <= n_c < w:
                    v = input[n_r][n_c]
                    if v in {"#", "~"}:
                        continue
                    n_herbs = herbs
                    if v.isalpha():
                        n_herbs |= 1 << (ord(v) - ord("A"))
                    yield (n_r, n_c, n_herbs)

        distance, _ = bfs((*start, 0), is_end, adjacent)
        return distance

    def part_1(self, input: InputData) -> Output1:
        return self.solve(input, start=(0, len(input[0]) // 2))

    def part_2(self, input: InputData) -> Output2:
        return self.solve(input, start=(0, len(input[0]) // 2))

    def part_3(self, input: InputData) -> Output3:
        w = len(input[0])

        def left() -> int:
            grid = tuple(line[: w // 3] for line in input)  # noqa E203
            start = (len(grid) - 2, len(grid[0]) - 1)
            return self.solve(grid, start) + 1

        def right() -> int:
            grid = tuple(line[2 * (w // 3) :] for line in input)  # noqa E203
            start = (len(grid) - 2, 0)
            return self.solve(grid, start) + 1

        def middle() -> int:
            lines = [
                line[w // 3 : 2 * (w // 3)] for line in input[:-2]  # noqa E203
            ]
            lines.append(
                input[-2][w // 3 : 2 * (w // 3)].replace(  # noqa E203
                    "K", "L", 1
                )
            )
            lines.append(input[-1][w // 3 : 2 * (w // 3)])  # noqa E203
            grid = tuple(lines)
            return self.solve(grid, start=(0, len(grid[0]) // 2)) + 2 + 4

        return left() + right() + middle()

    @ec_samples(
        (
            ("part_1", TEST1, 26),
            ("part_2", TEST2, 38),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 15)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
