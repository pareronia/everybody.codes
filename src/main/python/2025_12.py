#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 12
#

import operator
import sys
from collections import deque
from functools import reduce

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

Output1 = int
Output2 = int
Output3 = int
Cell = tuple[int, int]

TEST1 = """\
989601
857782
746543
766789
"""
TEST2 = """\
9589233445
9679121695
8469121876
8352919876
7342914327
7234193437
6789193538
6781219648
5691219769
5443329859
"""
TEST3 = """\
5411
3362
5235
3112
"""
TEST4 = """\
41951111131882511179
32112222211518122215
31223333322115122219
31234444432147511128
91223333322176121892
61112222211166431583
14661111166111111746
11111119142122222177
41222118881233333219
71222127839122222196
56111126279711111517
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def ignite(
        self,
        starts: set[Cell],
        grid: tuple[str, ...],
        exclude: set[Cell] | None = None,
    ) -> set[Cell]:
        q: deque[Cell] = deque(starts)
        seen = starts | (set(exclude) if exclude is not None else set())
        while len(q) != 0:
            r, c = q.popleft()
            for dr, dc in {(0, 1), (0, -1), (1, 0), (-1, 0)}:
                rr, cc = r + dr, c + dc
                if (
                    0 <= rr < len(grid)
                    and 0 <= cc < len(grid[0])
                    and grid[r][c] >= grid[rr][cc]
                    and (rr, cc) not in seen
                ):
                    seen.add((rr, cc))
                    q.append((rr, cc))
        return seen

    def part_1(self, input_data: InputData) -> Output1:
        return len(self.ignite({(0, 0)}, input_data))

    def part_2(self, input_data: InputData) -> Output2:
        return len(
            self.ignite(
                {(0, 0), (len(input_data) - 1, len(input_data[0]) - 1)},
                input_data,
            )
        )

    def part_3(self, input_data: InputData) -> Output3:
        def find_best(exploded: set[Cell]) -> set[Cell]:
            best = (0, set[Cell]())
            seen = set(exploded)
            for _, barrel in sorted(
                (
                    (ch, (r, c))
                    for r, line in enumerate(input_data)
                    for c, ch in enumerate(line)
                ),
                reverse=True,
            ):
                if barrel in seen:
                    continue
                new_exploded = (
                    self.ignite({barrel}, input_data, exploded) - exploded
                )
                seen |= new_exploded
                if len(new_exploded) > best[0]:
                    best = (len(new_exploded), new_exploded)
            return best[1]

        return len(
            reduce(
                lambda seen, _: operator.ior(seen, find_best(seen)),
                range(3),
                set(),
            )
        )

    @ec_samples(
        (
            ("part_1", TEST1, 16),
            ("part_2", TEST2, 58),
            ("part_3", TEST3, 14),
            ("part_3", TEST4, 136),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 12)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
