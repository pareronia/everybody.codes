package com.github.pareronia.everybody_codes.geometry;

import java.util.Arrays;

public enum Turn {
    LEFT('L'),
    RIGHT('R');

    private final Character letter;

    Turn(final Character letter) {
        this.letter = letter;
    }

    public static Turn fromChar(final char ch) {
        return Arrays.stream(values())
                .filter(v -> v.letter == ch)
                .findFirst()
                .orElseThrow(
                        () ->
                                new IllegalArgumentException(
                                        String.format("Invalid Direction: '%s'", ch)));
    }
}
