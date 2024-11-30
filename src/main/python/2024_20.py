#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 20
#

import itertools
import sys
from collections import defaultdict

from ec.common import Cell
from ec.common import Direction
from ec.common import InputData
from ec.common import SolutionBase
from ec.common import Turn
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int
DA = {
    "S": -1,
    "#": -(10**9),
    ".": -1,
    "A": -1,
    "B": -1,
    "C": -1,
    "-": -2,
    "+": 1,
}

TEST1 = """\
#....S....#
#.........#
#---------#
#.........#
#..+.+.+..#
#.+-.+.++.#
#.........#
"""
TEST2 = """\
####S####
#-.+++.-#
#.+.+.+.#
#-.+.+.-#
#A+.-.+C#
#.+-.-+.#
#.+.B.+.#
#########
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input: InputData) -> Output1:
        h, w = len(input), len(input[0])
        start = Cell(0, next(c for c in range(w) if input[0][c] == "S"))
        memo = defaultdict[tuple[Cell, Direction, int], int](lambda: -(10**9))
        for d in Direction.capitals():
            memo[(start, d, 0)] = 1000
        for t, r, c in itertools.product(range(100), range(h), range(w)):
            cell = Cell(r, c)
            for d in Direction.capitals():
                for dd in {d, d.turn(Turn.LEFT), d.turn(Turn.RIGHT)}:
                    n = cell.at(dd)
                    if not (0 <= n.row < h and 0 <= n.col < w):
                        continue
                    v = input[n.row][n.col]
                    n_key = (n, dd, t + 1)
                    memo[n_key] = max(memo[n_key], memo[(cell, d, t)] + DA[v])
        ans = 0
        for r in range(h):
            for c in range(w):
                cell = Cell(r, c)
                for d in Direction.capitals():
                    ans = max(ans, memo[(cell, d, 100)])
        return ans

    def part_2(self, input: InputData) -> Output2:
        return 0

    def part_3(self, input: InputData) -> Output3:
        h, w = len(input), len(input[0])
        start = Cell(0, next(c for c in range(w) if input[0][c] == "S"))
        ans = 0
        alt = 384_400
        for i in range(5):
            start = start.at(Direction.RIGHT)
            alt += DA[input[start.row][start.col]]
        while alt > 0:
            start = start.at(Direction.DOWN)
            start = Cell(start.row % h, start.col)
            alt += DA[input[start.row][start.col]]
            ans += 1
        return ans

    @ec_samples(
        (
            ("part_1", TEST1, 1045),
            # ("part_2", TEST2, 24),
            # ("part_3", TEST1, 0),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 20)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
