#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 1
#

import sys

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

POTIONS = {"A": 0, "B": 1, "C": 3, "D": 5}

Output1 = int
Output2 = int
Output3 = int


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, input_data: InputData, group_size: int) -> int:
        def potions(group: str) -> int:
            add = len(group) - group.count("x") - 1
            return sum(POTIONS[c] + add for c in group if c != "x")

        return sum(
            potions(input_data[0][i : i + group_size])
            for i in range(0, len(input_data[0]), group_size)
        )

    def part_1(self, input_data: InputData) -> Output1:
        return self.solve(input_data, group_size=1)

    def part_2(self, input_data: InputData) -> Output2:
        return self.solve(input_data, group_size=2)

    def part_3(self, input_data: InputData) -> Output3:
        return self.solve(input_data, group_size=3)

    @ec_samples(
        (
            ("part_1", "ABBAC", 5),
            ("part_2", "AxBCDDCAxD", 28),
            ("part_3", "xBxAAABCDxCC", 30),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 1)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
