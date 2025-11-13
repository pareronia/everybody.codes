#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 4
#

import sys
from math import prod

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
128
64
32
16
8
"""
TEST2 = """\
102
75
50
35
13
"""
TEST3 = """\
5
5|10
10|20
5
"""
TEST4 = """\
5
7|21
18|36
27|27
10|50
10|50
11
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input_data: InputData) -> Output1:
        a, b = map(int, (input_data[0], input_data[-1]))
        return 2025 * a // b

    def part_2(self, input_data: InputData) -> Output2:
        a, b = map(int, (input_data[0], input_data[-1]))
        q, r = divmod(10_000_000_000_000 * b, a)
        return q if r == 0 else q + 1

    def part_3(self, input_data: InputData) -> Output3:
        return int(
            prod(
                (
                    int(a) / int(b)
                    for a, b in (
                        s.split() for s in " ".join(input_data).split("|")
                    )
                ),
                start=100.0,
            )
        )

    @ec_samples(
        (
            ("part_1", TEST1, 32400),
            ("part_1", TEST2, 15888),
            ("part_2", TEST1, 625000000000),
            ("part_2", TEST2, 1274509803922),
            ("part_3", TEST3, 400),
            ("part_3", TEST4, 6818),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 4)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
