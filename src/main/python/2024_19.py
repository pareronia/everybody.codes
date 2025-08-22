#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 19
#

import itertools
import sys
from collections import deque

from ec.common import Direction
from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = str
Output2 = str
Output3 = str
Cell = tuple[int, int]

TEST1 = """\
LR

>-IN-
-----
W---<
"""
TEST2 = """\
RRLL

A.VI..>...T
.CC...<...O
.....EIB.R.
.DHB...YF..
.....F..G..
D.H........
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, grid: list[list[str]], key: str, rounds: int) -> str:  # noqa:C901
        """https://cp-algorithms.com/algebra/binary-exp.html#applying-a-permutation-k-times."""
        h, w = len(grid), len(grid[0])

        def rotate(grid: list[list[Cell]], key: str) -> None:
            keys = itertools.cycle(ch for ch in key)
            for r in range(1, h - 1):
                for c in range(1, w - 1):
                    q = deque[Cell]()
                    for d in Direction:
                        q.append(grid[r - d.y][c + d.x])
                    q.rotate(1 if next(keys) == "R" else -1)
                    for d in Direction:
                        grid[r - d.y][c + d.x] = q.popleft()

        def get_message(grid: list[list[str]]) -> str:
            ans = list[str]()
            in_msg = False
            for r in range(h):
                for c in range(w):
                    ch = grid[r][c]
                    if ch == ">":
                        in_msg = True
                    elif ch == "<":
                        return "".join(ans)
                    elif in_msg:
                        ans.append(ch)
            raise ValueError

        def find_paths(destination: dict[Cell, Cell]) -> list[list[Cell]]:
            paths = []
            seen = set()
            for r in range(h):
                for c in range(w):
                    if (r, c) in seen:
                        continue
                    path = []
                    rr, cc = r, c
                    while (rr, cc) not in seen:
                        path.append((rr, cc))
                        seen.add((rr, cc))
                        rr, cc = destination[(rr, cc)]
                    paths.append(path)
            return paths

        moves = [[(r, c) for c in range(w)] for r in range(h)]
        rotate(moves, key)
        destination = {moves[r][c]: (r, c) for r in range(h) for c in range(w)}
        new_grid = [[""] * w for _ in range(h)]
        for path in find_paths(destination):
            for i, (r, c) in enumerate(path):
                rr, cc = path[(i + rounds) % len(path)]
                new_grid[rr][cc] = grid[r][c]
        if __debug__:
            for r in range(h):
                print("".join([new_grid[r][c] for c in range(w)]))
        return get_message(new_grid)

    def part_1(self, input_data: InputData) -> Output1:
        grid = [list(line) for line in input_data[2:]]
        return self.solve(grid, input_data[0], 1)

    def part_2(self, input_data: InputData) -> Output2:
        grid = [list(line) for line in input_data[2:]]
        return self.solve(grid, input_data[0], 100)

    def part_3(self, input_data: InputData) -> Output3:
        grid = [list(line) for line in input_data[2:]]
        return self.solve(grid, input_data[0], 1_048_576_000)

    @ec_samples(
        (
            ("part_1", TEST1, "WIN"),
            ("part_2", TEST2, "VICTORY"),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 19)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
