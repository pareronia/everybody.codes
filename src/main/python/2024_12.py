#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 12
#

import sys

from ec.common import Cell
from ec.common import Direction
from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.common import log

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


class Solution(SolutionBase[Output1, Output2, Output3]):

    def calc_path(self, catapult: Cell, power: int) -> set[Cell]:
        ans = set[Cell]()
        c = Cell(catapult.row, catapult.col)
        for _ in range(power):
            c = c.at(Direction.RIGHT_AND_UP)
            ans.add(c)
        for _ in range(power):
            c = c.at(Direction.RIGHT)
            ans.add(c)
        while c.row < 120:
            c = c.at(Direction.RIGHT_AND_DOWN)
            ans.add(c)
        return ans

    def part_1(self, input: InputData) -> Output1:
        targets = []
        for r, line in enumerate(list(input)[1:], start=100):
            for c, ch in enumerate(line[1:]):
                if ch == "T":
                    targets.append(Cell(r, c))
        log(targets)

        ans = 0
        targets = sorted(targets, key=lambda t: t.row)
        while targets:
            t = targets.pop(0)
            for catapult, segment in {
                (Cell(102, 0), 1),
                (Cell(101, 0), 2),
                (Cell(100, 0), 3),
            }:
                for power in range(20):
                    path = self.calc_path(catapult, power)
                    if t in path:
                        break
                else:
                    continue
                log(f"Hit: {t}")
                ans += segment * power
        return ans

    def part_2(self, input: InputData) -> Output2:
        targets = []
        for r, line in enumerate(list(input)[1:], start=100):
            for c, ch in enumerate(line[1:]):
                if ch in {"H", "T"}:
                    targets.append((Cell(r, c), ch))

        paths = dict[tuple[Cell, ...], int]()
        for catapult, segment in {
            (Cell(102, 0), 1),
            (Cell(101, 0), 2),
            (Cell(100, 0), 3),
        }:
            for power in range(50):
                path = self.calc_path(catapult, power)
                paths[tuple(path)] = power * segment
        targets = sorted(targets, key=lambda t: t[0].row)
        ans = 0
        cnt = 0
        while targets:
            t, ch = targets.pop(0)
            x = [a for a in paths.items() if t in a[0]]
            assert len(x) == 1
            for p in paths.keys():
                if t in p:
                    break
            else:
                continue
            log(f"Hit: {t}")
            cnt += 1
            if ch == "H":
                ans += 2 * paths[p]
            else:
                ans += paths[p]
        log(cnt)
        return ans

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
