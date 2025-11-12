#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 7
#

import sys
from collections import defaultdict

from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples

TEST1 = """\
Oronris,Urakris,Oroneth,Uraketh

r > a,i,o
i > p,w
n > e,r
o > n,m
k > f,r
a > k
U > r
e > t
O > r
t > h
"""
TEST2 = """\
Xanverax,Khargyth,Nexzeth,Helther,Braerex,Tirgryph,Kharverax

r > v,e,a,g,y
a > e,v,x,r
e > r,x,v,t
h > a,e,v
g > r,y
y > p,t
i > v,r
K > h
v > e
B > r
t > h
N > e
p > h
H > e
l > t
z > e
X > a
n > v
x > z
T > i
"""
TEST3 = """\
Xaryt

X > a,o
a > r,t
r > y,e,a
h > a,e,v
t > h
v > e
y > p,t
"""
TEST4 = """\
Khara,Xaryt,Noxer,Kharax

r > v,e,a,g,y
a > e,v,x,r,g
e > r,x,v,t
h > a,e,v
g > r,y
y > p,t
i > v,r
K > h
v > e
B > r
t > h
N > e
p > h
H > e
l > t
z > e
X > a
n > v
x > z
T > i
"""

Output1 = str
Output2 = int
Output3 = int


class Solution(SolutionBase[Output1, Output2, Output3]):
    def parse(
        self, input_data: InputData
    ) -> tuple[list[str], dict[str, set[str]]]:
        names = input_data[0].split(",")
        edges = defaultdict[str, set[str]](set)
        for line in input_data[2:]:
            a, b = line.split(" > ")
            edges[a] |= set(b.split(","))
        return names, edges

    def possible(self, name: str, edges: dict[str, set[str]]) -> bool:
        return all(name[j] in edges[name[j - 1]] for j in range(1, len(name)))

    def part_1(self, input_data: InputData) -> Output1:
        names, edges = self.parse(input_data)
        return next(name for name in names if self.possible(name, edges))

    def part_2(self, input_data: InputData) -> Output2:
        names, edges = self.parse(input_data)
        return sum(
            i
            for i, name in enumerate(names, start=1)
            if self.possible(name, edges)
        )

    def part_3(self, input_data: InputData) -> Output3:
        def dfs(name: str, ans: set[str]) -> None:
            if 7 <= len(name) <= 11:
                ans.add(name)
            if len(name) < 11:
                for ch in edges[name[-1]]:
                    dfs(name + ch, ans)

        names, edges = self.parse(input_data)
        ans = set[str]()
        for name in names:
            if self.possible(name, edges):
                dfs(name, ans)
        return len(ans)

    @ec_samples(
        (
            ("part_1", TEST1, "Oroneth"),
            ("part_2", TEST2, 23),
            ("part_3", TEST3, 25),
            ("part_3", TEST4, 1154),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 7)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
