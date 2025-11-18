package com.github.pareronia.everybody_codes.utils;

public final class AssertUtils {

    private AssertUtils() {}

    public static void assertTrue(final boolean condition) {
        if (!condition) {
            throw buildException();
        }
    }

    private static IllegalArgumentException buildException() {
        return new IllegalArgumentException();
    }
}
