#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 15
#

import sys
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Self

from ec.common import Direction
from ec.common import InputData
from ec.common import SolutionBase
from ec.common import Turn
from ec.common import ec_samples
from ec.graph import bfs_with_cost

Output1 = int
Output2 = int
Output3 = int
Cell = tuple[int, int]

TEST1 = "R3,R4,L3,L4,R3,R6,R9"
TEST2 = "L6,L3,L6,R3,L6,L3,L3,R6,L6,R6,L6,L6,R3,L3,L3,R3,R3,L6,L6,L3"


@dataclass
class Instruction:
    turn: Turn
    amount: int

    @classmethod
    def from_input(cls, string: str) -> Self:
        return cls(Turn.from_str(string[0]), int(string[1:]))


@dataclass
class CompressedMaze:
    grid: list[list[str]]
    start: Cell
    end: Cell
    rows: list[int]
    cols: list[int]

    @classmethod
    def from_instructions(cls, instructions: list[Instruction]) -> Self:
        tmp_rows = list[int]()
        tmp_cols = list[int]()
        cell = (0, 0)
        tmp_rows.append(0)
        tmp_cols.append(0)
        direction = Direction.UP
        for instruction in instructions:
            direction = direction.turn(instruction.turn)
            cell = (
                cell[0] - instruction.amount * direction.y,
                cell[1] + instruction.amount * direction.x,
            )
            if direction.is_horizontal():
                tmp_cols.append(cell[1])
                tmp_cols.append(cell[1] + direction.x)
                tmp_rows.append(cell[0] - 1)
                tmp_rows.append(cell[0] + 1)
            else:
                tmp_cols.append(cell[1] - 1)
                tmp_cols.append(cell[1] + 1)
                tmp_rows.append(cell[0])
                tmp_rows.append(cell[0] - direction.y)
        rows = sorted(set(tmp_rows))
        cols = sorted(set(tmp_cols))
        c_rows = {rows[i]: i for i in range(len(rows))}
        c_cols = {cols[i]: i for i in range(len(cols))}
        start = (c_rows[0], c_cols[0])
        end = (c_rows[cell[0]], c_cols[cell[1]])
        grid = cls.build_grid(instructions, c_rows, c_cols)
        grid[start[0]][start[1]] = "S"
        grid[end[0]][end[1]] = "E"
        return cls(grid, start, end, rows, cols)

    @classmethod
    def build_grid(
        cls,
        instructions: list[Instruction],
        c_rows: dict[int, int],
        c_cols: dict[int, int],
    ) -> list[list[str]]:
        grid = [["."] * len(c_cols) for _ in range(len(c_rows))]
        cell = (0, 0)
        direction = Direction.UP
        for instruction in instructions:
            direction = direction.turn(instruction.turn)
            nxt = (
                cell[0] - instruction.amount * direction.y,
                cell[1] + instruction.amount * direction.x,
            )
            if direction.is_horizontal():
                col_0 = min(c_cols[cell[1]], c_cols[nxt[1]])
                col_1 = max(c_cols[cell[1]], c_cols[nxt[1]])
                row_0 = c_rows[cell[0]]
                for i in range(col_0, col_1 + 1):
                    grid[row_0][i] = "#"
            else:
                row_0 = min(c_rows[cell[0]], c_rows[nxt[0]])
                row_1 = max(c_rows[cell[0]], c_rows[nxt[0]])
                col_0 = c_cols[cell[1]]
                for i in range(row_0, row_1 + 1):
                    grid[i][col_0] = "#"
            cell = nxt
        return grid

    def solve(self) -> int:
        def adjacent(cell: Cell) -> Iterator[Cell]:
            for direction in Direction.capitals():
                nxt = (cell[0] - direction.y, cell[1] + direction.x)
                if (
                    0 <= nxt[0] < len(self.grid)
                    and 0 <= nxt[1] < len(self.grid[0])
                    and self.grid[nxt[0]][nxt[1]] != "#"
                ):
                    yield nxt

        def cost(curr: Cell, nxt: Cell) -> int:
            curr_o = (self.rows[curr[0]], self.cols[curr[1]])
            nxt_o = (self.rows[nxt[0]], self.cols[nxt[1]])
            return abs(curr_o[0] - nxt_o[0]) + abs(curr_o[1] - nxt_o[1])

        return bfs_with_cost(
            self.start, lambda cell: cell == self.end, adjacent, cost
        )


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, input_data: InputData) -> int:
        instructions = [
            Instruction.from_input(line) for line in input_data[0].split(",")
        ]
        return CompressedMaze.from_instructions(instructions).solve()

    def part_1(self, input_data: InputData) -> Output1:
        return self.solve(input_data)

    def part_2(self, input_data: InputData) -> Output2:
        return self.solve(input_data)

    def part_3(self, input_data: InputData) -> Output3:
        return self.solve(input_data)

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
