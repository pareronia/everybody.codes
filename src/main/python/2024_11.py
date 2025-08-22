#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 11
#

import sys
from collections import defaultdict

from ec.common import InputData
from ec.common import SolutionBase

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
A:B,C
B:C,A
C:A
"""
TEST2 = """\
A:B,C
B:C,A,A
C:A
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, input_data: InputData, start: str, days: int) -> int:
        life_cycles = dict[str, list[str]]()
        for line in input_data:
            category, nxt_gen = line.split(":")
            life_cycles.setdefault(category, nxt_gen.split(","))
        buckets = defaultdict[str, int](int)
        buckets[start] = 1
        for _ in range(days):
            new_buckets = defaultdict[str, int](int)
            for category in buckets:
                for nxt_gen in life_cycles[category]:
                    new_buckets[nxt_gen] += buckets[category]
            buckets = new_buckets
        return sum(buckets.values())

    def part_1(self, input_data: InputData) -> Output1:
        return self.solve(input_data, start="A", days=4)

    def part_2(self, input_data: InputData) -> Output2:
        return self.solve(input_data, start="Z", days=10)

    def part_3(self, input_data: InputData) -> Output3:
        hi, lo = -sys.maxsize, sys.maxsize
        for line in input_data:
            start, _ = line.split(":")
            population = self.solve(input_data, start, days=20)
            hi = max(hi, population)
            lo = min(lo, population)
        return hi - lo

    def samples(self) -> None:
        assert self.solve(tuple(TEST1.splitlines()), "A", 4) == 8
        assert self.part_3(tuple(TEST2.splitlines())) == 268815


solution = Solution(2024, 11)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
