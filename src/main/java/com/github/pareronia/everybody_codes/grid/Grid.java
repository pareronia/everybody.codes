package com.github.pareronia.everybody_codes.grid;

import java.util.function.Predicate;
import java.util.stream.Stream;
import java.util.stream.Stream.Builder;

@SuppressWarnings("PMD.ShortClassName")
public interface Grid<T> {
    int getHeight();

    int getWidth();

    T getValue(Cell cell);

    void setValue(Cell cell, T value);

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
