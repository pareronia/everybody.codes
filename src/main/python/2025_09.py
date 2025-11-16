#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 9
#

import itertools
import sys
from collections import defaultdict

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.graph import connected_components

Output1 = int
Output2 = int
Output3 = int

TEST1 = """\
1:CAAGCGCTAAGTTCGCTGGATGTGTGCCCGCG
2:CTTGAATTGGGCCGTTTACCTGGTTTAACCAT
3:CTAGCGCTGAGCTGGCTGCCTGGTTGACCGCG
"""
TEST2 = """\
1:GCAGGCGAGTATGATACCCGGCTAGCCACCCC
2:TCTCGCGAGGATATTACTGGGCCAGACCCCCC
3:GGTGGAACATTCGAAAGTTGCATAGGGTGGTG
4:GCTCGCGAGTATATTACCGAACCAGCCCCTCA
5:GCAGCTTAGTATGACCGCCAAATCGCGACTCA
6:AGTGGAACCTTGGATAGTCTCATATAGCGGCA
7:GGCGTAATAATCGGATGCTGCAGAGGCTGCTG
"""
TEST3 = """\
1:GCAGGCGAGTATGATACCCGGCTAGCCACCCC
2:TCTCGCGAGGATATTACTGGGCCAGACCCCCC
3:GGTGGAACATTCGAAAGTTGCATAGGGTGGTG
4:GCTCGCGAGTATATTACCGAACCAGCCCCTCA
5:GCAGCTTAGTATGACCGCCAAATCGCGACTCA
6:AGTGGAACCTTGGATAGTCTCATATAGCGGCA
7:GGCGTAATAATCGGATGCTGCAGAGGCTGCTG
8:GGCGTAAAGTATGGATGCTGGCTAGGCACCCG
"""


class Solution(SolutionBase[Output1, Output2, Output3]):
    def is_child(self, child: str, parent_1: str, parent_2: str) -> bool:
        for i in range(len(child)):
            ch = child[i]
            if ch != parent_1[i] and ch != parent_2[i]:
                return False
        return True

    def similarity(self, dna_1: str, dna_2: str, dna_3: str) -> int:
        if self.is_child(dna_1, dna_2, dna_3):
            child, parent_1, parent_2 = dna_1, dna_2, dna_3
        elif self.is_child(dna_2, dna_1, dna_3):
            child, parent_1, parent_2 = dna_2, dna_1, dna_3
        elif self.is_child(dna_3, dna_1, dna_2):
            child, parent_1, parent_2 = dna_3, dna_1, dna_2
        else:
            return 0
        ans_1, ans_2 = 0, 0
        for i in range(len(child)):
            ch = child[i]
            ans_1 += ch == parent_1[i]
            ans_2 += ch == parent_2[i]
        return ans_1 * ans_2

    def part_1(self, input_data: InputData) -> Output1:
        dnas = [line.split(":")[1] for line in input_data]
        return self.similarity(dnas[0], dnas[1], dnas[2])

    def part_2(self, input_data: InputData) -> Output2:
        dnas = [line.split(":")[1] for line in input_data]
        return sum(
            self.similarity(dnas[i], dnas[j], dnas[k])
            for i, j, k in itertools.combinations(range(len(dnas)), 3)
        )

    def part_3(self, input_data: InputData) -> Output3:
        dnas = [line.split(":")[1] for line in input_data]
        children = [0] * len(dnas)
        edges = defaultdict[int, set[int]](set)
        for i, j, k in itertools.combinations(range(len(dnas)), 3):
            dna_i, dna_j, dna_k = dnas[i], dnas[j], dnas[k]
            if children[i] != 1 and self.is_child(dna_i, dna_j, dna_k):
                children[i] = 1
                cid, pid_1, pid_2 = i, j, k
            elif children[j] != 1 and self.is_child(dna_j, dna_i, dna_k):
                children[j] = 1
                cid, pid_1, pid_2 = j, i, k
            elif children[k] != 1 and self.is_child(dna_k, dna_i, dna_j):
                children[k] = 1
                cid, pid_1, pid_2 = k, i, j
            else:
                continue
            edges[cid] |= {pid_1, pid_2}
            edges[pid_1].add(cid)
            edges[pid_2].add(cid)

        components = connected_components(
            set(edges.keys()), lambda n: (nxt for nxt in edges[n])
        )
        components.sort(key=len)
        return sum(n + 1 for n in components[-1])

    @ec_samples(
        (
            ("part_1", TEST1, 414),
            ("part_2", TEST2, 1245),
            ("part_3", TEST2, 12),
            ("part_3", TEST3, 36),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 9)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
