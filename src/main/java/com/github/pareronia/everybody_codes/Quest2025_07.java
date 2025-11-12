package com.github.pareronia.everybody_codes;

import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.StringUtils;
import com.github.pareronia.everybody_codes.utils.StringUtils.StringSplit;

import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Predicate;
import java.util.stream.IntStream;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_07 extends SolutionBase<String, Integer, Integer> {

    private static final int MIN_SIZE = 7;
    private static final int MAX_SIZE = 11;
    private static final String TEST1 =
            """
            Oronris,Urakris,Oroneth,Uraketh

            r > a,i,o
            i > p,w
            n > e,r
            o > n,m
            k > f,r
            a > k
            U > r
            e > t
            O > r
            t > h
            """;
    private static final String TEST2 =
            """
            Xanverax,Khargyth,Nexzeth,Helther,Braerex,Tirgryph,Kharverax

            r > v,e,a,g,y
            a > e,v,x,r
            e > r,x,v,t
            h > a,e,v
            g > r,y
            y > p,t
            i > v,r
            K > h
            v > e
            B > r
            t > h
            N > e
            p > h
            H > e
            l > t
            z > e
            X > a
            n > v
            x > z
            T > i
            """;
    private static final String TEST3 =
            """
            Xaryt

            X > a,o
            a > r,t
            r > y,e,a
            h > a,e,v
            t > h
            v > e
            y > p,t
            """;
    private static final String TEST4 =
            """
            Khara,Xaryt,Noxer,Kharax

            r > v,e,a,g,y
            a > e,v,x,r,g
            e > r,x,v,t
            h > a,e,v
            g > r,y
            y > p,t
            i > v,r
            K > h
            v > e
            B > r
            t > h
            N > e
            p > h
            H > e
            l > t
            z > e
            X > a
            n > v
            x > z
            T > i
            """;

    private Quest2025_07(final boolean debug) {
        super(debug);
    }

    public static Quest2025_07 create() {
        return new Quest2025_07(false);
    }

    public static Quest2025_07 createDebug() {
        return new Quest2025_07(true);
    }

    private boolean possible(final String name, final Map<Character, Set<Character>> edges) {
        return IntStream.range(1, name.length())
                .allMatch(i -> edges.get(name.charAt(i - 1)).contains(name.charAt(i)));
    }

    @Override
    public String solvePart1(final List<String> inputs) {
        final Input input = Input.fromInput(inputs);
        return input.names().stream()
                .filter(name -> this.possible(name, input.edges()))
                .findFirst()
                .orElseThrow();
    }

    @Override
    public Integer solvePart2(final List<String> inputs) {
        final Input input = Input.fromInput(inputs);
        return IntStream.range(0, input.names().size())
                .filter(i -> this.possible(input.names().get(i), input.edges()))
                .map(i -> i + 1)
                .sum();
    }

    @Override
    public Integer solvePart3(final List<String> inputs) {
        final Input input = Input.fromInput(inputs);
        final Predicate<String> shortestPrefix =
                name ->
                        !input.names().stream()
                                .anyMatch(other -> !other.equals(name) && name.startsWith(other));
        final Counter cnt = new Counter(input.edges);
        return input.names().stream()
                .filter(shortestPrefix)
                .filter(name -> this.possible(name, input.edges()))
                .mapToInt(name -> cnt.count(name.charAt(name.length() - 1), name.length()))
                .sum();
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "Oroneth"),
        @Sample(method = "part2", input = TEST2, expected = "23"),
        @Sample(method = "part3", input = TEST3, expected = "25"),
        @Sample(method = "part3", input = TEST4, expected = "1154"),
    })
    public static void main(final String[] args) {
        create().run();
    }

    private static class Counter {
        private final Map<Character, Set<Character>> edges;
        private final Map<CacheKey, Integer> cache;

        public Counter(final Map<Character, Set<Character>> edges) {
            this.edges = edges;
            this.cache = new HashMap<>();
        }

        public int count(final Character chr, final int size) {
            return this.cache.computeIfAbsent(new CacheKey(chr, size), k -> doCount(chr, size));
        }

        private int doCount(final Character chr, final int size) {
            int cnt = 0;
            if (size >= MIN_SIZE) {
                cnt++;
            }
            if (size < MAX_SIZE && this.edges.containsKey(chr)) {
                cnt += this.edges.get(chr).stream().mapToInt(nxt -> doCount(nxt, size + 1)).sum();
            }
            return cnt;
        }

        private record CacheKey(Character chr, int size) {}
    }

    private record Input(List<String> names, Map<Character, Set<Character>> edges) {

        @SuppressWarnings("PMD.AvoidInstantiatingObjectsInLoops")
        public static Input fromInput(final List<String> inputs) {
            final List<String> names = Arrays.stream(inputs.getFirst().split(",")).toList();
            final Map<Character, Set<Character>> edges = new HashMap<>();
            for (int i = 2; i < inputs.size(); i++) {
                final StringSplit<String> split = StringUtils.splitOnce(inputs.get(i), " > ");
                final char key = split.left().charAt(0);
                Arrays.stream(split.right().split(","))
                        .map(s -> s.charAt(0))
                        .forEach(ch -> edges.computeIfAbsent(key, k -> new HashSet<>()).add(ch));
            }
            return new Input(names, edges);
        }
    }
}
