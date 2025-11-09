#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 5
#

import sys
from dataclasses import dataclass
from operator import attrgetter
from typing import Self

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

TEST1 = """\
58:5,3,7,8,9,10,4,5,7,8,8
"""
TEST2 = """\
1:2,4,1,1,8,2,7,9,8,6
2:7,9,9,3,8,3,8,8,6,8
3:4,7,6,9,1,8,3,7,2,2
4:6,4,2,1,7,4,5,5,5,8
5:2,9,3,8,3,9,5,2,1,4
6:2,4,9,6,7,4,1,7,6,8
7:2,3,7,6,2,2,4,1,4,2
8:5,1,5,6,8,3,1,8,3,9
9:5,7,7,3,7,2,3,8,6,7
10:4,1,9,3,8,5,4,3,5,5
"""
TEST3 = """\
1:7,1,9,1,6,9,8,3,7,2
2:6,1,9,2,9,8,8,4,3,1
3:7,1,9,1,6,9,8,3,8,3
4:6,1,9,2,8,8,8,4,3,1
5:7,1,9,1,6,9,8,3,7,3
6:6,1,9,2,8,8,8,4,3,5
7:3,7,2,2,7,4,4,6,3,1
8:3,7,2,2,7,4,4,6,3,7
9:3,7,2,2,7,4,1,6,3,7
"""
TEST4 = """\
1:7,1,9,1,6,9,8,3,7,2
2:7,1,9,1,6,9,8,3,7,2
"""

Output1 = int
Output2 = int
Output3 = int
Spine = list[int | None]


@dataclass(frozen=True)
class Sword:
    sid: int
    quality: int
    sort_key: tuple[int, tuple[int, ...], int]

    @classmethod
    def from_input(cls, string: str) -> Self:
        sid, nums = string.split(":")
        spine = cls.spine([int(n) for n in nums.split(",")])
        quality = int("".join(str(spine[i]) for i in range(1, len(spine), 3)))
        return cls(int(sid), quality, (quality, cls.levels(spine), int(sid)))

    @classmethod
    def spine(cls, nums: list[int]) -> Spine:
        spine = [None, nums[0], None]
        for num in nums[1:]:
            for r in range(1, len(spine), 3):
                sp = spine[r]
                assert sp is not None
                if num < sp and spine[r - 1] is None:
                    spine[r - 1] = num
                    break
                if num > sp and spine[r + 1] is None:
                    spine[r + 1] = num
                    break
            else:
                spine.extend([None, num, None])
        return spine

    @classmethod
    def levels(cls, spine: Spine) -> tuple[int, ...]:
        return tuple(
            int(
                "".join(
                    str(spine[i + j]) if spine[i + j] is not None else ""
                    for j in range(3)
                )
            )
            for i in range(0, len(spine), 3)
        )


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input_data: InputData) -> Output1:
        return Sword.from_input(input_data[0]).quality

    def part_2(self, input_data: InputData) -> Output2:
        swords = [Sword.from_input(line) for line in input_data]
        swords.sort(key=attrgetter("quality"))
        return swords[-1].quality - swords[0].quality

    def part_3(self, input_data: InputData) -> Output3:
        swords = [Sword.from_input(line) for line in input_data]
        swords.sort(key=attrgetter("sort_key"), reverse=True)
        return sum(i * sw.sid for i, sw in enumerate(swords, start=1))

    @ec_samples(
        (
            ("part_1", TEST1, 581078),
            ("part_2", TEST2, 77053),
            ("part_3", TEST3, 260),
            ("part_3", TEST4, 4),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 5)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
