#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 1
#

import itertools
import sys

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.common import to_blocks

TEST1 = """\
*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.
*.*.*...*.*...*..
.*.*.*.*.*...*.*.
*.*.....*...*.*.*
.*.*.*.*.*.*.*.*.
*...*...*.*.*.*.*
.*.*.*.*.*.*.*.*.
*.*.*...*.*.*.*.*
.*...*...*.*.*.*.
*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.

RRRLRLRRRRRL
LLLLRLRRRRRR
RLLLLLRLRLRL
LRLLLRRRLRLR
LLRLLRLLLRRL
LRLRLLLRRRRL
LRLLLLLLRLLL
RRLLLRLLRLRR
RLLLLLRLLLRL
"""
TEST2 = """\
*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.*.*.*.*.
..*.*.*.*...*.*...*.*.*..
.*...*.*.*.*.*.*.....*.*.
*.*...*.*.*.*.*.*...*.*.*
.*.*.*.*.*.*.*.*.......*.
*.*.*.*.*.*.*.*.*.*...*..
.*.*.*.*.*.*.*.*.....*.*.
*.*...*.*.*.*.*.*.*.*....
.*.*.*.*.*.*.*.*.*.*.*.*.
*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.*...*.*.
*.*.*.*.*.*.*.*.*...*.*.*
.*.*.*.*.*.*.*.*.....*.*.
*.*.*.*.*.*.*.*...*...*.*
.*.*.*.*.*.*.*.*.*.*.*.*.
*.*.*...*.*.*.*.*.*.*.*.*
.*...*.*.*.*...*.*.*...*.
*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.*.*.*.*.

RRRLLRRRLLRLRRLLLRLR
RRRRRRRRRRLRRRRRLLRR
LLLLLLLLRLRRLLRRLRLL
RRRLLRRRLLRLLRLLLRRL
RLRLLLRRLRRRLRRLRRRL
LLLLLLLLRLLRRLLRLLLL
LRLLRRLRLLLLLLLRLRRL
LRLLRRLLLRRRRRLRRLRR
LRLLRRLRLLRLRRLLLRLL
RLLRRRRLRLRLRLRLLRRL
"""
TEST3 = """\
*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.
*.*.*...*.*...*..
.*.*.*.*.*...*.*.
*.*.....*...*.*.*
.*.*.*.*.*.*.*.*.
*...*...*.*.*.*.*
.*.*.*.*.*.*.*.*.
*.*.*...*.*.*.*.*
.*...*...*.*.*.*.
*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.

RRRLRLRRRRRL
LLLLRLRRRRRR
RLLLLLRLRLRL
LRLLLRRRLRLR
LLRLLRLLLRRL
LRLRLLLRRRRL
"""
TEST4 = """\
*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.*.*.*.*.
..*.*.*.*...*.*...*.*.*..
.*...*.*.*.*.*.*.....*.*.
*.*...*.*.*.*.*.*...*.*.*
.*.*.*.*.*.*.*.*.......*.
*.*.*.*.*.*.*.*.*.*...*..
.*.*.*.*.*.*.*.*.....*.*.
*.*...*.*.*.*.*.*.*.*....
.*.*.*.*.*.*.*.*.*.*.*.*.
*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.*...*.*.
*.*.*.*.*.*.*.*.*...*.*.*
.*.*.*.*.*.*.*.*.....*.*.
*.*.*.*.*.*.*.*...*...*.*
.*.*.*.*.*.*.*.*.*.*.*.*.
*.*.*...*.*.*.*.*.*.*.*.*
.*...*.*.*.*...*.*.*...*.
*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.*.*.*.*.

RRRLLRRRLLRLRRLLLRLR
RRRRRRRRRRLRRRRRLLRR
LLLLLLLLRLRRLLRRLRLL
RRRLLRRRLLRLLRLLLRRL
RLRLLLRRLRRRLRRLRRRL
LLLLLLLLRLLRRLLRLLLL
"""
TEST5 = """\
*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.
..*.*.*.*.*.*.........*.*.*.*.....*.*.*
.*.*...*.*.*.*.*.*.*.*.*.*.*...*.*.*.*.
*.*.*.*...*.*.*.*.*.....*.*.*.*...*.*..
.*...*.*...*.*.*.*.*.*.*.....*.*.*.*.*.
*.*.*.*.*.....*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*...*.*.*.*.....*.*.*.*...*.
*.*...*.*.*.*.*.*.*.*...*.*.*...*.*.*.*
.*...*.*.*.*.*.*.*.*...*.*.*.*.*.*.*.*.
*.*.*.*.*.*...*.....*.*...*...*.*.*.*.*
.*...*.*.*.*.*...*.*.*.*.*...*.*...*.*.
*.*.*.*.*...*.*.*.*.*.*.*.*...*.*.*.*.*
.*.*.*.*.*.*.*.*...*.*.*.*.*.*.*.*.*.*.
....*.*.*.*...*.*.*.*.*.*.*...*.*.*...*
.*.*.*...*.*.*.*.*...*.*.*.*.*.*.*.*...
*.*.*.*.*.*.*.....*...*...*.*.*.*.*.*.*
.*.*...*.....*.*.*.*.*.*.*...*.*.*.*.*.
*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*
.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.

RRRRLLRRLLLLLLLRLLRL
RRRRRRRLRRLRRLRRRLRR
RRRLLRRRRRLRRRRRLRRR
LLLLRRLLRRLLLLLRRLLL
LRRRRLRRLRLLRLLRRLRR
RRRRRRRRLRRRRLLRRRLR
"""

Output1 = int
Output2 = int
Output3 = str
CharGrid = list[list[str]]


class Solution(SolutionBase[Output1, Output2, Output3]):
    def toss(self, grid: tuple[str, ...], sequence: str, toss: int) -> int:
        row, col = 0, (toss - 1) * 2
        seq = iter(sequence)
        while row < len(grid):
            if grid[row][col] == "*":
                col += 1 if next(seq) == "R" else -1
                if col == -1:
                    col = 1
                elif col == len(grid[row]):
                    col -= 2
            else:
                row += 1
        return max(0, (col // 2 + 1) * 2 - toss)

    def part_1(self, input_data: InputData) -> Output1:
        grid, sequences = to_blocks(input_data)
        return sum(
            self.toss(grid, sequence, toss)
            for toss, sequence in enumerate(sequences, start=1)
        )

    def part_2(self, input_data: InputData) -> Output2:
        grid, sequences = to_blocks(input_data)
        tosses = range(1, len(grid[0]) // 2 + 2)
        return sum(
            max(self.toss(grid, sequence, toss) for toss in tosses)
            for sequence in sequences
        )

    def part_3(self, input_data: InputData) -> Output3:
        grid, sequences = to_blocks(input_data)
        seq_idxs = range(len(sequences))
        max_toss = len(grid[0]) // 2 + 1
        memo = [-1] * max_toss * len(sequences)
        lo, hi = sys.maxsize, 0
        for combo in itertools.permutations(range(1, max_toss + 1), r=6):
            coins = 0
            for i, c in zip(seq_idxs, combo, strict=True):
                idx = i * max_toss + c - 1
                if memo[idx] == -1:
                    memo[idx] = self.toss(grid, sequences[i], c)
                coins += memo[idx]
            lo, hi = min(lo, coins), max(hi, coins)
        return f"{lo} {hi}"

    @ec_samples(
        (
            ("part_1", TEST1, 26),
            ("part_2", TEST2, 115),
            ("part_3", TEST3, "13 43"),
            ("part_3", TEST4, "25 66"),
            ("part_3", TEST5, "39 122"),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2, 1)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
