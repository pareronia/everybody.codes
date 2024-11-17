#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 10
#

from __future__ import annotations

import sys
from collections import Counter
from typing import NamedTuple

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = str
Output2 = int
Output3 = int
CharGrid = list[list[str]]
Cell = tuple[int, int]


class RunicWordAndPower(NamedTuple):
    word: str
    power: int

    @classmethod
    def unsolvable(cls) -> RunicWordAndPower:
        return RunicWordAndPower("", 0)


TEST1 = """\
**PCBS**
**RLNW**
BV....PT
CR....HZ
FL....JW
SG....MN
**FTZV**
**GMJH**
"""
TEST2 = """\
**XFZB**DCST**
**LWQK**GQJH**
?G....WL....DQ
BS....H?....CN
P?....KJ....TV
NM....Z?....SG
**NSHM**VKWZ**
**PJGV**XFNL**
WQ....?L....YS
FX....DJ....HV
?Y....WM....?J
TJ....YK....LP
**XRTK**BMSP**
**DWZN**GCJV**
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, grid: CharGrid, start: Cell) -> RunicWordAndPower:
        r_s, c_s = start

        block = [
            (r_s + rr, c_s + cc) for rr in range(2, 6) for cc in range(2, 6)
        ]

        for r, c in block:
            if grid[r][c] not in {".", "?"}:
                continue
            row = {grid[r][c_s + i] for i in {0, 1, 6, 7}}
            col = {grid[r_s + i][c] for i in {0, 1, 6, 7}}
            both = row & col
            if len(both) == 1:
                grid[r][c] = next(iter(both))
            elif len(both) > 1:
                return RunicWordAndPower.unsolvable()

        for r, c in block:
            if grid[r][c] not in {".", "?"}:
                continue
            cnt = Counter[str]()
            missing = None
            for i in range(8):
                v = grid[r_s + i][c]
                if v == "?":
                    missing = (r_s + i, c)
                else:
                    cnt.update(v)
            for i in range(8):
                v = grid[r][c_s + i]
                if v == "?":
                    missing = (r, c_s + i)
                else:
                    cnt.update(v)
            singles = [(v, c) for v, c in cnt.items() if c == 1]
            if len(singles) == 1:
                if missing is not None:
                    grid[missing[0]][missing[1]] = singles[0][0]
                grid[r][c] = singles[0][0]

        word, power = "", 0
        for r, c in block:
            rune = grid[r][c]
            if rune in {".", "?"}:
                return RunicWordAndPower.unsolvable()
            word += rune
            power += (ord(rune) - ord("A") + 1) * len(word)
        return RunicWordAndPower(word, power)

    def part_1(self, input: InputData) -> Output1:
        grid = [[ch for ch in line] for line in input]
        return self.solve(grid, (0, 0)).word

    def part_2(self, input: InputData) -> Output2:
        grid = [[ch for ch in line] for line in input]
        return sum(
            self.solve(grid, (r, c)).power
            for r in range(0, len(grid), 9)
            for c in range(0, len(grid[0]), 9)
        )

    def part_3(self, input: InputData) -> Output3:
        ans = 0

        def power(start: Cell) -> bool:
            nonlocal ans

            solution = self.solve(grid, start)
            if solution == RunicWordAndPower.unsolvable():
                return True
            ans += solution.power
            return False

        grid = [[ch for ch in line] for line in input]
        starts = [
            (r, c)
            for r in range(0, len(grid) - 2, 6)
            for c in range(0, len(grid[0]) - 2, 6)
        ]
        prev_ans = -sys.maxsize
        while prev_ans < ans:
            prev_ans = ans
            starts = list(filter(power, starts))
        return ans

    @ec_samples(
        (
            ("part_1", TEST1, "PTBVRCZHFLJWGMNS"),
            ("part_2", TEST1, 1851),
            ("part_3", TEST2, 3889),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 10)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
