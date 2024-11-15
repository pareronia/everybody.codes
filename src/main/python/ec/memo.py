import json
import os
import sys

from ec.api import API


def get_everybody_codes_dir() -> str:
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
    if "EVERYBODY_CODES_TOKEN" in os.environ:
        return os.environ["EVERYBODY_CODES_TOKEN"]
    file = os.path.join(get_everybody_codes_dir(), "token")
    return read_lines_from_file(file)[0]


def get_user_id(token: str) -> str:
    file = os.path.join(get_everybody_codes_dir(), "token2id.json")
    with open(file, "r", encoding="utf-8") as f:
        ids = json.load(f)
    return str(ids[token])


def get_memo_dir() -> str:
    return os.path.join(get_everybody_codes_dir(), get_user_id(get_token()))


def get_part_string(part: int) -> str:
    if part not in {1, 2, 3}:
        raise ValueError("part should be 1, 2 or 3")
    return "a" if part == 1 else "b" if part == 2 else "c"


def get_input_file(year: int, day: int, part: int) -> str:
    p = get_part_string(part)
    return os.path.join(get_memo_dir(), f"{year}_{day:02}{p}_input.txt")


def download_input(year: int, day: int, part: int) -> str | None:
    return API(get_token()).get_input(year, day, part)


def get_input(year: int, day: int, part: int) -> tuple[str, ...] | None:
    file = get_input_file(year, day, part)
    if not os.path.exists(file):
        input = download_input(year, day, part)
        if input is not None:
            write_text_to_file(file, input)
            return tuple(_ for _ in input.splitlines())
        else:
            return None
    return tuple(_ for _ in read_lines_from_file(file))


def get_answer_file(year: int, day: int, part: int) -> str:
    p = get_part_string(part)
    return os.path.join(get_memo_dir(), f"{year}_{day:02}{p}_answer.txt")


def get_answer(year: int, day: int, part: int) -> str | None:
    file = get_answer_file(year, day, part)
    if not os.path.exists(file):
        return None
    lines = read_lines_from_file(file)
    if len(lines) == 0:
        return None
    return lines[0]


def get_title_file(year: int, day: int) -> str:
    return os.path.join(
        get_everybody_codes_dir(), "titles", f"{year}_{day:02}.txt"
    )


def download_title(year: int, day: int) -> str | None:
    return API(get_token()).get_title(year, day)


def get_title(year: int, day: int) -> str | None:
    file = get_title_file(year, day)
    if not os.path.exists(file):
        title = download_title(year, day)
        if title is not None:
            write_text_to_file(file, title)
        return title
    return read_lines_from_file(file)[0]


def read_lines_from_file(file: str) -> list[str]:
    with open(file, "r", encoding="utf-8") as f:
        data = f.read()
    return data.rstrip("\r\n").splitlines()


def write_text_to_file(file: str, text: str) -> None:
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, "w", encoding="utf-8") as f:
        f.write(text)
