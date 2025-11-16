#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 10
#

import sys
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cache
from typing import Self

from ec.common import InputData
from ec.common import SolutionBase

TEST1 = """\
...SSS.......
.S......S.SS.
..S....S...S.
..........SS.
..SSSS...S...
.....SS..S..S
SS....D.S....
S.S..S..S....
....S.......S
.SSS..SS.....
.........S...
.......S....S
SS.....S..S..
"""
TEST2 = """\
...SSS##.....
.S#.##..S#SS.
..S.##.S#..S.
.#..#S##..SS.
..SSSS.#.S.#.
.##..SS.#S.#S
SS##.#D.S.#..
S.S..S..S###.
.##.S#.#....S
.SSS.#SS..##.
..#.##...S##.
.#...#.S#...S
SS...#.S.#S..
"""
TEST3 = """\
SSS
..#
#.#
#D.
"""
TEST4 = """\
SSS
..#
..#
.##
.D#
"""
TEST5 = """\
..S..
.....
..#..
.....
..D..
"""
TEST6 = """\
.SS.S
#...#
...#.
##..#
.####
##D.#
"""
TEST7 = """\
SSS.S
.....
#.#.#
.#.#.
#.D.#
"""

Output1 = int
Output2 = int
Output3 = int
Cell = tuple[int, int]
State = tuple[tuple[int | None, ...], Cell]


@dataclass(frozen=True)
class Board:
    h: int
    w: int
    dragon: Cell
    sheep: set[Cell]
    hides: set[Cell]

    @classmethod
    def from_input(cls, input_data: InputData) -> Self:
        h, w = len(input_data), len(input_data[0])
        sheep = set[Cell]()
        hides = set[Cell]()
        for r in range(h):
            for c in range(w):
                match input_data[r][c]:
                    case "D":
                        dragon = (r, c)
                    case "S":
                        sheep.add((r, c))
                    case "#":
                        hides.add((r, c))
        return cls(h, w, dragon, sheep, hides)

    def knight_moves(self, start: Cell) -> Iterator[Cell]:
        r, c = start
        for dr, dc in {
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        }:
            rr, cc = r + dr, c + dc
            if 0 <= rr < self.h and 0 <= cc < self.w:
                yield rr, cc


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve_1(self, input_data: InputData, cnt: int) -> Output1:
        board = Board.from_input(input_data)
        moves = {board.dragon}
        for _ in range(cnt):
            moves |= {m for move in moves for m in board.knight_moves(move)}
        return sum(m in board.sheep for m in moves)

    def part_1(self, input_data: InputData) -> Output1:
        return self.solve_1(input_data, cnt=4)

    def solve_2(self, input_data: InputData, cnt: int) -> Output2:
        board = Board.from_input(input_data)
        moves, sheep = {board.dragon}, set(board.sheep)
        ans = 0
        for _ in range(cnt):
            moves = {m for move in moves for m in board.knight_moves(move)}
            for d in [0, 1]:
                sheep = {(r + d, c) for r, c in sheep if r < board.h - 1}
                eaten = sheep & moves - board.hides
                ans += len(eaten)
                sheep -= eaten
        return ans

    def part_2(self, input_data: InputData) -> Output2:
        return self.solve_2(input_data, cnt=20)

    def part_3(self, input_data: InputData) -> Output3:  # noqa:C901
        def dragon_moves(state: State) -> Iterator[State]:
            sheep, dragon = state
            for m in board.knight_moves(dragon):
                if m not in board.hides:
                    new_sheep = tuple(
                        sheep[c] if (sheep[c], c) != m else None
                        for c in range(board.w)
                    )
                else:
                    new_sheep = sheep
                yield (new_sheep, m)

        def sheep_moves(state: State) -> Iterator[State]:
            sheep, dragon = state
            ok = False
            for cs in range(board.w):
                rs = sheep[cs]
                if rs is None:
                    continue
                ns = (rs + 1, cs)
                if ns[0] == board.h or ns[0] == exits[ns[1]]:
                    ok = True
                elif ns != dragon or ns in board.hides:
                    ok = True
                    new_sheep = tuple(
                        sheep[c] if (sheep[c], c) != (rs, cs) else ns[0]
                        for c in range(board.w)
                    )
                    yield (new_sheep, dragon)
            if not ok:
                yield state

        @cache
        def dfs(state: State, sheep_turn: bool) -> int:  # noqa:FBT001
            if all(state[0][c] is None for c in range(board.w)):
                return 1
            if sheep_turn:
                return sum(
                    dfs(s, sheep_turn=False) for s in sheep_moves(state)
                )
            return sum(dfs(s, sheep_turn=True) for s in dragon_moves(state))

        board = Board.from_input(input_data)
        sheep = tuple(
            next((r for r in range(board.h) if (r, c) in board.sheep), None)
            for c in range(board.w)
        )
        exits = tuple(
            next(
                (
                    r
                    for r in range(board.h)
                    if all((rr, c) in board.hides for rr in range(r, board.h))
                ),
                None,
            )
            for c in range(board.w)
        )
        return dfs((sheep, board.dragon), sheep_turn=True)

    def samples(self) -> None:
        assert self.solve_1(tuple(TEST1.splitlines()), cnt=3) == 27
        assert self.solve_2(tuple(TEST2.splitlines()), cnt=3) == 27
        assert self.part_3(tuple(TEST3.splitlines())) == 15
        assert self.part_3(tuple(TEST4.splitlines())) == 8
        assert self.part_3(tuple(TEST5.splitlines())) == 44
        assert self.part_3(tuple(TEST6.splitlines())) == 4406
        assert self.part_3(tuple(TEST7.splitlines())) == 13033988838


solution = Solution(2025, 10)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
