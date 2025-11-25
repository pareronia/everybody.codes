#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 16
#

import sys
from math import prod

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.search import binary_search

Output1 = int
Output2 = int
Output3 = int

TEST1 = "1,2,3,5,9"
TEST2 = "1,2,2,2,2,3,1,2,3,3,1,3,1,2,3,2,1,4,1,3,2,2,1,3,2,2"


class Solution(SolutionBase[Output1, Output2, Output3]):
    def wall_from_spell(self, spell: list[int], size: int) -> int:
        return sum(size // n for n in spell)

    def spell_from_wall(self, columns: list[int]) -> list[int]:
        columns = [0, *columns]
        ans = list[int]()
        for i in range(1, len(columns)):
            if columns[i] > 0:
                ans.append(i)
                for j in range(i, len(columns), i):
                    columns[j] -= 1
        return ans

    def part_1(self, input_data: InputData) -> Output1:
        spell = [int(s) for s in input_data[0].split(",")]
        return self.wall_from_spell(spell, size=90)

    def part_2(self, input_data: InputData) -> Output2:
        columns = [int(s) for s in input_data[0].split(",")]
        return prod(self.spell_from_wall(columns))

    def part_3(self, input_data: InputData) -> Output3:
        columns = [int(s) for s in input_data[0].split(",")]
        spell = self.spell_from_wall(columns)
        return binary_search(
            lambda v: self.wall_from_spell(spell, size=v)
            <= 202_520_252_025_000
        )

    @ec_samples(
        (
            ("part_1", TEST1, 193),
            ("part_2", TEST2, 270),
            ("part_3", TEST2, 94_439_495_762_954),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 16)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
