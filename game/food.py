"""Food placement — TODO: implement (Aya El JANATI)."""

from dataclasses import dataclass


@dataclass
class Food:
    position: tuple[int, int]

    @classmethod
    def spawn(
        cls,
        board_width: int,
        board_height: int,
        occupied: set[tuple[int, int]],
    ) -> "Food":
        raise NotImplementedError("Aya: implement food.spawn()")
