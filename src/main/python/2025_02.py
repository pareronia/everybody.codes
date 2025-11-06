#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 2
#

import sys

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.common import log

Output1 = str
Output2 = int
Output3 = int

TEST1 = """\
A=[25,9]
"""
TEST2 = """\
A=[35300,-64910]
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input_data: InputData) -> Output1:
        x, y = map(int, input_data[0][:-1][3:].split(","))
        a, b = 0, 0
        for _ in range(3):
            a, b = a * a - b * b, a * b + b * a
            a, b = a // 10, b // 10
            a, b = a + x, b + y
        return f"[{a},{b}]"

    def part_2(self, input_data: InputData) -> Output2:
        x, y = map(int, input_data[0][:-1][3:].split(","))
        ans = 0
        cnt = 0
        for yy in range(y, y + 1010, 10):
            for xx in range(x, x + 1010, 10):
                a, b = 0, 0
                cnt += 1
                for _ in range(100):
                    a, b = a * a - b * b, a * b + b * a
                    a = a // 100_000 if a > 0 else -((-a) // 100_000)
                    b = b // 100_000 if b > 0 else -((-b) // 100_000)
                    a, b = a + xx, b + yy
                    if not (
                        -1_000_000 <= a <= 1_000_000
                        and -1_000_000 <= b <= 1_000_000
                    ):
                        break
                else:
                    ans += 1
        log(cnt)
        return ans

    def part_3(self, input_data: InputData) -> Output3:
        x, y = map(int, input_data[0][:-1][3:].split(","))
        log((x, y))
        ans = 0
        cnt = 0
        for yy in range(y, y + 1001, 1):
            for xx in range(x, x + 1001, 1):
                a, b = 0, 0
                cnt += 1
                for _ in range(100):
                    a, b = a * a - b * b, a * b + b * a
                    a = a // 100_000 if a > 0 else -((-a) // 100_000)
                    b = b // 100_000 if b > 0 else -((-b) // 100_000)
                    a, b = a + xx, b + yy
                    if not (
                        -1_000_000 <= a <= 1_000_000
                        and -1_000_000 <= b <= 1_000_000
                    ):
                        break
                else:
                    ans += 1
        log(cnt)
        return ans

    @ec_samples(
        (
            ("part_1", TEST1, "[357,862]"),
            ("part_2", TEST2, 4076),
            ("part_3", TEST2, 406954),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 2)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
