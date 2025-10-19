from __future__ import annotations  # noqa:I001

import argparse
import os
import time
from abc import ABC
from abc import abstractmethod
from collections.abc import Callable
from collections.abc import Iterator
from enum import Enum
from enum import unique
from typing import Any
from typing import NamedTuple
from typing import Self
from typing import TypeVar
from typing import cast

import prettyprinter
from ec import calendar
from prettyprinter import cpprint
from termcolor import colored

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
    def __init__(self, event: int, day: int) -> None:
        self.event = event
        self.day = day

    def is_released(self) -> bool:
        return calendar.is_released(self.event, self.day)

    def get_title(self) -> str | None:
        return memo_get_title(self.event, self.day)

    def get_input(self, part: int) -> tuple[str, ...] | None:
        return memo_get_input(self.event, self.day, part)

    def get_answer(self, part: int) -> str | None:
        return memo_get_answer(self.event, self.day, part)


InputData = tuple[str, ...]
type OUTPUT = str | int | None


class SolutionBase[
    OUTPUT1: OUTPUT,
    OUTPUT2: OUTPUT,
    OUTPUT3: OUTPUT,
](ABC):
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
            answer = colored(self.answer, "white", attrs=["bold"])
            if self.duration_as_ms <= 1_000:
                duration = f"{self.duration_as_ms:.3f}"
            elif self.duration_as_ms <= 5_000:
                duration = colored(f"{self.duration_as_ms:.0f}", "yellow")
            else:
                duration = colored(f"{self.duration_as_ms:.0f}", "red")
            return f"Part {self.part}: {answer}, took {duration} ms"

    def __init__(self, event: int, day: int) -> None:
        self.quest = Quest(event, day)
        self.callables = {"1": self.part_1, "2": self.part_2, "3": self.part_3}

    @abstractmethod
    def samples(self) -> None:
        pass

    @abstractmethod
    def part_1(self, input_data: InputData) -> OUTPUT1:
        pass

    @abstractmethod
    def part_2(self, input_data: InputData) -> OUTPUT2:
        pass

    @abstractmethod
    def part_3(self, input_data: InputData) -> OUTPUT3:
        pass

    def run(self, main_args: list[str]) -> None:  # noqa:C901
        def execute_part(
            part: SolutionBase.Part, f: Callable[[InputData], Any]
        ) -> SolutionBase.PartExecution:
            input_data = self.quest.get_input(part.int_value())
            if input_data is None:
                result = SolutionBase.PartExecution(part, no_input=True)
            else:
                start = time.time()
                answer = f(input_data)
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
                    f" Expected: '{expected}', got: '{answer}'"
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
                self.quest.event,
                self.quest.day,
                part,
                exec_part.answer,
            )
            for line in SubmitResponseFormatter.format(response):
                print(line)

        def print_header() -> None:
            event = "Story " if calendar.valid_story(self.quest.event) else ""
            event = f"{event}{self.quest.event}"
            header = colored(
                f"everybody.codes {event} Quest {self.quest.day}",
                "yellow",
            )
            if not self.quest.is_released():
                print()
                print(f"{header}: == Quest not available yet ==")
                print()
                return
            title = self.quest.get_title()
            title = (
                ""
                if title is None
                else colored(f": {title}", "white", attrs=["bold"])
            )
            print()
            print(header + title)
            print()

        print_header()
        if __debug__:
            prettyprinter.install_extras(include=["dataclasses"])
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
    def decorator(_: F) -> F:
        def wrapper(*args: OUTPUT) -> None:
            _self = args[0]
            for test in tests:
                func, _, expected = test
                input_data = tuple(_ for _ in test[1].splitlines())
                actual = getattr(_self, func)(input_data)
                message = (
                    f"FAILED '{func}'. Expected: '{expected}', was: '{actual}'"
                )
                assert actual == expected, message

        return cast("F", wrapper)

    return decorator


@unique
class Direction(Enum):
    x: int
    y: int

    def __new__(cls, x: int, y: int) -> Self:
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

    def turn(self, turn: Turn) -> Direction:
        if self == Direction.UP:
            return (
                Direction.DOWN
                if turn == Turn.AROUND
                else Direction.LEFT
                if turn == Turn.LEFT
                else Direction.RIGHT
            )
        if self == Direction.RIGHT:
            return (
                Direction.LEFT
                if turn == Turn.AROUND
                else Direction.UP
                if turn == Turn.LEFT
                else Direction.DOWN
            )
        if self == Direction.DOWN:
            return (
                Direction.UP
                if turn == Turn.AROUND
                else Direction.RIGHT
                if turn == Turn.LEFT
                else Direction.LEFT
            )
        if self == Direction.LEFT:
            return (
                Direction.RIGHT
                if turn == Turn.AROUND
                else Direction.DOWN
                if turn == Turn.LEFT
                else Direction.UP
            )
        raise ValueError


@unique
class Direction3D(Enum):
    x: int
    y: int
    z: int
    letter: str

    def __new__(cls, x: int, y: int, z: int, letter: str) -> Self:
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

    def manhattan_distance(self, other: Position) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


class Position3D(NamedTuple):
    x: int
    y: int
    z: int

    def at(self, direction: Direction3D) -> Position3D:
        return Position3D(
            self.x + direction.x, self.y + direction.y, self.z + direction.z
        )


class Turn(Enum):
    letter: str

    def __new__(cls, value: int, letter: str) -> Self:
        obj = object.__new__(cls)
        obj._value_ = value
        obj.letter = letter
        return obj

    LEFT = (270, "L")
    RIGHT = (90, "R")
    AROUND = (180, None)
