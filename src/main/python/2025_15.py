#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 15
#

import sys

from ec.common import Direction
from ec.common import InputData
from ec.common import SolutionBase
from ec.common import Turn
from ec.common import ec_samples
from ec.graph import bfs_path

Output1 = int
Output2 = int
Output3 = int
Cell = tuple[int, int]

TEST1 = """\
R3,R4,L3,L4,R3,R6,R9
"""
TEST2 = """\
L6,L3,L6,R3,L6,L3,L3,R6,L6,R6,L6,L6,R3,L3,L3,R3,R3,L6,L6,L3
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input_data: InputData) -> Output1:
        wall = list[Cell]()
        pos = (0, 0)
        d = Direction.UP
        for s in input_data[0].split(","):
            turn = Turn.from_str(s[0])
            a = int(s[1:])
            d = d.turn(turn)
            for _ in range(a):
                pos = (pos[0] + d.x, pos[1] + d.y)
                wall.append(pos)
        end = wall[-1]
        wall = wall[:-1]
        ans, _ = bfs_path(
            (0, 0),
            lambda cell: cell == end,
            lambda cell: (
                (cell[0] + dx, cell[1] + dy)
                for dx, dy in {(1, 0), (-1, 0), (0, 1), (0, -1)}
                if (cell[0] + dx, cell[1] + dy) not in wall
            ),
        )
        return ans

    def part_2(self, input_data: InputData) -> Output2:
        w = list[Cell]()
        pos = (0, 0)
        d = Direction.UP
        for s in input_data[0].split(","):
            turn = Turn.from_str(s[0])
            a = int(s[1:])
            d = d.turn(turn)
            for _ in range(a):
                pos = (pos[0] + d.x, pos[1] + d.y)
                w.append(pos)
        end = w[-1]
        wall = set(w[:-1])
        ans, _ = bfs_path(
            (0, 0),
            lambda cell: cell == end,
            lambda cell: (
                (cell[0] + dx, cell[1] + dy)
                for dx, dy in {(1, 0), (-1, 0), (0, 1), (0, -1)}
                if (cell[0] + dx, cell[1] + dy) not in wall
            ),
        )
        return ans

    def part_3(self, _input_data: InputData) -> Output3:
        return 0

    @ec_samples(
        (
            ("part_1", TEST1, 6),
            ("part_1", TEST2, 16),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 15)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
