package com.github.pareronia.everybody_codes.geometry;

import java.util.EnumSet;
import java.util.Set;

@SuppressWarnings("PMD.ShortVariable")
public enum Direction {
    UP(0, 1),
    RIGHT(1, 0),
    DOWN(0, -1),
    LEFT(-1, 0);

    public static final Set<Direction> CAPITAL = EnumSet.of(UP, RIGHT, DOWN, LEFT);

    private final int x;
    private final int y;

    Direction(final int x, final int y) {
        this.x = x;
        this.y = y;
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
