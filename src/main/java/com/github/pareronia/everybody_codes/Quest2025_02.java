package com.github.pareronia.everybody_codes;

import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.IterTools;
import com.github.pareronia.everybody_codes.utils.StringUtils;
import com.github.pareronia.everybody_codes.utils.StringUtils.StringSplit;

import java.util.Iterator;
import java.util.List;
import java.util.function.Predicate;
import java.util.stream.IntStream;
import java.util.stream.Stream;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_02 extends SolutionBase<String, Integer, Integer> {

    private static final String TEST1 = "A=[25,9]";
    private static final String TEST2 = "A=[35300,-64910]";

    private Quest2025_02(final boolean debug) {
        super(debug);
    }

    public static Quest2025_02 create() {
        return new Quest2025_02(false);
    }

    public static Quest2025_02 createDebug() {
        return new Quest2025_02(true);
    }

    private Point parse(final List<String> inputs) {
        final String string = inputs.getFirst();
        final StringSplit<Integer> split =
                StringUtils.splitOnceToInt(string.substring(3, string.length() - 1), ",");
        return new Point(split.left(), split.right());
    }

    @Override
    public String solvePart1(final List<String> inputs) {
        final Complex ans = this.calculate(this.parse(inputs), 3, 10).toList().getLast();
        return "[%d,%d]".formatted(ans.real(), ans.imag());
    }

    @Override
    public Integer solvePart2(final List<String> inputs) {
        final Point point = this.parse(inputs);
        return this.count(
                product(
                        IntStream.rangeClosed(0, 100).map(i -> point.x() + i * 10),
                        IntStream.rangeClosed(0, 100).map(i -> point.y() + i * 10)));
    }

    @Override
    public Integer solvePart3(final List<String> inputs) {
        final Point point = this.parse(inputs);
        return this.count(
                product(
                        IntStream.rangeClosed(point.x(), point.x() + 1000),
                        IntStream.rangeClosed(point.y(), point.y() + 1000)));
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "[357,862]"),
        @Sample(method = "part2", input = TEST2, expected = "4076"),
        @Sample(method = "part3", input = TEST2, expected = "406954")
    })
    public static void main(final String[] args) {
        create().run();
    }

    private record Complex(long real, long imag) {}

    @SuppressWarnings("PMD.ShortVariable")
    private record Point(int x, int y) {}

    private Stream<Point> product(final IntStream first, final IntStream second) {
        return IterTools.product(first.iterator(), second.iterator()).stream()
                .map(pp -> new Point(pp.first(), pp.second()));
    }

    private Stream<Complex> calculate(final Point point, final int iterations, final int factor) {
        @SuppressWarnings("PMD.ShortVariable")
        final Iterator<Complex> iter =
                new Iterator<>() {
                    private Complex c = new Complex(0, 0);
                    private int i;

                    @Override
                    public Complex next() {
                        c = calculate(point, factor);
                        i++;
                        return c;
                    }

                    @Override
                    public boolean hasNext() {
                        return i < iterations;
                    }

                    private Complex calculate(final Point point, final int factor) {
                        return new Complex(
                                point.x + (c.real() * c.real() - c.imag() * c.imag()) / factor,
                                point.y + 2 * c.real() * c.imag() / factor);
                    }
                };
        return IterTools.stream(iter);
    }

    private int count(final Stream<Point> points) {
        final Predicate<Complex> inRange =
                c -> Math.abs(c.real()) <= 1_000_000 && Math.abs(c.imag()) <= 1_000_000;
        return (int) points.filter(p -> this.calculate(p, 100, 100_000).allMatch(inRange)).count();
    }
}
