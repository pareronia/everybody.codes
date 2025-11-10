package com.github.pareronia.everybody_codes.solution;

import java.util.function.Supplier;

@SuppressWarnings("PMD.SystemPrintln")
public class Logger {

    private final boolean debug;

    public Logger(final boolean debug) {
        this.debug = debug;
    }

    public void log(final Object obj) {
        if (!debug) {
            return;
        }
        System.out.println(obj);
    }

    public void log(final Supplier<Object> supplier) {
        if (!debug) {
            return;
        }
        System.out.println(supplier.get());
    }
}
