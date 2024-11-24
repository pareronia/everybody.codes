from __future__ import annotations

import argparse
import os
import time
from abc import ABC
from abc import abstractmethod
from enum import Enum
from enum import unique
from typing import Any
from typing import Callable
from typing import Generic
from typing import Iterator
from typing import NamedTuple
from typing import TypeVar
from typing import cast

from prettyprinter import cpprint

from . import is_released
from .api import API
from .api import SubmitResponseFormatter
from .memo import get_answer as memo_get_answer
from .memo import get_input as memo_get_input
from .memo import get_title as memo_get_title
from .memo import get_token as memo_get_token


def clog(c: Callable[[], object]) -> None:
    if __debug__:
        log(c())


def log(msg: object) -> None:
    if __debug__:
        cpprint(msg)


class Quest:
    def __init__(self, year: int, day: int):
        self.year = year
        self.day = day

    def is_released(self) -> bool:
        return is_released(self.year, self.day)

    def get_title(self) -> str | None:
        return memo_get_title(self.year, self.day)

    def get_input(self, part: int) -> tuple[str, ...] | None:
        return memo_get_input(self.year, self.day, part)

    def get_answer(self, part: int) -> str | None:
        return memo_get_answer(self.year, self.day, part)


InputData = tuple[str, ...]
OUTPUT1 = TypeVar("OUTPUT1", bound=str | int)
OUTPUT2 = TypeVar("OUTPUT2", bound=str | int)
OUTPUT3 = TypeVar("OUTPUT3", bound=str | int)


class SolutionBase(ABC, Generic[OUTPUT1, OUTPUT2, OUTPUT3]):
    @unique
    class Part(Enum):

        PART_1 = "1"
        PART_2 = "2"
        PART_3 = "3"

        def __str__(self) -> str:
            return str(self._value_)

        def int_value(self) -> int:
            return int(self._value_)

        @classmethod
        def from_str(cls, part: str) -> SolutionBase.Part:
            for v in SolutionBase.Part:
                if v._value_ == part:
                    return v
            raise ValueError

    class PartExecution(NamedTuple):
        part: SolutionBase.Part
        answer: Any = None
        duration: int = 0
        no_input: bool = False

        @property
        def duration_as_ms(self) -> float:
            return self.duration / 1_000_000

        def __repr__(self) -> str:
            if self.no_input:
                return f"Part {self.part}: == NO INPUT FOUND =="
            return (
                f"Part {self.part}:"
                f" {self.answer}, took {self.duration_as_ms:.3f} ms"
            )

    def __init__(self, year: int, day: int):
        self.quest = Quest(year, day)
        self.callables = {"1": self.part_1, "2": self.part_2, "3": self.part_3}

    @abstractmethod
    def samples(self) -> None:
        pass

    @abstractmethod
    def part_1(self, input: InputData) -> OUTPUT1:
        pass

    @abstractmethod
    def part_2(self, input: InputData) -> OUTPUT2:
        pass

    @abstractmethod
    def part_3(self, input: InputData) -> OUTPUT3:
        pass

    def run(self, main_args: list[str]) -> None:  # noqa E103
        def execute_part(
            part: SolutionBase.Part, f: Callable[[InputData], Any]
        ) -> SolutionBase.PartExecution:
            input = self.quest.get_input(part.int_value())
            if input is None:
                result = SolutionBase.PartExecution(part, no_input=True)
            else:
                start = time.time()
                answer = f(input)
                result = SolutionBase.PartExecution(
                    part, answer, int((time.time() - start) * 1e9)
                )
            print(result)
            return result

        def check_answer(exec_part: SolutionBase.PartExecution) -> str:
            expected = self.quest.get_answer(exec_part.part.int_value())
            answer = exec_part.answer
            if (
                expected is not None
                and answer is not None
                and expected != str(answer)
            ):
                return (
                    f"Part {exec_part.part}:"
                    + f" Expected: '{expected}', got: '{answer}'"
                )
            return ""

        def submit_answer(exec_part: SolutionBase.PartExecution) -> None:
            part = exec_part.part.int_value()
            if self.quest.get_answer(part) is not None:
                print()
                print(f"*** Part {part}: already submitted ***")
                return
            token = memo_get_token()
            response = API(token).submit_answer(
                self.quest.year,
                self.quest.day,
                part,
                exec_part.answer,
            )
            for line in SubmitResponseFormatter.format(response):
                print(line)

        header = f"everybody.codes {self.quest.year} Quest {self.quest.day}"
        if not self.quest.is_released():
            print()
            print(f"{header}: == Quest not available yet ==")
            print()
            return
        title = self.quest.get_title()
        print()
        print(header + ("" if title is None else f": {title}"))
        print()

        if __debug__:
            self.samples()
        exec_parts = [
            execute_part(self.Part.from_str(part), self.callables[part])
            for part in ["1", "2", "3"]
        ]
        fails = [check_answer(exec_part) for exec_part in exec_parts]
        message = os.linesep.join(fails)
        if message.strip() != "":
            raise ValueError(os.linesep + message)
        if len(main_args) <= 1:
            return
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-s", "--submit", action="store_true", dest="submit"
        )
        args = parser.parse_args(main_args[1:])
        if args.submit:
            for part in range(3):
                submit_answer(exec_parts[part])


