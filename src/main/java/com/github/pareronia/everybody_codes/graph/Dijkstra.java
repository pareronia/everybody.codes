package com.github.pareronia.everybody_codes.graph;

import com.github.pareronia.everybody_codes.utils.AssertUtils;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Stream;

@SuppressWarnings({"PMD.ShortVariable", "PMD.CouplingBetweenObjects"})
public final class Dijkstra {

    private Dijkstra() {}

    public static <T> Result<T> best(
            final T start,
            final Predicate<T> end,
            final Function<T, Stream<T>> adjacent,
            final BiFunction<T, T, Long> cost,
            final Long limit) {

        return execute(start, end, adjacent, cost, Comparator.naturalOrder(), limit);
    }

    public static <T> Result<T> worst(
            final T start,
            final Predicate<T> end,
            final Function<T, Stream<T>> adjacent,
            final BiFunction<T, T, Long> cost) {

        return execute(start, end, adjacent, cost, Comparator.reverseOrder(), null);
    }

    @SuppressWarnings({"unchecked", "PMD.AvoidInstantiatingObjectsInLoops"})
    public static <T> Result<T> execute(
            final T start,
            final Predicate<T> end,
            final Function<T, Stream<T>> adjacent,
            final BiFunction<T, T, Long> cost,
            final Comparator<State<T>> comparator,
            final Long limit) {
        final Queue<State<T>> q = new PriorityQueue<>(comparator);
        q.add(new State<>(start, 0));
        final Map<T, Long> best = new HashMap<>();
        best.put(start, 0L);
        final Map<T, T> parent = new HashMap<>();
        while (!q.isEmpty()) {
            final State<T> state = q.poll();
            if (comparator.compare(state, new State<>(null, limit)) > 0) {
                return (Result<T>) Result.NONE;
            }
            if (end.test(state.node)) {
                break;
            }
            final long total = best.getOrDefault(state.node, Long.MAX_VALUE);
            adjacent.apply(state.node)
                    .forEach(
                            n -> {
                                final long newTotal = total + cost.apply(state.node, n);
                                if (newTotal < best.getOrDefault(n, Long.MAX_VALUE)) {
                                    best.put(n, newTotal);
                                    parent.put(n, state.node);
                                    q.add(new State<>(n, newTotal));
                                }
                            });
        }
        return new Result<>(start, best, parent);
    }

    @SuppressWarnings("PMD.OverrideBothEqualsAndHashCodeOnComparable")
    public record State<T>(T node, long cost) implements Comparable<State<T>> {

        @Override
        public int compareTo(final State<T> other) {
            AssertUtils.assertTrue(other != null);
            return Long.compare(this.cost, other.cost);
        }
    }

    public record Result<T>(T source, Map<T, Long> distances, Map<T, T> paths) {

        public static final Result<?> NONE = new Result<>(null, Map.of(), Map.of());

        public long getDistance(final T start) {
            return distances.get(start);
        }

        public List<T> getPath(final T start) {
            final List<T> path = new ArrayList<>();
            T parent = start;
            if (start.equals(this.source)) {
                path.add(this.source);
            } else {
                while (!parent.equals(this.source)) {
                    path.add(0, parent);
                    parent = this.paths.get(parent);
                }
                path.add(0, this.source);
            }
            return path;
        }
    }
}
