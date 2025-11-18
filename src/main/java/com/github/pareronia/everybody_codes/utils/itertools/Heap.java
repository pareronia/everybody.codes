package com.github.pareronia.everybody_codes.utils.itertools;

import java.util.function.Consumer;

@SuppressWarnings({
    "PMD.ShortClassName",
    "PMD.ShortVariable",
    "PMD.MethodNamingConventions",
    "PMD.AvoidLiteralsInIfCondition"
})
final class Heap {

    private Heap() {}

    public static void accept(final int[] a, final Consumer<int[]> consumer) {
        heaps_algorithm(a, a.length, consumer);
    }

    private static void heaps_algorithm(
            final int[] a, final int n, final Consumer<int[]> consumer) {
        if (n == 1) {
            // (got a new permutation)
            consumer.accept(a);
            return;
        }
        for (int i = 0; i < n - 1; i++) {
            heaps_algorithm(a, n - 1, consumer);
            // always swap the first when odd,
            // swap the i-th when even
            if (n % 2 == 0) {
                swap(a, n - 1, i);
            } else {
                swap(a, n - 1, 0);
            }
        }
        heaps_algorithm(a, n - 1, consumer);
    }

    private static void swap(final int[] a, final int i, final int j) {
        final int temp = a[i];
        a[i] = a[j];
        a[j] = temp;
    }
}
