package com.github.pareronia.everybody_codes.utils.itertools;

import com.github.pareronia.everybody_codes.utils.IntegerSequence.Range;

import java.util.Iterator;
import java.util.function.Consumer;
import java.util.stream.Stream;

public final class IterTools {

    private IterTools() {}

    public static <T> Stream<T> stream(final Iterator<T> iterator) {
        return Stream.generate(() -> null)
                .takeWhile(x -> iterator.hasNext())
                .map(n -> iterator.next());
    }

    @SuppressWarnings("PMD.ShortVariable")
    public static IterToolsIterator<int[]> combinations(final int n, final int k) {
        return asIterToolsIterator(Combinations.combinations(n, k));
    }

    public static <T> IterToolsIterator<Pair<T>> pairwise(final Stream<T> stream) {
        return pairwise(stream.iterator());
    }

    public static IterToolsIterator<Pair<Integer>> pairwise(final Range range) {
        return pairwise(range.iterator());
    }

    public static <T> IterToolsIterator<Pair<T>> pairwise(final Iterator<T> iterator) {
        return asIterToolsIterator(Pairwise.pairwise(iterator));
    }

    public static void permutations(final int[] nums, final Consumer<int[]> consumer) {
        Heap.accept(nums, consumer);
    }

    public static <T, U> IterToolsIterator<ProductPair<T, U>> product(
            final Iterator<T> first, final Iterator<U> second) {

        return asIterToolsIterator(Product.product(first, second));
    }

    private static <T> IterToolsIterator<T> asIterToolsIterator(final Iterator<T> iterator) {
        return new IterToolsIterator<>() {

            @Override
            public boolean hasNext() {
                return iterator.hasNext();
            }

            @Override
            public T next() {
                return iterator.next();
            }
        };
    }
}
