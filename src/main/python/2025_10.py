#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 10
#

from __future__ import annotations

import sys
from collections import deque
from functools import cache
from typing import TYPE_CHECKING
from typing import TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterator

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

DRAGON_MOVES = {
    (-2, -1),
    (-2, 1),
    (-1, -2),
    (-1, 2),
    (1, -2),
    (1, 2),
    (2, -1),
    (2, 1),
}


T = TypeVar("T")
Output1 = int
Output2 = int
Output3 = int
Cell = tuple[int, int]
State = tuple[tuple[int | None, ...], Cell]


def flood_fill(
    start: T,
    adjacent: Callable[[T], Iterator[T]],
) -> set[T]:
    q: deque[T] = deque()
    q.append(start)
    seen: set[T] = set()
    while len(q) != 0:
        node = q.popleft()
        for n in adjacent(node):
            if n in seen:
                continue
            seen.add(n)
            q.append(n)
    return seen


class Solution(SolutionBase[Output1, Output2, Output3]):
    def adjacent(
        self, state: tuple[int, int, int], h: int, w: int, max_cnt: int
    ) -> Iterator[tuple[int, int, int]]:
        r, c, cnt = state
        for dr, dc in DRAGON_MOVES:
            rr, cc = r + dr, c + dc
            if cnt < max_cnt and 0 <= rr < h and 0 <= cc < w:
                yield rr, cc, cnt + 1

    def moves(self, input_data: InputData, max_cnt: int) -> set[Cell]:
        rd, cd = next(
            (r, c)
            for r in range(len(input_data))
            for c in range(len(input_data[r]))
            if input_data[r][c] == "D"
        )
        return {
            (r, c)
            for r, c, _ in flood_fill(
                (rd, cd, 0),
                lambda c: self.adjacent(
                    c, len(input_data), len(input_data[0]), max_cnt
                ),
            )
        }

    def solve_1(self, input_data: InputData, max_cnt: int) -> Output1:
        moves = self.moves(input_data, max_cnt)
        return sum(input_data[r][c] == "S" for r, c in moves)

    def part_1(self, input_data: InputData) -> Output1:
        return self.solve_1(input_data, max_cnt=4)

    def solve_2(self, input_data: InputData, max_cnt: int) -> Output2:
        h, w = len(input_data), len(input_data[0])
        rd, cd = next(
            (r, c)
            for r in range(h)
            for c in range(w)
            if input_data[r][c] == "D"
        )
        sheep = {
            (r, c)
            for r in range(h)
            for c in range(w)
            if input_data[r][c] == "S"
        }
        hides = {
            (r, c)
            for r in range(h)
            for c in range(w)
            if input_data[r][c] == "#"
        }
        ans = 0
        moves = {(rd, cd)}
        for _ in range(max_cnt):
            new_moves = set[Cell]()
            for rm, cm in moves:
                new_moves |= {
                    (r, c) for r, c, _ in (self.adjacent((rm, cm, 0), h, w, 1))
                }
            moves = new_moves
            eaten = sheep & moves - hides
            ans += len(eaten)
            sheep -= eaten
            sheep = {(r + 1, c) for r, c in sheep if r < h - 1}
            eaten = sheep & moves - hides
            ans += len(eaten)
            sheep -= eaten
        return ans

    def part_2(self, input_data: InputData) -> Output2:
        return self.solve_2(input_data, max_cnt=20)

    def part_3(self, input_data: InputData) -> Output3:  # noqa:C901
        h, w = len(input_data), len(input_data[0])
        dragon = next(
            (r, c)
            for r in range(h)
            for c in range(w)
            if input_data[r][c] == "D"
        )
        sheep = tuple(
            next((r for r in range(h) if input_data[r][c] == "S"), None)
            for c in range(w)
        )
        hides = {
            (r, c)
            for r in range(h)
            for c in range(w)
            if input_data[r][c] == "#"
        }

        def dragon_moves(state: State) -> list[State]:
            states = list[State]()
            moves = (
                (r, c)
                for r, c, _ in (
                    self.adjacent((state[1][0], state[1][1], 0), h, w, 1)
                )
            )
            for m in moves:
                if m not in hides:
                    new_sheep = tuple(
                        state[0][c] if (state[0][c], c) != m else None
                        for c in range(w)
                    )
                else:
                    new_sheep = tuple(state[0])
                states.append((new_sheep, m))
            return states

        def sheep_moves(state: State) -> list[State]:
            states = list[State]()
            ok = False
            for cs in range(w):
                rs = state[0][cs]
                if rs is None:
                    continue
                ns = (rs + 1, cs)
                if (ns[0] == h) or (
                    cs != dragon[1]
                    and all((r, cs) in hides for r in range(ns[0], h))
                ):
                    ok = True
                elif ns != state[1] or ns in hides:
                    ok = True
                    new_sheep = tuple(
                        state[0][c] if (state[0][c], c) != (rs, cs) else ns[0]
                        for c in range(w)
                    )
                    states.append((new_sheep, state[1]))
            if not ok:
                states.append((tuple(state[0]), state[1]))
            return states

        @cache
        def dfs(state: State, sheep_turn: bool) -> int:  # noqa:FBT001
            if all(state[0][c] is None for c in range(w)):
                return 1
            ans = 0
            if sheep_turn:
                for s in sheep_moves(state):
                    ans += dfs(s, sheep_turn=False)
            else:
                for s in dragon_moves(state):
                    ans += dfs(s, sheep_turn=True)
            return ans

        state = (sheep, dragon)
        return dfs(state, sheep_turn=True)

    def samples(self) -> None:
        assert self.solve_1(tuple(TEST1.splitlines()), max_cnt=3) == 27
        assert self.solve_2(tuple(TEST2.splitlines()), max_cnt=3) == 27
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
