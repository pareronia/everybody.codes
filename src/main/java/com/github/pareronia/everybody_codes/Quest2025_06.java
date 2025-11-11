package com.github.pareronia.everybody_codes;

import static java.util.stream.Collectors.joining;

import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.Counter;

import java.util.List;
import java.util.stream.IntStream;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_06 extends SolutionBase<Long, Long, Long> {

    private static final String TEST = "ABabACacBCbca";

    private Quest2025_06(final boolean debug) {
        super(debug);
    }

    public static Quest2025_06 create() {
        return new Quest2025_06(false);
    }

    public static Quest2025_06 createDebug() {
        return new Quest2025_06(true);
    }

    @SuppressWarnings("PMD.ShortVariable")
    private Counter<Character> count(final List<String> input) {
        final Counter<Character> ans = new Counter<>();
        final Counter<Character> cnt = new Counter<>();
        for (int i = 0; i < input.getFirst().length(); i++) {
            final char ch = input.getFirst().charAt(i);
            if (Character.isUpperCase(ch)) {
                cnt.update(Character.toLowerCase(ch));
            } else {
                ans.add(ch, cnt.get(ch));
            }
        }
        return ans;
    }

    @Override
    public Long solvePart1(final List<String> input) {
        return this.count(input).get('a');
    }

    @Override
    public Long solvePart2(final List<String> input) {
        return this.count(input).total();
    }

    @Override
    @SuppressWarnings({"unchecked", "PMD.ShortVariable"})
    public Long solvePart3(final List<String> input) {
        final int limit = 1000;
        final String s = input.getFirst();
        final int size = s.length();
        final String s3 = IntStream.range(0, 3).mapToObj(i -> s).collect(joining());
        final Counter<?>[] cnts = {new Counter<>(), new Counter<>(), new Counter<>()};
        for (int i = 0; i < size; i++) {
            final char ch = s.charAt(i);
            if (Character.isUpperCase(ch)) {
                continue;
            }
            final int lo = size + i - limit;
            final int hi = size + i + limit;
            final char mentor = Character.toUpperCase(ch);
            final int[] starts = {Math.max(lo, size), lo, lo};
            final int[] ends = {hi, hi, Math.min(hi, 2 * size - 1)};
            for (int j = 0; j < 3; j++) {
                long cnt = 0;
                for (int k = starts[j]; k <= ends[j]; k++) {
                    if (s3.charAt(k) == mentor) {
                        cnt++;
                    }
                }
                ((Counter<Character>) cnts[j]).add(ch, cnt);
            }
        }
        return cnts[0].total() + 998 * cnts[1].total() + cnts[2].total();
    }

    @Samples({
        @Sample(method = "part1", input = TEST, expected = "5"),
        @Sample(method = "part2", input = TEST, expected = "11"),
    })
    public static void main(final String[] args) {
        create().run();
    }
}
