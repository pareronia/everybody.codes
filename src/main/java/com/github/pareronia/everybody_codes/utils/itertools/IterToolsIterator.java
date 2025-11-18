package com.github.pareronia.everybody_codes.utils.itertools;

import java.util.Iterator;
import java.util.stream.Stream;

public interface IterToolsIterator<T> extends Iterator<T> {
    default Stream<T> stream() {
        return IterTools.stream(this);
    }

    default Iterable<T> iterable() {
        return () -> this;
    }
}
