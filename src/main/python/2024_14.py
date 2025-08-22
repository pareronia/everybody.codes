#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 14
#

import sys
from collections import Counter
from collections.abc import Iterator

from ec.common import Direction3D
from ec.common import InputData
from ec.common import Position3D
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.graph import bfs_full

Output1 = int
Output2 = int
Output3 = int
Segment = tuple[int, int, int]

TEST1 = """\
U5,R3,D2,L5,U4,R5,D2
"""
TEST2 = """\
U5,R3,D2,L5,U4,R5,D2
U6,L1,D2,R3,U2,L1
"""
TEST3 = """\
U20,L1,B1,L2,B1,R2,L1,F1,U1
U10,F1,B1,R1,L1,B1,L1,F1,R2,U1
U30,L2,F1,R1,B1,R1,F2,U1,F1
U25,R1,L2,B1,U1,R2,F1,L2
U16,L1,B1,L1,B3,L1,B1,F1
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def grow(
        self, input_data: InputData
    ) -> tuple[set[Position3D], set[Position3D]]:
        segments, leaves = set(), set()
        for line in input_data:
            curr = Position3D(0, 0, 0)
            for step in line.split(","):
                d, a = step[0], int(step[1:])
                direction = Direction3D.from_str(d)
                for _ in range(a):
                    nxt = curr.at(direction)
                    segments.add(nxt)
                    curr = nxt
            leaves.add(curr)
        return segments, leaves

    def part_1(self, input_data: InputData) -> Output1:
        segments, _ = self.grow(input_data)
        return max(y for _, y, _ in segments)

    def part_2(self, input_data: InputData) -> Output2:
        segments, _ = self.grow(input_data)
        return len(segments)

    def part_3(self, input_data: InputData) -> Output3:
        def adjacent(s: Position3D) -> Iterator[Position3D]:
            return (
                n for d in Direction3D.capitals() if (n := s.at(d)) in segments
            )

        segments, leaves = self.grow(input_data)
        trunk = {s for s in segments if s.x == 0}
        dist = Counter[Position3D]()
        for lv in leaves:
            dist += bfs_full(lv, lambda s: s in trunk, adjacent)
        return min(dist.values())

    @ec_samples(
        (
            ("part_1", TEST1, 7),
            ("part_2", TEST2, 32),
            ("part_3", TEST2, 5),
            ("part_3", TEST3, 46),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2024, 14)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
