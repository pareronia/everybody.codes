package com.github.pareronia.everybody_codes.grid;

import com.github.pareronia.everybody_codes.geometry.Direction;

public record Cell(int row, int col) {

    @SuppressWarnings("PMD.ShortMethodName")
    public static Cell at(final int row, final int col) {
        return new Cell(row, col);
    }

    @SuppressWarnings("PMD.ShortMethodName")
    public Cell at(final Direction direction) {
        return new Cell(this.row - direction.getY(), this.col + direction.getX());
    }
}
