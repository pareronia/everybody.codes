#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 8
#

import sys
from typing import Callable

from ec.common import InputData
from ec.common import SolutionBase

Output1 = int
Output2 = int
Output3 = int


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, available: int, thickness: Callable[[int], int]) -> int:
        tot, nxt, layer = 0, 1, 1
        while True:
            tot += nxt * layer
            if tot >= available:
                return nxt * (tot - available)
            layer = thickness(layer)
            nxt += 2
        raise ValueError("")

    def solve_2(self, priests: int, acolytes: int, available: int) -> int:
        return self.solve(
            available, lambda layer: (layer * priests) % acolytes
        )

    def solve_3(self, priests: int, acolytes: int, available: int) -> int:
        cols, nxt, layer = [1], 1, 1
        while True:
            if cols[0] + 2 * sum(cols[1:]) >= available:
                break
            layer = (layer * priests) % acolytes + acolytes
            for i, c in enumerate(cols):
                cols[i] = c + layer
            cols.append(layer)
            nxt += 2
        rem = (priests * nxt * cols[0]) % acolytes
        for i in range(1, len(cols) - 1, 1):
            rem += 2 * ((priests * nxt * cols[i]) % acolytes)
        return cols[0] + 2 * sum(cols[1:]) - rem - available

    def part_1(self, input: InputData) -> Output1:
        available = int(list(input)[0])
        return self.solve(available, lambda layer: 1)

    def part_2(self, input: InputData) -> Output2:
        priests = int(list(input)[0])
        return self.solve_2(priests, 1111, 20_240_000)

    def part_3(self, input: InputData) -> Output3:
        priests = int(list(input)[0])
        return self.solve_3(priests, 10, 202_400_000)

    def samples(self) -> None:
        assert self.part_1(("13",)) == 21
        assert self.solve_2(3, 5, 50) == 27
        assert self.solve_3(2, 5, 160) == 2
        for n in [
            19,
            67,
            115,
            162,
            239,
            353,
            491,
            569,
            690,
            1885,
            7601,
            30655,
            123131,
            491005,
            1964801,
            7863295,
            31461371,
            125820925,
        ]:
            assert self.solve_3(2, 5, n) == 0


solution = Solution(2024, 8)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
