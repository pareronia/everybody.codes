#! /usr/bin/env python3
#
# everybody.codes S01 Quest 2
#

import sys
from dataclasses import dataclass
from typing import Self

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.common import log

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
TEST5 = (
    TEST4
    + """\
SWAP 5
"""
)


@dataclass
class Node:
    rank: int
    symbol: str
    left: Self | None = None
    right: Self | None = None

    def __hash__(self) -> int:
        return self.rank

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

    @classmethod
    def by_level(
        cls, root: Self | None, level: int, d: dict[int, set[Self]]
    ) -> None:
        if root is None:
            return
        d.setdefault(level, set[Self]()).add(root)
        cls.by_level(root.left, level + 1, d)
        cls.by_level(root.right, level + 1, d)

    @classmethod
    def ans(
        cls, root: Self | None, level: int, levels: dict[int, set[Self]]
    ) -> str:
        if root is None:
            return ""
        root_level = next(k for k, v in levels.items() if root in v)
        return (
            root.symbol
            if root_level == level
            else ""
            + cls.ans(root.right, level, levels)
            + cls.ans(root.left, level, levels)
        )


Output1 = str
Output2 = str
Output3 = str


class Solution(SolutionBase[Output1, Output2, Output3]):
    def part_1(self, input_data: InputData) -> Output1:
        root_left, root_right = None, None
        for line in input_data:
            _, nid, left, right = line.split()
            left, right = left.split("=")[1], right.split("=")[1]
            if nid.split("=")[1] == "1":
                root_left = Node.insert(root_left, Node.from_input(left))
                root_right = Node.insert(root_right, Node.from_input(right))
            else:
                Node.insert(root_left, Node.from_input(left))
                Node.insert(root_right, Node.from_input(right))
        left_d, right_d = dict[int, set[Node]](), dict[int, set[Node]]()
        Node.by_level(root_left, 0, left_d)
        Node.by_level(root_right, 0, right_d)
        left_m = max(left_d.items(), key=lambda item: len(item[1]))[0]
        right_m = max(right_d.items(), key=lambda item: len(item[1]))[0]
        return Node.ans(root_left, left_m, left_d) + Node.ans(
            root_right, right_m, right_d
        )

    def part_2(self, input_data: InputData) -> Output2:
        root_left, root_right = None, None
        nids_left, nids_right = dict[str, Node](), dict[str, Node]()
        for line in input_data:
            if line.startswith("ADD"):
                _, nid, left, right = line.split()
                nid = nid.split("=")[1]
                left, right = left.split("=")[1], right.split("=")[1]
                if nid == "1":
                    root_left = Node.insert(root_left, Node.from_input(left))
                    nids_left[nid] = root_left
                    root_right = Node.insert(
                        root_right, Node.from_input(right)
                    )
                    nids_right[nid] = root_right
                else:
                    node = Node.from_input(left)
                    nids_left[nid] = node
                    Node.insert(root_left, node)
                    node = Node.from_input(right)
                    nids_right[nid] = node
                    Node.insert(root_right, node)
            else:
                _, nid = line.split()
                swap_left, swap_right = nids_left[nid], nids_right[nid]
                tmp_rank, tmp_symbol = swap_right.rank, swap_right.symbol
                swap_right.rank = swap_left.rank
                swap_right.symbol = swap_left.symbol
                swap_left.rank = tmp_rank
                swap_left.symbol = tmp_symbol
        left_d, right_d = dict[int, set[Node]](), dict[int, set[Node]]()
        Node.by_level(root_left, 0, left_d)
        Node.by_level(root_right, 0, right_d)
        left_m = max(left_d.items(), key=lambda item: len(item[1]))[0]
        right_m = max(right_d.items(), key=lambda item: len(item[1]))[0]
        return Node.ans(root_left, left_m, left_d) + Node.ans(
            root_right, right_m, right_d
        )

    def part_3(self, input_data: InputData) -> Output3:
        root_left, root_right = None, None
        nids_left, nids_right = dict[str, Node](), dict[str, Node]()
        for line in input_data:
            if line.startswith("ADD"):
                _, nid, left, right = line.split()
                nid = nid.split("=")[1]
                left, right = left.split("=")[1], right.split("=")[1]
                if nid == "1":
                    root_left = Node.insert(root_left, Node.from_input(left))
                    nids_left[nid] = root_left
                    root_right = Node.insert(
                        root_right, Node.from_input(right)
                    )
                    nids_right[nid] = root_right
                else:
                    node = Node.from_input(left)
                    nids_left[nid] = node
                    Node.insert(root_left, node)
                    node = Node.from_input(right)
                    nids_right[nid] = node
                    Node.insert(root_right, node)
            else:
                _, nid = line.split()
                swap_left, swap_right = nids_left[nid], nids_right[nid]
                swap_left.rank, swap_right.rank = (
                    swap_right.rank,
                    swap_left.rank,
                )
                swap_left.symbol, swap_right.symbol = (
                    swap_right.symbol,
                    swap_left.symbol,
                )
                swap_left.left, swap_right.left = (
                    swap_right.left,
                    swap_left.left,
                )
                swap_left.right, swap_right.right = (
                    swap_right.right,
                    swap_left.right,
                )
        log((root_left, root_right))
        left_d, right_d = dict[int, set[Node]](), dict[int, set[Node]]()
        Node.by_level(root_left, 0, left_d)
        Node.by_level(root_right, 0, right_d)
        left_m = max(left_d.items(), key=lambda item: len(item[1]))[0]
        right_m = max(right_d.items(), key=lambda item: len(item[1]))[0]
        return Node.ans(root_left, left_m, left_d) + Node.ans(
            root_right, right_m, right_d
        )

    @ec_samples(
        (
            ("part_1", TEST1, "CFGNLK"),
            ("part_1", TEST2, "EVERYBODYCODES"),
            ("part_2", TEST3, "MGFLNK"),
            ("part_3", TEST4, "DJMGL"),
            ("part_3", TEST5, "DJCGL"),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(1, 2)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
