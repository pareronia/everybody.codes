#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 15
#

import multiprocessing
import sys
from collections.abc import Iterator

from ec.common import Direction
from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.graph import bfs

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
#####.#####
#.........#
#.######.##
#.........#
###.#.#####
#H.......H#
###########
"""
TEST2 = """\
##########.##########
#...................#
#.###.##.###.##.#.#.#
#..A#.#..~~~....#A#.#
#.#...#.~~~~~...#.#.#
#.#.#.#.~~~~~.#.#.#.#
#...#.#.B~~~B.#.#...#
#...#....BBB..#....##
#C............#....C#
#####################
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(
        self,
        input_data: tuple[str, ...],
        offset: int,
        width: int,
        start: tuple[int, int],
    ) -> int:
        height = len(input_data)
        complete = 0
        for r in range(height):
            for c in range(width):
                v = input_data[r][offset + c]
                if v.isalpha():
                    complete |= 1 << (ord(v) - ord("A"))

        def is_end(node: tuple[int, int, int]) -> bool:
            r, c, herbs = node
            return herbs == complete and (r, c) == start

        def adjacent(
            node: tuple[int, int, int],
        ) -> Iterator[tuple[int, int, int]]:
            r, c, herbs = node
            for d in Direction.capitals():
                n_r, n_c = r + d.y, c + d.x
                if 0 <= n_r < height and 0 <= n_c < width:
                    v = input_data[n_r][offset + n_c]
                    if v in {"#", "~"}:
                        continue
                    n_herbs = herbs
                    if v.isalpha():
                        n_herbs |= 1 << (ord(v) - ord("A"))
                    yield (n_r, n_c, n_herbs)

        return bfs((*start, 0), is_end, adjacent)

    def part_1(self, input_data: InputData) -> Output1:
        width = len(input_data[0])
        return self.solve(input_data, 0, width, start=(0, width // 2))

    def part_2(self, input_data: InputData) -> Output2:
        width = len(input_data[0])
        return self.solve(input_data, 0, width, start=(0, width // 2))

    def part_3(self, input_data: InputData) -> Output3:
        width = len(input_data[0]) // 3
        height = len(input_data)
        input_data = tuple(
            line.replace("K", "X", 1) if i == height - 2 else line
            for i, line in enumerate(input_data)
        )
        ans = multiprocessing.Manager().dict()

        def left() -> None:
            offset = 0
            start = (height - 2, width - 1)
            ans["left"] = self.solve(input_data, offset, width, start) + 1

        def right() -> None:
            offset = 2 * width
            start = (height - 2, 0)
            ans["right"] = self.solve(input_data, offset, width, start) + 1

        def middle() -> None:
            offset = width
            start = (0, width // 2)
            ans["middle"] = self.solve(input_data, offset, width, start) + 6

        if sys.platform.startswith("win"):
            left()
            middle()
            right()
        else:
            jobs = []
            for worker in {left, middle, right}:
                p = multiprocessing.Process(target=worker)
                jobs.append(p)
                p.start()
            for p in jobs:
                p.join()
        return sum(ans.values())

    @ec_samples(
        (
            ("part_1", TEST1, 26),
            ("part_2", TEST2, 38),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 15)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
