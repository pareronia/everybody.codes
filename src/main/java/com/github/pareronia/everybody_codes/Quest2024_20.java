package com.github.pareronia.everybody_codes;

import static java.util.stream.Collectors.toMap;

import com.github.pareronia.everybody_codes.geometry.Direction;
import com.github.pareronia.everybody_codes.geometry.Turn;
import com.github.pareronia.everybody_codes.grid.Cell;
import com.github.pareronia.everybody_codes.grid.CharGrid;
import com.github.pareronia.everybody_codes.grid.IntGrid;
import com.github.pareronia.everybody_codes.solution.SolutionBase;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Deque;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2024_20 extends SolutionBase<Long, Long, Long> {

    private static final List<Character> CHECKPOINTS = List.of('A', 'B', 'C');
    private static final char START = 'S';
    private static final char ROCK = '#';
    private static final char DEAD_AIR = '.';
    private static final char UPDRAFT = '+';
    private static final char DOWNDRAFT = '-';
    private static final int FLIGHT_TIME = 100;
    private static final long INITIAL_ALT = 1000L;

    private Quest2024_20(final boolean debug) {
        super(debug);
    }

    public static Quest2024_20 create() {
        return new Quest2024_20(false);
    }

    public static Quest2024_20 createDebug() {
        return new Quest2024_20(true);
    }

    @Override
    @SuppressWarnings({
        "PMD.ShortVariable",
        "PMD.AvoidInstantiatingObjectsInLoops",
        "PMD.LawOfDemeter"
    })
    public Long solvePart1(final List<String> input) {
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
            Set.of(Turn.RIGHT, Turn.LEFT).stream().map(state.dir::turn).forEach(dirs::add);
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

    @Override
    public Long solvePart2(final List<String> input) {
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

    @Override
    protected Long solvePart3(final List<String> input) {
        return 0L;
    }

    public static void main(final String[] args) {
        create().run();
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
            Set.of(Turn.RIGHT, Turn.LEFT).stream().map(state.dir::turn).forEach(dirs::add);
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
}
