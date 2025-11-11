#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 6
#

import sys
from collections import Counter

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int

TEST = "ABabACacBCbca"


class Solution(SolutionBase[Output1, Output2, Output3]):
    def count(self, input_data: InputData) -> Counter[str]:
        ans, cnt = Counter[str](), Counter[str]()
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

    def part_3(self, input_data: InputData) -> Output3:
        limit = 1000
        cnt_first, cnt_mid, cnt_last = (Counter[str]() for _ in range(3))
        s = input_data[0]
        size = len(s)
        s3 = s * 3
        for i, ch in enumerate(s):
            if ch.islower():
                lo, hi = size + i - limit, size + i + limit
                for (start, end), cnt in zip(
                    (
                        (max(lo, size), hi),
                        (lo, hi),
                        (lo, min(hi, 2 * size - 1)),
                    ),
                    (cnt_first, cnt_mid, cnt_last),
                    strict=True,
                ):
                    cnt[ch] += s3[start : end + 1].count(ch.upper())
        return (
            sum(cnt_first.values())
            + 998 * sum(cnt_mid.values())
            + sum(cnt_last.values())
        )

    @ec_samples(
        (
            ("part_1", TEST, 5),
            ("part_2", TEST, 11),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 6)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
