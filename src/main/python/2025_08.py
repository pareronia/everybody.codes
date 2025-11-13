#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 8
#

import itertools
import sys

from ec.common import InputData
from ec.common import SolutionBase

Output1 = int
Output2 = int
Output3 = int

TEST1 = "1,5,2,6,8,4,1,7,3"
TEST2 = "1,5,2,6,8,4,1,7,3,5,7,8,2"
TEST3 = "1,5,2,6,8,4,1,7,3,6"


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve_1(self, input_data: InputData, nails: int) -> int:
        return sum(
            1
            for a, b in itertools.pairwise(map(int, input_data[0].split(",")))
            if abs(a - b) == nails // 2
        )

    def part_1(self, input_data: InputData) -> Output1:
        return self.solve_1(input_data, 32)

    def part_2(self, input_data: InputData) -> Output2:
        def cross(t1: int, t2: int, a: int, b: int) -> bool:
            return (a > t1 and a < t2 and b > t2) or (
                b > t1 and b < t2 and a < t1
            )

        threads = set[tuple[int, int]]()
        ans = 0
        for t in itertools.pairwise(map(int, input_data[0].split(","))):
            a, b = sorted(t)
            ans += sum(cross(t1, t2, a, b) for t1, t2 in threads)
            threads.add((a, b))
        return ans

    def solve_3(self, input_data: InputData, nails: int) -> int:
        def cross(t1: int, t2: int, a: int, b: int) -> bool:
            return (
                (t1 == a and t2 == b)
                or (a > t1 and a < t2 and b > t2)
                or (b > t1 and b < t2 and a < t1)
            )

        threads = list[tuple[int, int]]()
        for t in itertools.pairwise(map(int, input_data[0].split(","))):
            a, b = sorted(t)
            threads.append((a, b))
        ans = 0
        for i in range(1, nails + 1):
            for j in range(i + 1, nails + 1):
                ans = max(ans, sum(cross(t1, t2, i, j) for t1, t2 in threads))
        return ans

    def part_3(self, input_data: InputData) -> Output3:
        return self.solve_3(input_data, 256)

    def samples(self) -> None:
        assert self.solve_1(tuple(TEST1.splitlines()), 8) == 4
        assert self.part_2(tuple(TEST2.splitlines())) == 21
        assert self.solve_3(tuple(TEST3.splitlines()), 8) == 7


solution = Solution(2025, 8)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
