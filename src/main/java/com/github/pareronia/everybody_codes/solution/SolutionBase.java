package com.github.pareronia.everybody_codes.solution;

import com.github.pareronia.everybody_codes.utils.StringUtils;
import com.github.pareronia.everybody_codes.utils.StringUtils.StringSplit;

import java.util.List;

@SuppressWarnings("PMD.TypeParameterNamingConventions")
public abstract class SolutionBase<Output1, Output2, Output3> implements LoggerEnabled {

    protected final boolean debug;
    protected final Logger logger;
    protected final Quest quest;

    protected SolutionBase(final boolean debug) {
        this.debug = debug;
        this.logger = new Logger(debug);
        this.quest = createQuest();
    }

    private Quest createQuest() {
        final String nums = this.getClass().getSimpleName().substring("Quest".length());
        final StringSplit<Integer> split = StringUtils.splitOnceToInt(nums, "_");
        return Quest.create(split.left(), split.right());
    }

    protected abstract Output1 solvePart1(List<String> input);

    protected abstract Output2 solvePart2(List<String> input);

    protected abstract Output3 solvePart3(List<String> input);

    @SuppressWarnings("PMD.EmptyMethodInAbstractClassShouldBeAbstract")
    protected void samples() {
        // nop
    }

    protected void run() {
        SolutionUtils.runSamples(this.getClass());

        this.samples();

        final List<String> input1 = quest.getInput(1);
        final Output1 answer1 = SolutionUtils.lap("Part 1", () -> this.solvePart1(input1));
        final List<String> input2 = quest.getInput(2);
        final Output2 answer2 = SolutionUtils.lap("Part 2", () -> this.solvePart2(input2));
        final List<String> input3 = quest.getInput(3);
        final Output3 answer3 = SolutionUtils.lap("Part 3", () -> this.solvePart3(input3));

        quest.check(answer1, answer2, answer3);
    }

    public Output1 part1(final List<String> input) {
        return this.solvePart1(input);
    }

    public Output2 part2(final List<String> input) {
        return this.solvePart2(input);
    }

    public Output3 part3(final List<String> input) {
        return this.solvePart3(input);
    }

    @Override
    public Logger getLogger() {
        return this.logger;
    }
}
