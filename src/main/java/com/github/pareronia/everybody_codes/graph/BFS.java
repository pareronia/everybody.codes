package com.github.pareronia.everybody_codes.graph;

import com.github.pareronia.everybody_codes.utils.AssertUtils;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Stream;

@SuppressWarnings("PMD.ShortClassName")
public final class BFS {

    private BFS() {}

    @SuppressWarnings("PMD.AvoidInstantiatingObjectsInLoops")
    public static <T> List<Set<T>> connectedComponents(
            final Set<T> nodes, final Function<T, Stream<T>> adjacent) {
        final List<Set<T>> components = new ArrayList<>();
        final Set<T> todo = new HashSet<>(nodes);
        while (!todo.isEmpty()) {
            T node = todo.iterator().next();
            todo.remove(node);
            final Set<T> component = new HashSet<>();
            component.add(node);
            final Deque<T> queue = new ArrayDeque<>(List.of(node));
            while (!queue.isEmpty()) {
                node = queue.pollFirst();
                adjacent.apply(node)
                        .forEach(
                                n -> {
                                    if (!component.contains(n)) {
                                        queue.add(n);
                                    }
                                    todo.remove(n);
                                    component.add(n);
                                });
            }
            components.add(component);
        }
        return components;
    }

    public static <T> int execute(
            final T start, final Predicate<T> isEnd, final Function<T, Stream<T>> adjacent) {
        return executeWithCost(start, isEnd, adjacent, (curr, nxt) -> 1);
    }

    public static <T> int executeWithCost(
            final T start,
            final Predicate<T> isEnd,
            final Function<T, Stream<T>> adjacent,
            final BiFunction<T, T, Integer> cost) {
        final Deque<State<T>> queue = new ArrayDeque<>(Set.of(new State<>(start, 0)));
        final Set<T> seen = new HashSet<>(Set.of(start));
        while (!queue.isEmpty()) {
            final State<T> state = queue.poll();
            if (isEnd.test(state.node)) {
                return state.cost;
            }
            adjacent.apply(state.node)
                    .filter(n -> !seen.contains(n))
                    .forEach(
                            n -> {
                                seen.add(n);
                                queue.add(new State<>(n, state.cost + cost.apply(state.node, n)));
                            });
        }
        throw AssertUtils.unreachable();
    }

    private record State<T>(T node, int cost) {}
}
