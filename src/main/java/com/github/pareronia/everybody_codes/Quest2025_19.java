package com.github.pareronia.everybody_codes;

import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.mapping;
import static java.util.stream.Collectors.toUnmodifiableSet;

import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;

import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_19 extends SolutionBase<Integer, Integer, Integer> {

    private static final String TEST1 =
            """
            7,7,2
            12,0,4
            15,5,3
            24,1,6
            28,5,5
            40,8,2
            """;
    private static final String TEST2 =
            """
            7,7,2
            7,1,3
            12,0,4
            15,5,3
            24,1,6
            28,5,5
            40,3,3
            40,8,2
            """;

    private Quest2025_19(final boolean debug) {
        super(debug);
    }

    public static Quest2025_19 create() {
        return new Quest2025_19(false);
    }

    public static Quest2025_19 createDebug() {
        return new Quest2025_19(true);
    }

    @Override
    public Integer solvePart1(final List<String> input) {
        return Chamber.fromInput(input).wingflaps();
    }

    @Override
    public Integer solvePart2(final List<String> input) {
        return Chamber.fromInput(input).wingflaps();
    }

    @Override
    public Integer solvePart3(final List<String> input) {
        return Chamber.fromInput(input).wingflaps();
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "24"),
        @Sample(method = "part2", input = TEST2, expected = "22"),
    })
    public static void main(final String[] args) {
        create().run();
    }

    @SuppressWarnings({"PMD.ShortVariable", "PMD.AvoidInstantiatingObjectsInLoops"})
    private record Chamber(Map<Integer, Set<Opening>> openings) {

        private record Opening(int y1, int y2) {

            public static Opening fromInput(final String input) {
                final String[] splits = input.split(",");
                final int y = Integer.parseInt(splits[1]);
                final int dy = Integer.parseInt(splits[2]);
                return new Opening(y, y + dy - 1);
            }
        }

        public static Chamber fromInput(final List<String> input) {
            final Map<Integer, Set<Opening>> openings =
                    input.stream()
                            .collect(
                                    groupingBy(
                                            line -> Integer.valueOf(line.split(",")[0]),
                                            mapping(Opening::fromInput, toUnmodifiableSet())));
            return new Chamber(Collections.unmodifiableMap(openings));
        }

        public int wingflaps() {
            int prevX = 0;
            Set<Integer> prevReachable = new HashSet<>(Set.of(0));
            final List<Integer> xs = this.openings().keySet().stream().sorted().toList();
            for (final int x : xs) {
                final Set<Integer> reachable = new HashSet<>();
                for (final Opening opening : this.openings.get(x)) {
                    for (int y = opening.y1; y <= opening.y2; y++) {
                        if (((x + y) & 1) != 0) {
                            continue;
                        }
                        for (final int prevY : prevReachable) {
                            if (Math.abs(y - prevY) <= x - prevX) {
                                reachable.add(y);
                                break;
                            }
                        }
                    }
                }
                prevX = x;
                prevReachable = reachable;
            }
            final int ansX = prevX;
            final int ansY = prevReachable.stream().mapToInt(Integer::valueOf).min().getAsInt();
            return ansY + (ansX - ansY) / 2;
        }
    }
}
