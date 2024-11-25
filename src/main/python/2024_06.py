#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 6
#

import sys
from collections import defaultdict

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.graph import bfs_path

Output1 = str
Output2 = str
Output3 = str

FLOWER = "@"
ROOT = "RR"

TEST = """\
RR:A,B,C
A:D,E
B:F,@
C:G,H
D:@
E:@
F:@
G:@
H:@
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, input: InputData) -> list[str]:
        d = defaultdict[str, list[str]](list)
        cnt = 1
        for line in input:
            if "BUG" in line or "ANT" in line:
                continue
            n1, rest = line.split(":")
            if rest.endswith(FLOWER):
                rest = rest[:-1] + f"{FLOWER}{cnt:02}"
                cnt += 1
            for n in rest.split(","):
                d[n].append(n1)
        c = defaultdict[int, list[list[str]]](list)
        for n in d:
            if n.startswith(FLOWER):
                _, path = bfs_path(
                    n,
                    lambda x: x == ROOT,
                    lambda x: (_ for _ in d[x]),
                )
                c[len(path)].append(path)
        ans = next(k for k, v in c.items() if len(v) == 1)
        return c[ans][0]

    def part_1(self, input: InputData) -> Output1:
        path = self.solve(input)
        return "".join(path[:-1]) + FLOWER

    def part_2(self, input: InputData) -> Output2:
        path = self.solve(input)
        return "".join(p[0] for p in path)

    def part_3(self, input: InputData) -> Output3:
        return self.part_2(input)

    @ec_samples((("part_1", TEST, "RRB@"),))
    def samples(self) -> None:
        pass


solution = Solution(2024, 6)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
