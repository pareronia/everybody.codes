package com.github.pareronia.everybody_codes;

import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.StringUtils;

import java.util.List;
import java.util.Map;
import java.util.stream.IntStream;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2024_01 extends SolutionBase<Long, Long, Long> {

    private static final String TEST1 = "ABBAC";
    private static final String TEST2 = "AxBCDDCAxD";
    private static final String TEST3 = "xBxAAABCDxCC";

    private Quest2024_01(final boolean debug) {
        super(debug);
    }

    public static Quest2024_01 create() {
        return new Quest2024_01(false);
    }

    public static Quest2024_01 createDebug() {
        return new Quest2024_01(true);
    }

    private long solve(final List<String> inputs, final int groupSize) {
        class Potions {
            private static final Map<Character, Long> POTIONS_MAP =
                    Map.of('A', 0L, 'B', 1L, 'C', 3L, 'D', 5L);

            private static long getPotions(final String group) {
                return StringUtils.asCharacterStream(group)
                        .filter(ch -> ch != 'x')
                        .mapToLong(POTIONS_MAP::get)
                        .map(g -> g + group.length() - StringUtils.count(group, 'x') - 1)
                        .sum();
            }
        }
        return IntStream.iterate(0, i -> i < inputs.getFirst().length(), i -> i + groupSize)
                .mapToObj(i -> inputs.getFirst().substring(i, i + groupSize))
                .mapToLong(Potions::getPotions)
                .sum();
    }

    @Override
    public Long solvePart1(final List<String> inputs) {
        return this.solve(inputs, 1);
    }

    @Override
    public Long solvePart2(final List<String> inputs) {
        return this.solve(inputs, 2);
    }

    @Override
    public Long solvePart3(final List<String> inputs) {
        return this.solve(inputs, 3);
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "5"),
        @Sample(method = "part2", input = TEST2, expected = "28"),
        @Sample(method = "part3", input = TEST3, expected = "30")
    })
    public static void main(final String[] args) {
        create().run();
    }
}
