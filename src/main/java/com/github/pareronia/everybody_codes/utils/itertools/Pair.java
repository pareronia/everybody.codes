package com.github.pareronia.everybody_codes.utils.itertools;

public record Pair<T>(T first, T second) {
    @SuppressWarnings("PMD.ShortMethodName")
    public static <T> Pair<T> of(final T first, final T second) {
        return new Pair<>(first, second);
    }
}
