package com.github.pareronia.everybody_codes.solution;

import java.util.function.Supplier;

@FunctionalInterface
public interface LoggerEnabled {

    default void log(final Object obj) {
        getLogger().log(obj);
    }

    default void log(final Supplier<Object> supplier) {
        getLogger().log(supplier);
    }

    Logger getLogger();
}
