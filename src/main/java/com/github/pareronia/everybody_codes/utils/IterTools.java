package com.github.pareronia.everybody_codes.utils;

import java.util.Iterator;
import java.util.List;
import java.util.stream.Stream;

public final class IterTools {

    private IterTools() {}

    public static <T> Stream<T> stream(final Iterator<T> iterator) {
        return Stream.generate(() -> null)
                .takeWhile(x -> iterator.hasNext())
                .map(n -> iterator.next());
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
}
