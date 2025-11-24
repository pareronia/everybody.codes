package com.github.pareronia.everybody_codes;

import static com.github.pareronia.everybody_codes.utils.IntegerSequence.Range.range;

import static java.util.stream.Collectors.toMap;

import com.github.pareronia.everybody_codes.geometry.Direction;
import com.github.pareronia.everybody_codes.geometry.Turn;
import com.github.pareronia.everybody_codes.graph.BFS;
import com.github.pareronia.everybody_codes.grid.Cell;
import com.github.pareronia.everybody_codes.grid.CharGrid;
import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.stream.Stream;

@SuppressWarnings({"PMD.ClassNamingConventions", "PMD.UseExplicitTypes"})
public final class Quest2025_15 extends SolutionBase<Integer, Integer, Long> {

    private static final String TEST1 = "R3,R4,L3,L4,R3,R6,R9";
    private static final String TEST2 =
            "L6,L3,L6,R3,L6,L3,L3,R6,L6,R6,L6,L6,R3,L3,L3,R3,R3,L6,L6,L3";

    private Quest2025_15(final boolean debug) {
        super(debug);
    }

    public static Quest2025_15 create() {
        return new Quest2025_15(false);
    }

    public static Quest2025_15 createDebug() {
        return new Quest2025_15(true);
    }

    @Override
    public Integer solvePart1(final List<String> input) {
        return this.solve(input);
    }

    @Override
    public Integer solvePart2(final List<String> input) {
        return this.solve(input);
    }

    @Override
    public Long solvePart3(final List<String> input) {
        return (long) this.solve(input);
    }

    private int solve(final List<String> input) {
        final var instructions =
                Arrays.stream(input.getFirst().split(",")).map(Instruction::fromInput).toList();
        final CompressedMaze maze = CompressedMaze.fromInstructions(instructions);
        log(() -> maze.grid().asString());
        return maze.solve();
    }

    private record Instruction(Turn turn, int amount) {

        public static Instruction fromInput(final String input) {
            return new Instruction(
                    Turn.fromChar(input.charAt(0)), Integer.parseInt(input.substring(1)));
        }
    }

    private record CompressedMaze(
            CharGrid grid, Cell start, Cell end, List<Integer> rows, List<Integer> cols) {

        public static CompressedMaze fromInstructions(final List<Instruction> instructions) {
            final List<Integer> tmpRows = new ArrayList<>();
            final List<Integer> tempCols = new ArrayList<>();
            Cell cell = Cell.at(0, 0);
            tmpRows.add(cell.row());
            tempCols.add(cell.col());
            var direction = Direction.UP;
            for (final var instruction : instructions) {
                direction = direction.turn(instruction.turn());
                cell = cell.at(direction, instruction.amount);
                if (direction.isHorizontal()) {
                    tempCols.add(cell.col());
                    tempCols.add(cell.at(direction).col());
                    tmpRows.add(cell.row() - 1);
                    tmpRows.add(cell.row() + 1);
                } else {
                    tempCols.add(cell.col() - 1);
                    tempCols.add(cell.col() + 1);
                    tmpRows.add(cell.row());
                    tmpRows.add(cell.at(direction).row());
                }
            }
            final var rows = tmpRows.stream().distinct().sorted().toList();
            final var cols = tempCols.stream().distinct().sorted().toList();
            final var cRows = range(rows.size()).stream().collect(toMap(i -> rows.get(i), i -> i));
            final var cCols = range(cols.size()).stream().collect(toMap(i -> cols.get(i), i -> i));
            final Cell start = Cell.at(cRows.get(0), cCols.get(0));
            final Cell end = Cell.at(cRows.get(cell.row()), cCols.get(cell.col()));
            final CharGrid grid = buildGrid(instructions, cRows, cCols);
            grid.setValue(start, 'S');
            grid.setValue(end, 'E');
            return new CompressedMaze(grid, start, end, rows, cols);
        }

        @SuppressWarnings("PMD.AvoidInstantiatingObjectsInLoops")
        private static CharGrid buildGrid(
                final List<Instruction> instructions,
                final Map<Integer, Integer> cRows,
                final Map<Integer, Integer> cCols) {
            final char[][] gridChars = new char[cRows.size()][cCols.size()];
            for (int j = 0; j < gridChars.length; j++) {
                final var row = new char[cCols.size()];
                Arrays.fill(row, '.');
                gridChars[j] = row;
            }
            Cell cell = Cell.at(0, 0);
            Direction direction = Direction.UP;
            for (final var instruction : instructions) {
                direction = direction.turn(instruction.turn());
                final Cell nxt = cell.at(direction, instruction.amount);
                if (direction.isHorizontal()) {
                    final int col0 = Math.min(cCols.get(cell.col()), cCols.get(nxt.col()));
                    final int col1 = Math.max(cCols.get(cell.col()), cCols.get(nxt.col()));
                    final int row0 = cRows.get(cell.row());
                    for (int j = col0; j <= col1; j++) {
                        gridChars[row0][j] = '#';
                    }
                } else {
                    final int row0 = Math.min(cRows.get(cell.row()), cRows.get(nxt.row()));
                    final int row1 = Math.max(cRows.get(cell.row()), cRows.get(nxt.row()));
                    final int col0 = cCols.get(cell.col());
                    for (int j = row0; j <= row1; j++) {
                        gridChars[j][col0] = '#';
                    }
                }
                cell = nxt;
            }
            return new CharGrid(gridChars);
        }

        public int solve() {
            final Function<Cell, Stream<Cell>> adjacent =
                    cell ->
                            Direction.CAPITAL.stream()
                                    .map(cell::at)
                                    .filter(n -> this.grid.isInBounds(n))
                                    .filter(n -> this.grid.getValue(n) != '#');
            final BiFunction<Cell, Cell, Integer> cost =
                    (curr, nxt) ->
                            toOriginalCoordinates(curr)
                                    .manhattanDistance(toOriginalCoordinates(nxt));
            return BFS.executeWithCost(this.start, cell -> cell.equals(this.end), adjacent, cost);
        }

        private Cell toOriginalCoordinates(final Cell cell) {
            return Cell.at(this.rows.get(cell.row()), this.cols.get(cell.col()));
        }
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "6"),
        @Sample(method = "part1", input = TEST2, expected = "16"),
    })
    public static void main(final String[] args) {
        create().run();
    }
}
