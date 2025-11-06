#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 3
#

import sys
from collections import Counter
from collections.abc import Iterator

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
10,5,1,10,3,8,5,2,2
"""
TEST2 = """\
4,51,13,64,57,51,82,57,16,88,89,48,32,49,49,2,84,65,49,43,9,13,2,3,75,72,63,\
48,61,14,40,77
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def crates(self, input_data: InputData) -> Iterator[int]:
        return map(int, input_data[0].split(","))

    def part_1(self, input_data: InputData) -> Output1:
        return sum(set(self.crates(input_data)))

    def part_2(self, input_data: InputData) -> Output2:
        return sum(sorted(set(self.crates(input_data)))[:20])

    def part_3(self, input_data: InputData) -> Output3:
        return Counter(self.crates(input_data)).most_common()[0][1]

    @ec_samples(
        (
            ("part_1", TEST1, 29),
            ("part_2", TEST2, 781),
            ("part_3", TEST2, 3),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 3)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
