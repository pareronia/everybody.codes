package com.github.pareronia.everybody_codes;

import static com.github.pareronia.everybody_codes.utils.IntegerSequence.Range.range;

import static java.util.stream.Collectors.toSet;

import com.github.pareronia.everybody_codes.geometry.Direction;
import com.github.pareronia.everybody_codes.grid.Cell;
import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Stream;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_14 extends SolutionBase<Integer, Integer, Long> {

    private static final List<Direction> DIAGONALS =
            List.of(
                    Direction.RIGHT_AND_UP,
                    Direction.RIGHT_AND_DOWN,
                    Direction.LEFT_AND_DOWN,
                    Direction.LEFT_AND_UP);
    private static final char SYMBOL = '#';
    private static final String TEST1 =
            """
            .#.##.
            ##..#.
            ..##.#
            .#.##.
            .###..
            ###.##
            """;
    private static final String TEST2 =
            """
            #......#
            ..#..#..
            .##..##.
            ...##...
            ...##...
            .##..##.
            ..#..#..
            #......#
            """;

    private Quest2025_14(final boolean debug) {
        super(debug);
    }

    public static Quest2025_14 create() {
        return new Quest2025_14(false);
    }

    public static Quest2025_14 createDebug() {
        return new Quest2025_14(true);
    }

    private int solve(final List<String> input, final int rounds) {
        final FixedGrid grid = FixedGrid.fromInput(input);
        GameOfLife<Cell, boolean[][]> gol =
                new GameOfLife<>(
                        grid,
                        new Rules(),
                        this.key(grid.initialAlive(), input.size()),
                        alive -> this.key(alive, input.size()));
        int ans = 0;
        for (int i = 0; i < rounds; i++) {
            gol = gol.nextGeneration();
            ans += this.count(gol.alive(), 1);
        }
        return ans;
    }

    @Override
    public Integer solvePart1(final List<String> input) {
        return this.solve(input, 10);
    }

    @Override
    public Integer solvePart2(final List<String> input) {
        return this.solve(input, 2025);
    }

    @Override
    public Long solvePart3(final List<String> input) {
        final int gridSize = 34;
        final int patternSize = input.size();
        final int offset = gridSize / 2 - patternSize / 2;
        final Set<Cell> patternOn = new HashSet<>();
        final Set<Cell> patternOff = new HashSet<>();
        cells(patternSize / 2, patternSize / 2)
                .forEach(
                        cell -> {
                            final char chr = input.get(cell.row()).charAt(cell.col());
                            if (chr == SYMBOL) {
                                patternOn.add(Cell.at(cell.row() + offset, cell.col() + offset));
                            } else {
                                patternOff.add(Cell.at(cell.row() + offset, cell.col() + offset));
                            }
                        });
        GameOfLife<Cell, boolean[][]> gol =
                new GameOfLife<>(
                        SymmetricSquareGrid.create(gridSize / 2),
                        new Rules(),
                        this.key(Stream.of(), gridSize / 2),
                        set -> this.key(set, gridSize / 2));
        long ans = 0L;
        int round = 0;
        final int rounds = 1_000_000_000;
        final int period = 4095;
        while (round < rounds) {
            gol = gol.nextGeneration();
            final boolean[][] alive = gol.alive();
            if (patternOn.stream().allMatch(cell -> alive[cell.row()][cell.col()])
                    && patternOff.stream().noneMatch(cell -> alive[cell.row()][cell.col()])) {
                ans += this.count(alive, 4);
            }
            if (round == period) {
                final int cycles = rounds / period;
                round *= cycles;
                ans *= cycles;
                continue;
            } else {
                round++;
            }
        }
        return ans;
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "200"),
        @Sample(method = "part3", input = TEST2, expected = "278388552"),
    })
    public static void main(final String[] args) {
        create().run();
    }

    private static Stream<Cell> cells(final int height, final int width) {
        return range(height).stream().flatMap(r -> range(width).stream().map(c -> Cell.at(r, c)));
    }

    @SuppressWarnings("PMD.AssignmentInOperand")
    private boolean[][] key(final Stream<Cell> cells, final int size) {
        final boolean[][] ans = new boolean[size][size];
        cells.forEach(cell -> ans[cell.row()][cell.col()] = true);
        return ans;
    }

    private int count(final boolean[][] alive, final int factor) {
        int ans = 0;
        for (final boolean[] element : alive) {
            for (final boolean element2 : element) {
                ans += element2 ? factor : 0;
            }
        }
        return ans;
    }

    private record GameOfLife<T, U>(
            GameOfLife.Universe<T, U> type,
            GameOfLife.Rules<T, U> rules,
            U alive,
            Function<Stream<T>, U> convert) {

        public GameOfLife<T, U> withAlive(final U alive) {
            return new GameOfLife<>(this.type, this.rules, alive, convert);
        }

        public GameOfLife<T, U> nextGeneration() {
            return this.withAlive(
                    convert.apply(
                            this.type
                                    .getNeighbourCounts(this.alive)
                                    .filter(e -> this.rules.alive(e.cell(), e.count(), this.alive))
                                    .map(Universe.NeigbourCount::cell)));
        }

        @SuppressWarnings("PMD.ImplicitFunctionalInterface")
        public interface Universe<T, U> {
            Stream<NeigbourCount<T>> getNeighbourCounts(U alive);

            public record NeigbourCount<T>(T cell, long count) {}
        }

        @SuppressWarnings("PMD.ImplicitFunctionalInterface")
        public interface Rules<T, U> {
            boolean alive(T cell, long cnt, U alive);
        }
    }

    private record FixedGrid(
            int height, int width, Stream<Cell> initialAlive, Map<Cell, Set<Cell>> neighboursCache)
            implements GameOfLife.Universe<Cell, boolean[][]> {

        public static FixedGrid fromInput(final List<String> input) {
            final Stream<Cell> alive =
                    cells(input.size(), input.getFirst().length())
                            .filter(cell -> input.get(cell.row()).charAt(cell.col()) == SYMBOL);
            return new FixedGrid(input.size(), input.getFirst().length(), alive, new HashMap<>());
        }

        @Override
        public Stream<NeigbourCount<Cell>> getNeighbourCounts(final boolean[][] alive) {
            return cells(height, width)
                    .map(
                            cell ->
                                    new NeigbourCount<>(
                                            cell,
                                            this.neighbours(cell)
                                                    .filter(n -> alive[n.row()][n.col()])
                                                    .count()));
        }

        private Stream<Cell> neighbours(final Cell cell) {
            final Predicate<? super Cell> inBounds =
                    n -> 0 <= n.row() && n.row() < height && 0 <= n.col() && n.col() < width;
            return this.neighboursCache
                    .computeIfAbsent(
                            cell,
                            c -> DIAGONALS.stream().map(c::at).filter(inBounds).collect(toSet()))
                    .stream();
        }
    }

    private record SymmetricSquareGrid(int size, Map<Cell, Set<Cell>> neighboursCache)
            implements GameOfLife.Universe<Cell, boolean[][]> {

        public static SymmetricSquareGrid create(final int size) {
            return new SymmetricSquareGrid(size, new HashMap<>());
        }

        @Override
        public Stream<NeigbourCount<Cell>> getNeighbourCounts(final boolean[][] alive) {
            final Predicate<Cell> filter =
                    n -> {
                        if (n.row() < size && n.col() < size) {
                            return alive[n.row()][n.col()];
                        } else if (n.row() == size && n.col() == size) {
                            return alive[n.row() - 1][n.col() - 1];
                        } else if (n.row() == size) {
                            return alive[n.row() - 1][n.col()];
                        } else {
                            return alive[n.row()][n.col() - 1];
                        }
                    };
            return cells(size, size)
                    .map(
                            cell ->
                                    new NeigbourCount<>(
                                            cell, this.neighbours(cell).filter(filter).count()));
        }

        private Stream<Cell> neighbours(final Cell cell) {
            final Predicate<? super Cell> inBounds = n -> 0 <= n.row() && 0 <= n.col();
            return this.neighboursCache
                    .computeIfAbsent(
                            cell,
                            c -> DIAGONALS.stream().map(c::at).filter(inBounds).collect(toSet()))
                    .stream();
        }
    }

    private static final class Rules implements GameOfLife.Rules<Cell, boolean[][]> {

        @Override
        public boolean alive(final Cell cell, final long cnt, final boolean[][] alive) {
            return alive[cell.row()][cell.col()] == (cnt % 2 == 1);
        }
    }
}
