#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 3
#

import sys

from ec.common import Cell
from ec.common import Direction
from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int


TEST = """\
..........
..###.##..
...####...
..######..
..######..
...####...
..........
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, input: InputData, dirs: set[Direction]) -> Output1:
        cubes = {
            Cell(r, c): 1
            for r in range(len(input))
            for c in range(len(input[0]))
            if input[r][c] == "#"
        }
        while True:
            new_cubes = dict[Cell, int]()
            for cell, v in cubes.items():
                if all(cubes.get(cell.at(dir), 0) == v for dir in dirs):
                    new_cubes[cell] = v + 1
            if len(new_cubes) == 0:
                break
            cubes.update(new_cubes)
        return sum(cubes.values())

    def part_1(self, input: InputData) -> Output1:
        return self.solve(input, Direction.capitals())

    def part_2(self, input: InputData) -> Output2:
        return self.solve(input, Direction.capitals())

    def part_3(self, input: InputData) -> Output3:
        return self.solve(input, Direction.octants())

    @ec_samples(
        (
            ("part_1", TEST, 35),
            ("part_3", TEST, 29),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 3)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
