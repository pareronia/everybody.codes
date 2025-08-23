package com.github.pareronia.everybody_codes;

import static java.util.stream.Collectors.toCollection;
import static java.util.stream.Collectors.toMap;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Deque;
import java.util.EnumMap;
import java.util.EnumSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Predicate;
import java.util.stream.Stream;
import java.util.stream.Stream.Builder;

@SuppressWarnings({"PMD.AtLeastOneConstructor", "PMD.ClassNamingConventions"})
public class Quest2024_20 {

    private static final List<Character> CHECKPOINTS = List.of('A', 'B', 'C');
    private static final char START = 'S';
    private static final char ROCK = '#';
    private static final char DEAD_AIR = '.';
    private static final char UPDRAFT = '+';
    private static final char DOWNDRAFT = '-';
    private static final int FLIGHT_TIME = 100;
    private static final int INITIAL_ALT = 1000;

    @SuppressWarnings("PMD.SystemPrintln")
    public static void main(final String[] args) throws IOException {
        final String memoDir = System.getenv("EVERYBODY_CODES_MEMO_DIR");
        final List<String> input1 = Files.readAllLines(Path.of(memoDir, "2024_20a_input.txt"));
        System.out.println("Part 1: %d".formatted(new Quest2024_20().part1(input1)));
        final List<String> input2 = Files.readAllLines(Path.of(memoDir, "2024_20b_input.txt"));
        System.out.println("Part 2: %d".formatted(new Quest2024_20().part2(input2)));
    }

    @SuppressWarnings({
        "PMD.ShortVariable",
        "PMD.AvoidInstantiatingObjectsInLoops",
        "PMD.LawOfDemeter"
    })
    public long part1(final List<String> input) {
        record State(Cell cell, Direction dir, int alt, int time) {}

        final CharGrid grid = new CharGrid(input);
        final Cell start = grid.getAllEqualTo(START).findFirst().orElseThrow();
        final Deque<State> q = new ArrayDeque<>();
        q.add(new State(start, Direction.DOWN, 0, 0));
        final Map<Direction, IntGrid> seen = new EnumMap<>(Direction.class);
        for (final Direction d : Direction.CAPITAL) {
            final IntGrid ig = new IntGrid(new int[grid.getHeight()][grid.getWidth()]);
            ig.getCells().forEach(cell -> ig.setValue(cell, Integer.MIN_VALUE));
            seen.put(d, ig);
        }
        int ans = 0;
        while (!q.isEmpty()) {
            final State state = q.pop();
            if (state.time == FLIGHT_TIME) {
                ans = Math.max(ans, state.alt);
                continue;
            }
            final List<Direction> dirs = new ArrayList<>();
            dirs.add(state.dir);
            Set.of(Turn.RIGHT, Turn.LEFT).stream()
                    .map(state.dir::turn)
                    .collect(toCollection(() -> dirs));
            for (final Direction d : dirs) {
                final Cell n = state.cell.at(d);
                if (!grid.isInBounds(n)) {
                    continue;
                }
                final Character v = grid.getValue(n);
                if (v == ROCK) {
                    continue;
                }
                final int alt =
                        switch (v) {
                            case UPDRAFT:
                                yield state.alt + 1;
                            case DOWNDRAFT:
                                yield state.alt - 2;
                            default:
                                yield state.alt - 1;
                        };
                if (seen.get(d).getValue(n) < alt) {
                    q.add(new State(n, d, alt, state.time + 1));
                    seen.get(d).setValue(n, alt);
                }
            }
        }
        return INITIAL_ALT + ans;
    }

    public long part2(final List<String> input) {
        final CharGrid grid = new CharGrid(input);
        final List<Character> cps = new ArrayList<>(CHECKPOINTS);
        cps.add(START);
        final Map<Character, Cell> checkpoints =
                grid.getCells()
                        .filter(c -> cps.contains(grid.getValue(c)))
                        .collect(toMap(grid::getValue, c -> c));
        long ans = 0;
        for (int i = 0; i < 4; i++) {
            grid.setValue(checkpoints.get(cps.get(0)), ROCK);
            grid.setValue(checkpoints.get(cps.get(1)), DEAD_AIR);
            grid.setValue(checkpoints.get(cps.get(2)), ROCK);
            grid.setValue(checkpoints.get(cps.get(3)), ROCK);
            ans += part(grid, checkpoints.get(cps.get(0)), checkpoints.get(cps.get(1)));
            Collections.rotate(cps, -1);
        }
        return ans;
    }

