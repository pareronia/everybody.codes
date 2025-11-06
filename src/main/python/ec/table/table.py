from pathlib import Path

from ec import calendar
from ec.stats.stats import Part
from ec.stats.stats import PartStats
from ec.stats.stats import get_user_stats


def get_py(event: int, day: int) -> str:
    py = (
        f"S{event:02}_{day:02}.py"
        if calendar.valid_story(event)
        else f"{event}_{day:02}.py"
    )
    path = Path("src") / "main" / "python" / py
    return f"[✓]({path})" if path.exists() else ""


def get_java(event: int, day: int) -> str:
    java = (
        f"S{event:02}_{day:02}.java"
        if calendar.valid_story(event)
        else f"Quest{event}_{day:02}.java"
    )
    path = Path("src").joinpath(
        "main", "java", "com", "github", "pareronia", "everybody_codes", java
    )
    return f"[✓]({path})" if path.exists() else ""


def get_rank(stats: dict[Part, PartStats], event: int, day: int) -> str:
    return "&nbsp;/&nbsp;".join(
        str(stats[(event, day, p)].place).rjust(4).replace(" ", "&nbsp;")
        for p in range(1, 4)
    )


def get_points(stats: dict[Part, PartStats], event: int, day: int) -> str:
    scores = []
    for p in range(1, 4):
        s = stats[(event, day, p)].score
        scores.append("-" if s == 0 else str(s))
    return "&nbsp;/&nbsp;".join(
        scores[p].rjust(3).replace(" ", "&nbsp;") for p in range(3)
    )


def main(file_name: str) -> None:
    with Path(file_name).open("r") as f:
        tmp = f.read()
    with Path(file_name).open("w") as f:
        in_table = False
        for line in tmp.splitlines():
            if line.startswith("<!-- @BEGIN:Quests"):
                in_table = True
                print(line, file=f)
                event = int(line.split("@")[1].split(":")[2])
                url = (
                    f"https://everybody.codes/event/{event}/quests/"
                    if calendar.valid_year(event)
                    else f"https://everybody.codes/story/{event}/quests/"
                )
                stats = get_user_stats(event)
                print("| Quest | python3 | java | Rank | Points |", file=f)
                print("| --- | :---: | :---: | --- | --- |", file=f)
                days = 3 if calendar.valid_story(event) else 20
                for day in range(1, days + 1):
                    if (event, day, 3) in stats:
                        py = get_py(event, day)
                        java = get_java(event, day)
                        rank = get_rank(stats, event, day)
                        points = get_points(stats, event, day)
                    else:
                        py, java, rank, points = "", "", "", ""
                    row = f"|[{day}]({url}{day})|{py}|{java}|{rank}|{points}|"
                    print(row, file=f)
            elif line.startswith("<!-- @END:Quests"):
                in_table = False
                print(line, file=f)
            elif not in_table:
                print(line, file=f)


if __name__ == "__main__":
    main("README.md")
