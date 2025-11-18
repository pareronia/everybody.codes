package com.github.pareronia.everybody_codes.utils;

import java.util.function.Supplier;

public final class AssertUtils {

    private AssertUtils() {}

    public static void assertTrue(final boolean condition) {
        if (!condition) {
            throw buildException();
        }
    }

    public static void assertTrue(final boolean condition, final Supplier<String> message) {
        if (!condition) {
            throw buildException(message);
        }
    }

    public static void assertFalse(final boolean condition, final Supplier<String> message) {
        if (condition) {
            throw buildException(message);
        }
    }

    private static IllegalArgumentException buildException() {
        return new IllegalArgumentException();
    }

    private static IllegalArgumentException buildException(final Supplier<String> message) {
        return new IllegalArgumentException(message.get());
    }
}
