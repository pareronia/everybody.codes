package com.github.pareronia.everybody_codes.utils.itertools;

public record ProductPair<T, U>(T first, U second) {
    @SuppressWarnings("PMD.ShortMethodName")
    public static <T, U> ProductPair<T, U> of(final T first, final U second) {
        return new ProductPair<>(first, second);
    }
}
