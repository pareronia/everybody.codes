#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 17
#

import sys
from math import prod
from typing import Iterator

from ec.common import InputData
from ec.common import Position
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.graph import prim

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
*...*
..*..
.....
.....
*.*..
"""
TEST2 = """\
.......................................
..*.......*...*.....*...*......**.**...
....*.................*.......*..*..*..
..*.........*.......*...*.....*.....*..
......................*........*...*...
..*.*.....*...*.....*...*........*.....
.......................................
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def parse(self, input: InputData) -> set[Position]:
        return {
            Position(x, y)
            for y in range(len(input))
            for x in range(len(input[0]))
            if input[y][x] == "*"
        }

    def part_1(self, input: InputData) -> Output1:
        stars = self.parse(input)
        dist, seen = prim(
            next(iter(stars)),
            lambda s: ((n, n.manhattan_distance(s)) for n in stars),
        )
        return dist + len(seen)

    def part_2(self, input: InputData) -> Output2:
        return self.part_1(input)

    def part_3(self, input: InputData) -> Output3:
        stars = self.parse(input)

        def adjacent(s: Position) -> Iterator[tuple[Position, int]]:
            for n in stars:
                md = n.manhattan_distance(s)
                if md < 6:
                    yield (n, md)

        constellations = []
        while len(stars) > 0:
            dist, seen = prim(next(iter(stars)), adjacent)
            constellations.append(dist + len(seen))
            stars -= seen
        return prod(sorted(constellations)[-3:])

    @ec_samples(
        (
            ("part_1", TEST1, 16),
            ("part_3", TEST2, 15624),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 17)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
