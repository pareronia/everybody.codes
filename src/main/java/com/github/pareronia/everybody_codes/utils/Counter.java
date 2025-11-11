package com.github.pareronia.everybody_codes.utils;

import static java.util.stream.Collectors.summingLong;

import java.util.HashMap;
import java.util.Map;

public class Counter<T> {

    private final Map<T, Long> counts;

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
}
