package com.github.pareronia.everybody_codes.utils;

import java.util.function.Predicate;

public final class BinarySearch {

    private BinarySearch() {}

    public static long search(final Predicate<Long> test) {
        return search(test, null, null);
    }

    /**
     * Search max value such that <code>test</code> is true.
     */
    @SuppressWarnings("PMD.AssignmentInOperand")
    public static long search(final Predicate<Long> test, final Long min, final Long max) {
        // set left
        long left = min != null ? min : 0;
        AssertUtils.assertTrue(test.test(left));
        // set right
        long right;
        long diff;
        if (max != null) {
            right = max;
            AssertUtils.assertTrue(!test.test(right));
        } else {
            diff = 1;
            right = left + diff;
            while (test.test(right)) {
                left = right;
                diff *= 2;
                right = left + diff;
            }
        }
        // bisect
        long mid;
        while ((diff = right - left) > 1) {
            mid = left + diff / 2;
            if (test.test(mid)) {
                left = mid;
            } else {
                right = mid;
            }
        }
        return left;
    }
}
