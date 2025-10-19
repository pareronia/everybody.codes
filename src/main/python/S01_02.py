#! /usr/bin/env python3
#
# everybody.codes S01 Quest 2
#

import sys
from dataclasses import dataclass
from enum import Enum
from enum import auto
from enum import unique
from typing import Self

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

TEST1 = """\
ADD id=1 left=[10,A] right=[30,H]
ADD id=2 left=[15,D] right=[25,I]
ADD id=3 left=[12,F] right=[31,J]
ADD id=4 left=[5,B] right=[27,L]
ADD id=5 left=[3,C] right=[28,M]
ADD id=6 left=[20,G] right=[32,K]
ADD id=7 left=[4,E] right=[21,N]
"""
TEST2 = """\
ADD id=1 left=[160,E] right=[175,S]
ADD id=2 left=[140,W] right=[224,D]
ADD id=3 left=[122,U] right=[203,F]
ADD id=4 left=[204,N] right=[114,G]
ADD id=5 left=[136,V] right=[256,H]
ADD id=6 left=[147,G] right=[192,O]
ADD id=7 left=[232,I] right=[154,K]
ADD id=8 left=[118,E] right=[125,Y]
ADD id=9 left=[102,A] right=[210,D]
ADD id=10 left=[183,Q] right=[254,E]
ADD id=11 left=[146,E] right=[148,C]
ADD id=12 left=[173,Y] right=[299,S]
ADD id=13 left=[190,B] right=[277,B]
ADD id=14 left=[124,T] right=[142,N]
ADD id=15 left=[153,R] right=[133,M]
ADD id=16 left=[252,D] right=[276,M]
ADD id=17 left=[258,I] right=[245,P]
ADD id=18 left=[117,O] right=[283,!]
ADD id=19 left=[212,O] right=[127,R]
ADD id=20 left=[278,A] right=[169,C]
"""
TEST3 = """\
ADD id=1 left=[10,A] right=[30,H]
ADD id=2 left=[15,D] right=[25,I]
ADD id=3 left=[12,F] right=[31,J]
ADD id=4 left=[5,B] right=[27,L]
ADD id=5 left=[3,C] right=[28,M]
SWAP 1
SWAP 5
ADD id=6 left=[20,G] right=[32,K]
ADD id=7 left=[4,E] right=[21,N]
"""
TEST4 = """\
ADD id=1 left=[10,A] right=[30,H]
ADD id=2 left=[15,D] right=[25,I]
ADD id=3 left=[12,F] right=[31,J]
ADD id=4 left=[5,B] right=[27,L]
ADD id=5 left=[3,C] right=[28,M]
SWAP 1
SWAP 5
ADD id=6 left=[20,G] right=[32,K]
ADD id=7 left=[4,E] right=[21,N]
SWAP 2
"""

L, R = "L", "R"


@dataclass
class Node:
    rank: int
    symbol: str
    left: Self | None = None
    right: Self | None = None

    @classmethod
    def from_input(cls, string: str) -> Self:
        rank, symbol = string[1:][:-1].split(",")
        return cls(int(rank), symbol)

    @classmethod
    def insert(cls, node: Self | None, other: Self) -> Self:
        if node is None:
            return other
        if node.rank < other.rank:
            node.left = cls.insert(node.left, other)
        elif node.rank > other.rank:
            node.right = cls.insert(node.right, other)
        return node

    def swap_data(self, other: Self) -> None:
        self.rank, other.rank = other.rank, self.rank
        self.symbol, other.symbol = other.symbol, self.symbol

    def swap_children(self, other: Self) -> None:
        self.left, other.left = other.left, self.left
        self.right, other.right = other.right, self.right

    def __hash__(self) -> int:
        return self.rank


@unique
class SwapMode(Enum):
    NONE = auto()
    NODE = auto()
    SUBTREE = auto()


Output1 = str
Output2 = str
Output3 = str


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, input_data: InputData, swap_mode: SwapMode) -> str:  # noqa:C901
        def build_tree() -> None:
            for line in input_data:
                if line.startswith("ADD"):
                    nid, left, right = (
                        s.split("=")[1] for s in line.split()[1:]
                    )
                    for s, l_r in zip((left, right), (L, R), strict=True):
                        node = Node.from_input(s)
                        nids[l_r][nid] = node
                        Node.insert(nids[l_r].get("1", None), node)
                else:
                    nid = line.split()[1]
                    if swap_mode != SwapMode.NONE:
                        nids[L][nid].swap_data(nids[R][nid])
                    if swap_mode == SwapMode.SUBTREE:
                        nids[L][nid].swap_children(nids[R][nid])

        def ans(nids: dict[str, Node]) -> str:
            def group_by_level(root: Node | None, level: int) -> None:
                if root is None:
                    return
                by_level.setdefault(level, set[Node]()).add(root)
                group_by_level(root.left, level + 1)
                group_by_level(root.right, level + 1)

            def get_symbols(root: Node | None, level: int) -> str:
                if root is None:
                    return ""
                root_level = next(k for k, v in by_level.items() if root in v)
                return (
                    (root.symbol if root_level == level else "")
                    + get_symbols(root.right, level)
                    + get_symbols(root.left, level)
                )

            by_level = dict[int, set[Node]]()
            group_by_level(nids["1"], 0)
            level = max(by_level.keys(), key=lambda k: len(by_level[k]))
            return get_symbols(nids["1"], level)

        nids = {L: dict[str, Node](), R: dict[str, Node]()}
        build_tree()
        return ans(nids[L]) + ans(nids[R])

    def part_1(self, input_data: InputData) -> Output1:
        return self.solve(input_data, SwapMode.NONE)

    def part_2(self, input_data: InputData) -> Output2:
        return self.solve(input_data, SwapMode.NODE)

    def part_3(self, input_data: InputData) -> Output3:
        return self.solve(input_data, SwapMode.SUBTREE)

    @ec_samples(
        (
            ("part_1", TEST1, "CFGNLK"),
            ("part_1", TEST2, "EVERYBODYCODES"),
            ("part_2", TEST3, "MGFLNK"),
            ("part_3", TEST4, "DJMGL"),
            ("part_3", TEST4 + "SWAP 5", "DJCGL"),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(1, 2)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
