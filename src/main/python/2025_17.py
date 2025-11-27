#! /usr/bin/env python3
#
# everybody.codes 2025 Quest 17
#

import sys
from collections.abc import Iterator
from dataclasses import dataclass
from math import prod
from typing import Self

from ec.common import Direction
from ec.common import InputData
from ec.common import SolutionBase
from ec.common import ec_samples
from ec.graph import dijkstra

TEST1 = """\
189482189843433862719
279415473483436249988
432746714658787816631
428219317375373724944
938163982835287292238
627369424372196193484
539825864246487765271
517475755641128575965
685934212385479112825
815992793826881115341
1737798467@7983146242
867597735651751839244
868364647534879928345
519348954366296559425
134425275832833829382
764324337429656245499
654662236199275446914
317179356373398118618
542673939694417586329
987342622289291613318
971977649141188759131
"""
TEST2 = """\
4547488458944
9786999467759
6969499575989
7775645848998
6659696497857
5569777444746
968586@767979
6476956899989
5659745697598
6874989897744
6479994574886
6694118785585
9568991647449
"""
TEST3 = """\
2645233S5466644
634566343252465
353336645243246
233343552544555
225243326235365
536334634462246
666344656233244
6426432@2366453
364346442652235
253652463426433
426666225623563
555462553462364
346225464436334
643362324542432
463332353552464
"""
TEST4 = """\
545233443422255434324
5222533434S2322342222
523444354223232542432
553522225435232255242
232343243532432452524
245245322252324442542
252533232225244224355
523533554454232553332
522332223232242523223
524523432425432244432
3532242243@4323422334
542524223994422443222
252343244322522222332
253355425454255523242
344324325233443552555
423523225325255345522
244333345244325322335
242244352245522323422
443332352222535334325
323532222353523253542
553545434425235223552
"""
TEST5 = """\
5441525241225111112253553251553
133522122534119S911411222155114
3445445533355599933443455544333
3345333555434334535435433335533
5353333345335554434535533555354
3533533435355443543433453355553
3553353435335554334453355435433
5435355533533355533535335345335
4353545353545354555534334453353
4454543553533544443353355553453
5334554534533355333355543533454
4433333345445354553533554555533
5554454343455334355445533453453
4435554534445553335434455334353
3533435453433535345355533545555
534433533533535@353533355553345
4453545555435334544453344455554
4353333535535354535353353535355
4345444453554554535355345343354
3534544535533355333333445433555
3535333335335334333534553543535
5433355333553344355555344553435
5355535355535334555435534555344
3355433335553553535334544544333
3554333535553335343555345553535
3554433545353554334554345343343
5533353435533535333355343333555
5355555353355553535354333535355
4344534353535455333455353335333
5444333535533453535335454535553
3534343355355355553543545553345
"""

Output1 = int
Output2 = int
Output3 = int
Cell = tuple[int, int]


@dataclass(frozen=True)
class Field:
    grid: tuple[str, ...]
    volcano: Cell
    start: Cell | None = None

    @classmethod
    def from_input(cls, input_data: InputData) -> Self:
        start = None
        for r in range(len(input_data)):
            for c in range(len(input_data[r])):
                if input_data[r][c] == "S":
                    start = (r, c)
                if input_data[r][c] == "@":
                    volcano = (r, c)
        return cls(input_data, volcano, start)

    def lava_growth(self, radius: int) -> set[Cell]:
        inner = (radius - 1) * (radius - 1)
        outer = radius * radius
        ans = set[Cell]()
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if (r, c) != self.volcano and inner < (self.volcano[0] - r) * (
                    self.volcano[0] - r
                ) + (self.volcano[1] - c) * (self.volcano[1] - c) <= outer:
                    ans.add((r, c))
        return ans

    def value(self, cells: set[Cell]) -> int:
        return sum(int(self.grid[r][c]) for r, c in cells)

    def ccw_around_volcano(self, curr: Cell, nxt: Cell) -> bool:
        return (
            nxt[0] >= self.volcano[0] and curr[1] < self.volcano[1] <= nxt[1]
        )

    def cw_around_volcano(self, curr: Cell, nxt: Cell) -> bool:
        return (
            nxt[0] >= self.volcano[0] and nxt[1] < self.volcano[1] <= curr[1]
        )


class Solution(SolutionBase[Output1, Output2, Output3]):
    def solve(self, input_data: InputData, radius: int) -> set[Cell]:
        ans = set[Cell]()
        rv, cv = len(input_data) // 2, len(input_data[0]) // 2
        inner = (radius - 1) * (radius - 1)
        outer = radius * radius
        for r in range(len(input_data)):
            for c in range(len(input_data[0])):
                if (r, c) == (rv, cv):
                    continue
                if inner < (rv - r) * (rv - r) + (cv - c) * (cv - c) <= outer:
                    ans.add((r, c))
        return ans

    def part_1(self, input_data: InputData) -> Output1:
        field = Field.from_input(input_data)
        return sum(field.value(field.lava_growth(r)) for r in range(1, 11))

    def part_2(self, input_data: InputData) -> Output2:
        field = Field.from_input(input_data)
        hi = max(
            (
                (radius, field.value(field.lava_growth(radius)))
                for radius in range(1, len(field.grid) // 2)
            ),
            key=lambda x: x[1],
        )
        return prod(hi)

    def part_3(self, input_data: InputData) -> Output3:
        field = Field.from_input(input_data)
        assert field.start is not None
        radius = 1
        while field.volcano[0] + radius < len(field.grid):
            cells = self.solve(input_data, radius)

            def adjacent(
                node: tuple[Cell, int], lava: set[Cell] = cells
            ) -> Iterator[tuple[Cell, int]]:
                cell, z = node
                for nr, nc in (
                    (cell[0] - d.y, cell[1] + d.x)
                    for d in Direction.capitals()
                ):
                    if (
                        0 <= nr < len(field.grid)
                        and 0 <= nc < len(field.grid[cell[0]])
                        and (nr, nc) not in lava
                    ):
                        new_z = (
                            1
                            if field.ccw_around_volcano(cell, (nr, nc))
                            else 0
                            if field.cw_around_volcano(cell, (nr, nc))
                            else z
                        )
                        yield ((nr, nc), new_z)

            limit = (radius + 1) * 30
            cost, _, _ = dijkstra(
                start=(field.start, 0),
                is_end=lambda node: node == (field.start, 1),
                adjacent=adjacent,
                get_cost=lambda _, nxt: 0
                if nxt[0] == field.start
                else int(input_data[nxt[0][0]][nxt[0][1]]),
                limit=limit,
            )
            if 0 < cost < limit:
                return cost * radius
            radius += 1
        raise AssertionError

    @ec_samples(
        (
            ("part_1", TEST1, 1573),
            ("part_2", TEST2, 1090),
            ("part_3", TEST3, 592),
            ("part_3", TEST4, 330),
            ("part_3", TEST5, 3180),
        )
    )
    def samples(self) -> None:
        pass


solution = Solution(2025, 17)


def main() -> None:
    solution.run(sys.argv)


if __name__ == "__main__":
    main()
