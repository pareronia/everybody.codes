package com.github.pareronia.everybody_codes.grid;

import java.util.Arrays;

public class IntGrid implements Grid<Integer> {

    private final int[][] values;

    @SuppressWarnings("PMD.UseVarargs")
    public IntGrid(final int[][] values) {
        this.values = Arrays.stream(values).map(int[]::clone).toArray(int[][]::new);
    }

    @Override
    public int getWidth() {
        assert this.values.length > 0;
        return this.values[0].length;
    }

    @Override
    public int getHeight() {
        return this.values.length;
    }

    @Override
    public Integer getValue(final Cell cell) {
        return this.values[cell.row()][cell.col()];
    }

    @Override
    public void setValue(final Cell cell, final Integer value) {
        this.values[cell.row()][cell.col()] = value;
    }
}
