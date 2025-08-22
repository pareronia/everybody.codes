#! /usr/bin/env python3
#
# everybody.codes 2024 Quest 7
#

import itertools
import sys
from collections import defaultdict

from ec.common import Cell
from ec.common import InputData
from ec.common import SolutionBase
from ec.graph import bfs_path

Output1 = str
Output2 = str
Output3 = int

TEST = """\
A:+,-,=,=
B:+,=,-,+
C:=,-,+,+
D:=,=,=,+
"""
TRACK1 = "=" * 10
TRACK2 = [
    "S-=++=-==++=++=-=+=-=+=+=--=-=++=-==++=-+=-=+=-=+=+=++=-+==++=++=-=-=--",
    "-                                                                     -",
    "=                                                                     =",
    "+                                                                     +",
    "=                                                                     +",
    "+                                                                     =",
    "=                                                                     =",
    "-                                                                     -",
    "--==++++==+=+++-=+=-=+=-+-=+-=+-=+=-=+=--=+++=++=+++==++==--=+=++==+++-",
]
TRACK3 = [
    "S+= +=-== +=++=     =+=+=--=    =-= ++=     +=-  =+=++=-+==+ =++=-=-=--",
    "- + +   + =   =     =      =   == = - -     - =  =         =-=        -",
    "= + + +-- =-= ==-==-= --++ +  == == = +     - =  =    ==++=    =++=-=++",
    "+ + + =     +         =  + + == == ++ =     = =  ==   =   = =++=       ",
    "= = + + +== +==     =++ == =+=  =  +  +==-=++ =   =++ --= + =          ",
    "+ ==- = + =   = =+= =   =       ++--          +     =   = = =--= ==++==",
    "=     ==- ==+-- = = = ++= +=--      ==+ ==--= +--+=-= ==- ==   =+=    =",
    "-               = = = =   +  +  ==+ = = +   =        ++    =          -",
    "-               = + + =   +  -  = + = = +   =        +     =          -",
    "--==++++==+=+++-= =-= =-+-=  =+-= =-= =--   +=++=+++==     -=+=++==+++-",
]


class Solution(SolutionBase[Output1, Output2, Output3]):
    def get_track(self, input_data: list[str]) -> str:
        _, path = bfs_path(
            Cell(0, 1),
            lambda cell: cell.row == 1 and cell.col == 0,
            lambda cell: (
                n
                for n in cell.get_capital_neighbours()
                if n.row >= 0
                and n.row < len(input_data)
                and n.col >= 0
                and n.col < len(input_data[0])
                and input_data[n.row][n.col] in {"+", "-", "="}
            ),
        )
        return (
            "".join(input_data[cell.row][cell.col] for cell in path[::-1])
            + "S"
        )

    def run_race(
        self, input_data: list[tuple[str, list[str]]], track: str, loops: int
    ) -> dict[str, list[int]]:
        d = defaultdict[str, list[int]](list)
        for line in input_data:
            k, plan = line
            d[k] = [10]
            actions = itertools.cycle(plan)
            for _ in range(loops):
                for t in track:
                    v = next(actions)
                    v = t if t in {"+", "-"} else v
                    d[k].append(
                        d[k][-1] + (1 if v == "+" else -1 if v == "-" else 0)
                    )
        return d

    def ranked(self, input_data: InputData, track: str) -> str:
        plans = []
        for line in input_data:
            k, rest = line.split(":")
            plans.append((k, rest.split(",")))
        d = self.run_race(plans, track, 10)
        return "".join(
            sorted(
                d.keys(),
                key=lambda k: sum(d[k][1:]),
                reverse=True,
            )
        )

    def part_1(self, input_data: InputData) -> Output1:
        return self.ranked(input_data, TRACK1)

    def part_2(self, input_data: InputData) -> Output2:
        return self.ranked(input_data, self.get_track(TRACK2))

    def part_3(self, input_data: InputData) -> Output3:
        """https://old.reddit.com/r/everybodycodes/comments/1gpylzn/2024_q7_solution_spotlight/lwurl8x/.

        If each 11 laps results in the same increase in power and essence
        then we can multiple a shorter race of 11 laps by 184 to get the answer
        faster
        """
        track = self.get_track(TRACK3)
        k, plan = input_data[0].split(":")
        d = self.run_race([(k, plan.split(","))], track, 11)
        rival = sum(d["A"][1:])
        strategies = set(
            itertools.permutations(
                ["+", "-", "=", "+", "-", "=", "+", "-", "=", "+", "+"]
            )
        )
        ans = 0
        for s in strategies:
            d = self.run_race([("A", list(s))], track, 11)
            if sum(d["A"][1:]) > rival:
                ans += 1
        return ans

    def samples(self) -> None:
        test = tuple(_ for _ in TEST.splitlines())
        assert self.part_1(test) == "BDCA"
        assert self.ranked(test, "+===++-=+=-S") == "DCBA"


solution = Solution(2024, 7)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
