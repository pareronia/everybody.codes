#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 1
#

import sys
from collections.abc import Iterator

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = str
Output2 = str
Output3 = str

TEST1 = """\
Vyrdax,Drakzyph,Fyrryn,Elarzris

R3,L2,R3,L1
"""
TEST2 = """\
Vyrdax,Drakzyph,Fyrryn,Elarzris

R3,L2,R3,L3
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def parse(
        self, input_data: InputData
    ) -> tuple[list[str], Iterator[tuple[str, int]]]:
        return input_data[0].split(","), (
            (x[0], int(x[1:])) for x in input_data[2].split(",")
        )

    def part_1(self, input_data: InputData) -> Output1:
        names, moves = self.parse(input_data)
        pos = 0
        for d, a in moves:
            pos = min(max(pos + (a if d == "R" else -a), 0), len(names) - 1)
        return names[pos]

    def part_2(self, input_data: InputData) -> Output2:
        names, moves = self.parse(input_data)
        pos = 0
        for d, a in moves:
            pos = (pos + (a if d == "R" else -a)) % len(names)
        return names[pos]

    def part_3(self, input_data: InputData) -> Output3:
        names, moves = self.parse(input_data)
        for d, a in moves:
            swp = (a if d == "R" else -a) % len(names)
            names[0], names[swp] = names[swp], names[0]
        return names[0]

    @ec_samples(
        (
            ("part_1", TEST1, "Fyrryn"),
            ("part_2", TEST1, "Elarzris"),
            ("part_3", TEST2, "Drakzyph"),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 1)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
