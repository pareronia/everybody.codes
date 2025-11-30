package com.github.pareronia.everybody_codes;

import static com.github.pareronia.everybody_codes.utils.IntegerSequence.Range.range;

import static java.util.stream.Collectors.toMap;
import static java.util.stream.Collectors.toSet;

import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.StringUtils;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Predicate;
import java.util.stream.Stream;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_18 extends SolutionBase<Long, Long, Long> {

    private static final String TEST1 =
            """
            Plant 1 with thickness 1:
            - free branch with thickness 1

            Plant 2 with thickness 1:
            - free branch with thickness 1

            Plant 3 with thickness 1:
            - free branch with thickness 1

            Plant 4 with thickness 17:
            - branch to Plant 1 with thickness 15
            - branch to Plant 2 with thickness 3

            Plant 5 with thickness 24:
            - branch to Plant 2 with thickness 11
            - branch to Plant 3 with thickness 13

            Plant 6 with thickness 15:
            - branch to Plant 3 with thickness 14

            Plant 7 with thickness 10:
            - branch to Plant 4 with thickness 15
            - branch to Plant 5 with thickness 21
            - branch to Plant 6 with thickness 34
            """;
    private static final String TEST2 =
            """
            Plant 1 with thickness 1:
            - free branch with thickness 1

            Plant 2 with thickness 1:
            - free branch with thickness 1

            Plant 3 with thickness 1:
            - free branch with thickness 1

            Plant 4 with thickness 10:
            - branch to Plant 1 with thickness -25
            - branch to Plant 2 with thickness 17
            - branch to Plant 3 with thickness 12

            Plant 5 with thickness 14:
            - branch to Plant 1 with thickness 14
            - branch to Plant 2 with thickness -26
            - branch to Plant 3 with thickness 15

            Plant 6 with thickness 150:
            - branch to Plant 4 with thickness 5
            - branch to Plant 5 with thickness 6


            1 0 1
            0 0 1
            0 1 1
            """;
    private static final String TEST3 =
            """
            Plant 1 with thickness 1:
            - free branch with thickness 1

            Plant 2 with thickness 1:
            - free branch with thickness 1

            Plant 3 with thickness 1:
            - free branch with thickness 1

            Plant 4 with thickness 1:
            - free branch with thickness 1

            Plant 5 with thickness 8:
            - branch to Plant 1 with thickness -8
            - branch to Plant 2 with thickness 11
            - branch to Plant 3 with thickness 13
            - branch to Plant 4 with thickness -7

            Plant 6 with thickness 7:
            - branch to Plant 1 with thickness 14
            - branch to Plant 2 with thickness -9
            - branch to Plant 3 with thickness 12
            - branch to Plant 4 with thickness 9

            Plant 7 with thickness 23:
            - branch to Plant 5 with thickness 17
            - branch to Plant 6 with thickness 18


            0 1 0 0
            0 1 0 1
            0 1 1 1
            1 1 0 1
            """;

    private Quest2025_18(final boolean debug) {
        super(debug);
    }

    public static Quest2025_18 create() {
        return new Quest2025_18(false);
    }

    public static Quest2025_18 createDebug() {
        return new Quest2025_18(true);
    }

    @Override
    public Long solvePart1(final List<String> input) {
        final Plants plants = Plants.fromInput(StringUtils.toBlocks(input));
        final Map<Integer, Boolean> leafOn =
                plants.getLeaves().stream().collect(toMap(Plant::pid, p -> true));
        return plants.energy(plants.getRoot(), leafOn);
    }

    @Override
    public Long solvePart2(final List<String> input) {
        final List<List<String>> blocks = StringUtils.toBlocks(input);
        final Plants plants = Plants.fromInput(blocks.subList(0, blocks.size() - 2));
        return blocks.getLast().stream().mapToLong(test -> test(plants, test)).sum();
    }

    @Override
    public Long solvePart3(final List<String> input) {
        final List<List<String>> blocks = StringUtils.toBlocks(input);
        final Plants plants = Plants.fromInput(blocks.subList(0, blocks.size() - 2));
        final Map<Integer, Boolean> bestOn =
                plants.getLeaves().stream()
                        .collect(toMap(Plant::pid, plants::isConnectedWithAtLeastThickness1));
        final long best = plants.energy(plants.getRoot(), bestOn);
        return solve3(blocks, plants, best);
    }

    public Long sample3(final List<String> input) {
        final List<List<String>> blocks = StringUtils.toBlocks(input);
        final Plants plants = Plants.fromInput(blocks.subList(0, blocks.size() - 2));
        final Set<Plant> leaves = plants.getLeaves();
        final long best =
                product(leaves.size())
                        .mapToLong(
                                lst -> {
                                    final Map<Integer, Boolean> bestOn = new HashMap<>();
                                    for (final Plant leaf : leaves) {
                                        bestOn.put(leaf.pid(), lst.get(leaf.pid() - 1));
                                    }
                                    return plants.energy(plants.getRoot(), bestOn);
                                })
                        .max()
                        .getAsLong();
        return solve3(blocks, plants, best);
    }

    private long test(final Plants plants, final String test) {
        final String[] split = test.split(" ");
        final Map<Integer, Boolean> leafOn =
                range(split.length).stream().collect(toMap(i -> i + 1, i -> "1".equals(split[i])));
        return plants.energy(plants.getRoot(), leafOn);
    }

    private Long solve3(final List<List<String>> blocks, final Plants plants, final long best) {
        return blocks.getLast().stream()
                .mapToLong(test -> test(plants, test))
                .filter(e -> e > 0)
                .map(e -> best - e)
                .sum();
    }

    @SuppressWarnings("PMD.AvoidLiteralsInIfCondition")
    private Stream<List<Boolean>> product(final int depth) {
        if (depth == 1) {
            return Stream.of(List.of(true), List.of(false));
        }
        final List<List<Boolean>> product = product(depth - 1).toList();
        return Set.of(true, false).stream()
                .flatMap(
                        b ->
                                product.stream()
                                        .map(
                                                lst -> {
                                                    final List<Boolean> ans = new ArrayList<>();
                                                    ans.add(b);
                                                    ans.addAll(lst);
                                                    return ans;
                                                }));
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "774"),
        @Sample(method = "part2", input = TEST2, expected = "324"),
        @Sample(method = "sample3", input = TEST3, expected = "946"),
    })
    public static void main(final String[] args) {
        create().run();
    }

    private record Plant(int pid, int threshold, Set<Connection> connections) {}

    private record Connection(Plant plant, int thickness) {}

    private record Plants(Map<Integer, Plant> plants) {

        @SuppressWarnings({
            "PMD.AvoidInstantiatingObjectsInLoops",
            "PMD.AvoidLiteralsInIfCondition"
        })
        public static Plants fromInput(final List<List<String>> blocks) {
            final Map<Integer, Plant> plants = new HashMap<>();
            for (final List<String> block : blocks) {
                final String[] splits1 = block.getFirst().replace(":", "").split(" ");
                final int pid = Integer.parseInt(splits1[1]);
                final int treshold = Integer.parseInt(splits1[4]);
                final Set<Connection> connections = new HashSet<>();
                for (int i = 1; i < block.size(); i++) {
                    final String[] splits2 = block.get(i).split(" ");
                    if ("free".equals(splits2[1])) {
                        continue;
                    }
                    final Plant dst = plants.get(Integer.parseInt(splits2[4]));
                    final int thickness = Integer.parseInt(splits2[7]);
                    connections.add(new Connection(dst, thickness));
                }
                plants.put(pid, new Plant(pid, treshold, Collections.unmodifiableSet(connections)));
            }
            return new Plants(plants);
        }

        public Plant getRoot() {
            return this.plants.get(
                    plants.keySet().stream().mapToInt(Integer::intValue).max().getAsInt());
        }

        public Set<Plant> getLeaves() {
            return this.plants.values().stream()
                    .filter(p -> p.connections.isEmpty())
                    .collect(toSet());
        }

        @SuppressWarnings("PMD.LongVariable")
        public boolean isConnectedWithAtLeastThickness1(final Plant plant) {
            final Predicate<Plant> areConnectedWithAtLeastThickness1 =
                    p ->
                            p.connections.stream()
                                    .anyMatch(c -> c.plant.equals(plant) && c.thickness > 0);
            return this.plants.values().stream().anyMatch(areConnectedWithAtLeastThickness1);
        }

        public long energy(final Plant root, final Map<Integer, Boolean> leafOn) {
            if (root.connections().isEmpty()) {
                return leafOn.get(root.pid) ? root.threshold : 0;
            }
            int energy = 0;
            for (final Connection connection : root.connections()) {
                energy += connection.thickness * energy(connection.plant, leafOn);
            }
            return energy >= root.threshold ? energy : 0;
        }
    }
}
