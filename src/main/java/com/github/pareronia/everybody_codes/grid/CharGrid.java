package com.github.pareronia.everybody_codes.grid;

import com.github.pareronia.everybody_codes.utils.AssertUtils;

import java.util.Arrays;
import java.util.List;

public class CharGrid implements Grid<Character> {

    private final char[][] cells;

    @SuppressWarnings("PMD.UseVarargs")
    public CharGrid(final char[][] cells) {
        this.cells = Arrays.stream(cells).map(char[]::clone).toArray(char[][]::new);
    }

    public CharGrid(final List<String> strings) {
        final char[][] cells = new char[strings.size()][strings.get(0).length()];
        for (int i = 0; i < strings.size(); i++) {
            cells[i] = strings.get(i).toCharArray();
        }
        this.cells = cells;
    }

    @Override
    public int getHeight() {
        return this.cells.length;
    }

    @Override
    public int getWidth() {
        return this.cells[0].length;
    }

    public char[] getRow(final Integer row) {
        AssertUtils.assertTrue(0 <= row && row < getHeight());
        return Arrays.copyOf(this.cells[row], getWidth());
    }

    @Override
    public Character getValue(final Cell cell) {
        return this.cells[cell.row()][cell.col()];
    }

    @Override
    public void setValue(final Cell cell, final Character value) {
        this.cells[cell.row()][cell.col()] = value;
    }

    @Override
    public String getRowAsString(final int row) {
        return new String(getRow(row));
    }
}
