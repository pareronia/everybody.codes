#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 5
#

import sys

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
Sword = tuple[int, list[int]]


class Solution(SolutionBase[Output1, Output2, Output3]):
    def spine(self, nums: list[int]) -> list[int]:
        spine = [-1, -1, -1]
        spine[1] = nums[0]
        for num in nums[1:]:
            for r in range(len(spine) // 3):
                if num < spine[r * 3 + 1] and spine[r * 3] < 0:
                    spine[r * 3] = num
                    break
                if num > spine[r * 3 + 1] and spine[r * 3 + 2] < 0:
                    spine[r * 3 + 2] = num
                    break
            else:
                spine.extend([-1, -1, -1])
                r += 1
                spine[r * 3 + 1] = num
        return spine

    def quality(self, spine: list[int]) -> int:
        return int("".join(str(spine[i]) for i in range(1, len(spine), 3)))

    def part_1(self, input_data: InputData) -> Output1:
        nums = [int(n) for n in input_data[0].split(":")[1].split(",")]
        return self.quality(self.spine(nums))

    def part_2(self, input_data: InputData) -> Output2:
        lo, hi = sys.maxsize, -sys.maxsize
        for line in input_data:
            nums = [int(n) for n in line.split(":")[1].split(",")]
            q = self.quality(self.spine(nums))
            lo, hi = min(lo, q), max(hi, q)
        return hi - lo

    def part_3(self, input_data: InputData) -> Output3:
        def sort_key(sword: Sword) -> tuple[int, tuple[int, ...], int]:
            sid, spine = sword
            q = self.quality(spine)
            lvls = tuple(
                int(
                    "".join(
                        str(spine[i + j]) if spine[i + j] != -1 else ""
                        for j in range(3)
                    )
                )
                for i in range(0, len(spine), 3)
            )
            return (q, lvls, sid)

        swords = list[Sword]()
        for line in input_data:
            sid, nn = line.split(":")
            nums = [int(n) for n in nn.split(",")]
            swords.append((int(sid), self.spine(nums)))
        swords.sort(key=sort_key, reverse=True)
        return sum((i + 1) * sw[0] for i, sw in enumerate(swords))

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
