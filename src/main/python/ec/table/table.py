from pathlib import Path

from ec.stats.stats import Part
from ec.stats.stats import PartStats
from ec.stats.stats import get_user_stats


def get_py(year: int, day: int) -> str:
    path = Path("src") / "main" / "python" / f"{year}_{day:02}.py"
    return f"[✓]({path})" if path.exists() else ""


def get_java(year: int, day: int) -> str:
    path = Path("src").joinpath(
        "main",
        "java",
        "com",
        "github",
        "pareronia",
        "everybody_codes",
        f"Quest{year}_{day:02}.java",
    )
    return f"[✓]({path})" if path.exists() else ""


def get_rank(stats: dict[Part, PartStats], year: int, day: int) -> str:
    return "&nbsp;/&nbsp;".join(
        str(stats[(year, day, p)].place).rjust(4).replace(" ", "&nbsp;")
        for p in range(1, 4)
    )


def get_points(stats: dict[Part, PartStats], year: int, day: int) -> str:
    scores = []
    for p in range(1, 4):
        s = stats[(year, day, p)].score
        scores.append("-" if s == 0 else str(s))
    return "&nbsp;/&nbsp;".join(
        scores[p].rjust(3).replace(" ", "&nbsp;") for p in range(3)
    )


def main(file_name: str) -> None:
    url = "https://everybody.codes/event/2024/quests/"
    with Path(file_name).open("r") as f:
        tmp = f.read()
    with Path(file_name).open("w") as f:
        in_table = False
        for line in tmp.splitlines():
            if line.startswith("<!-- @BEGIN:Quests"):
                in_table = True
                print(line, file=f)
                year = int(line.split("@")[1].split(":")[2])
                stats = get_user_stats(year)
                print("| Quest | python3 | java | Rank | Points |", file=f)
                print("| --- | --- | --- | --- | --- |", file=f)
                for day in range(1, 21):
                    if (year, day, 3) in stats:
                        py = get_py(year, day)
                        java = get_java(year, day)
                        rank = get_rank(stats, year, day)
                        points = get_points(stats, year, day)
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
