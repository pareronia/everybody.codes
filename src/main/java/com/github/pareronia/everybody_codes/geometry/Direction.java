package com.github.pareronia.everybody_codes.geometry;

import java.util.Arrays;
import java.util.EnumSet;
import java.util.Optional;
import java.util.Set;

@SuppressWarnings({"PMD.ShortVariable", "PMD.NonSerializableClass"})
public enum Direction {
    UP(0, 1, Optional.of('U')),
    RIGHT(1, 0, Optional.of('R')),
    DOWN(0, -1, Optional.of('D')),
    LEFT(-1, 0, Optional.of('L'));

    public static final Set<Direction> CAPITAL = EnumSet.of(UP, RIGHT, DOWN, LEFT);

    private final int x;
    private final int y;
    private final Optional<Character> letter;

    Direction(final int x, final int y, final Optional<Character> letter) {
        this.x = x;
        this.y = y;
        this.letter = letter;
    }

    public static Direction fromChar(final char ch) {
        return Arrays.stream(values())
                .filter(v -> v.letter.isPresent() && v.letter.get() == ch)
                .findFirst()
                .orElseThrow(
                        () ->
                                new IllegalArgumentException(
                                        String.format("Invalid Direction: '%s'", ch)));
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public Direction turn(final Turn turn) {
        return switch (this) {
            case UP -> turn == Turn.LEFT ? LEFT : RIGHT;
            case RIGHT -> turn == Turn.LEFT ? UP : DOWN;
            case DOWN -> turn == Turn.LEFT ? RIGHT : LEFT;
            case LEFT -> turn == Turn.LEFT ? DOWN : UP;
        };
    }
}
