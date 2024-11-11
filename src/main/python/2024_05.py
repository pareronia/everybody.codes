#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 5
#

import sys
from collections import defaultdict
from typing import Sequence

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
2 3 4 5
3 4 5 2
4 5 2 3
5 2 3 4
"""
TEST2 = """\
2 3 4 5
6 7 8 9
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def shout(self, cols: Sequence[Sequence[int]]) -> int:
        return int("".join(str(cols[j][0]) for j in range(len(cols))))

    def get_cols(self, input: InputData) -> list[list[int]]:
        cols: list[list[int]] = [[], [], [], []]
        for line in input:
            nums = list(map(int, line.split()))
            for j in range(len(cols)):
                cols[j].append(nums[j])
        return cols

    def round(self, cols: list[list[int]], r: int) -> int:
        n = cols[r % len(cols)].pop(0)
        dest = (r + 1) % len(cols)
        size = 2 * len(cols[dest])
        rem = (n - 1) % size
        pos = min(rem, size - rem)
        cols[dest].insert(pos, n)
        return self.shout(cols)

    def part_1(self, input: InputData) -> Output1:
        cols = self.get_cols(input)
        for r in range(10):
            ans = self.round(cols, r)
        return ans

    def part_2(self, input: InputData) -> Output2:
        cols = self.get_cols(input)
        nums = defaultdict[int, int](int)
        r = 0
        while True:
            ans = self.round(cols, r)
            nums[ans] += 1
            if nums[ans] == 2024:
                return ans * (r + 1)
            r += 1

    def part_3(self, input: InputData) -> Output3:
        cols = self.get_cols(input)
        seen = set[tuple[tuple[int, ...], ...]]()
        r = 0
        while True:
            self.round(cols, r)
            key = tuple(tuple(c for c in col) for col in cols)
            if key in seen:
                break
            seen.add(key)
            r += 1
        return max(self.shout(x) for x in seen)

    @ec_samples(
        (
            ("part_1", TEST1, 2323),
            ("part_2", TEST2, 50877075),
            ("part_3", TEST2, 6584),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 5)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
