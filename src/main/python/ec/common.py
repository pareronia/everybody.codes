from __future__ import annotations

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

import ec.memo as memo
from prettyprinter import cpprint

DIR_INPUTS = os.path.join(os.getcwd(), "inputs")


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

    def get_input(self, part: int) -> tuple[str, ...]:
        return memo.get_input(self.year, self.day, part)

    def get_answer(self, part: int) -> str | None:
        return memo.get_answer(self.year, self.day, part)


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

    class PartExecution(NamedTuple):
        part: SolutionBase.Part
        answer: Any
        duration: int

        @property
        def duration_as_ms(self) -> float:
            return self.duration / 1_000_000

        def __repr__(self) -> str:
            return (
                f"Part {self.part}:"
                f" {self.answer}, took {self.duration_as_ms:.3f} ms"
            )

    def __init__(self, year: int, day: int):
        self.quest = Quest(year, day)

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

    def run(self, args: list[str]) -> None:  # noqa E103
        def execute_part(
            part: SolutionBase.Part, f: Callable[[InputData], Any]
        ) -> SolutionBase.PartExecution:
            input = self.quest.get_input(part.int_value())
            start = time.time()
            answer = f(input)
            return SolutionBase.PartExecution(
                part, answer, int((time.time() - start) * 1e9)
            )

        def check_part(part: SolutionBase.Part, result: Any) -> str:
            expected = self.quest.get_answer(part.int_value())
            if (
                expected is not None
                and result is not None
                and expected != str(result)
            ):
                return f"Part {part}: Expected: '{expected}', got: '{result}'"
            return ""

        print()
        print(f"everybody.codes {self.quest.year} Quest {self.quest.day}")
        print()
        if __debug__:
            self.samples()
        exec_part1 = execute_part(
            self.Part.PART_1, lambda input: self.part_1(input)
        )
        print(exec_part1)
        exec_part2 = execute_part(
            self.Part.PART_2, lambda input: self.part_2(input)
        )
        print(exec_part2)
        exec_part3 = execute_part(
            self.Part.PART_3, lambda input: self.part_3(input)
        )
        print(exec_part3)
        fail_1 = check_part(self.Part.PART_1, exec_part1.answer)
        fail_2 = check_part(self.Part.PART_2, exec_part2.answer)
        fail_3 = check_part(self.Part.PART_3, exec_part3.answer)
        message = os.linesep.join([fail_1, fail_2, fail_3])
        if message.strip() != "":
            raise ValueError(os.linesep + message)


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


class Cell(NamedTuple):
    row: int
    col: int

    def at(self, direction: Direction) -> Cell:
        return Cell(self.row - direction.y, self.col + direction.x)

    def get_capital_neighbours(self) -> Iterator[Cell]:
        return (self.at(d) for d in Direction.capitals())
