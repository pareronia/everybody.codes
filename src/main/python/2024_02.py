#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 2
#

import re
import sys

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.common import log

Output1 = int
Output2 = int
Output3 = int
OFFSET = len("WORDS:")

TEST1 = """\
WORDS:THE,OWE,MES,ROD,HER

AWAKEN THE POWER ADORNED WITH THE FLAMES BRIGHT IRE
"""
TEST2 = """\
WORDS:THE,OWE,MES,ROD,HER

AWAKEN THE POWE ADORNED WITH THE FLAMES BRIGHT IRE
THE FLAME SHIELDED THE HEART OF THE KINGS
POWE PO WER P OWE R
THERE IS THE END
"""
TEST3 = """\
WORDS:THE,OWE,MES,ROD,RODEO

HELWORLT
ENIGWDXL
TRODEOAL
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input: InputData) -> Output1:
        words, inscription = input[0][OFFSET:].split(","), input[2]
        return sum(inscription.count(w) for w in words)

    def part_2(self, input: InputData) -> Output2:
        words, inscription = input[0][OFFSET:].split(","), input[2:]
        words.extend([w[::-1] for w in words])
        ans = 0
        for line in inscription:
            runes = set[int]()
            for w in words:
                for m in re.finditer(rf"(?={w})", line):
                    runes |= {j for j in range(m.start(), m.start() + len(w))}
            ans += len(runes)
        return ans

    def part_3(self, input: InputData) -> Output3:
        words, inscription = input[0][OFFSET:].split(","), input[2:]
        extra = max(len(w) for w in words)
        runes = set[tuple[int, int]]()
        for i, line in enumerate(inscription):
            log(line)
            for w in words:
                log(f" -> {w}")
                for m in re.finditer(rf"(?={w})", line + line[:extra]):
                    log(f"    -> ({i}, {m.start()})")
                    runes |= {
                        (i, j % len(line))
                        for j in range(m.start(), m.start() + len(w))
                    }
            log(f"{len(runes)}")
        for c in range(len(inscription[0])):
            line = "".join(inscription[r][c] for r in range(len(inscription)))
            log(line)
            for w in words:
                log(f" -> {w}")
                for m in re.finditer(rf"(?={w})", line):
                    log(f"    -> ({m.start()}, {c})")
                    runes |= {
                        (j, c) for j in range(m.start(), m.start() + len(w))
                    }
            log(f"{len(runes)}")
        return len(runes)

    @ec_samples(
        (
            ("part_1", TEST1, 4),
            ("part_2", TEST2, 37),
            ("part_3", TEST3, 10),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 2)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
