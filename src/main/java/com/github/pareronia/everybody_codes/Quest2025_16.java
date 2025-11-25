package com.github.pareronia.everybody_codes;

import static com.github.pareronia.everybody_codes.utils.IntegerSequence.Range.range;

import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.BinarySearch;
import com.github.pareronia.everybody_codes.utils.StringUtils;

import java.util.ArrayList;
import java.util.List;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_16 extends SolutionBase<Long, Long, Long> {

    private static final String TEST1 = "1,2,3,5,9";
    private static final String TEST2 = "1,2,2,2,2,3,1,2,3,3,1,3,1,2,3,2,1,4,1,3,2,2,1,3,2,2";

    private Quest2025_16(final boolean debug) {
        super(debug);
    }

    public static Quest2025_16 create() {
        return new Quest2025_16(false);
    }

    public static Quest2025_16 createDebug() {
        return new Quest2025_16(true);
    }

    private long wallFromSpell(final List<Integer> spell, final long columns) {
        return spell.stream().mapToLong(i -> columns / i).sum();
    }

    private List<Integer> spellFromWall(final List<Integer> columns) {
        final List<Integer> cols = new ArrayList<>(columns);
        cols.add(0, 0);
        final List<Integer> ans = new ArrayList<>();
        for (int i = 1; i < cols.size(); i++) {
            if (cols.get(i) > 0) {
                ans.add(i);
                range(i, cols.size(), i).intStream().forEach(j -> cols.set(j, cols.get(j) - 1));
            }
        }
        return ans;
    }

    @Override
    public Long solvePart1(final List<String> input) {
        final List<Integer> spell = StringUtils.splitToInt(input.getFirst(), ",").boxed().toList();
        return this.wallFromSpell(spell, 90);
    }

    @Override
    public Long solvePart2(final List<String> input) {
        final List<Integer> columns =
                StringUtils.splitToInt(input.getFirst(), ",").boxed().toList();
        return this.spellFromWall(columns).stream()
                .mapToLong(Integer::longValue)
                .reduce(1L, (acc, b) -> acc * b);
    }

    @Override
    public Long solvePart3(final List<String> input) {
        final List<Integer> columns =
                StringUtils.splitToInt(input.getFirst(), ",").boxed().toList();
        final List<Integer> spell = this.spellFromWall(columns);
        return BinarySearch.search(v -> this.wallFromSpell(spell, v) <= 202_520_252_025_000L);
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "193"),
        @Sample(method = "part2", input = TEST2, expected = "270"),
        @Sample(method = "part3", input = TEST2, expected = "94439495762954"),
    })
    public static void main(final String[] args) {
        create().run();
    }
}
