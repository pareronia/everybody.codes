import os
import sys


def get_memo_dir() -> str:
    if "EVERYBODY_CODES_DIR" in os.environ:
        return os.environ["EVERYBODY_CODES_DIR"]
    else:
        if sys.platform.startswith("win"):
            return os.path.join(os.environ["APPDATA"], "everybody.codes")
        elif sys.platform.startswith("linux"):
            return os.path.join(
                os.environ["HOME"], ".config", "everybody.codes"
            )
        else:
            raise RuntimeError("OS not supported")


def get_token() -> str:
    file = os.path.join(get_memo_dir(), "token")
    return read_lines_from_file(file)[0]


def get_part_string(part: int) -> str:
    if part not in {1, 2, 3}:
        raise ValueError("part should be 1, 2 or 3")
    return "a" if part == 1 else "b" if part == 2 else "c"


def get_input_file(year: int, day: int, part: int) -> str:
    p = get_part_string(part)
    return os.path.join(
        get_memo_dir(),
        get_token(),
        f"{year}_{day:02}{p}_input.txt",
    )


def get_input(year: int, day: int, part: int) -> tuple[str, ...]:
    return tuple(
        _ for _ in read_lines_from_file(get_input_file(year, day, part))
    )


def get_answer_file(year: int, day: int, part: int) -> str:
    p = get_part_string(part)
    return os.path.join(
        get_memo_dir(),
        get_token(),
        f"{year}_{day:02}{p}_answer.txt",
    )


def get_answer(year: int, day: int, part: int) -> str | None:
    f = get_answer_file(year, day, part)
    if not os.path.exists(f):
        return None
    lines = read_lines_from_file(f)
    if len(lines) == 0:
        return None
    return lines[0]


def read_lines_from_file(file: str) -> list[str]:
    with open(file, "r", encoding="utf-8") as f:
        data = f.read()
    return data.rstrip("\r\n").splitlines()
