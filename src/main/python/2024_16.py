#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 16
#

import math
import sys
from collections import Counter
from functools import reduce
from typing import Callable

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
    def parse(self, input: InputData) -> tuple[list[int], list[int]]:
        steps = list(map(int, input[0].split(",")))
        sizes = list[int]()
        for i in range(len(steps)):
            j = 0
            while 2 + j < len(input) and input[2 + j][i * 4] != " ":
                j += 1
            sizes.append(j)
        return steps, sizes

    def right_lever(
        self,
        input: InputData,
        new_pos: list[int],
        sizes: list[int],
        steps: list[int],
        pulls: int = 1,
    ) -> tuple[str, int, list[int]]:
        ans = 0
        for _ in range(pulls):
            new_pos = [
                (new_pos[i] + p) % sizes[i] for i, p in enumerate(steps)
            ]
            s = " ".join(
                input[2 + p][i * 4 : i * 4 + 3]  # noqa E203
                for i, p in enumerate(new_pos)
            )
            ctr = Counter(ch for i, ch in enumerate(s) if i % 2 != 1)
            score = sum(v - 2 for k, v in ctr.items() if v >= 3)
            ans += score
        return s, ans, new_pos

    def part_1(self, input: InputData) -> Output1:
        steps, sizes = self.parse(input)
        ans, _, _ = self.right_lever(
            input, [0] * len(steps), sizes, steps, 100
        )
        return ans

    def part_2(self, input: InputData) -> Output2:
        steps, sizes = self.parse(input)
        pulls = 202_420_242_024
        new_pos = [0] * len(steps)
        lcm = reduce(lambda agg, s: math.lcm(agg, s), sizes, 1)
        cycles = pulls // lcm
        rest = pulls % lcm
        _, ans1, new_pos = self.right_lever(input, new_pos, sizes, steps, lcm)
        _, ans2, new_pos = self.right_lever(input, new_pos, sizes, steps, rest)
        return ans1 * cycles + ans2

    def part_3(self, input: InputData) -> Output3:
        steps, sizes = self.parse(input)
        memo = {
            min: dict[tuple[tuple[int, ...], int], int](),
            max: dict[tuple[tuple[int, ...], int], int](),
        }

        def score(
            pos: list[int], step: int, f: Callable  # type:ignore
        ) -> int:
            key = tuple(p for p in pos)
            if (key, step) in memo[f]:
                return memo[f][(key, step)]
            _, ss_none, pos_none = self.right_lever(input, pos, sizes, steps)
            newpos_up = [(p + 1) % sizes[i] for i, p in enumerate(pos)]
            _, ss_up, pos_up = self.right_lever(input, newpos_up, sizes, steps)
            newpos_dn = [(p - 1) % sizes[i] for i, p in enumerate(pos)]
            _, ss_dn, pos_dn = self.right_lever(input, newpos_dn, sizes, steps)
            if step > 1:
                ss_none += score(pos_none, step - 1, f)
                ss_up += score(pos_up, step - 1, f)
                ss_dn += score(pos_dn, step - 1, f)
            ans = f(ss_none, ss_up, ss_dn)
            memo[f][(key, step)] = ans
            return ans  # type:ignore

        pulls = 256
        ans_min = score([0] * len(steps), pulls, min)
        ans_max = score([0] * len(steps), pulls, max)
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
