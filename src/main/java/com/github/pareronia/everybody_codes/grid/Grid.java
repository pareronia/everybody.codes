package com.github.pareronia.everybody_codes.grid;

import static java.util.stream.Collectors.joining;

import com.github.pareronia.everybody_codes.utils.itertools.IterTools;

import java.util.Iterator;
import java.util.function.Predicate;
import java.util.stream.Stream;
import java.util.stream.Stream.Builder;

@SuppressWarnings("PMD.ShortClassName")
public interface Grid<T> {
    int getHeight();

    int getWidth();

    default int getMaxRowIndex() {
        return this.getHeight() - 1;
    }

    default int getMaxColIndex() {
        return this.getWidth() - 1;
    }

    T getValue(Cell cell);

    void setValue(Cell cell, T value);

    String getRowAsString(int row);

    default Stream<String> getRowsAsStrings() {
        return IterTools.stream(
                new Iterator<>() {
                    private int row;

                    @Override
                    public boolean hasNext() {
                        return row <= Grid.this.getMaxRowIndex();
                    }

                    @Override
                    public String next() {
                        return Grid.this.getRowAsString(row++);
                    }
                });
    }

    default String asString() {
        return this.getRowsAsStrings().collect(joining(System.lineSeparator()));
    }

    default boolean isInBounds(final Cell cell) {
        return 0 <= cell.row()
                && cell.row() < this.getHeight()
                && 0 <= cell.col()
                && cell.col() < this.getWidth();
    }

    @SuppressWarnings("PMD.AvoidInstantiatingObjectsInLoops")
    default Stream<Cell> getCells() {
        final Builder<Cell> builder = Stream.builder();
        for (int r = 0; r < this.getHeight(); r++) {
            for (int c = 0; c < this.getWidth(); c++) {
                builder.add(new Cell(r, c));
            }
        }
        return builder.build();
    }

    default Stream<Cell> findAllMatching(final Predicate<T> test) {
        return this.getCells().filter(cell -> test.test(this.getValue(cell)));
    }

    default Stream<Cell> getAllEqualTo(final T value) {
        return this.findAllMatching(c -> c.equals(value));
    }
}
