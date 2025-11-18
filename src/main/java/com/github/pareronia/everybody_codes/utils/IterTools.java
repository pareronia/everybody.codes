package com.github.pareronia.everybody_codes.utils;

import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.toSet;

import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.function.Consumer;
import java.util.stream.IntStream;
import java.util.stream.Stream;

@SuppressWarnings("PMD.CouplingBetweenObjects")
public final class IterTools {

    private IterTools() {}

    public static <T> Stream<T> stream(final Iterator<T> iterator) {
        return Stream.generate(() -> null)
                .takeWhile(x -> iterator.hasNext())
                .map(n -> iterator.next());
    }

    public static void permutations(final int[] nums, final Consumer<int[]> consumer) {
        Heap.accept(nums, consumer);
    }

    public static <T, U> IterToolsIterator<ProductPair<T, U>> product(
            final Iterator<T> first, final Iterator<U> second) {
        final List<U> lstU = stream(second).toList();
        final Iterator<ProductPair<T, U>> ans =
                stream(first)
                        .flatMap(a -> lstU.stream().map(b -> new ProductPair<>(a, b)))
                        .iterator();
        return new IterToolsIterator<>() {
            @Override
            public boolean hasNext() {
                return ans.hasNext();
            }

            @Override
            public ProductPair<T, U> next() {
                return ans.next();
            }
        };
    }

    public static <T> IterToolsIterator<Pair<T>> pairwise(final Stream<T> stream) {
        return pairwise(stream.iterator());
    }

    public static <T> IterToolsIterator<Pair<T>> pairwise(final Iterator<T> iterator) {
        return new IterToolsIterator<>() {
            private T first = iterator.next();

            @Override
            public boolean hasNext() {
                return iterator.hasNext();
            }

            @Override
            public Pair<T> next() {
                final T second = iterator.next();
                final Pair<T> pair = Pair.of(first, second);
                first = second;
                return pair;
            }
        };
    }

    @SuppressWarnings({"PMD.ShortVariable", "PMD.CognitiveComplexity"})
    public static IterToolsIterator<int[]> combinations(final int n, final int k) {
        AssertUtils.assertTrue(n > 0 && k <= n);

        return new IterToolsIterator<>() {
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

    public record Pair<T>(T first, T second) {
        @SuppressWarnings("PMD.ShortMethodName")
        public static <T> Pair<T> of(final T first, final T second) {
            return new Pair<>(first, second);
        }
    }

    public record ProductPair<T, U>(T first, U second) {
        @SuppressWarnings("PMD.ShortMethodName")
        public static <T, U> ProductPair<T, U> of(final T first, final U second) {
            return new ProductPair<>(first, second);
        }
    }

    public interface IterToolsIterator<T> extends Iterator<T> {
        default Stream<T> stream() {
            return IterTools.stream(this);
        }

        default Iterable<T> iterable() {
            return () -> this;
        }
    }

    @SuppressWarnings({
        "PMD.ShortClassName",
        "PMD.ShortVariable",
        "PMD.MethodNamingConventions",
        "PMD.AvoidLiteralsInIfCondition"
    })
    private static final class Heap {

        public static void accept(final int[] a, final Consumer<int[]> consumer) {
            heaps_algorithm(a, a.length, consumer);
        }

        private static void heaps_algorithm(
                final int[] a, final int n, final Consumer<int[]> consumer) {
            if (n == 1) {
                // (got a new permutation)
                consumer.accept(a);
                return;
            }
            for (int i = 0; i < n - 1; i++) {
                heaps_algorithm(a, n - 1, consumer);
                // always swap the first when odd,
                // swap the i-th when even
                if (n % 2 == 0) {
                    swap(a, n - 1, i);
                } else {
                    swap(a, n - 1, 0);
                }
            }
            heaps_algorithm(a, n - 1, consumer);
        }

        private static void swap(final int[] a, final int i, final int j) {
            final int temp = a[i];
            a[i] = a[j];
            a[j] = temp;
        }
    }

    @SuppressWarnings("PMD.SystemPrintln")
    public static void main(final String[] args) {
        assertMatches(
                combinations(4, 3).stream().collect(toSet()),
                Set.of("{0, 1, 2}", "{0, 1, 3}", "{0, 2, 3}", "{1, 2, 3}"));
        assertMatches(
                combinations(3, 2).stream().collect(toSet()), Set.of("{0, 1}", "{0, 2}", "{1, 2}"));
        assertMatches(combinations(3, 3).stream().collect(toSet()), Set.of("{0, 1, 2}"));
        assert combinations(20, 6).stream().count() == 38_760;
        try {
            combinations(3, 4);
        } catch (final IllegalArgumentException expected) {
        }
        try {
            combinations(0, 3);
        } catch (final IllegalArgumentException expected) {
        }
        System.out.println("OK");
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