F = TypeVar("F", bound=Callable[..., Any])


def ec_samples(tests: tuple[tuple[str, str, Any], ...]) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        def wrapper(*args: Any) -> Any:
            _self = args[0]
            for test in tests:
                func, _, expected = test
                input_data = tuple(_ for _ in test[1].splitlines())
                actual = getattr(_self, func)(input_data)
                message = (
                    f"FAILED '{func}'. Expected: '{expected}', was: '{actual}'"
                )
                assert actual == expected, message

        return cast(F, wrapper)

    return decorator


@unique
class Direction(Enum):
    x: int
    y: int

    def __new__(cls, x: int, y: int) -> Direction:
        obj = object.__new__(cls)
        obj.x = x
        obj.y = y
        return obj

    UP = (0, 1)
    RIGHT_AND_UP = (1, 1)
    RIGHT = (1, 0)
    RIGHT_AND_DOWN = (1, -1)
    DOWN = (0, -1)
    LEFT_AND_DOWN = (-1, -1)
    LEFT = (-1, 0)
    LEFT_AND_UP = (-1, 1)

    @classmethod
    def capitals(cls) -> set[Direction]:
        return {
            Direction.UP,
            Direction.RIGHT,
            Direction.DOWN,
            Direction.LEFT,
        }

    @classmethod
    def octants(cls) -> set[Direction]:
        return {
            Direction.UP,
            Direction.RIGHT_AND_UP,
            Direction.RIGHT,
            Direction.RIGHT_AND_DOWN,
            Direction.DOWN,
            Direction.LEFT_AND_DOWN,
            Direction.LEFT,
            Direction.LEFT_AND_UP,
        }


@unique
class Direction3D(Enum):
    x: int
    y: int
    z: int
    letter: str

    def __new__(cls, x: int, y: int, z: int, letter: str) -> Direction3D:
        obj = object.__new__(cls)
        obj.x = x
        obj.y = y
        obj.z = z
        obj.letter = letter
        return obj

    UP = (0, 1, 0, "U")
    RIGHT = (1, 0, 0, "R")
    DOWN = (0, -1, 0, "D")
    LEFT = (-1, 0, 0, "L")
    FORWARD = (0, 0, -1, "F")
    BACK = (0, 0, 1, "B")

    @classmethod
    def from_str(cls, s: str) -> Direction3D:
        for v in Direction3D:
            if v.letter is not None and v.letter == s:
                return v
        raise ValueError

    @classmethod
    def capitals(cls) -> set[Direction3D]:
        return {
            Direction3D.UP,
            Direction3D.RIGHT,
            Direction3D.DOWN,
            Direction3D.LEFT,
            Direction3D.FORWARD,
            Direction3D.BACK,
        }


class Cell(NamedTuple):
    row: int
    col: int

    def at(self, direction: Direction) -> Cell:
        return Cell(self.row - direction.y, self.col + direction.x)

    def get_capital_neighbours(self) -> Iterator[Cell]:
        return (self.at(d) for d in Direction.capitals())


class Position(NamedTuple):
    x: int
    y: int

    def at(self, direction: Direction) -> Position:
        return Position(self.x + direction.x, self.y + direction.y)


class Position3D(NamedTuple):
    x: int
    y: int
    z: int

    def at(self, direction: Direction3D) -> Position3D:
        return Position3D(
            self.x + direction.x, self.y + direction.y, self.z + direction.z
        )
