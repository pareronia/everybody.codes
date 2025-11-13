package com.github.pareronia.everybody_codes.utils;

import static java.util.Comparator.comparing;
import static java.util.stream.Collectors.counting;
import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.summingLong;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;

public class Counter<T> {

    private final Map<T, Long> counts;

    public Counter(final Stream<T> stream) {
        this.counts = stream.collect(groupingBy(o -> o, counting()));
    }

    public Counter() {
        this.counts = new HashMap<>();
    }

    public Long get(final T value) {
        return this.counts.getOrDefault(value, 0L);
    }

    public void add(final T key, final long value) {
        this.counts.merge(key, value, Long::sum);
    }

    public void update(final T key) {
        this.add(key, 1L);
    }

    public long total() {
        return this.counts.values().stream().collect(summingLong(Long::valueOf));
    }

    public List<Entry<T>> mostCommon() {
        return this.counts.entrySet().stream()
                .sorted(comparing(Map.Entry<T, Long>::getValue).reversed())
                .map(e -> new Entry<T>(e.getKey(), e.getValue()))
                .toList();
    }

    public record Entry<T>(T value, long count) {}
}
