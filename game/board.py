"""Board grid — TODO: implement (Aya El JANATI)."""

from dataclasses import dataclass


@dataclass
class Board:
    width: int
    height: int

    def is_inside(self, x: int, y: int) -> bool:
        raise NotImplementedError("Aya: implement board.is_inside()")

    def is_collision(self, x: int, y: int) -> bool:
        raise NotImplementedError("Aya: implement board.is_collision()")
