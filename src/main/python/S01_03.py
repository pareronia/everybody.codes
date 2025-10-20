#! /usr/bin/env python3
#
# everybody.codes S01 Quest 3
#

import itertools
import math
import sys

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.common import log

Output1 = int
Output2 = int
Output3 = int

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


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input_data: InputData) -> Output1:
        snails = list[tuple[int, int]]()
        for line in input_data:
            x, y = map(int, (sp.split("=")[1] for sp in line.split()))
            snails.append((x, y))
        ans = 0
        for x, y in snails:
            s = x + y
            m = s - 1
            t = 100 % m
            xx, yy = x, y
            for _ in range(t):
                xx, yy = xx + 1, yy - 1
                if yy < 1:
                    xx = 1
                    yy = s - xx
            ans += xx + 100 * yy
        return ans

    def part_2(self, input_data: InputData) -> Output2:
        snails = list[tuple[int, int]]()
        for line in input_data:
            x, y = map(int, (sp.split("=")[1] for sp in line.split()))
            s = x + y
            m = s - 1
            xx, yy = x, y
            for i in range(m):
                if yy == 1:
                    snails.append((i, m))
                    break
                xx, yy = xx + 1, yy - 1
                if yy < 1:
                    xx = 1
                    yy = s - xx
        return next(
            i
            for i in itertools.count()
            if all(i % period == offset for offset, period in snails)
        )

    def part_3(self, input_data: InputData) -> Output3:  # noqa:C901
        log("part 3")
        snails = list[tuple[int, int]]()
        for line in input_data:
            x, y = map(int, (sp.split("=")[1] for sp in line.split()))
            s = x + y
            m = s - 1
            xx, yy = x, y
            for i in range(m):
                if yy == 1:
                    snails.append((i, m))
                    break
                xx, yy = xx + 1, yy - 1
                if yy < 1:
                    xx = 1
                    yy = s - xx
        log(snails)

        def chinese_remainder(
            periods: tuple[int, ...], offsets: tuple[int, ...]
        ) -> int:
            def mul_inv(a: int, b: int) -> int:
                b0 = b
                x0, x1 = 0, 1
                if b == 1:
                    return 1
                while a > 1:
                    q = a // b
                    a, b = b, a % b
                    x0, x1 = x1 - q * x0, x0
                if x1 < 0:
                    x1 += b0
                return x1

            the_sum = 0
            prod = math.prod(periods)
            for period, offset in zip(periods, offsets, strict=True):
                p = prod // period
                the_sum += offset * mul_inv(p, period) * p
            return the_sum % prod

        offset = tuple(s[0] for s in snails)
        periods = tuple(s[1] for s in snails)
        return chinese_remainder(periods, offset)

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
