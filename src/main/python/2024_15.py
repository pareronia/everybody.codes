#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 15
#

import sys
from collections import deque
from collections.abc import Iterator

from ec.common import Cell
from ec.common import Direction
from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.common import log
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
    def part_1(self, input: InputData) -> Output1:
        h = len(input)
        w = len(input[0])

        def adjacent(c: Cell) -> Iterator[Cell]:
            for d in Direction.capitals():
                n = c.at(d)
                if (
                    n.row >= 0
                    and n.row < h
                    and n.col >= 0
                    and n.col < w
                    and input[n.row][n.col] != "#"
                ):
                    yield n

        dist, _ = bfs(
            Cell(0, w // 2), lambda c: input[c.row][c.col] == "H", adjacent
        )
        return 2 * dist

    def solve(self, input: tuple[str, ...], start: Cell) -> int:
        h = len(input)
        w = len(input[0])
        H = list(
            {
                input[r][c]
                for r in range(h)
                for c in range(w)
                if input[r][c].isalpha()
            }
        )
        log(H)

        def adjacent(c: Cell) -> Iterator[Cell]:
            for d in Direction.capitals():
                n = c.at(d)
                if (
                    n.row >= 0
                    and n.row < h
                    and n.col >= 0
                    and n.col < w
                    and input[n.row][n.col] not in {"#", "~"}
                ):
                    yield n

        q: deque[tuple[int, Cell, str]] = deque()
        q.append((0, start, "0" * len(H)))
        seen: set[tuple[Cell, str]] = set()
        while not len(q) == 0:
            distance, node, herbs = q.popleft()
            if (node, herbs) in seen:
                continue
            seen.add((node, herbs[:]))
            if node == start and herbs == ("1" * len(H)):
                return distance
            for n in adjacent(node):
                if (n, herbs) in seen:
                    continue
                n_herbs = herbs[:]
                v = input[n.row][n.col]
                if v.isalpha():
                    n_herbs = "".join(
                        "1" if i == H.index(v) else ch
                        for i, ch in enumerate(herbs)
                    )
                q.append((distance + 1, n, n_herbs))
        raise RuntimeError("unsolvable")

    def part_2(self, input: InputData) -> Output2:
        w = len(input[0])
        start = Cell(0, w // 2)
        return self.solve(input, start)

    def part_3(self, input: InputData) -> Output3:
        w = len(input[0])
        start = Cell(0, w // 2)
        ans = 0
        # 1
        grid = tuple(line[: w // 3] for line in input)  # noqa E203
        start = Cell(len(grid) - 2, len(grid[0]) - 1)
        ans += self.solve(grid, start) + 1
        # 3
        grid = tuple(line[2 * (w // 3) :] for line in input)  # noqa E203
        start = Cell(len(grid) - 2, 0)
        ans += self.solve(grid, start) + 1
        # 2
        lines = [
            line[w // 3 : 2 * (w // 3)] for line in input[:-2]  # noqa E203
        ]
        lines.append(
            input[-2][w // 3 : 2 * (w // 3)].replace("K", "L", 1)  # noqa E203
        )
        lines.append(input[-1][w // 3 : 2 * (w // 3)])  # noqa E203
        grid = tuple(lines)
        start = Cell(0, len(grid[0]) // 2)
        ans += self.solve(grid, start) + 2 + 4
        return ans

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
