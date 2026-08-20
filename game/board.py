"""Board grid for Snake."""

from dataclasses import dataclass


@dataclass
class Board:
    width: int
    height: int

    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def is_collision(self, x: int, y: int) -> bool:
        return not self.is_inside(x, y)
