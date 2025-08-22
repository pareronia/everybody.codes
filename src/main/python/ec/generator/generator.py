import shutil
from pathlib import Path
from string import Template


def main(args: list[str]) -> None:
    if len(args) != 2:
        msg = f"Usage: {__name__} <year> <day>"
        raise ValueError(msg)

    year = args[0]
    day = args[1]
    day2 = f"{args[1]:0>2}"
    template = Path("src") / "main" / "resources" / "generator" / "template.py"
    destination = Path("src") / "main" / "python" / f"{year}_{day2}.py"
    if destination.exists():
        print(f"'{destination}' already exists")
        return
    destination.parent.mkdir(exist_ok=True, parents=True)
    mappings = {"year": year, "day": day, "day2": day2}
    target = shutil.copyfile(template, destination)
    with target.open("r", encoding="utf-8") as f:
        t = Template(f.read())
        s = t.substitute(mappings)
    with target.open("w", encoding="utf-8") as f:
        f.write(s)
    print(f"Generated '{target}'")
    return


if __name__ == "__main__":
    main(["2024", "12"])
