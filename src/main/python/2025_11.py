#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 11
#

import itertools
import sys

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

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
    def make_non_decreasing(self, ducks: list[int]) -> int:
        rounds = 0
        while (
            k := next(
                (
                    i
                    for i, j in itertools.pairwise(range(len(ducks)))
                    if ducks[i] > ducks[j]
                ),
                None,
            )
        ) is not None:
            for i, j in itertools.pairwise(range(k, len(ducks))):
                if ducks[i] > ducks[j]:
                    ducks[i] -= 1
                    ducks[j] += 1
            rounds += 1
        return rounds

    def part_1(self, input_data: InputData) -> Output1:
        ducks = [int(line) for line in input_data]
        rounds = self.make_non_decreasing(ducks)
        while rounds < 10 and any(
            ducks[i] < ducks[j]
            for i, j in itertools.pairwise(range(len(ducks)))
        ):
            for i, j in itertools.pairwise(range(len(ducks))):
                if ducks[i] < ducks[j]:
                    ducks[i] += 1
                    ducks[j] -= 1
            rounds += 1
        return sum(i * dd for i, dd in enumerate(ducks, start=1))

    def part_2(self, input_data: InputData) -> Output2:
        ducks = [int(line) for line in input_data]
        rounds = self.make_non_decreasing(ducks)
        avg = sum(ducks) // len(ducks)
        return rounds + sum(abs(avg - dd) for dd in ducks) // 2

    def part_3(self, input_data: InputData) -> Output3:
        return self.part_2(input_data)

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