    @SuppressWarnings({
        "PMD.ShortVariable",
        "PMD.AvoidInstantiatingObjectsInLoops",
        "PMD.LawOfDemeter"
    })
    private long part(final CharGrid grid, final Cell start, final Cell end) {
        record State(Cell cell, Direction dir, int alt, int time) {}

        final Deque<State> q = new ArrayDeque<>();
        q.add(new State(start, Direction.DOWN, 0, 0));
        final Map<Direction, IntGrid> seen = new EnumMap<>(Direction.class);
        for (final Direction d : Direction.CAPITAL) {
            final IntGrid ig = new IntGrid(new int[grid.getHeight()][grid.getWidth()]);
            ig.getCells().forEach(cell -> ig.setValue(cell, Integer.MIN_VALUE));
            seen.put(d, ig);
        }
        while (!q.isEmpty()) {
            final State state = q.pop();
            if (state.cell.equals(end)) {
                if (state.alt >= 0) {
                    return state.time - 1;
                }
                continue;
            }
            final List<Direction> dirs = new ArrayList<>();
            dirs.add(state.dir);
            Set.of(Turn.RIGHT, Turn.LEFT).stream()
                    .map(state.dir::turn)
                    .collect(toCollection(() -> dirs));
            for (final Direction d : dirs) {
                final Cell n = state.cell.at(d);
                if (!grid.isInBounds(n)) {
                    continue;
                }
                final Character v = grid.getValue(n);
                if (v == ROCK) {
                    continue;
                }
                final int alt =
                        switch (v) {
                            case UPDRAFT:
                                yield state.alt + 1;
                            case DOWNDRAFT:
                                yield state.alt - 2;
                            default:
                                yield state.alt - 1;
                        };
                if (seen.get(d).getValue(n) < alt) {
                    q.add(new State(n, d, alt, state.time + 1));
                    seen.get(d).setValue(n, alt);
                }
            }
        }
        throw new IllegalStateException("Unsolvable");
    }

    @SuppressWarnings("PMD.ShortVariable")
    public enum Direction {
        UP(0, 1),
        RIGHT(1, 0),
        DOWN(0, -1),
        LEFT(-1, 0);

        public static final Set<Direction> CAPITAL = EnumSet.of(UP, RIGHT, DOWN, LEFT);

        private final int x;
        private final int y;

        Direction(final int x, final int y) {
            this.x = x;
            this.y = y;
        }

        public int getX() {
            return x;
        }

        public int getY() {
            return y;
        }

        public Direction turn(final Turn turn) {
            return switch (this) {
                case UP -> turn == Turn.LEFT ? LEFT : RIGHT;
                case RIGHT -> turn == Turn.LEFT ? UP : DOWN;
                case DOWN -> turn == Turn.LEFT ? RIGHT : LEFT;
                case LEFT -> turn == Turn.LEFT ? DOWN : UP;
            };
        }
    }

    public enum Turn {
        LEFT,
        RIGHT;
    }

    public record Cell(int row, int col) {

        @SuppressWarnings("PMD.ShortMethodName")
        public Cell at(final Direction direction) {
            return new Cell(this.row - direction.getY(), this.col + direction.getX());
        }
    }

    @SuppressWarnings("PMD.ShortClassName")
    private interface Grid<T> {
        int getHeight();

        int getWidth();

        T getValue(Cell cell);

        void setValue(Cell cell, T value);

        default boolean isInBounds(final Cell cell) {
            return 0 <= cell.row
                    && cell.row < this.getHeight()
                    && 0 <= cell.col
                    && cell.col < this.getWidth();
        }

        @SuppressWarnings("PMD.AvoidInstantiatingObjectsInLoops")
        default Stream<Cell> getCells() {
            final Builder<Cell> builder = Stream.builder();
            for (int r = 0; r < this.getHeight(); r++) {
                for (int c = 0; c < this.getWidth(); c++) {
                    builder.add(new Cell(r, c));
                }
            }
            return builder.build();
        }

        default Stream<Cell> findAllMatching(final Predicate<T> test) {
            return this.getCells().filter(cell -> test.test(this.getValue(cell)));
        }

        default Stream<Cell> getAllEqualTo(final T value) {
            return this.findAllMatching(c -> c.equals(value));
        }
    }

    private static class CharGrid implements Grid<Character> {

        private final char[][] cells;

        public CharGrid(final List<String> strings) {
            final char[][] cells = new char[strings.size()][strings.get(0).length()];
            for (int i = 0; i < strings.size(); i++) {
                cells[i] = strings.get(i).toCharArray();
            }
            this.cells = cells;
        }

        @Override
        public int getHeight() {
            return this.cells.length;
        }

        @Override
        public int getWidth() {
            return this.cells[0].length;
        }

        @Override
        public Character getValue(final Cell cell) {
            return this.cells[cell.row()][cell.col()];
        }

        @Override
        public void setValue(final Cell cell, final Character value) {
            this.cells[cell.row()][cell.col()] = value;
        }
    }

    private static class IntGrid implements Grid<Integer> {
        private final int[][] values;

        @SuppressWarnings("PMD.UseVarargs")
        public IntGrid(final int[][] values) {
            this.values = Arrays.stream(values).map(int[]::clone).toArray(int[][]::new);
        }

        @Override
        public int getWidth() {
            assert this.values.length > 0;
            return this.values[0].length;
        }

        @Override
        public int getHeight() {
            return this.values.length;
        }

        @Override
        public Integer getValue(final Cell cell) {
            return this.values[cell.row()][cell.col()];
        }

        @Override
        public void setValue(final Cell cell, final Integer value) {
            this.values[cell.row()][cell.col()] = value;
        }
    }
}
