package com.github.pareronia.everybody_codes.solution.ecd;

import com.github.pareronia.everybody_codes.utils.ECException;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

public final class SystemUtils {

    private SystemUtils() {}

    public static long getSystemNanoTime() {
        return System.nanoTime();
    }

    public static List<String> readAllLines(final Path path) {
        try {
            return Files.readAllLines(Objects.requireNonNull(path), StandardCharsets.UTF_8);
        } catch (final IOException e) {
            throw new ECException(e);
        }
    }

    public static List<String> readAllLinesIfExists(final Path path) {
        if (Files.notExists(Objects.requireNonNull(path))) {
            return List.of();
        }
        return readAllLines(path);
    }

    public static Optional<String> readFirstLineIfExists(final Path path) {
        return readAllLinesIfExists(path).stream().findFirst();
    }
}
