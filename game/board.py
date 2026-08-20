"""Board grid for Snake."""

from dataclasses import dataclass


@dataclass
class Board:
    width: int
    height: int

    def is_inside(self, x: int, y: int) -> bool:
        raise NotImplementedError

    def is_collision(self, x: int, y: int) -> bool:
        raise NotImplementedError
