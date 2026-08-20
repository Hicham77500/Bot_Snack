"""Food placement for Snake."""

import random
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
        free_cells = [
            (x, y)
            for x in range(board_width)
            for y in range(board_height)
            if (x, y) not in occupied
        ]
        if not free_cells:
            raise RuntimeError("No free cell to spawn food")
        return cls(position=random.choice(free_cells))
