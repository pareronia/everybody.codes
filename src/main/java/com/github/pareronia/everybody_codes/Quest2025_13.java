package com.github.pareronia.everybody_codes;

import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.AssertUtils;
import com.github.pareronia.everybody_codes.utils.StringUtils;
import com.github.pareronia.everybody_codes.utils.StringUtils.StringSplit;

import java.util.ArrayList;
import java.util.List;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_13 extends SolutionBase<Long, Long, Long> {

    private static final String TEST1 =
            """
            72
            58
            47
            61
            67
            """;
    private static final String TEST2 =
            """
            10-15
            12-13
            20-21
            19-23
            30-37
            """;

    private Quest2025_13(final boolean debug) {
        super(debug);
    }

    public static Quest2025_13 create() {
        return new Quest2025_13(false);
    }

    public static Quest2025_13 createDebug() {
        return new Quest2025_13(true);
    }

    private long solve(final List<String> input, final long positions) {
        record RangeInclusive(long start, long end) {

            public long size() {
                return Math.abs(this.start - this.end) + 1;
            }
        }

        final List<RangeInclusive> dial = new ArrayList<>(List.of(new RangeInclusive(1L, 1L)));
        boolean append = true;
        long before = 0;
        long after = 0;
        for (final String element : input) {
            final StringSplit<Long> split = StringUtils.splitOnceToLong(element, "-");
            if (append) {
                dial.add(new RangeInclusive(split.left(), split.right()));
                after += dial.getLast().size();
            } else {
                dial.add(0, new RangeInclusive(split.right(), split.left()));
                before += dial.getFirst().size();
            }
            append = !append;
        }
        final long target = (before + positions) % (before + 1 + after);
        long tot = 0L;
        for (final RangeInclusive rng : dial) {
            final long nxt = tot + rng.size();
            if (nxt > target) {
                return rng.start() + (rng.start() < rng.end() ? target - tot : -(target - tot));
            }
            tot = nxt;
        }
        throw AssertUtils.unreachable();
    }

    @Override
    public Long solvePart1(final List<String> input) {
        final List<String> ranges = input.stream().map(s -> "%s-%s".formatted(s, s)).toList();
        return this.solve(ranges, 2025);
    }

    @Override
    public Long solvePart2(final List<String> input) {
        return this.solve(input, 20_252_025L);
    }

    @Override
    public Long solvePart3(final List<String> input) {
        return this.solve(input, 202_520_252_025L);
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "67"),
        @Sample(method = "part2", input = TEST2, expected = "30"),
    })
    public static void main(final String[] args) {
        create().run();
    }
}
