#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 12
#

import sys

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

CATAPULTS = {(Position(1, 1), 1), (Position(1, 2), 2), (Position(1, 3), 3)}


class Solution(SolutionBase[Output1, Output2, Output3]):

    def parse(self, input: InputData) -> dict[Position, int]:
        return {
            Position(x, len(input) - y - 1): 1 if input[y][x] == "T" else 2
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
            for power in range(max_power):
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
        return 0

    @ec_samples(
        (
            ("part_1", TEST1, 13),
            ("part_2", TEST2, 22),
            ("part_3", TEST1, 0),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 12)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
