#! /usr/bin/env python3
#
# everybody.codes S01 Quest 3
#

import itertools
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Self

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.math import chinese_remainder

TEST1 = """\
x=1 y=2
x=2 y=3
x=3 y=4
x=4 y=4
"""
TEST2 = """\
x=12 y=2
x=8 y=4
x=7 y=1
x=1 y=5
x=1 y=3
"""
TEST3 = """\
x=3 y=1
x=3 y=9
x=1 y=5
x=4 y=10
x=5 y=3
"""


@dataclass(frozen=True)
class Snail:
    x: int
    y: int

    @classmethod
    def from_input(cls, s: str) -> Self:
        return cls(*map(int, (sp.split("=")[1] for sp in s.split())))

    def crawl(self) -> Iterator[tuple[int, int]]:
        yield (self.x, self.y)
        xx, yy = self.x, self.y
        for _ in itertools.count():
            xx, yy = xx + 1, yy - 1
            if yy < 1:
                xx = 1
                yy = self.x + self.y - 1
            yield (xx, yy)

    def crawl_for(self, time: int) -> tuple[int, int]:
        t = time % self.period
        return next(itertools.islice(self.crawl(), t, t + 1))

    @property
    def period(self) -> int:
        return self.x + self.y - 1

    @property
    def offset(self) -> int:
        it = self.crawl()
        for i in range(self.period):
            if next(it)[1] == 1:
                return i
        raise AssertionError


Output1 = int
Output2 = int
Output3 = int


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input_data: InputData) -> Output1:
        return sum(
            x + 100 * y
            for x, y in (
                snail.crawl_for(100)
                for snail in (Snail.from_input(line) for line in input_data)
            )
        )

    def part_2(self, input_data: InputData) -> Output2:
        return self.part_3(input_data)

    def part_3(self, input_data: InputData) -> Output3:
        snails = [Snail.from_input(line) for line in input_data]
        return chinese_remainder(
            tuple(s.period for s in snails), tuple(s.offset for s in snails)
        )

    @ec_samples(
        (
            ("part_1", TEST1, 1310),
            ("part_2", TEST2, 14),
            ("part_2", TEST3, 13659),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(1, 3)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
