package com.github.pareronia.everybody_codes;

import static java.util.stream.Collectors.toSet;

import com.github.pareronia.everybody_codes.grid.Cell;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.StringUtils;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.IntStream;
import java.util.stream.Stream;
import java.util.stream.Stream.Builder;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_10 extends SolutionBase<Long, Integer, Long> {

    private static final String TEST1 =
            """
            ...SSS.......
            .S......S.SS.
            ..S....S...S.
            ..........SS.
            ..SSSS...S...
            .....SS..S..S
            SS....D.S....
            S.S..S..S....
            ....S.......S
            .SSS..SS.....
            .........S...
            .......S....S
            SS.....S..S..
            """;
    private static final String TEST2 =
            """
            ...SSS##.....
            .S#.##..S#SS.
            ..S.##.S#..S.
            .#..#S##..SS.
            ..SSSS.#.S.#.
            .##..SS.#S.#S
            SS##.#D.S.#..
            S.S..S..S###.
            .##.S#.#....S
            .SSS.#SS..##.
            ..#.##...S##.
            .#...#.S#...S
            SS...#.S.#S..
            """;
    private static final String TEST3 =
            """
            SSS
            ..#
            #.#
            #D.
            """;
    private static final String TEST4 =
            """
            SSS
            ..#
            ..#
            .##
            .D#
            """;
    private static final String TEST5 =
            """
            ..S..
            .....
            ..#..
            .....
            ..D..
            """;
    private static final String TEST6 =
            """
            .SS.S
            #...#
            ...#.
            ##..#
            .####
            ##D.#
            """;
    private static final String TEST7 =
            """
            SSS.S
            .....
            #.#.#
            .#.#.
            #.D.#
            """;

    private Quest2025_10(final boolean debug) {
        super(debug);
    }

    public static Quest2025_10 create() {
        return new Quest2025_10(false);
    }

    public static Quest2025_10 createDebug() {
        return new Quest2025_10(true);
    }

    private long solve1(final List<String> input, final int cnt) {
        final Board board = Board.fromInput(input);
        final Set<Cell> moves = new HashSet<>(Set.of(board.dragon()));
        for (int i = 0; i < cnt; i++) {
            moves.addAll(moves.stream().flatMap(board::knightMoves).collect(toSet()));
        }
        return moves.stream().filter(board.sheep()::contains).count();
    }

    @Override
    public Long solvePart1(final List<String> input) {
        return this.solve1(input, 4);
    }

    private int solve2(final List<String> input, final int cnt) {
        final Board board = Board.fromInput(input);
        Set<Cell> moves = new HashSet<>(Set.of(board.dragon()));
        Set<Cell> sheep = new HashSet<>(board.sheep());
        int ans = 0;
        for (int i = 0; i < cnt; i++) {
            final Set<Cell> newMoves = moves.stream().flatMap(board::knightMoves).collect(toSet());
            for (final Integer d : List.of(0, 1)) {
                sheep =
                        sheep.stream()
                                .filter(s -> s.row() < board.h - 1)
                                .map(s -> Cell.at(s.row() + d, s.col()))
                                .collect(toSet());
                final Set<Cell> eaten =
                        sheep.stream()
                                .filter(s -> newMoves.contains(s) && !board.hides().contains(s))
                                .collect(toSet());
                ans += eaten.size();
                sheep.removeAll(eaten);
            }
            moves = newMoves;
        }
        return ans;
    }

    @Override
    public Integer solvePart2(final List<String> input) {
        return this.solve2(input, 20);
    }

    @Override
    public Long solvePart3(final List<String> input) {
        return new DFS(Board.fromInput(input)).execute();
    }

    @Override
    protected void samples() {
        final Quest2025_10 test = createDebug();
        assert test.solve1(StringUtils.splitLines(TEST1), 3) == 27;
        assert test.solve2(StringUtils.splitLines(TEST2), 3) == 27;
        assert test.solvePart3(StringUtils.splitLines(TEST3)) == 15;
        assert test.solvePart3(StringUtils.splitLines(TEST4)) == 8;
        assert test.solvePart3(StringUtils.splitLines(TEST5)) == 44;
        assert test.solvePart3(StringUtils.splitLines(TEST6)) == 4406;
        assert test.solvePart3(StringUtils.splitLines(TEST7)) == 13_033_988_838L;
    }

    public static void main(final String[] args) {
        create().run();
    }

    @SuppressWarnings("PMD.ShortClassName")
    private static class DFS {
        private final Board board;
        private final Map<Integer, Long> cache;

        private enum Turn {
            DRAGON,
            SHEEP
        }

        private record State(Set<Cell> sheep, Cell dragon) {}

        public DFS(final Board board) {
            this.board = board;
            this.cache = new HashMap<>();
        }

        private Stream<State> dragonMoves(final State state) {
            return this.board
                    .knightMoves(state.dragon())
                    .map(
                            m -> {
                                if (this.board.hides().contains(m)) {
                                    return new State(state.sheep(), m);
                                } else {
                                    final Set<Cell> newSheep =
                                            state.sheep().stream()
                                                    .filter(s -> !s.equals(m))
                                                    .collect(toSet());
                                    return new State(newSheep, m);
                                }
                            });
        }

        @SuppressWarnings("PMD.AvoidInstantiatingObjectsInLoops")
        private Stream<State> sheepMoves(final State state) {
            boolean validMoves = false;
            final Builder<State> builder = Stream.<State>builder();
            for (final Cell sheep : state.sheep()) {
                final Cell newSh = Cell.at(sheep.row() + 1, sheep.col());
                if (newSh.row() == this.board.h() || this.board.exits().contains(newSh)) {
                    validMoves = true;
                } else if (!newSh.equals(state.dragon()) || this.board.hides().contains(newSh)) {
                    validMoves = true;
                    final Set<Cell> newSheep =
                            state.sheep().stream()
                                    .map(s -> s.equals(sheep) ? newSh : s)
                                    .collect(toSet());
                    builder.add(new State(newSheep, state.dragon()));
                }
            }
            if (!validMoves) {
                builder.add(state);
            }
            return builder.build();
        }

        private long dfs(final State state, final Turn turn) {
            int shk = 0;
            for (final Cell sheep : state.sheep()) {
                shk |= (this.board.h() + 1 - sheep.row()) << (sheep.col() * 3);
            }
            final int drk = state.dragon().row() * this.board.w() + state.dragon().col();
            final int key = shk << 7 | drk << 1 | (turn == Turn.SHEEP ? 0 : 1);
            if (this.cache.containsKey(key)) {
                return this.cache.get(key);
            }
            final long ans;
            if (state.sheep().isEmpty()) {
                ans = 1L;
            } else {
                ans =
                        switch (turn) {
                            case Turn.SHEEP ->
                                    this.sheepMoves(state)
                                            .mapToLong(s -> dfs(s, Turn.DRAGON))
                                            .sum();

                            case Turn.DRAGON ->
                                    this.dragonMoves(state)
                                            .mapToLong(s -> dfs(s, Turn.SHEEP))
                                            .sum();
                        };
            }
            this.cache.put(key, ans);
            return ans;
        }

        public long execute() {
            return this.dfs(new State(this.board.sheep(), this.board.dragon()), Turn.SHEEP);
        }
    }

    @SuppressWarnings("PMD.ShortVariable")
    private record Board(
            int h, int w, Cell dragon, Set<Cell> sheep, Set<Cell> hides, Set<Cell> exits) {

        private static final Set<Move> KNIGHT_MOVES =
                Set.of(
                        new Move(-2, -1),
                        new Move(-2, 1),
                        new Move(-1, -2),
                        new Move(-1, 2),
                        new Move(1, -2),
                        new Move(1, 2),
                        new Move(2, -1),
                        new Move(2, 1));

        private record Move(int dRow, int dCol) {}

        @SuppressWarnings("PMD.AssignmentInOperand")
        public static Board fromInput(final List<String> input) {
            final int h = input.size();
            final int w = input.getFirst().length();
            Cell dragon = null;
            final Set<Cell> sheep = new HashSet<>();
            final Set<Cell> hides = new HashSet<>();
            for (int r = 0; r < h; r++) {
                for (int c = 0; c < w; c++) {
                    switch (input.get(r).charAt(c)) {
                        case 'D' -> dragon = Cell.at(r, c);
                        case 'S' -> sheep.add(Cell.at(r, c));
                        case '#' -> hides.add(Cell.at(r, c));
                        default -> {}
                    }
                }
            }
            final Set<Cell> exits = new HashSet<>();
            for (int c = 0; c < w; c++) {
                final int col = c;
                for (int r = 0; r < h; r++) {
                    if (IntStream.range(r, h).allMatch(row -> hides.contains(Cell.at(row, col)))) {
                        exits.add(Cell.at(r, c));
                        break;
                    }
                }
            }
            return new Board(h, w, dragon, sheep, hides, exits);
        }

        public Stream<Cell> knightMoves(final Cell start) {
            return KNIGHT_MOVES.stream()
                    .map(move -> Cell.at(start.row() + move.dRow(), start.col() + move.dCol()))
                    .filter(c -> 0 <= c.row() && c.row() < h && 0 <= c.col() && c.col() < w);
        }
    }
}
