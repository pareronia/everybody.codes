package com.github.pareronia.everybody_codes;

import static java.util.stream.Collectors.joining;

import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.StringUtils;

import java.util.Arrays;
import java.util.List;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_04 extends SolutionBase<Long, Long, Long> {

    private static final String TEST1 =
            """
            128
            64
            32
            16
            8
            """;
    private static final String TEST2 =
            """
            102
            75
            50
            35
            13
            """;
    private static final String TEST3 =
            """
            5
            5|10
            10|20
            5
            """;
    private static final String TEST4 =
            """
            5
            7|21
            18|36
            27|27
            10|50
            10|50
            11
            """;

    private Quest2025_04(final boolean debug) {
        super(debug);
    }

    public static Quest2025_04 create() {
        return new Quest2025_04(false);
    }

    public static Quest2025_04 createDebug() {
        return new Quest2025_04(true);
    }

    @Override
    public Long solvePart1(final List<String> input) {
        return 2025 * Long.parseLong(input.getFirst()) / Long.parseLong(input.getLast());
    }

    @Override
    public Long solvePart2(final List<String> input) {
        return Math.ceilDiv(
                10_000_000_000_000L * Long.parseLong(input.getLast()),
                Long.parseLong(input.getFirst()));
    }

    @Override
    public Long solvePart3(final List<String> input) {
        return (long)
                Arrays.stream(input.stream().collect(joining(" ")).split("\\|"))
                        .map(s -> StringUtils.splitOnceToDouble(s, " "))
                        .mapToDouble(split -> split.left() / split.right())
                        .reduce(100d, (acc, val) -> acc * val);
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "32400"),
        @Sample(method = "part1", input = TEST2, expected = "15888"),
        @Sample(method = "part2", input = TEST1, expected = "625000000000"),
        @Sample(method = "part2", input = TEST2, expected = "1274509803922"),
        @Sample(method = "part3", input = TEST3, expected = "400"),
        @Sample(method = "part3", input = TEST4, expected = "6818"),
    })
    public static void main(final String[] args) {
        create().run();
    }
}
