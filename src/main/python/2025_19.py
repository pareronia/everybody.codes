#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 19
#

import sys
from collections import defaultdict
from math import ceil

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
7,7,2
12,0,4
15,5,3
24,1,6
28,5,5
40,8,2
"""
TEST2 = """\
7,7,2
7,1,3
12,0,4
15,5,3
24,1,6
28,5,5
40,3,3
40,8,2
"""

Position = tuple[int, int]


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, input_data: InputData) -> int:
        passages = defaultdict[int, list[int]](list)
        for line in input_data:
            x, y, _ = (int(n) for n in line.split(","))
            passages[x].append(y)
        return max(ceil((x + passages[x][0]) / 2) for x in passages)

    def part_1(self, input_data: InputData) -> Output1:
        return self.solve(input_data)

    def part_2(self, input_data: InputData) -> Output2:
        return self.solve(input_data)

    def part_3(self, input_data: InputData) -> Output3:
        return self.solve(input_data)

    @ec_samples(
        (
            ("part_1", TEST1, 24),
            ("part_2", TEST2, 22),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 19)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
