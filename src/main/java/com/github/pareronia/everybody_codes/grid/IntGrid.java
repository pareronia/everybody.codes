package com.github.pareronia.everybody_codes.grid;

import com.github.pareronia.everybody_codes.utils.StringUtils;

import java.util.Arrays;
import java.util.List;

public class IntGrid implements Grid<Integer> {

    private final int[][] values;

    @SuppressWarnings("PMD.UseVarargs")
    public IntGrid(final int[][] values) {
        this.values = Arrays.stream(values).map(int[]::clone).toArray(int[][]::new);
    }

    public static IntGrid from(final List<String> strings) {
        final int[][] values = new int[strings.size()][strings.get(0).length()];
        strings.stream()
                .map(
                        s ->
                                StringUtils.asCharacterStream(s)
                                        .mapToInt(ch -> Integer.parseInt(String.valueOf(ch)))
                                        .toArray())
                .toArray(a -> values);
        return new IntGrid(values);
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
