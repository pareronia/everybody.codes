#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 13
#

import sys

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
72
58
47
61
67
"""
TEST2 = """\
10-15
12-13
20-21
19-23
30-37
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, input_data: InputData, positions: int) -> int:
        d = [(1, 1)]
        for i, line in enumerate(input_data):
            start, end = map(int, line.split("-"))
            if i % 2 == 0:
                d.append((start, end))
            else:
                d.insert(0, (end, start))
        home_idx = d.index((1, 1))
        home = sum(abs(d[i][0] - d[i][1]) + 1 for i in range(home_idx))
        size = sum(abs(start - end) + 1 for start, end in d)
        target = (home + positions) % size
        cnt = 0
        for i in range(len(d)):
            start, end = d[i % len(d)]
            nxt = cnt + abs(start - end) + 1
            if nxt > target:
                if start < end:
                    return start + target - cnt
                return start - (target - cnt)
            cnt = nxt
        raise AssertionError

    def part_1(self, input_data: InputData) -> Output1:
        d = [1]
        for i, line in enumerate(input_data):
            if i % 2 == 0:
                d.append(int(line))
            else:
                d.insert(0, int(line))
        return d[(d.index(1) + 2025) % len(d)]

    def part_2(self, input_data: InputData) -> Output2:
        return self.solve(input_data, 20252025)

    def part_3(self, input_data: InputData) -> Output3:
        return self.solve(input_data, 202520252025)

    @ec_samples(
        (
            ("part_1", TEST1, 67),
            ("part_2", TEST2, 30),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 13)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
