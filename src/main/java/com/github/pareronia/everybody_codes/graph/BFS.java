package com.github.pareronia.everybody_codes.graph;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.function.Function;
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
            @SuppressWarnings("PMD.ShortVariable")
            final Deque<T> q = new ArrayDeque<>(List.of(node));
            while (!q.isEmpty()) {
                node = q.pollFirst();
                adjacent.apply(node)
                        .forEach(
                                n -> {
                                    if (!component.contains(n)) {
                                        q.add(n);
                                    }
                                    todo.remove(n);
                                    component.add(n);
                                });
            }
            components.add(component);
        }
        return components;
    }
}
