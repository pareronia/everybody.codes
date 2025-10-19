#! /usr/bin/env python3
#
# everybody.codes S01 Quest 1
#

import sys
from enum import Enum
from enum import auto
from enum import unique

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
A=4 B=4 C=6 X=3 Y=4 Z=5 M=11
A=8 B=4 C=7 X=8 Y=4 Z=6 M=12
A=2 B=8 C=6 X=2 Y=4 Z=5 M=13
A=5 B=9 C=6 X=8 Y=6 Z=8 M=14
A=5 B=9 C=7 X=6 Y=6 Z=8 M=15
A=8 B=8 C=8 X=6 Y=9 Z=6 M=16
"""
TEST2 = """\
A=4 B=4 C=6 X=3 Y=14 Z=15 M=11
A=8 B=4 C=7 X=8 Y=14 Z=16 M=12
A=2 B=8 C=6 X=2 Y=14 Z=15 M=13
A=5 B=9 C=6 X=8 Y=16 Z=18 M=14
A=5 B=9 C=7 X=6 Y=16 Z=18 M=15
A=8 B=8 C=8 X=6 Y=19 Z=16 M=16
"""
TEST3 = """\
A=3657 B=3583 C=9716 X=903056852 Y=9283895500 Z=85920867478 M=188
A=6061 B=4425 C=5082 X=731145782 Y=1550090416 Z=87586428967 M=107
A=7818 B=5395 C=9975 X=122388873 Y=4093041057 Z=58606045432 M=102
A=7681 B=9603 C=5681 X=716116871 Y=6421884967 Z=66298999264 M=196
A=7334 B=9016 C=8524 X=297284338 Y=1565962337 Z=86750102612 M=145
"""
TEST4 = """\
A=4 B=4 C=6 X=3000 Y=14000 Z=15000 M=110
A=8 B=4 C=7 X=8000 Y=14000 Z=16000 M=120
A=2 B=8 C=6 X=2000 Y=14000 Z=15000 M=130
A=5 B=9 C=6 X=8000 Y=16000 Z=18000 M=140
A=5 B=9 C=7 X=6000 Y=16000 Z=18000 M=150
A=8 B=8 C=8 X=6000 Y=19000 Z=16000 M=160
"""


@unique
class EniMode(Enum):
    MODE_1 = auto()
    MODE_2 = auto()
    MODE_3 = auto()

    def eni(self, n: int, exp: int, mod: int) -> int:
        match self:
            case EniMode.MODE_1:
                ans = list[int]()
                d = n % mod
                num = 1
                for _ in range(exp):
                    num *= d
                    num = num % mod
                    ans.append(num)
                return int("".join(str(_) for _ in reversed(ans)))
            case EniMode.MODE_2:
                ans = list[int]()
                d = n % mod
                num = pow(n, exp - 5, mod) if exp > 5 else 1
                for _ in range(min(exp, 5)):
                    num *= d
                    num = num % mod
                    ans.append(num)
                return int("".join(str(_) for _ in reversed(ans[-6:])))
            case EniMode.MODE_3:
                remainder = 1
                total = 0
                seen = dict[int, tuple[int, int]]()
                i = 0
                while i < exp:
                    remainder = (remainder * n) % mod
                    total += remainder
                    i += 1
                    if remainder in seen:
                        s = seen[remainder]
                        period = i - s[0]
                        amount = total - s[1]
                        cycles = (exp - i) // period
                        total += cycles * amount
                        i += cycles * period
                    seen[remainder] = (i, total)
                return total


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, input_data: InputData, mode: EniMode) -> int:
        ans = -sys.maxsize
        for line in input_data:
            a, b, c, x, y, z, m = map(
                int, (split.split("=")[1] for split in line.split())
            )
            ans = max(
                ans, mode.eni(a, x, m) + mode.eni(b, y, m) + mode.eni(c, z, m)
            )
        return ans

    def part_1(self, input_data: InputData) -> Output1:
        return self.solve(input_data, mode=EniMode.MODE_1)

    def part_2(self, input_data: InputData) -> Output2:
        return self.solve(input_data, mode=EniMode.MODE_2)

    def part_3(self, input_data: InputData) -> Output3:
        return self.solve(input_data, mode=EniMode.MODE_3)

    @ec_samples(
        (
            ("part_1", TEST1, 11611972920),
            ("part_2", TEST2, 11051340),
            ("part_2", TEST3, 1507702060886),
            ("part_3", TEST4, 3279640),
            ("part_3", TEST3, 7276515438396),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(1, 1)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
