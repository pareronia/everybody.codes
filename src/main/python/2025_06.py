#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 6
#

import sys
from collections import Counter

from ec.common import InputData
from ec.common import SolutionBase

Output1 = int
Output2 = int
Output3 = int

TEST1 = "ABabACacBCbca"
TEST2 = "AABCBABCABCabcabcABCCBAACBCa"


class Solution(SolutionBase[Output1, Output2, Output3]):
    def count(self, input_data: InputData) -> Counter[str]:
        ans = Counter[str]()
        cnt = Counter[str]()
        for ch in input_data[0]:
            if ch.isupper():
                cnt.update(ch.lower())
            else:
                ans[ch] += cnt[ch]
        return ans

    def part_1(self, input_data: InputData) -> Output1:
        return self.count(input_data)["a"]

    def part_2(self, input_data: InputData) -> Output2:
        return sum(self.count(input_data).values())

    def solve_3(
        self, input_data: InputData, repeat: int = 1000, limit: int = 1000
    ) -> int:
        ans = 0
        s = "".join(input_data[0] for _ in range(repeat))
        for i, ch in enumerate(s):
            if ch.isupper():
                continue
            lo, hi = max(0, i - limit), min(i + limit, len(s) - 1)
            ans += s[lo : hi + 1].count(ch.upper())
        return ans

    def part_3(self, input_data: InputData) -> Output3:
        return self.solve_3(input_data)

    def samples(self) -> None:
        input_data = tuple(TEST1.splitlines())
        assert self.part_1(input_data) == 5
        assert self.part_2(input_data) == 11
        input_data = tuple(TEST2.splitlines())
        assert self.solve_3(input_data, 1, 10) == 34
        assert self.solve_3(input_data, 2, 10) == 72
        assert self.solve_3(input_data, 1000, 1000) == 3442321


solution = Solution(2025, 6)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
