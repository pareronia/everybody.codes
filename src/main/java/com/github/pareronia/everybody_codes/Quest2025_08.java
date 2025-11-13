package com.github.pareronia.everybody_codes;

import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.IterTools;
import com.github.pareronia.everybody_codes.utils.IterTools.IterToolsIterator;
import com.github.pareronia.everybody_codes.utils.IterTools.Pair;
import com.github.pareronia.everybody_codes.utils.StringUtils;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.IntStream;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_08 extends SolutionBase<Long, Long, Long> {

    private static final String TEST1 = "1,5,2,6,8,4,1,7,3";
    private static final String TEST2 = "1,5,2,6,8,4,1,7,3,5,7,8,2";
    private static final String TEST3 = "1,5,2,6,8,4,1,7,3,6";

    private Quest2025_08(final boolean debug) {
        super(debug);
    }

    public static Quest2025_08 create() {
        return new Quest2025_08(false);
    }

    public static Quest2025_08 createDebug() {
        return new Quest2025_08(true);
    }

    private long solve1(final List<String> input, final int nails) {
        return IterTools.pairwise(StringUtils.splitToInt(input.getFirst(), ",").boxed()).stream()
                .filter(pair -> Math.abs(pair.first() - pair.second()) == nails / 2)
                .count();
    }

    @Override
    public Long solvePart1(final List<String> input) {
        return this.solve1(input, 32);
    }

    @Override
    public Long solvePart2(final List<String> input) {
        final Set<Thread> threads = new HashSet<>();
        long ans = 0;
        final IterToolsIterator<Pair<Integer>> pairs =
                IterTools.pairwise(StringUtils.splitToInt(input.getFirst(), ",").boxed());
        for (final Pair<Integer> pair : pairs.iterable()) {
            final Thread thread = Thread.of(pair);
            ans += threads.stream().filter(t -> t.crosses(thread)).count();
            threads.add(thread);
        }
        return ans;
    }

    private long solve3(final List<String> input, final int nails) {
        final List<Thread> threads =
                IterTools.pairwise(StringUtils.splitToInt(input.getFirst(), ",").boxed()).stream()
                        .map(Thread::of)
                        .toList();
        return IntStream.rangeClosed(1, nails)
                .boxed()
                .flatMap(
                        t1 ->
                                IntStream.rangeClosed(t1 + 1, nails)
                                        .mapToObj(t2 -> new Thread(t1, t2)))
                .mapToLong(t -> threads.stream().filter(t1 -> t1.crosses(t)).count())
                .max()
                .getAsLong();
    }

    @Override
    public Long solvePart3(final List<String> input) {
        return this.solve3(input, 256);
    }

    @Override
    protected void samples() {
        final Quest2025_08 test = createDebug();
        assert test.solve1(StringUtils.splitLines(TEST1), 8) == 4;
        assert test.solvePart2(StringUtils.splitLines(TEST2)) == 21;
        assert test.solve3(StringUtils.splitLines(TEST3), 8) == 7;
    }

    public static void main(final String[] args) {
        create().run();
    }

    private record Thread(int first, int second) {

        @SuppressWarnings("PMD.ShortMethodName")
        public static Thread of(final Pair<Integer> pair) {
            return new Thread(
                    Math.min(pair.first(), pair.second()), Math.max(pair.first(), pair.second()));
        }

        public boolean crosses(final Thread other) {
            return this.equals(other)
                    || (this.first < other.first
                            && other.first < this.second
                            && this.second < other.second)
                    || (other.first < this.first
                            && this.first < other.second
                            && other.second < this.second);
        }
    }
}
