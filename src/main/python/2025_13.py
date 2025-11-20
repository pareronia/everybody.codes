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
    def solve(self, input_data: tuple[str, ...], positions: int) -> int:
        d = [(1, 1, 1)]
        append, before, after = True, 0, 0
        for line in input_data:
            start, end = map(int, line.split("-"))
            sz = abs(start - end) + 1
            if append:
                d.append((start, end, sz))
                after += sz
            else:
                d.insert(0, (end, start, sz))
                before += sz
            append = not append
        tot, target = 0, (before + positions) % (before + 1 + after)
        for start, end, sz in d:
            nxt = tot + sz
            if nxt > target:
                return start + (
                    target - tot if start < end else -(target - tot)
                )
            tot = nxt
        raise AssertionError

    def part_1(self, input_data: InputData) -> Output1:
        return self.solve(tuple(s + "-" + s for s in input_data), 2025)

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
