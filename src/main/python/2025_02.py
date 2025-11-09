#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 2
#

import itertools
import sys
from collections.abc import Iterator

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

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
    def calculate(
        self, x: int, y: int, iterations: int, factor: int
    ) -> Iterator[tuple[int, int]]:
        a, b = 0, 0
        for _ in range(iterations):
            a, b = (
                x + int((a * a - b * b) / factor),
                y + int((2 * a * b) / factor),
            )
            yield a, b

    def count(self, points: Iterator[tuple[int, int]]) -> int:
        return sum(
            all(
                abs(a) <= 1_000_000 and abs(b) <= 1_000_000
                for a, b in self.calculate(
                    x, y, iterations=100, factor=100_000
                )
            )
            for x, y in points
        )

    def part_1(self, input_data: InputData) -> Output1:
        x, y = map(int, input_data[0][:-1][3:].split(","))
        a, b = list(self.calculate(x, y, iterations=3, factor=10))[-1]
        return f"[{a},{b}]"

    def part_2(self, input_data: InputData) -> Output2:
        x, y = map(int, input_data[0][:-1][3:].split(","))
        return self.count(
            itertools.product(range(x, x + 1010, 10), range(y, y + 1010, 10))
        )

    def part_3(self, input_data: InputData) -> Output3:
        x, y = map(int, input_data[0][:-1][3:].split(","))
        return self.count(
            itertools.product(range(x, x + 1001), range(y, y + 1001))
        )

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
