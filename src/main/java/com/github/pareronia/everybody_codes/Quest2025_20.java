package com.github.pareronia.everybody_codes;

import com.github.pareronia.everybody_codes.graph.BFS;
import com.github.pareronia.everybody_codes.grid.Cell;
import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;

import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Stream;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_20 extends SolutionBase<Long, Integer, Integer> {

    private static final String TEST1 =
            """
            T#TTT###T##
            .##TT#TT##.
            ..T###T#T..
            ...##TT#...
            ....T##....
            .....#.....
            """;
    private static final String TEST2 =
            """
            TTTTTTTTTTTTTTTTT
            .TTTT#T#T#TTTTTT.
            ..TT#TTTETT#TTT..
            ...TT#T#TTT#TT...
            ....TTT#T#TTT....
            .....TTTTTT#.....
            ......TT#TT......
            .......#TT.......
            ........S........
            """;
    private static final String TEST3 =
            """
            T####T#TTT##T##T#T#
            .T#####TTTT##TTT##.
            ..TTTT#T###TTTT#T..
            ...T#TTT#ETTTT##...
            ....#TT##T#T##T....
            .....#TT####T#.....
            ......T#TT#T#......
            .......T#TTT.......
            ........TT#........
            .........S.........
            """;

    private Quest2025_20(final boolean debug) {
        super(debug);
    }

    public static Quest2025_20 create() {
        return new Quest2025_20(false);
    }

    public static Quest2025_20 createDebug() {
        return new Quest2025_20(true);
    }

    @Override
    public Long solvePart1(final List<String> input) {
        final Triangle triangle = Triangle.fromInput(input);
        return triangle.cells().stream()
                .mapToLong(
                        cell -> {
                            final Set<Cell> cells = new HashSet<>();
                            cells.add(triangle.getRight(cell));
                            triangle.getDown(cell).ifPresent(cells::add);
                            return cells.stream().filter(triangle.cells()::contains).count();
                        })
                .sum();
    }

    @Override
    public Integer solvePart2(final List<String> input) {
        return Triangle.fromInput(input).solveMaze(Rotation.NONE);
    }

    @Override
    public Integer solvePart3(final List<String> input) {
        return Triangle.fromInput(input).solveMaze(Rotation.CLOCKWISE);
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "7"),
        @Sample(method = "part2", input = TEST2, expected = "32"),
        @Sample(method = "part3", input = TEST3, expected = "23"),
    })
    public static void main(final String[] args) {
        create().run();
    }

    private record RotatedCell(Cell cell, int rotation) {}

    private enum Rotation {
        NONE,
        CLOCKWISE;

        public RotatedCell execute(final Triangle triangle, final RotatedCell cell) {
            return switch (this) {
                case NONE -> cell;
                case CLOCKWISE ->
                        new RotatedCell(triangle.rotate(cell.cell), (cell.rotation + 1) % 3);
            };
        }
    }

    private record Triangle(
            List<String> input, Set<Cell> cells, Cell start, Cell end, int height, int width) {

        public static Triangle fromInput(final List<String> input) {
            final Set<Cell> cells = new HashSet<>();
            Cell start = null;
            Cell end = null;
            for (int r = 0; r < input.size(); r++) {
                for (int c = 0; c < input.get(r).length(); c++) {
                    switch (input.get(r).charAt(c)) {
                        case 'S':
                            start = Cell.at(r, c);
                            break;
                        case 'E':
                            end = Cell.at(r, c);
                            break;
                        case 'T':
                            break;
                        default:
                            continue;
                    }
                    cells.add(Cell.at(r, c));
                }
            }
            return new Triangle(input, cells, start, end, input.size(), input.getFirst().length());
        }

        private boolean isDownCell(final Cell cell) {
            return cell.row() % 2 == cell.col() % 2;
        }

        public Cell rotate(final Cell cell) {
            final int row = this.height - 1 - (cell.col() - cell.row()) / 2 - cell.row();
            final int col = (this.width - cell.col() + cell.row()) / 2 + cell.row();
            return isDownCell(cell) ? Cell.at(row, col) : Cell.at(row - 1, col);
        }

        public Cell getRight(final Cell cell) {
            return Cell.at(cell.row(), cell.col() + 1);
        }

        public Optional<Cell> getDown(final Cell cell) {
            return isDownCell(cell)
                    ? Optional.empty()
                    : Optional.of(Cell.at(cell.row() + 1, cell.col()));
        }

        @SuppressWarnings("PMD.ShortVariable")
        public int solveMaze(final Rotation rotation) {
            final Function<RotatedCell, Stream<RotatedCell>> adjacent =
                    r -> {
                        final RotatedCell nr = rotation.execute(this, r);
                        final Cell rotated = nr.cell();
                        final int nrotation = nr.rotation();
                        final Cell up =
                                Cell.at(
                                        rotated.row() + (isDownCell(rotated) ? -1 : 1),
                                        rotated.col());
                        final Cell left = Cell.at(rotated.row(), rotated.col() - 1);
                        final Cell right = getRight(rotated);
                        return Stream.of(rotated, up, left, right)
                                .filter(this.cells::contains)
                                .map(n -> new RotatedCell(n, nrotation));
                    };
            return BFS.execute(
                    new RotatedCell(this.start, 0), cell -> cell.cell.equals(this.end), adjacent);
        }
    }
}
