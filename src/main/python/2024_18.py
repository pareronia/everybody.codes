#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 18
#

import sys
from collections import defaultdict
from collections import deque

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int
Cell = tuple[int, int]
DIRS = {(-1, 0), (1, 0), (0, -1), (0, 1)}

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
        self, input_data: InputData, starts: set[Cell], palms: int
    ) -> list[int]:
        h, w = len(input_data), len(input_data[0])
        ans = []
        frontier = set(starts)
        seen = set(starts)
        t = 0
        while len(frontier) > 0:
            t += 1
            new_frontier = set()
            for r, c in frontier:
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in seen or not (0 <= nr < h and 0 <= nc < w):
                        continue
                    seen.add((nr, nc))
                    v = input_data[nr][nc]
                    if v == "#":
                        continue
                    if v == "P":
                        palms -= 1
                        ans.append(t)
                    new_frontier.add((nr, nc))
            if palms == 0:
                break
            frontier = new_frontier
        return ans

    def part_1(self, input_data: InputData) -> Output1:
        palms = len([ch for line in input_data for ch in line if ch == "P"])
        row = next(
            iter(r for r in range(len(input_data)) if input_data[r][0] == ".")
        )
        return self.flood(input_data, {(row, 0)}, palms)[-1]

    def part_2(self, input_data: InputData) -> Output2:
        h, w = len(input_data), len(input_data[0])
        palms = len([ch for line in input_data for ch in line if ch == "P"])
        row_1 = next(iter(r for r in range(h) if input_data[r][0] == "."))
        row_2 = next(iter(r for r in range(h) if input_data[r][w - 1] == "."))
        starts = {(row_1, 0), (row_2, w - 1)}
        return self.flood(input_data, starts, palms)[-1]

    def part_3(self, input_data: InputData) -> Output3:
        h, w = len(input_data), len(input_data[0])
        palms = {
            (r, c)
            for r in range(h)
            for c in range(w)
            if input_data[r][c] == "P"
        }
        distances = defaultdict[Cell, int](int)
        for p in palms:
            q: deque[tuple[int, Cell]] = deque({(0, p)})
            seen = {p}
            while len(q) > 0:
                distance, (r, c) = q.pop()
                distances[(r, c)] += distance
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    # Don't need boundary check; entries will already be seen
                    if (nr, nc) in seen or input_data[nr][nc] == "#":
                        continue
                    seen.add((nr, nc))
                    q.append((distance + 1, (nr, nc)))
        start = min(
            ((r, c) for r, c in distances if input_data[r][c] == "."),
            key=lambda k: distances[k],
        )
        return sum(_ for _ in self.flood(input_data, {start}, len(palms)))

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
