package com.github.pareronia.everybody_codes.grid;

import com.github.pareronia.everybody_codes.geometry.Direction;
import com.github.pareronia.everybody_codes.utils.AssertUtils;

import java.util.stream.Stream;

public record Cell(int row, int col) {

    @SuppressWarnings("PMD.ShortMethodName")
    public static Cell at(final int row, final int col) {
        return new Cell(row, col);
    }

    @SuppressWarnings("PMD.ShortMethodName")
    public Cell at(final Direction direction) {
        return this.at(direction, 1);
    }

    @SuppressWarnings("PMD.ShortMethodName")
    public Cell at(final Direction direction, final int amount) {
        return new Cell(this.row - amount * direction.getY(), this.col + amount * direction.getX());
    }

    public Stream<Cell> capitalNeighbours() {
        return Direction.CAPITAL.stream().map(this::at);
    }

    public int manhattanDistance(final Cell other) {
        AssertUtils.assertTrue(other != null);
        return Math.abs(this.row - other.row) + Math.abs(this.col - other.col);
    }
}
