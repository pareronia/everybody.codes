package com.github.pareronia.everybody_codes;

import static java.util.Comparator.comparing;
import static java.util.stream.Collectors.toSet;

import com.github.pareronia.everybody_codes.grid.Cell;
import com.github.pareronia.everybody_codes.grid.IntGrid;
import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.function.BiFunction;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_12 extends SolutionBase<Integer, Integer, Integer> {

    private static final String TEST1 =
            """
            989601
            857782
            746543
            766789
            """;
    private static final String TEST2 =
            """
            9589233445
            9679121695
            8469121876
            8352919876
            7342914327
            7234193437
            6789193538
            6781219648
            5691219769
            5443329859
            """;
    private static final String TEST3 =
            """
            5411
            3362
            5235
            3112
            """;
    private static final String TEST4 =
            """
            41951111131882511179
            32112222211518122215
            31223333322115122219
            31234444432147511128
            91223333322176121892
            61112222211166431583
            14661111166111111746
            11111119142122222177
            41222118881233333219
            71222127839122222196
            56111126279711111517
            """;

    private Quest2025_12(final boolean debug) {
        super(debug);
    }

    public static Quest2025_12 create() {
        return new Quest2025_12(false);
    }

    public static Quest2025_12 createDebug() {
        return new Quest2025_12(true);
    }

    @Override
    public Integer solvePart1(final List<String> input) {
        return this.ignite(Set.of(Cell.at(0, 0)), IntGrid.from(input), Set.of()).size();
    }

    @Override
    public Integer solvePart2(final List<String> input) {
        final IntGrid grid = IntGrid.from(input);
        final Set<Cell> starts =
                Set.of(Cell.at(0, 0), Cell.at(grid.getMaxRowIndex(), grid.getMaxColIndex()));
        return this.ignite(starts, grid, Set.of()).size();
    }

    @Override
    public Integer solvePart3(final List<String> input) {
        final BiFunction<IntGrid, Set<Cell>, Set<Cell>> findBest =
                (grid, exploded) -> {
                    final Set<Cell> seen = new HashSet<>(exploded);
                    return grid.getCells()
                            .sorted(comparing(grid::getValue).reversed())
                            .filter(barrel -> !seen.contains(barrel))
                            .map(
                                    barrel -> {
                                        final Set<Cell> newExploded =
                                                this.ignite(Set.of(barrel), grid, exploded).stream()
                                                        .filter(cell -> !exploded.contains(cell))
                                                        .collect(toSet());
                                        seen.addAll(newExploded);
                                        return newExploded;
                                    })
                            .max(comparing(Set::size))
                            .orElseThrow();
                };
        final IntGrid grid = IntGrid.from(input);
        final Set<Cell> seen = new HashSet<>();
        for (int i = 0; i < 3; i++) {
            seen.addAll(findBest.apply(grid, seen));
        }
        return seen.size();
    }

    private Set<Cell> ignite(final Set<Cell> starts, final IntGrid grid, final Set<Cell> exclude) {
        final Deque<Cell> queue = new ArrayDeque<>(starts);
        final Set<Cell> seen = new HashSet<>(exclude);
        seen.addAll(starts);
        while (!queue.isEmpty()) {
            final Cell cell = queue.pollFirst();
            cell.capitalNeighbours()
                    .filter(
                            n ->
                                    grid.isInBounds(n)
                                            && grid.getValue(cell) >= grid.getValue(n)
                                            && !seen.contains(n))
                    .forEach(
                            n -> {
                                seen.add(n);
                                queue.add(n);
                            });
        }
        return seen;
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "16"),
        @Sample(method = "part2", input = TEST2, expected = "58"),
        @Sample(method = "part3", input = TEST3, expected = "14"),
        @Sample(method = "part3", input = TEST4, expected = "136"),
    })
    public static void main(final String[] args) {
        createDebug().run();
    }
}
