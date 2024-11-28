#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 18
#

import sys

from ec.common import Cell
from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
##########
..#......#
#.P.####P#
#.#...P#.#
##########
"""
TEST2 = """\
#######################
...P..P...#P....#.....#
#.#######.#.#.#.#####.#
#.....#...#P#.#..P....#
#.#####.#####.#########
#...P....P.P.P.....P#.#
#.#######.#####.#.#.#.#
#...#.....#P...P#.#....
#######################
"""
TEST3 = """\
##########
#.#......#
#.P.####P#
#.#...P#.#
##########
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input: InputData) -> Output1:
        start = Cell(
            next(iter(r for r in range(len(input)) if input[r][0] == ".")),
            0,
        )
        palms = 0
        for line in input:
            for ch in line:
                if ch == "P":
                    palms += 1
        ans = 0
        f = {start}
        seen = set()
        seen.add(start)
        while True:
            ans += 1
            nf = set()
            for node in f:
                for n in node.get_capital_neighbours():
                    if n in seen:
                        continue
                    seen.add(n)
                    v = input[n.row][n.col]
                    if v == "#":
                        continue
                    if v == "P":
                        palms -= 1
                    nf.add(n)
            if palms == 0:
                break
            f = nf
        return ans

    def part_2(self, input: InputData) -> Output2:
        start_1 = Cell(
            next(iter(r for r in range(len(input)) if input[r][0] == ".")),
            0,
        )
        h, w = len(input), len(input[0])
        start_2 = Cell(
            next(iter(r for r in range(len(input)) if input[r][w - 1] == ".")),
            w - 1,
        )
        palms = 0
        for line in input:
            for ch in line:
                if ch == "P":
                    palms += 1
        ans = 0
        f = {start_1, start_2}
        seen = set()
        seen.add(start_1)
        seen.add(start_2)
        while True:
            ans += 1
            nf = set()
            for node in f:
                for n in node.get_capital_neighbours():
                    if n in seen:
                        continue
                    if not (0 <= n.row < h and 0 <= n.col < w):
                        continue
                    seen.add(n)
                    v = input[n.row][n.col]
                    if v == "#":
                        continue
                    if v == "P":
                        palms -= 1
                    nf.add(n)
            if palms == 0:
                break
            f = nf
        return ans

    def part_3(self, input: InputData) -> Output3:
        h, w = len(input), len(input[0])
        palms = 0
        for line in input:
            for ch in line:
                if ch == "P":
                    palms += 1

        def flood(start: Cell) -> int:
            t = 0
            ans = 0
            p = palms
            f = {start}
            seen = set()
            seen.add(start)
            while True:
                t += 1
                nf = set()
                for node in f:
                    for n in node.get_capital_neighbours():
                        if n in seen:
                            continue
                        if not (0 <= n.row < h and 0 <= n.col < w):
                            continue
                        seen.add(n)
                        v = input[n.row][n.col]
                        if v == "#":
                            continue
                        if v == "P":
                            p -= 1
                            ans += t
                        nf.add(n)
                if p == 0:
                    break
                f = nf
            return ans

        ans = sys.maxsize
        cnt = 0
        for start in (
            Cell(r, c)
            for r in range(h)
            for c in range(w)
            if input[r][c] == "."
        ):
            cnt += 1
            print(cnt, end="\r")
            ans = min(ans, flood(start))
        return ans

    @ec_samples(
        (
            ("part_1", TEST1, 11),
            ("part_2", TEST2, 21),
            ("part_3", TEST3, 12),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 18)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
