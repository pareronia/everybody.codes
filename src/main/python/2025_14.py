#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 14
#

import sys
from collections.abc import Iterable
from typing import cast

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.common import log
from ec.game_of_life import GameOfLife

Output1 = int
Output2 = int
Output3 = int
Cell = tuple[int, int]

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


class ECRules(GameOfLife.Rules[Cell]):
    def alive(self, cell: Cell, count: int, alive: Iterable[Cell]) -> bool:
        return (cell in alive and count % 2 == 1) or (
            cell not in alive and count % 2 == 0
        )


class FixedGrid(GameOfLife.Universe[Cell]):
    def __init__(self, input_data: InputData) -> None:
        self.height = len(input_data)
        self.width = len(input_data[0])
        self.initial_alive = {
            (r, c)
            for r in range(self.height)
            for c in range(self.width)
            if input_data[r][c] == "#"
        }

    def neighbour_count(self, alive: Iterable[Cell]) -> dict[Cell, int]:
        return {
            cell: sum(n in alive for n in self.neighbours(cell))
            for cell in (
                (r, c) for r in range(self.height) for c in range(self.width)
            )
        }

    def neighbours(self, cell: Cell) -> set[Cell]:
        r, c = cell
        return {
            (r + dr, c + dc)
            for dr, dc in {(-1, -1), (1, 1), (1, -1), (-1, 1)}
            if 0 <= r + dr < self.height and 0 <= c + dc < self.width
        }


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input_data: InputData) -> Output1:
        grid = FixedGrid(input_data)
        gol = GameOfLife(grid.initial_alive, grid, ECRules())
        ans = 0
        for _ in range(10):
            gol.next_generation()
            ans += len(set(gol.alive))
        return ans

    def part_2(self, input_data: InputData) -> Output2:
        grid = FixedGrid(input_data)
        gol = GameOfLife(grid.initial_alive, grid, ECRules())
        ans = 0
        for _ in range(2025):
            gol.next_generation()
            ans += len(set(gol.alive))
        return ans

    def part_3(self, input_data: InputData) -> Output3:
        def key(cells: set[Cell]) -> tuple[int, ...]:
            ans = [0] * grid_sz
            for cell in cells:
                ans[cell[0]] |= 1 << cell[1]
            return tuple(ans)

        grid_sz = 34
        pattern_sz = len(input_data)
        offset = grid_sz // 2 - pattern_sz // 2
        pattern_on = {
            (r + offset, c + offset)
            for r in range(pattern_sz)
            for c in range(pattern_sz)
            if input_data[r][c] == "#"
        }
        pattern_off = {
            (r + offset, c + offset)
            for r in range(pattern_sz)
            for c in range(pattern_sz)
            if input_data[r][c] == "."
        }
        grid = FixedGrid(tuple("." * grid_sz for _ in range(grid_sz)))
        gol = GameOfLife(grid.initial_alive, grid, ECRules())
        seen = set[tuple[int, ...]]()
        ans, i, rounds = 0, 0, 1_000_000_000
        while i < rounds:
            gol.next_generation()
            alive = set(gol.alive)
            k = key(cast("set[Cell]", alive))
            if k in seen:
                log(f"loop: {i}")
                p = rounds // i
                i = p * i
                seen.clear()
                ans *= p
                continue
            seen.add(k)
            if all(p in alive for p in pattern_on) and not any(
                p in alive for p in pattern_off
            ):
                log(f"match: {i}")
                ans += len(alive)
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
