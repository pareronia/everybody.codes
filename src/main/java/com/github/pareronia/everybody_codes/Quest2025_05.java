package com.github.pareronia.everybody_codes;

import static java.util.Comparator.comparing;
import static java.util.stream.Collectors.joining;

import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.StringUtils;
import com.github.pareronia.everybody_codes.utils.StringUtils.StringSplit;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.IntStream;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_05 extends SolutionBase<Long, Long, Long> {

    private static final String TEST1 = "58:5,3,7,8,9,10,4,5,7,8,8";
    private static final String TEST2 =
            """
            1:2,4,1,1,8,2,7,9,8,6
            2:7,9,9,3,8,3,8,8,6,8
            3:4,7,6,9,1,8,3,7,2,2
            4:6,4,2,1,7,4,5,5,5,8
            5:2,9,3,8,3,9,5,2,1,4
            6:2,4,9,6,7,4,1,7,6,8
            7:2,3,7,6,2,2,4,1,4,2
            8:5,1,5,6,8,3,1,8,3,9
            9:5,7,7,3,7,2,3,8,6,7
            10:4,1,9,3,8,5,4,3,5,5
            """;
    private static final String TEST3 =
            """
            1:7,1,9,1,6,9,8,3,7,2
            2:6,1,9,2,9,8,8,4,3,1
            3:7,1,9,1,6,9,8,3,8,3
            4:6,1,9,2,8,8,8,4,3,1
            5:7,1,9,1,6,9,8,3,7,3
            6:6,1,9,2,8,8,8,4,3,5
            7:3,7,2,2,7,4,4,6,3,1
            8:3,7,2,2,7,4,4,6,3,7
            9:3,7,2,2,7,4,1,6,3,7
            """;
    private static final String TEST4 =
            """
            1:7,1,9,1,6,9,8,3,7,2
            2:7,1,9,1,6,9,8,3,7,2
            """;

    private Quest2025_05(final boolean debug) {
        super(debug);
    }

    public static Quest2025_05 create() {
        return new Quest2025_05(false);
    }

    public static Quest2025_05 createDebug() {
        return new Quest2025_05(true);
    }

    @Override
    public Long solvePart1(final List<String> input) {
        return Sword.fromInput(input.get(0)).quality();
    }

    @Override
    public Long solvePart2(final List<String> input) {
        final List<Sword> swords = new ArrayList<>();
        input.stream().map(Sword::fromInput).forEach(swords::add);
        swords.sort(comparing(Sword::quality));
        return swords.getLast().quality() - swords.getFirst().quality();
    }

    @Override
    public Long solvePart3(final List<String> input) {
        final List<Sword> swords = new ArrayList<>();
        input.stream().map(Sword::fromInput).forEach(swords::add);
        swords.sort(
                comparing(Sword::quality)
                        .thenComparing(Sword::levels)
                        .thenComparing(Sword::sid)
                        .reversed());
        return IntStream.range(0, swords.size()).mapToLong(i -> (i + 1) * swords.get(i).sid).sum();
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "581078"),
        @Sample(method = "part2", input = TEST2, expected = "77053"),
        @Sample(method = "part3", input = TEST3, expected = "260"),
        @Sample(method = "part3", input = TEST4, expected = "4")
    })
    public static void main(final String[] args) {
        create().run();
    }

    private record Sword(int sid, long quality, Levels levels) {

        public static Sword fromInput(final String string) {
            final StringSplit<String> split = StringUtils.splitOnce(string, ":");
            final int[] nums = StringUtils.splitToInt(split.right(), ",").toArray();
            final List<Integer> spine = spine(nums);
            @SuppressWarnings({"PMD.AssignmentInOperand", "PMD.UnusedAssignment"})
            final String quality =
                    IntStream.iterate(1, i -> i < spine.size(), i -> i += 3)
                            .mapToObj(i -> String.valueOf(spine.get(i)))
                            .collect(joining());
            return new Sword(
                    Integer.parseInt(split.left()),
                    Long.parseLong(quality),
                    Levels.fromSpine(spine));
        }

        private static List<Integer> spine(final int... nums) {
            final List<Integer> spine = new ArrayList<>(Arrays.asList(null, nums[0], null));
            for (int i = 1; i < nums.length; i++) {
                final int num = nums[i];
                boolean set = false;
                for (int r = 1; r < spine.size(); r += 3) {
                    final Integer mid = spine.get(r);
                    assert mid != null;
                    if (num < mid && spine.get(r - 1) == null) {
                        spine.set(r - 1, num);
                        set = true;
                        break;
                    }
                    if (num > mid && spine.get(r + 1) == null) {
                        spine.set(r + 1, num);
                        set = true;
                        break;
                    }
                }
                if (!set) {
                    spine.addAll(Arrays.asList(null, num, null));
                }
            }
            return spine;
        }

        private record Levels(List<Integer> levels) implements Comparable<Levels> {

            public static Levels fromSpine(final List<Integer> spine) {
                final List<Integer> levels = new ArrayList<>();
                for (int i = 0; i < spine.size(); i += 3) {
                    final int row = i;
                    final String lvl =
                            IntStream.range(0, 3)
                                    .mapToObj(j -> spine.get(row + j))
                                    .filter(s -> s != null)
                                    .map(String::valueOf)
                                    .collect(joining(""));
                    levels.add(Integer.parseInt(lvl));
                }
                return new Levels(levels);
            }

            @Override
            @SuppressWarnings("PMD.OverrideBothEqualsAndHashCodeOnComparable")
            public int compareTo(final Levels other) {
                assert this.levels.size() == other.levels.size();
                for (int i = 0; i < this.levels.size(); i++) {
                    final int ans = Integer.compare(this.levels.get(i), other.levels.get(i));
                    if (ans != 0) {
                        return ans;
                    }
                }
                return 0;
            }
        }
    }
}
