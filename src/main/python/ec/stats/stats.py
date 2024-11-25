from datetime import timedelta
from typing import NamedTuple

from ..api import API
from ..memo import get_title as memo_get_title
from ..memo import get_token as memo_get_token

Part = tuple[int, int, int]


class PartStats(NamedTuple):
    year: int
    day: int
    part: int
    global_time: int
    local_time: int
    place: int
    score: int

    @property
    def global_timedelta(self) -> timedelta:
        return timedelta(microseconds=self.global_time * 1000)

    @property
    def global_timedelta_str(self) -> str:
        t = self.global_timedelta
        hours = t.seconds // 3600
        minutes = (t.seconds - hours * 3600) // 60
        if t.days > 0:
            return f"{t.days:3}d {hours:2}:{minutes:02}"
        else:
            return f"{hours:2}:{minutes:02}".rjust(10)


class QuestStats(NamedTuple):
    year: int
    day: int
    completed_1: int
    completed_2: int
    completed_3: int


def get_user_stats(year: int) -> dict[Part, PartStats]:
    stats = API(memo_get_token()).get_user_stats(year)
    ans = dict[Part, PartStats]()
    for quest in stats:
        for part in stats[quest]:
            ans[(year, quest, part)] = PartStats(
                year=year,
                day=quest,
                part=part,
                global_time=stats[quest][part]["time"],
                local_time=stats[quest][part]["localTime"],
                place=stats[quest][part]["globalPlace"],
                score=stats[quest][part]["globalScore"],
            )
    return ans


def get_quest_stats(year: int) -> dict[int, QuestStats]:
    stats = API(memo_get_token()).get_quest_stats(year)
    ans = dict[int, QuestStats]()
    for quest in stats:
        ans[quest] = QuestStats(
            year=year,
            day=quest,
            completed_1=stats[quest]["p1"],
            completed_2=stats[quest]["p2"],
            completed_3=stats[quest]["p3"],
        )
    return ans


def main(args: list[str]) -> None:
    if len(args) == 1:
        print_year(int(args[0]))


def print_year(year: int) -> None:
    user_stats = get_user_stats(year)
    quest_stats = get_quest_stats(year)
    finished = f"{len(user_stats)}/60"
    total = sum(s.score for s in user_stats.values())
    wd, wp, ws = 34, 23, 15

    def headers() -> str:
        ans = "".join(f"   ------ Part {i} ------" for i in range(1, 4))
        assert len(ans) == 3 * wp
        return ans

    def time(day: int, part: int) -> str:
        return (
            user_stats[(year, day, part)].global_timedelta_str
            if (year, day, part) in user_stats
            else "--:--"
        )

    def rank(day: int, part: int) -> str:
        return (
            (
                str(user_stats[(year, day, part)].place)
                if (year, day, part) in user_stats
                else "-"
            ).rjust(4)
            + "/"
            + str(getattr(quest_stats[day], "completed_" + str(part))).rjust(4)
        )

    def score(day: int, part: int) -> str:
        return (
            str(user_stats[(year, day, part)].score)
            if (year, day, part) in user_stats
            else "-"
        )

    print("".ljust(wd) + headers())
    print()
    days = {d for _, d, _ in user_stats.keys()}
    for day in sorted(days):
        day_title = memo_get_title(year, day)
        title = f"{day:2} {day_title}".ljust(wd - 1)[: wd - 1] + ":"
        parts = "".join(
            (f"{time(day, p)} {rank(day, p)}").rjust(wp) for p in range(1, 4)
        )
        scores = "/".join(score(day, p).rjust(3) for p in range(1, 4)).rjust(
            ws
        )
        assert len(title) + len(parts) + len(scores) == wd + 3 * wp + ws
        print(title + parts + scores)
    print()
    print("-" * wd + " " * 3 * wp + " " + "-" * (ws - 1))
    print(finished.rjust(wd) + str(total).rjust(3 * wp + ws))
