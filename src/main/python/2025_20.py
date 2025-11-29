#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 20
#

import sys
from collections import deque
from collections.abc import Iterator

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.graph import bfs

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
T#TTT###T##
.##TT#TT##.
..T###T#T..
...##TT#...
....T##....
.....#.....
"""
TEST2 = """\
TTTTTTTTTTTTTTTTT
.TTTT#T#T#TTTTTT.
..TT#TTTETT#TTT..
...TT#T#TTT#TT...
....TTT#T#TTT....
.....TTTTTT#.....
......TT#TT......
.......#TT.......
........S........
"""
TEST3 = """\
T####T#TTT##T##T#T#
.T#####TTTT##TTT##.
..TTTT#T###TTTT#T..
...T#TTT#ETTTT##...
....#TT##T#T##T....
.....#TT####T#.....
......T#TT#T#......
.......T#TTT.......
........TT#........
.........S.........
"""

Triangle = tuple[int, int, int]
Cell = tuple[int, int]


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input_data: InputData) -> Output1:
        tr = set[Cell]()
        for r, line in enumerate(input_data):
            for c, ch in enumerate(line):
                if ch == "T":
                    tr.add((r, c))
        pairs = set[tuple[Cell, ...]]()
        for r, c in tr:
            if (r, c - 1) in tr:
                s = sorted([(r, c), (r, c - 1)])
                pairs.add(tuple(s))
            if (r, c + 1) in tr:
                s = sorted([(r, c), (r, c + 1)])
                pairs.add(tuple(s))
            if r % 2 == c % 2:
                # down
                if (r - 1, c) in tr:
                    s = sorted([(r, c), (r - 1, c)])
                    pairs.add(tuple(s))
            elif (r + 1, c) in tr:
                s = sorted([(r, c), (r + 1, c)])
                pairs.add(tuple(s))
        return len(pairs)

    def part_2(self, input_data: InputData) -> Output2:
        tr = set[Cell]()
        for r, line in enumerate(input_data):
            for c, ch in enumerate(line):
                if ch == "S":
                    start = (r, c)
                    tr.add((r, c))
                if ch == "E":
                    end = (r, c)
                    tr.add((r, c))
                if ch == "T":
                    tr.add((r, c))

        def adjacent(cell: Cell) -> Iterator[Cell]:
            r, c = cell
            for dc in (-1, 1):
                if (r, c + dc) in tr:
                    yield (r, c + dc)
            v = (r + (-1 if r % 2 == c % 2 else 1), c)
            if v in tr:
                yield v

        return bfs(start, lambda cell: cell == end, adjacent)

    def part_3(self, input_data: InputData) -> Output3:  # noqa:PLR0912,PLR0915,C901
        h, w = len(input_data), len(input_data[0])
        tr = [set[Cell](), set[Cell](), set[Cell]()]
        end = [(0, 0), (0, 0), (0, 0)]
        for r in range(h):
            for c in range(w):
                if input_data[r][c] == "S":
                    start = (r, c)
                    tr[0].add((r, c))
                if input_data[r][c] == "E":
                    end[0] = (r, c)
                    tr[0].add((r, c))
                if input_data[r][c] == "T":
                    tr[0].add((r, c))
        r, c = h - 1, w // 2
        rrr, ccc = 0, 0
        while r >= 0 and c < w:
            rr, cc = r, c
            while rr >= 0 and cc >= 2 * abs((w // 2) - c):
                if input_data[rr][cc] == "E":
                    end[1] = (rrr, ccc)
                    tr[1].add((rrr, ccc))
                if input_data[rr][cc] in ("S", "T"):
                    tr[1].add((rrr, ccc))
                if rr % 2 == cc % 2:
                    rr -= 1
                else:
                    cc -= 1
                ccc += 1
            rrr += 1
            ccc = rrr
            r, c = r - 1, c + 1
        rrr, ccc = 0, 0
        for c in range(w - 1, -1, -2):
            rr, cc = 0, c
            while rr < h and cc >= 0:
                if input_data[rr][cc] == "E":
                    end[2] = (rrr, ccc)
                    tr[2].add((rrr, ccc))
                if input_data[rr][cc] in ("S", "T"):
                    tr[2].add((rrr, ccc))
                if rr % 2 != cc % 2:
                    rr += 1
                else:
                    cc -= 1
                ccc += 1
            rrr += 1
            ccc = rrr
        q: deque[tuple[int, int, int, int]] = deque()
        q.append((0, start[0], start[1], 0))
        seen: set[tuple[int, int, int]] = set()
        seen.add((start[0], start[1], 0))
        while len(q) != 0:
            distance, r, c, lyr = q.popleft()
            if (r, c) == end[lyr % 3]:
                return distance
            ns = set[tuple[int, int, int]]()
            nlyr = (lyr + 1) % 3
            for dc in (-1, 1):
                if (r, c + dc) in tr[nlyr]:
                    ns.add((r, c + dc, nlyr))
            v = (r + (-1 if r % 2 == c % 2 else 1), c)
            if v in tr[nlyr]:
                ns.add((v[0], v[1], nlyr))
            if (r, c) in tr[nlyr]:
                ns.add((r, c, nlyr))
            for n in ns:
                if n in seen:
                    continue
                seen.add(n)
                q.append((distance + 1, *n))
        raise AssertionError

    @ec_samples(
        (
            ("part_1", TEST1, 7),
            ("part_2", TEST2, 32),
            ("part_3", TEST3, 23),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 20)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
