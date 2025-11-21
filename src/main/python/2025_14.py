#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 14
#

import sys
from collections.abc import Iterator
from functools import cache
from typing import cast

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.game_of_life import GameOfLife

Output1 = int
Output2 = int
Output3 = int
Cell = tuple[int, int]
Alive = tuple[tuple[bool, ...], ...]

SYMBOL = "#"
DIAGONALS = {(-1, -1), (1, 1), (1, -1), (-1, 1)}

TEST1 = """\
.#.##.
##..#.
..##.#
.#.##.
.###..
###.##
"""
TEST2 = """\
#......#
..#..#..
.##..##.
...##...
...##...
.##..##.
..#..#..
#......#
"""


class Rules(GameOfLife.Rules[Cell, Alive]):
    def alive(self, cell: Cell, count: int, alive: Alive) -> bool:
        row, col = cell
        return alive[row][col] == (count % 2 == 1)


class FixedGrid(GameOfLife.Universe[Cell, Alive]):
    def __init__(self, input_data: InputData) -> None:
        self.height = len(input_data)
        self.width = len(input_data[0])
        self.initial_alive = {
            (row, col)
            for row in range(self.height)
            for col in range(self.width)
            if input_data[row][col] == SYMBOL
        }

    def neighbour_count(self, alive: Alive) -> Iterator[tuple[Cell, int]]:
        return (
            (
                cell,
                sum(alive[row][col] for row, col in self.neighbours(cell)),
            )
            for cell in (
                (r, c) for r in range(self.height) for c in range(self.width)
            )
        )

    @cache  # noqa:B019
    def neighbours(self, cell: Cell) -> set[Cell]:
        row, col = cell
        return {
            (row + dr, col + dc)
            for dr, dc in DIAGONALS
            if 0 <= row + dr < self.height and 0 <= col + dc < self.width
        }


class SymmetricSquareGrid(GameOfLife.Universe[Cell, Alive]):
    def __init__(self, size: int) -> None:
        self.size = size

    def neighbour_count(self, alive: Alive) -> Iterator[tuple[Cell, int]]:
        def predicate(n: Cell) -> bool:
            row, col = n
            if row < self.size and col < self.size:
                return alive[row][col]
            if row == self.size and col == self.size:
                return alive[row - 1][col - 1]
            if row == self.size:
                return alive[row - 1][col]
            return alive[row][col - 1]

        return (
            (cell, sum(predicate(n) for n in self.neighbours(cell)))
            for cell in (
                (r, c) for r in range(self.size) for c in range(self.size)
            )
        )

    @cache  # noqa:B019
    def neighbours(self, cell: Cell) -> set[Cell]:
        r, c = cell
        return {
            (r + dr, c + dc)
            for dr, dc in DIAGONALS
            if r + dr >= 0 and c + dc >= 0
        }


class Solution(SolutionBase[Output1, Output2, Output3]):
    def key(self, cells: Iterator[Cell], size: int) -> Alive:
        ans = [[False] * size for _ in range(size)]
        for row, col in cells:
            ans[row][col] = True
        return tuple(tuple(_) for _ in ans)

    def count(self, alive: Alive) -> int:
        return sum(
            alive[row][col]
            for row in range(len(alive))
            for col in range(len(alive[row]))
        )

    def solve(self, input_data: InputData, rounds: int) -> int:
        grid = FixedGrid(input_data)
        gol = GameOfLife(
            self.key(iter(grid.initial_alive), len(input_data)),
            grid,
            Rules(),
            lambda s: self.key(s, len(input_data)),
        )
        ans = 0
        for _ in range(rounds):
            gol.next_generation()
            alive = cast("Alive", gol.alive)
            ans += self.count(alive)
        return ans

    def part_1(self, input_data: InputData) -> Output1:
        return self.solve(input_data, rounds=10)

    def part_2(self, input_data: InputData) -> Output2:
        return self.solve(input_data, rounds=2025)

    def part_3(self, input_data: InputData) -> Output3:
        grid_sz = 34
        pattern_sz = len(input_data)
        offset = grid_sz // 2 - pattern_sz // 2
        pattern_on, pattern_off = set[Cell](), set[Cell]()
        for row in range(pattern_sz // 2):
            for col in range(pattern_sz // 2):
                cell = (row + offset, col + offset)
                if input_data[row][col] == SYMBOL:
                    pattern_on.add(cell)
                else:
                    pattern_off.add(cell)
        gol = GameOfLife(
            self.key(iter(set()), grid_sz // 2),
            SymmetricSquareGrid(grid_sz // 2),
            Rules(),
            lambda s: self.key(s, grid_sz // 2),
        )
        ans, i, rounds, period = 0, 0, 1_000_000_000, 4095
        while i < rounds:
            gol.next_generation()
            alive = cast("Alive", gol.alive)
            if all(alive[row][col] for row, col in pattern_on) and not any(
                alive[row][col] for row, col in pattern_off
            ):
                ans += 4 * self.count(alive)
            if i == period:
                cycles = rounds // period
                i *= cycles
                ans *= cycles
            else:
                i += 1
        return ans

    @ec_samples(
        (
            ("part_1", TEST1, 200),
            ("part_3", TEST2, 278388552),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 14)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
