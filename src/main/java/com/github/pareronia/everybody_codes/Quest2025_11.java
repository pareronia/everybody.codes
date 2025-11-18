package com.github.pareronia.everybody_codes;

import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.itertools.IterTools;
import com.github.pareronia.everybody_codes.utils.itertools.Pair;

import java.util.Arrays;
import java.util.List;
import java.util.stream.IntStream;
import java.util.stream.Stream;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_11 extends SolutionBase<Long, Long, Long> {

    private static final String TEST1 =
            """
            9
            1
            1
            4
            9
            6
            """;
    private static final String TEST2 =
            """
            805
            706
            179
            48
            158
            150
            232
            885
            598
            524
            423
            """;

    private Quest2025_11(final boolean debug) {
        super(debug);
    }

    public static Quest2025_11 create() {
        return new Quest2025_11(false);
    }

    public static Quest2025_11 createDebug() {
        return new Quest2025_11(true);
    }

    @Override
    public Long solvePart1(final List<String> input) {
        final long[] ducks = input.stream().mapToLong(Long::parseLong).toArray();
        int rounds = this.makeNonDecreasing(ducks);
        while (rounds < 10) {
            final long changed =
                    pairwise(ducks)
                            .filter(pair -> ducks[pair.first()] < ducks[pair.second()])
                            .map(
                                    pair -> {
                                        ducks[pair.first()]++;
                                        ducks[pair.second()]--;
                                        return pair;
                                    })
                            .count();
            if (changed == 0) {
                break;
            }
            rounds++;
        }
        return IntStream.range(0, ducks.length).mapToLong(i -> (i + 1) * ducks[i]).sum();
    }

    @Override
    public Long solvePart2(final List<String> input) {
        final long[] ducks = input.stream().mapToLong(Long::parseLong).toArray();
        final long rounds = this.makeNonDecreasing(ducks);
        final long avg = (long) Arrays.stream(ducks).average().orElseThrow();
        return rounds + Arrays.stream(ducks).map(d -> Math.abs(avg - d)).sum() / 2;
    }

    @Override
    public Long solvePart3(final List<String> input) {
        return this.solvePart2(input);
    }

    private Stream<Pair<Integer>> pairwise(final long... ducks) {
        return IterTools.pairwise(Stream.iterate(0, i -> i < ducks.length, i -> i + 1)).stream();
    }

    private int makeNonDecreasing(final long... ducks) {
        int rounds = 0;
        while (true) {
            final long changed =
                    pairwise(ducks)
                            .filter(pair -> ducks[pair.first()] > ducks[pair.second()])
                            .map(
                                    pair -> {
                                        ducks[pair.first()]--;
                                        ducks[pair.second()]++;
                                        return pair;
                                    })
                            .count();
            if (changed == 0) {
                break;
            }
            rounds++;
        }
        return rounds;
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "109"),
        @Sample(method = "part2", input = TEST1, expected = "11"),
        @Sample(method = "part2", input = TEST2, expected = "1579"),
    })
    public static void main(final String[] args) {
        create().run();
    }
}
