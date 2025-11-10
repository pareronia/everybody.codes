package com.github.pareronia.everybody_codes.grid;

import java.util.List;

public class CharGrid implements Grid<Character> {

    private final char[][] cells;

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

    @Override
    public Character getValue(final Cell cell) {
        return this.cells[cell.row()][cell.col()];
    }

    @Override
    public void setValue(final Cell cell, final Character value) {
        this.cells[cell.row()][cell.col()] = value;
    }
}
