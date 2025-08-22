import importlib
from argparse import ArgumentParser

from ec.calendar import days
from ec.calendar import now
from ec.calendar import valid_year


class Runner:
    def run(self, year: int, quest: int) -> None:
        try:
            quest_mod = importlib.import_module(f"{year}_{quest:0>2}")
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
            help="Year and quest to run.",
        )
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="Run all quests",
        )
        args = parser.parse_args(main_args)
        if args.all:
            quests = list[tuple[int, int]]()
            year = now().year
            while valid_year(year):
                for day in days(year):
                    quests.append((year, day))
                year -= 1
            for year, quest in sorted(quests):
                self.run(year, quest)
        else:
            self.run(*args.quest)
