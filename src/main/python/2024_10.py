#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 10
#

import sys
from collections import Counter

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.common import log

Output1 = str
Output2 = int
Output3 = int

TEST1 = """\
**PCBS**
**RLNW**
BV....PT
CR....HZ
FL....JW
SG....MN
**FTZV**
**GMJH**
"""
TEST2 = """\
**XFZB**DCST**
**LWQK**GQJH**
?G....WL....DQ
BS....H?....CN
P?....KJ....TV
NM....Z?....SG
**NSHM**VKWZ**
**PJGV**XFNL**
WQ....?L....YS
FX....DJ....HV
?Y....WM....?J
TJ....YK....LP
**XRTK**BMSP**
**DWZN**GCJV**
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, grid: list[list[str]]) -> str:
        for r in range(2, 6):
            for c in range(2, 6):
                cnt = Counter[str]()
                cnt.update((grid[r][i] for i in {0, 1, 6, 7}))
                cnt.update((grid[i][c] for i in {0, 1, 6, 7}))
                ch, tot = cnt.most_common(1)[0]
                if tot == 2:
                    grid[r][c] = ch
        return "".join(grid[r][c] for r in range(2, 6) for c in range(2, 6))

    def part_1(self, input: InputData) -> Output1:
        grid = [[ch for ch in line] for line in input]
        return self.solve(grid)

    def part_2(self, input: InputData) -> Output2:
        ans = 0
        lines = list(input)
        for r in range(0, len(lines), 9):
            for c in range(0, len(lines[0]), 9):
                grid = [
                    [lines[rr][cc] for cc in range(c, c + 8)]
                    for rr in range(r, r + 8)
                ]
                word = self.solve(grid)
                ans += sum(
                    (ord(word[i]) - 64) * (i + 1) for i in range(len(word))
                )
        return ans

    def part_3(self, input: InputData) -> Output3:
        grid = [[ch for ch in line] for line in input]
        for r in range(0, len(grid) - 2, 6):
            for c in range(0, len(grid[0]) - 2, 6):
                block = [
                    [grid[rr][cc] for cc in range(c, c + 8)]
                    for rr in range(r, r + 8)
                ]
                word = self.solve(block)
                it = (ch for ch in word)
                for rr in range(r + 2, r + 6):
                    for cc in range(c + 2, c + 6):
                        grid[rr][cc] = next(it)
        for _ in range(2):
            for r in range(0, len(grid) - 2, 6):
                for c in range(0, len(grid[0]) - 2, 6):
                    for rr in range(r + 2, r + 6):
                        for cc in range(c + 2, c + 6):
                            if grid[rr][cc] in {".", "?"}:
                                ccnt = Counter[str]()
                                missing = set[tuple[int, int]]()
                                for rrr in range(r, r + 8):
                                    if rrr != rr:
                                        ccnt.update(grid[rrr][cc])
                                    if grid[rrr][cc] in {".", "?"}:
                                        missing.add((rrr, cc))
                                rcnt = Counter[str]()
                                for ccc in range(c, c + 8):
                                    if ccc != cc:
                                        rcnt.update(grid[rr][ccc])
                                    if grid[rr][ccc] in {".", "?"}:
                                        missing.add((rr, ccc))
                                rsingles = [
                                    (e, c)
                                    for e, c in rcnt.items()
                                    if c == 1 and e not in {".", "?"}
                                ]
                                # log(rsingles)
                                csingles = [
                                    (e, c)
                                    for e, c in ccnt.items()
                                    if c == 1 and e not in {".", "?"}
                                ]
                                # log(csingles)
                                if len(rsingles) == 1:
                                    for rrr, ccc in missing:
                                        assert rsingles[0][0] != "?"
                                        grid[rrr][ccc] = rsingles[0][0]
                                if len(csingles) == 1:
                                    for rrr, ccc in missing:
                                        assert csingles[0][0] != "?"
                                        grid[rrr][ccc] = csingles[0][0]
        # log(grid)
        # print()
        # lines = []
        # for r in range(0, len(grid)):
        #     lines.append("".join(grid[r][c] for c in range(len(grid[0]))))
        # print("\n".join(lines))
        ans = 0
        for r in range(0, len(grid) - 2, 6):
            for c in range(0, len(grid[0]) - 2, 6):
                word = "".join(
                    grid[rr][cc]
                    for rr in range(r + 2, r + 6)
                    for cc in range(c + 2, c + 6)
                )
                log((r, c))
                log(word)
                assert len(word) == 16
                # assert "?" not in word
                if "." in word or "?" in word:
                    continue
                ans += sum(
                    (ord(word[i]) - 64) * (i + 1) for i in range(len(word))
                )
        return ans

    @ec_samples(
        (
            ("part_1", TEST1, "PTBVRCZHFLJWGMNS"),
            ("part_2", TEST1, 1851),
            ("part_3", TEST2, 3889),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 10)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
