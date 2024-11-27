#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 12
#

import sys
from collections import defaultdict

from ec.common import Direction
from ec.common import InputData
from ec.common import Position
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
.............
.C...........
.B......T....
.A......T.T..
=============
"""
TEST2 = """\
.............
.C...........
.B......H....
.A......T.H..
=============
"""
TEST3 = """\
6 5
6 7
10 5
5 5
"""

CATAPULTS = {(Position(0, 0), 1), (Position(0, 1), 2), (Position(0, 2), 3)}


class Solution(SolutionBase[Output1, Output2, Output3]):

    def parse(self, input: InputData) -> dict[Position, int]:
        return {
            Position(x - 1, len(input) - y - 2): 1 if input[y][x] == "T" else 2
            for x in range(len(input[0]))
            for y in range(len(input))
            if input[y][x] in {"H", "T"}
        }

    def at_my_signal_unleash_hell(
        self, targets: dict[Position, int], max_power: int
    ) -> int:
        def score(pos: Position, power: int, segment: int) -> int:
            if targets.get(pos, 0) != 0:
                score = power * segment * targets[pos]
                targets[pos] = 0
                return score
            return 0

        ans = 0
        for catapult in CATAPULTS:
            for power in range(1, max_power):
                pos = catapult[0]
                for _ in range(power):
                    pos = pos.at(Direction.RIGHT_AND_UP)
                    ans += score(pos, power, catapult[1])
                for _ in range(power):
                    pos = pos.at(Direction.RIGHT)
                    ans += score(pos, power, catapult[1])
                while pos.y > 0:
                    pos = pos.at(Direction.RIGHT_AND_DOWN)
                    ans += score(pos, power, catapult[1])
        return ans

    def part_1(self, input: InputData) -> Output1:
        targets = self.parse(input)
        return self.at_my_signal_unleash_hell(targets, 20)

    def part_2(self, input: InputData) -> Output2:
        targets = self.parse(input)
        return self.at_my_signal_unleash_hell(targets, 40)

    def part_3(self, input: InputData) -> Output3:
        """https://old.reddit.com/r/everybodycodes/comments/1gvap61/2024_q12_solution_spotlight/ly2adkc/"""  # noqa E501
        M = set[tuple[int, int]]()
        for line in input:
            x, y = map(int, line.split())
            M.add((x, y))

        class Projectile:
            def __init__(
                self, pos: tuple[int, int], hor: int, rank: int
            ) -> None:
                self.pos = pos
                self.hor = hor
                self.rank = rank

        G = [((0, 0), 0, 1), ((0, 1), 0, 2), ((0, 2), 0, 3)]
        P = list[Projectile]()
        D = defaultdict[tuple[int, int], int](lambda: sys.maxsize)
        ans = 0
        while len(M) > 0:
            for p in P:
                if p.hor > 0:
                    p.hor -= 1
                    p.pos = (p.pos[0] + 1, p.pos[1])
                else:
                    p.pos = (p.pos[0] + 1, p.pos[1] - 1)
            P = [p for p in P if p.pos[1] >= 0]
            for i in range(len(G)):
                pos, power, segment = G[i]
                g = ((pos[0] + 1, pos[1] + 1), power + 1, segment)
                G[i] = g
                P.append(Projectile((g[0][0], g[0][1]), g[1], g[1] * g[2]))
            for p in P:
                D[p.pos] = min(D[p.pos], p.rank)
            MM = set()
            for m in M:
                m = (m[0] - 1, m[1] - 1)
                if m in D:
                    ans += D[m]
                else:
                    MM.add(m)
            M = MM
        return ans

    @ec_samples(
        (
            ("part_1", TEST1, 13),
            ("part_2", TEST2, 22),
            ("part_3", TEST3, 13),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 12)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
