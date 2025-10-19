import importlib
from argparse import ArgumentParser

from ec import calendar


class Runner:
    def run(self, event: str, quest: int) -> None:
        try:
            quest_mod = importlib.import_module(f"{event}_{quest:0>2}")
            quest_mod.solution.run([])
        except ModuleNotFoundError:
            return

    def main(self, main_args: list[str]) -> None:
        parser = ArgumentParser(
            prog="everybody.codes",
            description="i18n-puzzles Puzzle runner",
        )
        parser.add_argument(
            "-q",
            "--quest",
            type=int,
            nargs=2,
            help="Year/Story and quest to run.",
        )
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="Run all quests",
        )
        args = parser.parse_args(main_args)
        if args.all:
            quests = list[tuple[str, int]]()
            year = calendar.now().year
            while calendar.valid_year(year):
                for day in calendar.days(year):
                    quests.append((str(year), day))
                year -= 1
            story = 1
            while calendar.valid_story(story):
                quests.append((f"S{story:0>2}", day))
                story += 1
            for event, quest in sorted(quests):
                self.run(event, quest)
        elif calendar.valid_year(args.quest[0]):
            self.run(str(args.quest[0]), args.quest[1])
        elif calendar.valid_story(args.quest[0]):
            self.run(f"S{args.quest[0]:0>2}", args.quest[1])
