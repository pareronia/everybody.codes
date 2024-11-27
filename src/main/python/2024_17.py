#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 17
#

import sys
from math import prod
from queue import PriorityQueue

from ec.common import InputData
from ec.common import Position
from ec.common import SolutionBase
from ec.common import ec_samples

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
    def part_1(self, input: InputData) -> Output1:
        stars = set[Position]()
        for y in range(len(input)):
            for x in range(len(input[0])):
                if input[y][x] == "*":
                    stars.add(Position(x, y))

        q = PriorityQueue[tuple[int, Position]]()
        q.put((0, next(_ for _ in stars)))
        seen = set[Position]()
        dist = 0
        while not q.empty():
            d, s = q.get()
            if s in seen:
                continue
            dist += d
            seen.add(s)
            for n in stars:
                if n in seen:
                    continue
                q.put((n.manhattan_distance(s), n))
        return dist + len(seen)

    def part_2(self, input: InputData) -> Output2:
        return self.part_1(input)

    def part_3(self, input: InputData) -> Output3:
        stars = set[Position]()
        for y in range(len(input)):
            for x in range(len(input[0])):
                if input[y][x] == "*":
                    stars.add(Position(x, y))

        constellations = []
        while len(stars) > 0:
            q = PriorityQueue[tuple[int, Position]]()
            q.put((0, next(_ for _ in stars)))
            seen = set[Position]()
            dist = 0
            while not q.empty():
                d, s = q.get()
                if s in seen:
                    continue
                dist += d
                seen.add(s)
                for n in stars:
                    if n in seen:
                        continue
                    md = n.manhattan_distance(s)
                    if md < 6:
                        q.put((n.manhattan_distance(s), n))
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
