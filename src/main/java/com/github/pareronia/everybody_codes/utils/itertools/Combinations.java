package com.github.pareronia.everybody_codes.utils.itertools;

import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.toSet;

import com.github.pareronia.everybody_codes.utils.AssertUtils;

import java.util.Arrays;
import java.util.Iterator;
import java.util.Set;
import java.util.stream.IntStream;

final class Combinations {

    private Combinations() {}

    @SuppressWarnings("PMD.ShortVariable")
    public static Iterator<int[]> combinations(final int n, final int k) {
        AssertUtils.assertTrue(n > 0 && k <= n);

        return new Iterator<>() {
            private final int[] its = IntStream.range(0, k).toArray();

            @Override
            public int[] next() {
                final int[] ans = new int[k];
                System.arraycopy(its, 0, ans, 0, k);
                its[k - 1]++;
                for (int j = 0; j < k; j++) {
                    for (int i = 1; i < k - j; i++) {
                        if (its[i] == n - k + 1 + i) {
                            its[i - 1]++;
                            for (int m = i; m < k; m++) {
                                its[m] = its[m - 1] + 1;
                            }
                        }
                    }
                }
                return ans;
            }

            @Override
            public boolean hasNext() {
                return its[k - 1] < n;
            }
        };
    }

    @SuppressWarnings("PMD.SystemPrintln")
    public static void main(final String[] args) {
        assertMatches(collect(4, 3), Set.of("{0, 1, 2}", "{0, 1, 3}", "{0, 2, 3}", "{1, 2, 3}"));
        assertMatches(collect(3, 2), Set.of("{0, 1}", "{0, 2}", "{1, 2}"));
        assertMatches(collect(3, 3), Set.of("{0, 1, 2}"));
        assert collect(20, 6).size() == 38_760;
        try {
            collect(3, 4);
        } catch (final IllegalArgumentException expected) {
        }
        try {
            collect(0, 3);
        } catch (final IllegalArgumentException expected) {
        }
        System.out.println("OK");
    }

    @SuppressWarnings("PMD.ShortVariable")
    private static Set<int[]> collect(final int n, final int k) {
        return IterTools.stream(combinations(n, k)).collect(toSet());
    }

    @SuppressWarnings("PMD.SystemPrintln")
    private static void assertMatches(final Set<int[]> combo, final Set<String> set) {
        final Set<String> print = print(combo);
        System.out.println(print);
        assert combo.size() == set.size();
        assert print.containsAll(set);
    }

    private static Set<String> print(final Set<int[]> combo) {
        return combo.stream()
                .map(c -> Arrays.stream(c).mapToObj(String::valueOf).collect(joining(", ")))
                .map(s -> "{" + s + "}")
                .collect(toSet());
    }
}
