package com.github.pareronia.everybody_codes.solution;

import com.github.pareronia.everybody_codes.solution.ecd.SystemUtils;
import com.github.pareronia.everybody_codes.utils.ECException;
import com.github.pareronia.everybody_codes.utils.StringUtils;

import java.lang.reflect.InvocationTargetException;
import java.time.Duration;
import java.util.List;
import java.util.Objects;
import java.util.stream.Stream;

public final class SolutionUtils {

    private SolutionUtils() {}

    @SuppressWarnings("PMD.AvoidLiteralsInIfCondition")
    public static String printDuration(final Duration duration) {
        final double timeSpent = duration.toNanos() / 1_000_000.0;
        final String time;
        if (timeSpent <= 1000) {
            time = String.format("%.3f", timeSpent);
        } else if (timeSpent <= 5_000) {
            time = ANSIColors.yellow(String.format("%.0f", timeSpent));
        } else {
            time = ANSIColors.red(String.format("%.0f", timeSpent));
        }
        return String.format("%s ms", time);
    }

    @SuppressWarnings("PMD.SystemPrintln")
    public static <V> V lap(final String prefix, final Callable<V> callable) {
        final Timed<V> timed = Timed.timed(callable, SystemUtils::getSystemNanoTime);
        final V answer = timed.result();
        final String duration = printDuration(timed.duration());
        System.out.println(
                String.format(
                        "%s : %s, took: %s", prefix, ANSIColors.bold(answer.toString()), duration));
        return answer;
    }

    public static void runSamples(final Class<?> klass) {
        final List<Sample> samples =
                Stream.of(klass.getMethods())
                        .filter(m -> m.isAnnotationPresent(Samples.class))
                        .map(m -> m.getAnnotation(Samples.class))
                        .flatMap(ann -> Stream.of(ann.value()))
                        .toList();
        for (final Sample sample : samples) {
            runSample(klass, sample);
        }
    }

    private static void runSample(final Class<?> klass, final Sample sample) {
        try {
            final Object quest =
                    klass.getDeclaredMethod("create" + (sample.debug() ? "Debug" : ""))
                            .invoke(null);
            final List<String> input = StringUtils.splitLines(sample.input());
            final Object answer =
                    quest.getClass().getMethod(sample.method(), List.class).invoke(quest, input);
            assert Objects.equals(sample.expected(), String.valueOf(answer))
                    : String.format(
                            "FAIL '%s(%s)'. Expected: '%s', got '%s'",
                            sample.method(), input, sample.expected(), String.valueOf(answer));
        } catch (IllegalAccessException
                | InvocationTargetException
                | NoSuchMethodException
                | SecurityException e) {
            throw new ECException(e);
        }
    }
}
