package com.github.pareronia.everybody_codes.utils;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public final class StringUtils {

    public static final String EMPTY = "";

    private StringUtils() {}

    public static Stream<Character> asCharacterStream(final String string) {
        return IntStream.range(0, Objects.requireNonNull(string).length()).mapToObj(string::charAt);
    }

    public record StringSplit<T>(T left, T right) {}

    public static StringSplit<String> splitOnce(final String string, final String regex) {
        final String[] splits = Objects.requireNonNull(string).split(regex);
        return new StringSplit<>(splits[0], splits[1]);
    }

    public static StringSplit<Integer> splitOnceToInt(final String string, final String regex) {
        final String[] splits = Objects.requireNonNull(string).split(regex);
        return new StringSplit<>(Integer.parseInt(splits[0]), Integer.parseInt(splits[1]));
    }

    public static StringSplit<Double> splitOnceToDouble(final String string, final String regex) {
        final String[] splits = Objects.requireNonNull(string).split(regex);
        return new StringSplit<>(Double.parseDouble(splits[0]), Double.parseDouble(splits[1]));
    }

    public static IntStream splitToInt(final String string, final String regex) {
        return Arrays.stream(Objects.requireNonNull(string).split(regex))
                .mapToInt(Integer::parseInt);
    }

    public static List<String> splitLines(final String input) {
        return Arrays.asList((Objects.requireNonNull(input) + "\n").split("\\r?\\n"));
    }

    public static List<List<String>> toBlocks(final List<String> inputs) {
        if (inputs.isEmpty()) {
            return List.of();
        }
        final List<List<String>> blocks = new ArrayList<>();
        final int last = inputs.size() - 1;
        blocks.add(new ArrayList<>());
        for (int j = 0; j <= last; j++) {
            if (inputs.get(j).isEmpty()) {
                blocks.add(List.copyOf(blocks.removeLast()));
                if (j != last) {
                    blocks.add(new ArrayList<>());
                }
            } else {
                blocks.getLast().add(inputs.get(j));
            }
        }
        return List.copyOf(blocks);
    }

    public static int length(final CharSequence chs) {
        return chs == null ? 0 : chs.length();
    }

    public static boolean isBlank(final CharSequence chs) {
        final int strLen = length(chs);
        if (strLen == 0) {
            return true;
        }
        for (int i = 0; i < strLen; i++) {
            if (!Character.isWhitespace(chs.charAt(i))) {
                return false;
            }
        }
        return true;
    }

    public static boolean isNotBlank(final CharSequence chs) {
        return !isBlank(chs);
    }

    public static boolean isEmpty(final CharSequence chs) {
        return chs == null || chs.length() == 0;
    }
}
