#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 1
#

import sys

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
    def part_1(self, input_data: InputData) -> Output1:
        names = input_data[0].split(",")
        pos = 0
        for m in input_data[2].split(","):
            if m.startswith("R"):
                pos = min(pos + int(m[1:]), len(names) - 1)
            else:
                pos = max(pos - int(m[1:]), 0)
        return names[pos]

    def part_2(self, input_data: InputData) -> Output2:
        names = input_data[0].split(",")
        pos = 0
        for m in input_data[2].split(","):
            if m.startswith("R"):
                pos = (pos + int(m[1:])) % len(names)
            else:
                pos = (pos - int(m[1:])) % len(names)
        return names[pos]

    def part_3(self, input_data: InputData) -> Output3:
        names = input_data[0].split(",")
        pos = 0
        for m in input_data[2].split(","):
            if m.startswith("R"):
                swp = (pos + int(m[1:])) % len(names)
            else:
                swp = (len(names) + pos - int(m[1:])) % len(names)
            tmp = names[swp]
            names[swp] = names[pos]
            names[pos] = tmp
        return names[pos]

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
