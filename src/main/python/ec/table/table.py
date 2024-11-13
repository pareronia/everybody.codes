import os


def get_py(year: int, day: int) -> str:
    path = os.path.join("src", "main", "python", f"{year}_{day:02}.py")
    return f"[✓]({path})" if os.path.exists(path) else ""


def main(file_name: str) -> None:
    url = "https://everybody.codes/event/2024/quests/"
    with open(file_name, "r") as f:
        tmp = f.read()
    with open(file_name, "w") as f:
        in_table = False
        for line in tmp.splitlines():
            if line.startswith("<!-- @BEGIN:Quests"):
                print(line, file=f)
                print("| Quest | python3 | ", file=f)
                print("| --- | --- |", file=f)
                for i in range(1, 21):
                    print(
                        f"|[{i}]({url}{i})|{get_py(2024, i)}|",
                        file=f,
                    )
                in_table = True
            elif line.startswith("<!-- @END:Quests"):
                in_table = False
                print(line, file=f)
            else:
                if not in_table:
                    print(line, file=f)


if __name__ == "__main__":
    main("README.md")
