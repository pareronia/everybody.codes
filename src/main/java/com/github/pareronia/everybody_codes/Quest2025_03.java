package com.github.pareronia.everybody_codes;

import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.Counter;
import com.github.pareronia.everybody_codes.utils.StringUtils;

import java.util.List;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_03 extends SolutionBase<Integer, Integer, Integer> {

    private static final String TEST1 = "10,5,1,10,3,8,5,2,2";
    private static final String TEST2 =
            "4,51,13,64,57,51,82,57,16,88,89,48,32,49,49,2,84,65,49,43,9,13,2,3,75,72,63,48,61,14,40,77";

    private Quest2025_03(final boolean debug) {
        super(debug);
    }

    public static Quest2025_03 create() {
        return new Quest2025_03(false);
    }

    public static Quest2025_03 createDebug() {
        return new Quest2025_03(true);
    }

    @Override
    public Integer solvePart1(final List<String> input) {
        return StringUtils.splitToInt(input.getFirst(), ",").distinct().sum();
    }

    @Override
    public Integer solvePart2(final List<String> input) {
        return StringUtils.splitToInt(input.getFirst(), ",").distinct().sorted().limit(20).sum();
    }

    @Override
    public Integer solvePart3(final List<String> input) {
        return (int)
                new Counter<>(StringUtils.splitToInt(input.getFirst(), ",").boxed())
                        .mostCommon()
                        .getFirst()
                        .count();
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "29"),
        @Sample(method = "part2", input = TEST2, expected = "781"),
        @Sample(method = "part3", input = TEST2, expected = "3"),
    })
    public static void main(final String[] args) {
        create().run();
    }
}
