package com.github.pareronia.everybody_codes.solution.ecd;

import static java.util.stream.Collectors.joining;

import com.github.pareronia.everybody_codes.utils.ECException;
import com.github.pareronia.everybody_codes.utils.StringUtils;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Locale;
import java.util.NoSuchElementException;
import java.util.Optional;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class ECData {

    private ECData() {}

    public static Path getEverybodyCodesDir() {
        final String env = System.getenv("EVERYBODY_CODES_DIR");
        if (StringUtils.isNotBlank(env)) {
            return Paths.get(env);
        } else if (isOsWindows()) {
            return Paths.get(System.getenv("APPDATA"), "everybody.codes");
        } else if (isOsLinux()) {
            return Paths.get(getSystemProperty("user.home"), ".config", "everybody.codes");
        } else {
            throw new UnsupportedOperationException("OS not supported");
        }
    }

    public static String getToken() {
        final String env = System.getenv("EVERYBODY_CODES_TOKEN");
        if (StringUtils.isNotBlank(env)) {
            return env;
        }
        return SystemUtils.readAllLines(getEverybodyCodesDir().resolve("token")).get(0);
    }

    public static String getUserId(final String token) {
        final String json =
                SystemUtils.readAllLines(getEverybodyCodesDir().resolve("token2id.json")).stream()
                        .map(s -> s.replaceAll("\\s", ""))
                        .collect(joining(""));
        final Matcher matcher = Pattern.compile("\"" + token + "\":\"([\\.\\w]+)\"").matcher(json);
        if (matcher.find()) {
            return matcher.group(1);
        }
        throw new ECException(new NoSuchElementException());
    }

    public static Path getMemoDir() {
        return getEverybodyCodesDir().resolve(getUserId(getToken()));
    }

    public static String getPartString(final int part) {
        if (!Set.of(1, 2, 3).contains(part)) {
            throw new ECException("");
        }
        return part == 1 ? "a" : part == 2 ? "b" : "c";
    }

    public static Path getInputFile(final int event, final int quest, final int part) {
        final String name = "%d_%02d%s_input.txt".formatted(event, quest, getPartString(part));
        return getMemoDir().resolve(name);
    }

    public static List<String> getInput(final int event, final int quest, final int part) {
        return List.copyOf(SystemUtils.readAllLines(getInputFile(event, quest, part)));
    }

    public static Path getAnswerFile(final int event, final int quest, final int part) {
        final String name = "%d_%02d%s_answer.txt".formatted(event, quest, getPartString(part));
        return getMemoDir().resolve(name);
    }

    public static Optional<String> getAnswer(final int event, final int quest, final int part) {
        return SystemUtils.readFirstLineIfExists(getAnswerFile(event, quest, part));
    }

    private static boolean isOsWindows() {
        return getOsName().startsWith("Windows");
    }

    private static boolean isOsLinux() {
        return getOsName().toLowerCase(Locale.US).startsWith("linux");
    }

    private static String getOsName() {
        return getSystemProperty("os.name");
    }

    private static String getSystemProperty(final String property) {
        return System.getProperty(property);
    }
}
