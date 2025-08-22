#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 9
#

import sys
from collections.abc import Iterable

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
2
4
7
16
"""
TEST2 = """\
33
41
55
99
"""
TEST3 = """\
156488
352486
546212
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(
        self,
        input_data: Iterable[int],
        stamps: list[int],
        memo: dict[int, int],
    ) -> list[int]:
        def beetles(brightness: int) -> int:
            if brightness < 0:
                return sys.maxsize
            if brightness == 0:
                return 0
            if brightness in memo:
                return memo[brightness]
            best = sys.maxsize
            for stamp in stamps:
                best = min(best, beetles(brightness - stamp) + 1)
            memo[brightness] = best
            return best

        return [beetles(n) for n in input_data]

    def part_1(self, input_data: InputData) -> Output1:
        stamps = [10, 5, 3, 1]
        memo = dict[int, int]()
        return sum(b for b in self.solve(map(int, input_data), stamps, memo))

    def part_2(self, input_data: InputData) -> Output2:
        stamps = [1, 3, 5, 10, 15, 16, 20, 24, 25, 30]
        stamps.reverse()
        memo = dict[int, int]()
        return sum(b for b in self.solve(map(int, input_data), stamps, memo))

    def part_3(self, input_data: InputData) -> Output3:
        stamps = [1, 3, 5, 10, 15, 16, 20, 24, 25]
        stamps.extend([30, 37, 38, 49, 50, 74, 75, 100, 101])
        stamps.reverse()
        memo = dict[int, int]()
        ans = 0
        for brightness in map(int, input_data):
            ans_b = sys.maxsize
            b1 = brightness // 2
            b2 = brightness - b1
            while abs(b1 - b2) <= 100:
                ans_b = min(ans_b, sum(self.solve([b1, b2], stamps, memo)))
                b1, b2 = b1 - 1, b2 + 1
            ans += ans_b
        return ans

    @ec_samples(
        (
            ("part_1", TEST1, 10),
            ("part_2", TEST2, 10),
            ("part_3", TEST3, 10449),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 9)
sys.setrecursionlimit(10_000)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
