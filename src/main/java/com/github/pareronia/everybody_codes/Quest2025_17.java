package com.github.pareronia.everybody_codes;

import static com.github.pareronia.everybody_codes.utils.IntegerSequence.Range.range;
import static com.github.pareronia.everybody_codes.utils.IntegerSequence.Range.rangeClosed;

import static java.util.Comparator.comparing;
import static java.util.stream.Collectors.toSet;

import com.github.pareronia.everybody_codes.geometry.Direction;
import com.github.pareronia.everybody_codes.graph.Dijkstra;
import com.github.pareronia.everybody_codes.graph.Dijkstra.Result;
import com.github.pareronia.everybody_codes.grid.Cell;
import com.github.pareronia.everybody_codes.grid.IntGrid;
import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.AssertUtils;
import com.github.pareronia.everybody_codes.utils.StringUtils;

import java.util.List;
import java.util.Set;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.stream.IntStream;
import java.util.stream.Stream;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_17 extends SolutionBase<Integer, Integer, Long> {

    private static final String TEST1 =
            """
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
            """;
    private static final String TEST2 =
            """
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
            """;
    private static final String TEST3 =
            """
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
            """;
    private static final String TEST4 =
            """
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
            """;
    private static final String TEST5 =
            """
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
            """;

    private Quest2025_17(final boolean debug) {
        super(debug);
    }

    public static Quest2025_17 create() {
        return new Quest2025_17(false);
    }

    public static Quest2025_17 createDebug() {
        return new Quest2025_17(true);
    }

    @Override
    public Integer solvePart1(final List<String> input) {
        final Field field = Field.fromInput(input);
        return rangeClosed(1, 10).stream().mapToInt(r -> field.value(field.lavaGrowth(r))).sum();
    }

    @Override
    public Integer solvePart2(final List<String> input) {
        record Step(int radius, Set<Cell> cells, int damage) {
            public static Step create(final Field field, final int radius) {
                final Set<Cell> cells = field.lavaGrowth(radius);
                return new Step(radius, cells, field.value(cells));
            }
        }

        final Field field = Field.fromInput(input);
        return IntStream.iterate(1, r -> r + 1)
                .mapToObj(r -> Step.create(field, r))
                .takeWhile(step -> step.cells().stream().noneMatch(field::onEdge))
                .max(comparing(Step::damage))
                .map(step -> step.radius * step.damage)
                .get();
    }

    @Override
    public Long solvePart3(final List<String> input) {
        record State(Cell cell, @SuppressWarnings("PMD.ShortVariable") int z) {}

        final Field field = Field.fromInput(input);
        final State start = new State(field.start, 0);
        final State end = new State(field.start, 1);
        final BiFunction<State, Cell, Integer> zed =
                (curr, nxt) ->
                        field.ccwAroundVulcano(curr.cell, nxt)
                                ? 1
                                : field.cwAroundVulcano(curr.cell, nxt) ? 0 : curr.z;
        final BiFunction<State, State, Long> cost =
                (curr, nxt) -> (long) field.value(Set.of(nxt.cell));

        int radius = 1;
        while (field.volcano().row() + radius < field.grid().getHeight()) {
            final long limit = (radius + 1) * 30;
            final Set<Cell> cells = field.lavaGrowth(radius);
            @SuppressWarnings("PMD.AvoidInstantiatingObjectsInLoops")
            final Function<State, Stream<State>> adjacent =
                    state ->
                            Direction.CAPITAL.stream()
                                    .map(state.cell::at)
                                    .filter(field.grid()::isInBounds)
                                    .filter(nxt -> !cells.contains(nxt))
                                    .map(nxt -> new State(nxt, zed.apply(state, nxt)));
            final Result<State> result =
                    Dijkstra.best(start, cell -> cell.equals(end), adjacent, cost, limit);
            if (result != Result.NONE && result.getDistance(end) < limit) {
                return result.getDistance(end) * radius;
            }
            radius++;
        }
        throw AssertUtils.unreachable();
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "1573"),
        @Sample(method = "part2", input = TEST2, expected = "1090"),
        @Sample(method = "part3", input = TEST3, expected = "592"),
        @Sample(method = "part3", input = TEST4, expected = "330"),
        @Sample(method = "part3", input = TEST5, expected = "3180"),
    })
    public static void main(final String[] args) {
        create().run();
    }

    private record Field(IntGrid grid, Cell volcano, Cell start) {

        public static Field fromInput(final List<String> input) {
            final Cell volcano =
                    range(input.size()).stream()
                            .flatMap(
                                    r ->
                                            range(input.get(r).length())
                                                    .intStream()
                                                    .mapToObj(c -> Cell.at(r, c)))
                            .filter(cell -> input.get(cell.row()).charAt(cell.col()) == '@')
                            .findFirst()
                            .orElseThrow();
            final Cell start =
                    range(input.size()).stream()
                            .flatMap(
                                    r ->
                                            range(input.get(r).length())
                                                    .intStream()
                                                    .mapToObj(c -> Cell.at(r, c)))
                            .filter(cell -> input.get(cell.row()).charAt(cell.col()) == 'S')
                            .findFirst()
                            .orElse(null);
            final int[][] values =
                    input.stream()
                            .map(
                                    line ->
                                            StringUtils.asCharacterStream(line)
                                                    .mapToInt(
                                                            ch -> {
                                                                if (Set.of('@', 'S').contains(ch)) {
                                                                    return 0;
                                                                }
                                                                return Integer.parseInt(
                                                                        String.valueOf(ch));
                                                            })
                                                    .toArray())
                            .toArray(int[][]::new);
            return new Field(new IntGrid(values), volcano, start);
        }

        public Set<Cell> lavaGrowth(final int radius) {
            final int inner = (radius - 1) * (radius - 1);
            final int outer = radius * radius;
            return this.grid
                    .getCells()
                    .filter(cell -> !cell.equals(volcano))
                    .filter(
                            cell -> {
                                final int dRow = volcano.row() - cell.row();
                                final int dCol = volcano.col() - cell.col();
                                final int dist = dRow * dRow + dCol * dCol;
                                return inner < dist && dist <= outer;
                            })
                    .collect(toSet());
        }

        public boolean onEdge(final Cell cell) {
            return cell.row() == 0
                    || cell.row() == this.grid.getMaxRowIndex()
                    || cell.col() == 0
                    || cell.col() == this.grid.getMaxColIndex();
        }

        public int value(final Set<Cell> cells) {
            return cells.stream().mapToInt(this.grid::getValue).sum();
        }

        public boolean ccwAroundVulcano(final Cell curr, final Cell nxt) {
            return nxt.row() >= this.volcano.row()
                    && curr.col() < this.volcano.col()
                    && this.volcano.col() <= nxt.col();
        }

        public boolean cwAroundVulcano(final Cell curr, final Cell nxt) {
            return nxt.row() >= this.volcano.row()
                    && nxt.col() < this.volcano.col()
                    && this.volcano.col() <= curr.col();
        }
    }
}
