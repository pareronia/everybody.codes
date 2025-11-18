package com.github.pareronia.everybody_codes;

import static java.util.Comparator.comparing;

import com.github.pareronia.everybody_codes.graph.BFS;
import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;
import com.github.pareronia.everybody_codes.utils.IntegerSequence.Range;
import com.github.pareronia.everybody_codes.utils.StringUtils;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_09 extends SolutionBase<Integer, Integer, Integer> {

    private static final String TEST1 =
            """
            1:CAAGCGCTAAGTTCGCTGGATGTGTGCCCGCG
            2:CTTGAATTGGGCCGTTTACCTGGTTTAACCAT
            3:CTAGCGCTGAGCTGGCTGCCTGGTTGACCGCG
            """;
    private static final String TEST2 =
            """
            1:GCAGGCGAGTATGATACCCGGCTAGCCACCCC
            2:TCTCGCGAGGATATTACTGGGCCAGACCCCCC
            3:GGTGGAACATTCGAAAGTTGCATAGGGTGGTG
            4:GCTCGCGAGTATATTACCGAACCAGCCCCTCA
            5:GCAGCTTAGTATGACCGCCAAATCGCGACTCA
            6:AGTGGAACCTTGGATAGTCTCATATAGCGGCA
            7:GGCGTAATAATCGGATGCTGCAGAGGCTGCTG
            """;
    private static final String TEST3 =
            """
            1:GCAGGCGAGTATGATACCCGGCTAGCCACCCC
            2:TCTCGCGAGGATATTACTGGGCCAGACCCCCC
            3:GGTGGAACATTCGAAAGTTGCATAGGGTGGTG
            4:GCTCGCGAGTATATTACCGAACCAGCCCCTCA
            5:GCAGCTTAGTATGACCGCCAAATCGCGACTCA
            6:AGTGGAACCTTGGATAGTCTCATATAGCGGCA
            7:GGCGTAATAATCGGATGCTGCAGAGGCTGCTG
            8:GGCGTAAAGTATGGATGCTGGCTAGGCACCCG
            """;

    private Quest2025_09(final boolean debug) {
        super(debug);
    }

    public static Quest2025_09 create() {
        return new Quest2025_09(false);
    }

    public static Quest2025_09 createDebug() {
        return new Quest2025_09(true);
    }

    private boolean isChild(final String child, final String parent1, final String parent2) {
        for (int i = 0; i < child.length(); i++) {
            final char chr = child.charAt(i);
            if (chr != parent1.charAt(i) && chr != parent2.charAt(i)) {
                return false;
            }
        }
        return true;
    }

    private int similarity(final String dna1, final String dna2, final String dna3) {
        final String child;
        final String parent1;
        final String parent2;
        if (this.isChild(dna1, dna2, dna3)) {
            child = dna1;
            parent1 = dna2;
            parent2 = dna3;
        } else if (this.isChild(dna2, dna1, dna3)) {
            child = dna2;
            parent1 = dna1;
            parent2 = dna3;
        } else if (this.isChild(dna3, dna1, dna2)) {
            child = dna3;
            parent1 = dna1;
            parent2 = dna2;
        } else {
            return 0;
        }
        int ans1 = 0;
        int ans2 = 0;
        for (int j = 0; j < child.length(); j++) {
            final char chr = child.charAt(j);
            ans1 += chr == parent1.charAt(j) ? 1 : 0;
            ans2 += chr == parent2.charAt(j) ? 1 : 0;
        }
        return ans1 * ans2;
    }

    @Override
    public Integer solvePart1(final List<String> input) {
        final List<String> dnas =
                input.stream().map(s -> StringUtils.splitOnce(s, ":").right()).toList();
        return this.similarity(dnas.get(0), dnas.get(1), dnas.get(2));
    }

    @Override
    public Integer solvePart2(final List<String> input) {
        final List<String> dnas =
                input.stream().map(s -> StringUtils.splitOnce(s, ":").right()).toList();
        int ans = 0;
        for (int i = 0; i < input.size(); i++) {
            for (int j = i + 1; j < input.size(); j++) {
                for (int k = j + 1; k < input.size(); k++) {
                    ans += this.similarity(dnas.get(i), dnas.get(j), dnas.get(k));
                }
            }
        }
        return ans;
    }

    @Override
    @SuppressWarnings("PMD.AvoidInstantiatingObjectsInLoops")
    public Integer solvePart3(final List<String> input) {
        final List<String> dnas =
                input.stream().map(s -> StringUtils.splitOnce(s, ":").right()).toList();
        final Map<Integer, Set<Integer>> edges = new HashMap<>();
        final int[] children = Range.range(dnas.size()).toArray();
        for (int i = 0; i < dnas.size(); i++) {
            for (int j = i + 1; j < dnas.size(); j++) {
                for (int k = j + 1; k < dnas.size(); k++) {
                    final int cid;
                    final int pid1;
                    final int pid2;
                    final String dnaI = dnas.get(i);
                    final String dnaJ = dnas.get(j);
                    final String dnaK = dnas.get(k);
                    if (children[i] != 1 && this.isChild(dnaI, dnaJ, dnaK)) {
                        children[i] = 1;
                        cid = i;
                        pid1 = j;
                        pid2 = k;
                    } else if (children[j] != 1 && this.isChild(dnaJ, dnaI, dnaK)) {
                        children[j] = 1;
                        cid = j;
                        pid1 = i;
                        pid2 = k;
                    } else if (children[k] != 1 && this.isChild(dnaK, dnaI, dnaJ)) {
                        children[k] = 1;
                        cid = k;
                        pid1 = i;
                        pid2 = j;
                    } else {
                        continue;
                    }
                    edges.computeIfAbsent(cid, x -> new HashSet<>()).addAll(List.of(pid1, pid2));
                    edges.computeIfAbsent(pid1, x -> new HashSet<>()).add(cid);
                    edges.computeIfAbsent(pid2, x -> new HashSet<>()).add(cid);
                }
            }
        }

        final List<Set<Integer>> components =
                BFS.connectedComponents(edges.keySet(), node -> edges.get(node).stream());
        components.sort(comparing(Set::size));
        return components.getLast().stream().mapToInt(i -> i + 1).sum();
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "414"),
        @Sample(method = "part2", input = TEST2, expected = "1245"),
        @Sample(method = "part3", input = TEST2, expected = "12"),
        @Sample(method = "part3", input = TEST3, expected = "36"),
    })
    public static void main(final String[] args) {
        create().run();
    }
}
