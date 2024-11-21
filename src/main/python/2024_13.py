#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 13
#

import sys
from typing import Iterator

from ec.common import Cell
from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.graph import dijkstra

Output1 = int
Output2 = int
Output3 = int
Platform = tuple[Cell, int]

TEST1 = """\
#######
#6769##
S50505E
#97434#
#######
"""
TEST2 = """\
SSSSSSSSSSS
S674345621S
S###6#4#18S
S53#6#4532S
S5450E0485S
S##7154532S
S2##314#18S
S971595#34S
SSSSSSSSSSS
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, input: InputData) -> int:
        def parse(
            input: InputData,
        ) -> tuple[dict[Cell, int], set[Platform], Platform]:
            platforms = dict[Cell, int]()
            starts = set()
            for r in range(len(input)):
                for c in range(len(input[0])):
                    if input[r][c] == "S":
                        start = Cell(r, c)
                        platforms[start] = 0
                        starts.add((start, 0))
                    elif input[r][c] == "E":
                        end = Cell(r, c)
                        platforms[end] = 0
                    elif input[r][c] not in {"#", " "}:
                        platforms[Cell(r, c)] = int(input[r][c])
            return platforms, starts, (end, 0)

        def adjacent(p: Platform) -> Iterator[Platform]:
            return (
                (n, platforms[n])
                for n in p[0].get_capital_neighbours()
                if n in platforms
            )

        def time(p: Platform, n: Platform) -> int:
            d = abs(p[1] - n[1])
            return 1 + (10 % d if d > 5 else d)

        platforms, starts, end = parse(input)
        ans, _, _ = dijkstra(
            start=end,
            is_end=lambda p: p in starts,
            adjacent=adjacent,
            get_cost=time,
        )
        return ans

    def part_1(self, input: InputData) -> Output1:
        return self.solve(input)

    def part_2(self, input: InputData) -> Output2:
        return self.solve(input)

    def part_3(self, input: InputData) -> Output3:
        return self.solve(input)

    @ec_samples(
        (
            ("part_1", TEST1, 28),
            ("part_3", TEST2, 14),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 13)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
