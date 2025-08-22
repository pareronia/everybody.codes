import json
import os
import sys
from pathlib import Path

from . import EVERYBODY_CODES_DIR
from . import EVERYBODY_CODES_TOKEN
from .api import API


def get_everybody_codes_dir() -> Path:
    if EVERYBODY_CODES_DIR in os.environ:
        return Path(os.environ[EVERYBODY_CODES_DIR])
    if sys.platform.startswith("win"):
        return Path(os.environ["APPDATA"]) / "everybody.codes"
    if sys.platform.startswith("linux"):
        return Path(os.environ["HOME"]) / ".config" / "everybody.codes"
    msg = "OS not supported"
    raise RuntimeError(msg)


def get_token() -> str:
    if EVERYBODY_CODES_TOKEN in os.environ:
        return os.environ[EVERYBODY_CODES_TOKEN]
    file = get_everybody_codes_dir() / "token"
    return read_lines_from_file(file)[0]


def get_user_id(token: str) -> str:
    file = get_everybody_codes_dir() / "token2id.json"
    with file.open("r", encoding="utf-8") as f:
        ids = json.load(f)
    return str(ids[token])


def get_memo_dir() -> Path:
    return get_everybody_codes_dir() / get_user_id(get_token())


def get_part_string(part: int) -> str:
    if part not in {1, 2, 3}:
        msg = "part should be 1, 2 or 3"
        raise ValueError(msg)
    return "a" if part == 1 else "b" if part == 2 else "c"


def get_input_file(year: int, day: int, part: int) -> Path:
    p = get_part_string(part)
    return get_memo_dir() / f"{year}_{day:02}{p}_input.txt"


def download_input(year: int, day: int, part: int) -> str | None:
    return API(get_token()).get_input(year, day, part)


def get_input(year: int, day: int, part: int) -> tuple[str, ...] | None:
    file = get_input_file(year, day, part)
    if not file.exists():
        input_data = download_input(year, day, part)
        if input_data is None:
            return None
        write_text_to_file(file, input_data)
    return tuple(_ for _ in read_lines_from_file(file))


def get_answer_file(year: int, day: int, part: int) -> Path:
    p = get_part_string(part)
    return get_memo_dir() / f"{year}_{day:02}{p}_answer.txt"


def download_answer(year: int, day: int, part: int) -> str | None:
    return API(get_token()).get_answer(year, day, part)


def get_answer(year: int, day: int, part: int) -> str | None:
    file = get_answer_file(year, day, part)
    if not file.exists():
        answer = download_answer(year, day, part)
        if answer is None:
            return None
        write_text_to_file(file, answer)
    lines = read_lines_from_file(file)
    if len(lines) == 0:
        return None
    return lines[0]


def get_title_file(year: int, day: int) -> Path:
    return get_everybody_codes_dir() / "titles" / f"{year}_{day:02}.txt"


def download_title(year: int, day: int) -> str | None:
    return API(get_token()).get_title(year, day)


def get_title(year: int, day: int) -> str | None:
    file = get_title_file(year, day)
    if not file.exists():
        title = download_title(year, day)
        if title is None:
            return None
        write_text_to_file(file, title)
    return read_lines_from_file(file)[0]


def read_lines_from_file(file: Path) -> list[str]:
    with file.open("r", encoding="utf-8") as f:
        data = f.read()
    return data.rstrip("\r\n").splitlines()


def write_text_to_file(file: Path, text: str) -> None:
    file.parent.mkdir(exist_ok=True)
    with file.open("w", encoding="utf-8") as f:
        f.write(text)
