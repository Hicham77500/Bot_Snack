"""Snake entity — TODO: implement (Aya El JANATI)."""

from dataclasses import dataclass, field

DIRECTIONS = {
    0: (0, -1),   # UP
    1: (0, 1),    # DOWN
    2: (-1, 0),   # LEFT
    3: (1, 0),    # RIGHT
}


@dataclass
class Snake:
    body: list[tuple[int, int]] = field(default_factory=list)
    direction: tuple[int, int] = (1, 0)

    def head(self) -> tuple[int, int]:
        raise NotImplementedError("Aya: implement snake.head()")

    def set_direction(self, action: int) -> None:
        raise NotImplementedError("Aya: implement snake.set_direction()")

    def move(self, grow: bool = False) -> tuple[int, int]:
        raise NotImplementedError("Aya: implement snake.move()")

    def collides_with_self(self, position: tuple[int, int]) -> bool:
        raise NotImplementedError("Aya: implement snake.collides_with_self()")
