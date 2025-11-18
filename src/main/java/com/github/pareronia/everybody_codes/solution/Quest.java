package com.github.pareronia.everybody_codes.solution;

import static java.util.stream.Collectors.joining;

import com.github.pareronia.everybody_codes.solution.ecd.ECData;
import com.github.pareronia.everybody_codes.utils.StringUtils;

import java.util.List;
import java.util.Optional;
import java.util.stream.Stream;

public record Quest(
        int event,
        int quest,
        Optional<String> title,
        Optional<String> expected1,
        Optional<String> expected2,
        Optional<String> expected3) {

    public static Quest create(final int event, final int quest) {
        return new Quest(
                event,
                quest,
                ECData.getTitle(event, quest),
                ECData.getAnswer(event, quest, 1),
                ECData.getAnswer(event, quest, 2),
                ECData.getAnswer(event, quest, 3));
    }

    public List<String> getInput(final int part) {
        return ECData.getInput(event, quest, part);
    }

    @SuppressWarnings("PMD.TypeParameterNamingConventions")
    public <A1, A2, A3> void check(final A1 answer1, final A2 answer2, final A3 answer3) {
        final String[] expected = {
            expected1.orElse(null), expected2.orElse(null), expected3.orElse(null)
        };
        final String[] actual = {
            String.valueOf(answer1), String.valueOf(answer2), String.valueOf(answer3)
        };
        final String[] fails = {"", "", ""};
        final FailDecider failDecider = new FailDecider();
        for (int i = 0; i < 3; i++) {
            if (failDecider.fail(expected[i], actual[i]) == FailDecider.Status.FAIL) {
                fails[i] =
                        "%sPart %d: Expected: '%s', got '%s'"
                                .formatted(System.lineSeparator(), i + 1, expected[i], actual[i]);
            }
        }
        for (final String fail : fails) {
            if (StringUtils.isNotBlank(fail)) {
                throw new AssertionError(Stream.of(fails).collect(joining()));
            }
        }
    }

    public static final class FailDecider {
        @SuppressWarnings("PMD.ShortVariable")
        public enum Status {
            OK,
            FAIL,
            UNKNOWN
        }

        public Status fail(final String expected, final String actual) {
            if (StringUtils.isEmpty(expected) || actual == null) {
                return Status.UNKNOWN;
            }
            return expected.equals(actual) ? Status.OK : Status.FAIL;
        }
    }
}
