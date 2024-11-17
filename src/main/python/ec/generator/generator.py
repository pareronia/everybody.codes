import os
import shutil
from string import Template


def main(args: list[str]) -> None:
    if len(args) != 2:
        raise ValueError(f"Usage: {__name__} <year> <day>")

    year = args[0]
    day = args[1]
    day2 = f"{args[1]:0>2}"
    template = os.path.join(
        "src", "main", "resources", "generator", "template.py"
    )
    destination = os.path.join("src", "main", "python", f"{year}_{day2}.py")
    if os.path.exists(destination):
        print(f"'{destination}' already exists")
        return
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    mappings = {"year": year, "day": day, "day2": day2}
    target = shutil.copyfile(template, destination)
    with open(target, "r", encoding="utf-8") as f:
        t = Template(f.read())
        s = t.substitute(mappings)
    with open(target, "w", encoding="utf-8") as f:
        f.write(s)
    print(f"Generated '{target}'")
    return


if __name__ == "__main__":
    main(["2024", "12"])
