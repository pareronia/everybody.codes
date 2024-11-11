#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 4
#

import sys

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
3
4
7
8
"""
TEST2 = """\
2
4
5
6
8
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input: InputData) -> Output1:
        nums = list(map(int, input))
        m = min(nums)
        return sum(n - m for n in nums)

    def part_2(self, input: InputData) -> Output2:
        return self.part_1(input)

    def part_3(self, input: InputData) -> Output3:
        nums = list(map(int, input))
        return min(sum(abs(n1 - n2) for n2 in nums) for n1 in nums)

    @ec_samples(
        (
            ("part_1", TEST1, 10),
            ("part_3", TEST2, 8),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 4)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
