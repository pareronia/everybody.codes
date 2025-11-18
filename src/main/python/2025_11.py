#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 11
#

import itertools
import sys

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.common import log

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
9
1
1
4
9
6
"""
TEST2 = """\
805
706
179
48
158
150
232
885
598
524
423
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input_data: InputData) -> Output1:
        d = [int(line) for line in input_data]
        rounds = 0
        while rounds < 10 and any(
            d[i] > d[j] for i, j in itertools.pairwise(range(len(d)))
        ):
            log(d)
            for i, j in itertools.pairwise(range(len(d))):
                if d[i] > d[j]:
                    d[i] -= 1
                    d[j] += 1
            rounds += 1
        while rounds < 10 and any(
            d[i] < d[j] for i, j in itertools.pairwise(range(len(d)))
        ):
            log(d)
            for i, j in itertools.pairwise(range(len(d))):
                if d[i] < d[j]:
                    d[i] += 1
                    d[j] -= 1
            rounds += 1
        log(d)
        return sum(i * dd for i, dd in enumerate(d, start=1))

    def part_2(self, input_data: InputData) -> Output2:
        d = [int(line) for line in input_data]
        rounds = 0
        while any(d[i] > d[j] for i, j in itertools.pairwise(range(len(d)))):
            for i, j in itertools.pairwise(range(len(d))):
                if d[i] > d[j]:
                    d[i] -= 1
                    d[j] += 1
            rounds += 1
        tot = sum(d)
        assert tot % len(d) == 0
        avg = tot // len(d)
        return rounds + sum(abs(avg - dd) for dd in d) // 2

    def part_3(self, input_data: InputData) -> Output3:
        d = [int(line) for line in input_data]
        rounds = 0
        while any(d[i] > d[j] for i, j in itertools.pairwise(range(len(d)))):
            for i, j in itertools.pairwise(range(len(d))):
                if d[i] > d[j]:
                    d[i] -= 1
                    d[j] += 1
            rounds += 1
        tot = sum(d)
        assert tot % len(d) == 0
        avg = tot // len(d)
        return rounds + sum(abs(avg - dd) for dd in d) // 2

    @ec_samples(
        (
            ("part_1", TEST1, 109),
            ("part_2", TEST1, 11),
            ("part_2", TEST2, 1579),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 11)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
