#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 16
#

import math
import sys
from collections import Counter
from functools import cache

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = str
Output2 = int
Output3 = str

TEST1 = """\
1,2,3

^_^ -.- ^,-
>.- ^_^ >.<
-_- -.- >.<
    -.^ ^_^
    >.>    \
"""
TEST2 = """\
1,2,3

^_^ -.- ^,-
>.- ^_^ >.<
-_- -.- ^.^
    -.^ >.<
    >.>    \
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def parse(
        self, input_data: InputData
    ) -> tuple[tuple[int, ...], list[int]]:
        steps = tuple(map(int, input_data[0].split(",")))
        sizes = list[int]()
        for i in range(len(steps)):
            j = 0
            while 2 + j < len(input_data) and input_data[2 + j][i * 4] != " ":
                j += 1
            sizes.append(j)
        return steps, sizes

    def positions(
        self, sizes: list[int], steps: tuple[int, ...], amount: int
    ) -> tuple[int, ...]:
        return tuple((amount * s) % sizes[i] for i, s in enumerate(steps))

    def sequence(self, input_data: InputData, pos: tuple[int, ...]) -> str:
        return " ".join(
            input_data[2 + p][i * 4 : i * 4 + 3] for i, p in enumerate(pos)
        )

    def score(self, sequence: str) -> int:
        ctr = Counter(ch for i, ch in enumerate(sequence) if i % 2 != 1)
        return sum(v - 2 for v in ctr.values() if v >= 3)

    def part_1(self, input_data: InputData) -> Output1:
        steps, sizes, pulls = *self.parse(input_data), 100
        return self.sequence(input_data, self.positions(sizes, steps, pulls))

    def part_2(self, input_data: InputData) -> Output2:
        steps, sizes, pulls = *self.parse(input_data), 202_420_242_024
        lcm = math.lcm(*sizes)
        cycles, rest = divmod(pulls, lcm)
        score_lcm = 0
        for i in range(1, lcm + 1):
            sequence = self.sequence(
                input_data, self.positions(sizes, steps, i)
            )
            score_lcm += self.score(sequence)
            if i == rest:
                score_rest = score_lcm
        return score_lcm * cycles + score_rest

    def part_3(self, input_data: InputData) -> Output3:
        steps, sizes, pulls = *self.parse(input_data), 256

        @cache
        def scores(left_lever: int, pull: int) -> tuple[int, int]:
            if pull == 0:
                min_score, max_score = 0, 0
            else:
                new_pos = tuple(
                    (step * pull + left_lever) % sizes[i]
                    for i, step in enumerate(steps)
                )
                score = self.score(self.sequence(input_data, new_pos))
                min_score, max_score = score, score
            if pulls - pull > 0:
                min_max = [
                    scores(left_lever + ll, pull + 1) for ll in (-1, 0, 1)
                ]
                min_score += min(m for m, _ in min_max)
                max_score += max(m for _, m in min_max)
            return min_score, max_score

        ans_min, ans_max = scores(0, 0)
        return f"{ans_max} {ans_min}"

    @ec_samples(
        (
            ("part_1", TEST1, ">.- -.- ^,-"),
            ("part_2", TEST1, 280014668134),
            ("part_3", TEST2, "627 128"),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 16)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
