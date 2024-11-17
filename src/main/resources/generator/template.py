#! /usr/bin/env python3
#
# everybody.codes ${year} Quest ${day}
#

import sys

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int

TEST = """\
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input: InputData) -> Output1:
        return 0

    def part_2(self, input: InputData) -> Output2:
        return 0

    def part_3(self, input: InputData) -> Output3:
        return 0

    @ec_samples(
        (
            ("part_1", TEST, 0),
            ("part_2", TEST, 0),
            ("part_3", TEST, 0),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(${year}, ${day})


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
