package com.github.pareronia.everybody_codes;

import com.github.pareronia.everybody_codes.geometry.Direction;
import com.github.pareronia.everybody_codes.solution.Sample;
import com.github.pareronia.everybody_codes.solution.Samples;
import com.github.pareronia.everybody_codes.solution.SolutionBase;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@SuppressWarnings("PMD.ClassNamingConventions")
public final class Quest2025_01 extends SolutionBase<String, String, String> {

    private static final String TEST1 =
            """
            Vyrdax,Drakzyph,Fyrryn,Elarzris

            R3,L2,R3,L1
            """;
    private static final String TEST2 =
            """
            Vyrdax,Drakzyph,Fyrryn,Elarzris

            R3,L2,R3,L3
            """;

    private Quest2025_01(final boolean debug) {
        super(debug);
    }

    public static Quest2025_01 create() {
        return new Quest2025_01(false);
    }

    public static Quest2025_01 createDebug() {
        return new Quest2025_01(true);
    }

    @Override
    public String solvePart1(final List<String> inputs) {
        final Input input = Input.fromInput(inputs);
        final int pos =
                input.moves().stream()
                        .map(move -> (move.direction() == Direction.RIGHT ? 1 : -1) * move.amount())
                        .reduce(
                                0,
                                (acc, amt) ->
                                        Math.min(Math.max(acc + amt, 0), input.names().size() - 1));
        return input.names().get(pos);
    }

    @Override
    public String solvePart2(final List<String> inputs) {
        final Input input = Input.fromInput(inputs);
        final int size = input.names().size();
        final int pos =
                input.moves().stream()
                        .map(move -> (move.direction() == Direction.RIGHT ? 1 : -1) * move.amount())
                        .reduce(0, (acc, amt) -> (acc + amt) % size);
        return input.names().get((size + pos) % size);
    }

    @Override
    public String solvePart3(final List<String> inputs) {
        final Input input = Input.fromInput(inputs);
        final List<String> names = new ArrayList<>(input.names());
        final int size = names.size();
        for (final Input.Move move : input.moves()) {
            final int amount = (move.direction() == Direction.RIGHT ? 1 : -1) * move.amount();
            final int swp = (size + (amount % size)) % size;
            final String tmp = names.get(swp);
            names.set(swp, names.get(0));
            names.set(0, tmp);
        }
        return names.getFirst();
    }

    @Samples({
        @Sample(method = "part1", input = TEST1, expected = "Fyrryn"),
        @Sample(method = "part2", input = TEST1, expected = "Elarzris"),
        @Sample(method = "part3", input = TEST2, expected = "Drakzyph")
    })
    public static void main(final String[] args) {
        create().run();
    }

    private record Input(List<String> names, List<Move> moves) {

        public static Input fromInput(final List<String> strings) {
            return new Input(
                    Arrays.stream(strings.get(0).split(",")).toList(),
                    Arrays.stream(strings.get(2).split(",")).map(Move::fromInput).toList());
        }

        private record Move(Direction direction, int amount) {

            public static Move fromInput(final String string) {
                return new Move(
                        Direction.fromChar(string.charAt(0)),
                        Integer.parseInt(string.substring(1)));
            }
        }
    }
}
