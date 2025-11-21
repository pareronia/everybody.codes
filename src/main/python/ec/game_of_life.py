from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterable

T = TypeVar("T")


class GameOfLife:
    def __init__(
        self, alive: Iterable[T], universe: Universe[T], rules: Rules[T]
    ) -> None:
        self.alive = alive
        self.universe = universe
        self.rules = rules

    def next_generation(self) -> None:
        self.alive = {
            cell
            for cell, count in self.universe.neighbour_count(
                self.alive
            ).items()
            if self.rules.alive(cell, count, self.alive)
        }

    class Universe(ABC, Generic[T]):
        @abstractmethod
        def neighbour_count(self, alive: Iterable[T]) -> dict[T, int]:
            pass

    class Rules(ABC, Generic[T]):
        @abstractmethod
        def alive(self, cell: T, count: int, alive: Iterable[T]) -> bool:
            pass
