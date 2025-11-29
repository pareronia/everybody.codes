#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 20
#

import itertools
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Self

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.graph import bfs

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
T#TTT###T##
.##TT#TT##.
..T###T#T..
...##TT#...
....T##....
.....#.....
"""
TEST2 = """\
TTTTTTTTTTTTTTTTT
.TTTT#T#T#TTTTTT.
..TT#TTTETT#TTT..
...TT#T#TTT#TT...
....TTT#T#TTT....
.....TTTTTT#.....
......TT#TT......
.......#TT.......
........S........
"""
TEST3 = """\
T####T#TTT##T##T#T#
.T#####TTTT##TTT##.
..TTTT#T###TTTT#T..
...T#TTT#ETTTT##...
....#TT##T#T##T....
.....#TT####T#.....
......T#TT#T#......
.......T#TTT.......
........TT#........
.........S.........
"""

Cell = tuple[int, int]
RotatedCell = tuple[Cell, int]


def parity(cell: Cell) -> bool:
    return cell[0] % 2 == cell[1] % 2


@dataclass(frozen=True)
class Triangle:
    cells: set[Cell]
    start: Cell
    end: Cell

    @classmethod
    def from_input(cls, input_data: InputData) -> Self:
        tr = set[Cell]()
        start = end = (-1, -1)
        for r in range(len(input_data)):
            for c in range(len(input_data[r])):
                match input_data[r][c]:
                    case "S":
                        start = (r, c)
                    case "E":
                        end = (r, c)
                    case "T":
                        pass
                    case _:
                        continue
                tr.add((r, c))
        return cls(tr, start or None, end)

    @classmethod
    def from_input_rotate_120(cls, input_data: InputData) -> Self:
        h, w = len(input_data), len(input_data[0])
        tr = set[Cell]()
        r, c, rrr = h - 1, w // 2, 0
        while r >= 0 and c < w:
            rr, cc, ccc = r, c, rrr
            while rr >= 0 and cc >= 2 * abs((w // 2) - c):
                match input_data[rr][cc]:
                    case "E":
                        end = (rrr, ccc)
                        tr.add((rrr, ccc))
                    case "S" | "T":
                        tr.add((rrr, ccc))
                    case _:
                        pass
                if parity((rr, cc)):
                    rr -= 1
                else:
                    cc -= 1
                ccc += 1
            rrr += 1
            r, c = r - 1, c + 1
        return cls(tr, (-1, -1), end)

    @classmethod
    def from_input_rotate_240(cls, input_data: InputData) -> Self:
        h, w = len(input_data), len(input_data[0])
        tr = set[Cell]()
        for rrr, c in enumerate(range(w - 1, -1, -2)):
            rr, cc, ccc = 0, c, rrr
            while rr < h and cc >= 0:
                match input_data[rr][cc]:
                    case "E":
                        end = (rrr, ccc)
                        tr.add((rrr, ccc))
                    case "S" | "T":
                        tr.add((rrr, ccc))
                    case _:
                        pass
                if parity((rr, cc)):
                    cc -= 1
                else:
                    rr += 1
                ccc += 1
        return cls(tr, (-1, -1), end)


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input_data: InputData) -> Output1:
        triangle = Triangle.from_input(input_data)
        return sum(
            sum(
                (
                    (r, c + 1) in triangle.cells,
                    not parity((r, c)) and (r + 1, c) in triangle.cells,
                )
            )
            for r, c in triangle.cells
        )

    def solve_maze(self, triangles: list[Triangle]) -> int:
        def adjacent(cell: RotatedCell) -> Iterator[RotatedCell]:
            (r, c), lyr = cell
            nlyr = lyr if len(triangles) == 1 else (lyr + 1) % len(triangles)
            for n in itertools.chain(
                ((r, c), (r + (-1 if parity((r, c)) else 1), c)),
                ((r, c + dc) for dc in (-1, 1)),
            ):
                if n in triangles[nlyr].cells:
                    yield (n, nlyr)

        return bfs(
            start=(triangles[0].start, 0),
            is_end=lambda cell: cell[0] == triangles[cell[1]].end,
            adjacent=adjacent,
        )

    def part_2(self, input_data: InputData) -> Output2:
        return self.solve_maze([Triangle.from_input(input_data)])

    def part_3(self, input_data: InputData) -> Output3:
        return self.solve_maze(
            [
                Triangle.from_input(input_data),
                Triangle.from_input_rotate_120(input_data),
                Triangle.from_input_rotate_240(input_data),
            ]
        )

    @ec_samples(
        (
            ("part_1", TEST1, 7),
            ("part_2", TEST2, 32),
            ("part_3", TEST3, 23),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 20)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
