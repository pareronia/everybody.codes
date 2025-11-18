package com.github.pareronia.everybody_codes.utils;

import java.util.Iterator;
import java.util.stream.IntStream;
import java.util.stream.Stream;

@SuppressWarnings("PMD.MissingStaticMethodInNonInstantiatableClass")
public final class IntegerSequence {

    private IntegerSequence() {}

    @SuppressWarnings("PMD.ShortVariable")
    public static final class Range implements Iterable<Integer> {

        private final int from;
        private final int to;
        private final int step;

        private Range(final int from, final int to, final int step) {
            AssertUtils.assertTrue(step != 0, () -> "step should be != 0");
            AssertUtils.assertTrue(from <= to, () -> "from should not be greater than to");
            this.from = from;
            this.to = to;
            this.step = step;
        }

        public static Range range(final int to) {
            AssertUtils.assertTrue(to > 0, () -> "to should be > 0");
            return new Range(0, to, 1);
        }

        public static Range rangeClosed(final int to) {
            AssertUtils.assertTrue(to > 0, () -> "to should be > 0");
            return new Range(0, to + 1, 1);
        }

        public static Range range(final int from, final int to) {
            return new Range(from, to, 1);
        }

        public static Range rangeClosed(final int from, final int to) {
            return new Range(from, to + 1, 1);
        }

        public static Range range(final int from, final int to, final int step) {
            return new Range(from, to, step);
        }

        public static Range rangeClosed(final int from, final int to, final int step) {
            return new Range(from, to + 1, step);
        }

        @Override
        public Iterator<Integer> iterator() {
            return stream().iterator();
        }

        public IntStream intStream() {
            return IntStream.iterate(this.from, i -> i < this.to, i -> i + this.step);
        }

        public Stream<Integer> stream() {
            return Stream.iterate(this.from, i -> i < this.to, i -> i + this.step);
        }

        public int[] toArray() {
            return this.intStream().toArray();
        }
    }
}
