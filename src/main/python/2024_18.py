#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 18
#

import sys
from collections import defaultdict
from collections import deque

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
    def flood(
        self, input: InputData, starts: set[Cell], palms: int
    ) -> list[int]:
        h, w = len(input), len(input[0])
        ans = []
        frontier = {_ for _ in starts}
        seen = {_ for _ in starts}
        t = 0
        while True:
            t += 1
            new_frontier = set()
            for node in frontier:
                for n in node.get_capital_neighbours():
                    if n in seen or not (0 <= n.row < h and 0 <= n.col < w):
                        continue
                    seen.add(n)
                    v = input[n.row][n.col]
                    if v == "#":
                        continue
                    if v == "P":
                        palms -= 1
                        ans.append(t)
                    new_frontier.add(n)
            if palms == 0:
                break
            frontier = new_frontier
        return ans

    def part_1(self, input: InputData) -> Output1:
        palms = len([ch for line in input for ch in line if ch == "P"])
        row = next(iter(r for r in range(len(input)) if input[r][0] == "."))
        return self.flood(input, {Cell(row, 0)}, palms)[-1]

    def part_2(self, input: InputData) -> Output2:
        h, w = len(input), len(input[0])
        palms = len([ch for line in input for ch in line if ch == "P"])
        row_1 = next(iter(r for r in range(h) if input[r][0] == "."))
        row_2 = next(iter(r for r in range(h) if input[r][w - 1] == "."))
        starts = {Cell(row_1, 0), Cell(row_2, w - 1)}
        return self.flood(input, starts, palms)[-1]

    def part_3(self, input: InputData) -> Output3:
        palms = [
            Cell(r, c)
            for r in range(len(input))
            for c in range(len(input[0]))
            if input[r][c] == "P"
        ]
        distances = defaultdict[Cell, int](int)
        for p in palms:
            q: deque[tuple[int, Cell]] = deque({(0, p)})
            seen = {p}
            while len(q) > 0:
                distance, node = q.pop()
                distances[node] += distance
                for n in node.get_capital_neighbours():
                    if n in seen or input[n.row][n.col] == "#":
                        continue
                    seen.add(n)
                    q.append((distance + 1, n))
        start = min(
            (c for c in distances.keys() if input[c.row][c.col] == "."),
            key=lambda k: distances[k],
        )
        return sum(_ for _ in self.flood(input, {start}, len(palms)))

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
