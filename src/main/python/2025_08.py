#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 8
#

import itertools
import sys
from collections import defaultdict

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
            abs(a - b) == nails // 2
            for a, b in itertools.pairwise(map(int, input_data[0].split(",")))
        )

    def part_1(self, input_data: InputData) -> Output1:
        return self.solve_1(input_data, 32)

    def part_2(self, input_data: InputData) -> Output2:
        threads = set[tuple[int, int]]()
        ans = 0
        for a, b in map(
            sorted, itertools.pairwise(map(int, input_data[0].split(",")))
        ):
            ans += sum(
                (t1 < a < t2 < b) or (a < t1 < b < t2) for t1, t2 in threads
            )
            threads.add((a, b))
        return ans

    def solve_3(self, input_data: InputData, nails: int) -> int:
        threads = defaultdict[int, list[int]](list)
        for a, b in itertools.pairwise(map(int, input_data[0].split(","))):
            threads[a].append(b)
            threads[b].append(a)
        ans = 0
        for a in range(1, nails + 1):
            cnt = 0
            for b in range(a + 2, nails + 1):
                cnt -= sum(a < c < b - 1 for c in threads[b])
                cnt += sum(not (a <= c <= b) for c in threads[b - 1])
                ans = max(ans, cnt + sum(c == b for c in threads[a]))
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
