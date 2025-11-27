#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 18
#

import sys
from collections import defaultdict
from functools import cache

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.common import to_blocks

TEST1 = """\
Plant 1 with thickness 1:
- free branch with thickness 1

Plant 2 with thickness 1:
- free branch with thickness 1

Plant 3 with thickness 1:
- free branch with thickness 1

Plant 4 with thickness 17:
- branch to Plant 1 with thickness 15
- branch to Plant 2 with thickness 3

Plant 5 with thickness 24:
- branch to Plant 2 with thickness 11
- branch to Plant 3 with thickness 13

Plant 6 with thickness 15:
- branch to Plant 3 with thickness 14

Plant 7 with thickness 10:
- branch to Plant 4 with thickness 15
- branch to Plant 5 with thickness 21
- branch to Plant 6 with thickness 34
"""
TEST2 = """\
Plant 1 with thickness 1:
- free branch with thickness 1

Plant 2 with thickness 1:
- free branch with thickness 1

Plant 3 with thickness 1:
- free branch with thickness 1

Plant 4 with thickness 10:
- branch to Plant 1 with thickness -25
- branch to Plant 2 with thickness 17
- branch to Plant 3 with thickness 12

Plant 5 with thickness 14:
- branch to Plant 1 with thickness 14
- branch to Plant 2 with thickness -26
- branch to Plant 3 with thickness 15

Plant 6 with thickness 150:
- branch to Plant 4 with thickness 5
- branch to Plant 5 with thickness 6


1 0 1
0 0 1
0 1 1
"""
TEST3 = """\
Plant 1 with thickness 1:
- free branch with thickness 1

Plant 2 with thickness 1:
- free branch with thickness 1

Plant 3 with thickness 1:
- free branch with thickness 1

Plant 4 with thickness 1:
- free branch with thickness 1

Plant 5 with thickness 8:
- branch to Plant 1 with thickness -8
- branch to Plant 2 with thickness 11
- branch to Plant 3 with thickness 13
- branch to Plant 4 with thickness -7

Plant 6 with thickness 7:
- branch to Plant 1 with thickness 14
- branch to Plant 2 with thickness -9
- branch to Plant 3 with thickness 12
- branch to Plant 4 with thickness 9

Plant 7 with thickness 23:
- branch to Plant 5 with thickness 17
- branch to Plant 6 with thickness 18


0 1 0 0
0 1 0 1
0 1 1 1
1 1 0 1
"""

Output1 = int
Output2 = int
Output3 = int
Plant = tuple[int, int]
Branch = tuple[int, int]


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input_data: InputData) -> Output1:
        blocks = to_blocks(input_data)
        free = list[int]()
        plants = dict[int, int]()
        branches = defaultdict[int, set[Branch]](set)
        for block in blocks:
            sp = block[0][:-1].split()
            plant, thickness = int(sp[1]), int(sp[4])
            plants[plant] = thickness
            for line in block[1:]:
                sp = line[2:].split()
                if sp[0] == "free":
                    free.append(plant)
                else:
                    branches[plant].add((int(sp[3]), int(sp[6])))

        def energy(plant: int) -> int:
            if plant in free:
                return 1
            ans = 0
            for branch, thickness in branches[plant]:
                e = energy(branch)
                if e >= plants[branch]:
                    ans += e * thickness
            return ans

        pl = max(plants.keys())
        return energy(pl)

    def part_2(self, input_data: InputData) -> Output2:  # noqa:C901
        blocks = to_blocks(input_data)
        free = list[int]()
        plants = dict[int, int]()
        branches = defaultdict[int, set[Branch]](set)
        for block in blocks[:-2]:
            sp = block[0][:-1].split()
            plant, thickness = int(sp[1]), int(sp[4])
            plants[plant] = thickness
            for line in block[1:]:
                sp = line[2:].split()
                if sp[0] == "free":
                    free.append(plant)
                else:
                    branches[plant].add((int(sp[3]), int(sp[6])))

        @cache
        def leaves(root: int) -> list[int]:
            if root in free:
                return [root]
            ans = set[int]()
            for branch in sorted(b[0] for b in branches[root]):
                ans |= set(leaves(branch))
            return sorted(ans)

        @cache
        def energy(plant: int, switch: tuple[tuple[int, int], ...]) -> int:
            if plant in free:
                return next(v for i, v in switch if i == plant)
            ans = 0
            lvs = leaves(plant)
            new_switch = tuple(
                (i, v) for lv in lvs for i, v in switch if i == lv
            )
            for branch, thickness in branches[plant]:
                e = energy(branch, new_switch)
                if e >= plants[branch]:
                    ans += e * thickness
            return ans

        pl = max(plants.keys())
        ans = 0
        for line in blocks[-1]:
            switch = tuple(
                (i, v)
                for i, v in enumerate(list(map(int, line.split())), start=1)
            )
            e = energy(pl, switch)
            if e >= plants[pl]:
                ans += e
        return ans

    def part_3(self, input_data: InputData) -> Output3:  # noqa:C901
        blocks = to_blocks(input_data)
        free = list[int]()
        plants = dict[int, int]()
        branches = defaultdict[int, set[Branch]](set)
        for block in blocks[:-2]:
            sp = block[0][:-1].split()
            plant, thickness = int(sp[1]), int(sp[4])
            plants[plant] = thickness
            for line in block[1:]:
                sp = line[2:].split()
                if sp[0] == "free":
                    free.append(plant)
                else:
                    branches[plant].add((int(sp[3]), int(sp[6])))

        def total(switch: list[int]) -> int:
            e = {i + 1: switch[i] for i in range(len(switch))}
            for pl in range(len(free) + 1, len(plants) + 1):
                ans = 0
                for branch, thickness in branches[pl]:
                    ans += e[branch] * thickness
                e[pl] = ans if ans >= plants[pl] else 0
            return e[max(plants.keys())]

        switch = [0] * len(free)
        for br in branches.values():
            for b, thickness in br:
                if b in free and thickness > 0:
                    switch[b - 1] = 1
        best = total(switch)
        ans = list[int]()
        for line in blocks[-1]:
            switch = list(map(int, line.split()))
            e = total(switch)
            if e > 0:
                ans.append(e)
        return sum(best - a for a in ans)

    @ec_samples(
        (
            ("part_1", TEST1, 774),
            ("part_2", TEST2, 324),
            # ("part_3", TEST3, 946),  # noqa:ERA001
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 18)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
