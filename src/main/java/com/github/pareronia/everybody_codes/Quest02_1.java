package com.github.pareronia.everybody_codes;

import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.StringUtils;
import com.github.pareronia.everybody_codes.utils.itertools.IterTools;

import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.function.Consumer;
import java.util.function.ToIntFunction;
import java.util.stream.IntStream;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest02_1 extends SolutionBase<Integer, Integer, String> {

    public static final String TEST1 =
            """
            *.*.*.*.*.*.*.*.*
            .*.*.*.*.*.*.*.*.
            *.*.*...*.*...*..
            .*.*.*.*.*...*.*.
            *.*.....*...*.*.*
            .*.*.*.*.*.*.*.*.
            *...*...*.*.*.*.*
            .*.*.*.*.*.*.*.*.
            *.*.*...*.*.*.*.*
            .*...*...*.*.*.*.
            *.*.*.*.*.*.*.*.*
            .*.*.*.*.*.*.*.*.

            RRRLRLRRRRRL
            LLLLRLRRRRRR
            RLLLLLRLRLRL
            LRLLLRRRLRLR
            LLRLLRLLLRRL
            LRLRLLLRRRRL
            LRLLLLLLRLLL
            RRLLLRLLRLRR
            RLLLLLRLLLRL
            """;
    public static final String TEST2 =
            """
            *.*.*.*.*.*.*.*.*.*.*.*.*
            .*.*.*.*.*.*.*.*.*.*.*.*.
            ..*.*.*.*...*.*...*.*.*..
            .*...*.*.*.*.*.*.....*.*.
            *.*...*.*.*.*.*.*...*.*.*
            .*.*.*.*.*.*.*.*.......*.
            *.*.*.*.*.*.*.*.*.*...*..
            .*.*.*.*.*.*.*.*.....*.*.
            *.*...*.*.*.*.*.*.*.*....
            .*.*.*.*.*.*.*.*.*.*.*.*.
            *.*.*.*.*.*.*.*.*.*.*.*.*
            .*.*.*.*.*.*.*.*.*...*.*.
            *.*.*.*.*.*.*.*.*...*.*.*
            .*.*.*.*.*.*.*.*.....*.*.
            *.*.*.*.*.*.*.*...*...*.*
            .*.*.*.*.*.*.*.*.*.*.*.*.
            *.*.*...*.*.*.*.*.*.*.*.*
            .*...*.*.*.*...*.*.*...*.
            *.*.*.*.*.*.*.*.*.*.*.*.*
            .*.*.*.*.*.*.*.*.*.*.*.*.

            RRRLLRRRLLRLRRLLLRLR
            RRRRRRRRRRLRRRRRLLRR
            LLLLLLLLRLRRLLRRLRLL
            RRRLLRRRLLRLLRLLLRRL
            RLRLLLRRLRRRLRRLRRRL
            LLLLLLLLRLLRRLLRLLLL
            LRLLRRLRLLLLLLLRLRRL
            LRLLRRLLLRRRRRLRRLRR
            LRLLRRLRLLRLRRLLLRLL
            RLLRRRRLRLRLRLRLLRRL
            """;
    public static final String TEST3 =
            """
            *.*.*.*.*.*.*.*.*
            .*.*.*.*.*.*.*.*.
            *.*.*...*.*...*..
            .*.*.*.*.*...*.*.
            *.*.....*...*.*.*
            .*.*.*.*.*.*.*.*.
            *...*...*.*.*.*.*
            .*.*.*.*.*.*.*.*.
            *.*.*...*.*.*.*.*
            .*...*...*.*.*.*.
            *.*.*.*.*.*.*.*.*
            .*.*.*.*.*.*.*.*.

            RRRLRLRRRRRL
            LLLLRLRRRRRR
            RLLLLLRLRLRL
            LRLLLRRRLRLR
            LLRLLRLLLRRL
            LRLRLLLRRRRL
            """;
    public static final String TEST4 =
            """
            *.*.*.*.*.*.*.*.*.*.*.*.*
            .*.*.*.*.*.*.*.*.*.*.*.*.
            ..*.*.*.*...*.*...*.*.*..
            .*...*.*.*.*.*.*.....*.*.
            *.*...*.*.*.*.*.*...*.*.*
            .*.*.*.*.*.*.*.*.......*.
            *.*.*.*.*.*.*.*.*.*...*..
            .*.*.*.*.*.*.*.*.....*.*.
            *.*...*.*.*.*.*.*.*.*....
            .*.*.*.*.*.*.*.*.*.*.*.*.
            *.*.*.*.*.*.*.*.*.*.*.*.*
            .*.*.*.*.*.*.*.*.*...*.*.
            *.*.*.*.*.*.*.*.*...*.*.*
            .*.*.*.*.*.*.*.*.....*.*.
            *.*.*.*.*.*.*.*...*...*.*
            .*.*.*.*.*.*.*.*.*.*.*.*.
            *.*.*...*.*.*.*.*.*.*.*.*
            .*...*.*.*.*...*.*.*...*.
            *.*.*.*.*.*.*.*.*.*.*.*.*
            .*.*.*.*.*.*.*.*.*.*.*.*.

            RRRLLRRRLLRLRRLLLRLR
            RRRRRRRRRRLRRRRRLLRR
            LLLLLLLLRLRRLLRRLRLL
            RRRLLRRRLLRLLRLLLRRL
            RLRLLLRRLRRRLRRLRRRL
            LLLLLLLLRLLRRLLRLLLL
            """;
    public static final String TEST5 =
            """
            *.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*
            .*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.
            ..*.*.*.*.*.*.........*.*.*.*.....*.*.*
            .*.*...*.*.*.*.*.*.*.*.*.*.*...*.*.*.*.
            *.*.*.*...*.*.*.*.*.....*.*.*.*...*.*..
            .*...*.*...*.*.*.*.*.*.*.....*.*.*.*.*.
            *.*.*.*.*.....*.*.*.*.*.*.*.*.*.*.*.*.*
            .*.*.*.*.*.*...*.*.*.*.....*.*.*.*...*.
            *.*...*.*.*.*.*.*.*.*...*.*.*...*.*.*.*
            .*...*.*.*.*.*.*.*.*...*.*.*.*.*.*.*.*.
            *.*.*.*.*.*...*.....*.*...*...*.*.*.*.*
            .*...*.*.*.*.*...*.*.*.*.*...*.*...*.*.
            *.*.*.*.*...*.*.*.*.*.*.*.*...*.*.*.*.*
            .*.*.*.*.*.*.*.*...*.*.*.*.*.*.*.*.*.*.
            ....*.*.*.*...*.*.*.*.*.*.*...*.*.*...*
            .*.*.*...*.*.*.*.*...*.*.*.*.*.*.*.*...
            *.*.*.*.*.*.*.....*...*...*.*.*.*.*.*.*
            .*.*...*.....*.*.*.*.*.*.*...*.*.*.*.*.
            *.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*
            .*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.

            RRRRLLRRLLLLLLLRLLRL
            RRRRRRRLRRLRRLRRRLRR
            RRRLLRRRRRLRRRRRLRRR
            LLLLRRLLRRLLLLLRRLLL
            LRRRRLRRLRLLRLLRRLRR
            RRRRRRRRLRRRRLLRRRLR
            """;

    private Quest02_1(final boolean debug) {
        super(debug);
    }

    public static Quest02_1 create() {
        return new Quest02_1(false);
    }

    public static Quest02_1 createDebug() {
        return new Quest02_1(true);
    }

    @Override
    public Integer solvePart1(final List<String> inputs) {
        final List<List<String>> blocks = StringUtils.toBlocks(inputs);
        final Machine machine = Machine.fromInput(blocks.getFirst());
        return IntStream.range(0, blocks.getLast().size())
                .map(i -> machine.toss(blocks.getLast().get(i), i + 1))
                .sum();
    }

    @Override
    public Integer solvePart2(final List<String> inputs) {
        final List<List<String>> blocks = StringUtils.toBlocks(inputs);
        final Machine machine = Machine.fromInput(blocks.getFirst());
        @SuppressWarnings("PMD.LongVariable")
        final ToIntFunction<String> bestScoreForSequence =
                tokens ->
                        IntStream.rangeClosed(1, machine.maxToss())
                                .map(i -> machine.toss(tokens, i))
                                .max()
                                .getAsInt();
        return blocks.getLast().stream().mapToInt(bestScoreForSequence).sum();
    }

    @Override
    public String solvePart3(final List<String> inputs) {
        final List<List<String>> blocks = StringUtils.toBlocks(inputs);
        final int sequences = blocks.getLast().size();
        final Machine machine = Machine.fromInput(blocks.getFirst());
        final int maxToss = machine.maxToss();
        final int[] memo = new int[sequences * maxToss];
        Arrays.fill(memo, -1);
        final int[] extremes = {Integer.MAX_VALUE, 0};
        final Consumer<int[]> consumer =
                p -> {
                    int coins = 0;
                    for (int i = 0; i < sequences; i++) {
                        final int idx = i * maxToss + p[i];
                        if (memo[idx] == -1) {
                            final String token = blocks.getLast().get(i);
                            memo[idx] = machine.toss(token, p[i] + 1);
                        }
                        coins += memo[idx];
                    }
                    extremes[0] = Math.min(extremes[0], coins);
                    extremes[1] = Math.max(extremes[1], coins);
                };
        IterTools.combinations(machine.maxToss(), sequences)
                .forEachRemaining(a -> IterTools.permutations(a, consumer));
        return "%d %d".formatted(extremes[0], extremes[1]);
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "26"),
        @Sample(method = "part2", input = TEST2, expected = "115"),
        @Sample(method = "part3", input = TEST3, expected = "13 43"),
        @Sample(method = "part3", input = TEST4, expected = "25 66"),
        @Sample(method = "part3", input = TEST5, expected = "39 122"),
    })
    public static void main(final String[] args) {
        create().run();
    }

    private record Machine(boolean[][] nails) {

        @SuppressWarnings("PMD.AvoidInstantiatingObjectsInLoops")
        public static Machine fromInput(final List<String> input) {
            final int height = input.size();
            final int width = input.get(0).length();
            final boolean[][] nails = new boolean[height][width];
            for (int r = 0; r < height; r++) {
                final boolean[] row = new boolean[width];
                for (int c = 0; c < width; c++) {
                    row[c] = input.get(r).charAt(c) == '*';
                }
                nails[r] = row;
            }
            return new Machine(nails);
        }

        public int toss(final String tokens, final int toss) {
            final Iterator<Character> token = StringUtils.asCharacterStream(tokens).iterator();
            int row = 0;
            int col = (toss - 1) * 2;
            while (row < this.nails.length) {
                if (this.nails[row][col]) {
                    col += token.next() == 'R' ? 1 : -1;
                    if (col == -1) {
                        col += 2;
                    } else if (col == this.nails[row].length) {
                        col -= 2;
                    }
                } else {
                    row++;
                }
            }
            return Math.max(0, (col / 2 + 1) * 2 - toss);
        }

        public int maxToss() {
            return nails[0].length / 2 + 1;
        }
    }
}
