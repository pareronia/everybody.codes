from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterator

T = TypeVar("T")
U = TypeVar("U")


class GameOfLife:
    def __init__(
        self,
        alive: U,
        universe: Universe[T, U],
        rules: Rules[T, U],
        convert: Callable[[Iterator[T]], U],
    ) -> None:
        self.alive = alive
        self.universe = universe
        self.rules = rules
        self.convert = convert

    def next_generation(self) -> None:
        self.alive = self.convert(
            (
                cell
                for cell, count in self.universe.neighbour_count(self.alive)
                if self.rules.alive(cell, count, self.alive)
            )
        )

    class Universe(ABC, Generic[T, U]):
        @abstractmethod
        def neighbour_count(self, alive: U) -> Iterator[tuple[T, int]]:
            pass

    class Rules(ABC, Generic[T, U]):
        @abstractmethod
        def alive(self, cell: T, count: int, alive: U) -> bool:
            pass
