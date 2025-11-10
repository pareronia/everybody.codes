package com.github.pareronia.everybody_codes.solution;

import java.time.Duration;
import java.time.temporal.ChronoUnit;
import java.util.function.Supplier;

public record Timed<V>(V result, Duration duration) {

    public static <V> Timed<V> timed(
            final Callable<V> callable, final Supplier<Long> nanoTimeSupplier) {
        final long timerStart = nanoTimeSupplier.get();
        final V answer = callable.call();
        final long timerEnd = nanoTimeSupplier.get();
        return new Timed<>(answer, Duration.of(timerEnd - timerStart, ChronoUnit.NANOS));
    }
}
