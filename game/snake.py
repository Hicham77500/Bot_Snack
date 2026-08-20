"""Snake entity."""

from dataclasses import dataclass, field

DIRECTIONS = {
    0: (0, -1),
    1: (0, 1),
    2: (-1, 0),
    3: (1, 0),
}


@dataclass
class Snake:
    body: list[tuple[int, int]] = field(default_factory=list)
    direction: tuple[int, int] = (1, 0)

    def head(self) -> tuple[int, int]:
        raise NotImplementedError

    def set_direction(self, action: int) -> None:
        raise NotImplementedError

    def move(self, grow: bool = False) -> tuple[int, int]:
        raise NotImplementedError

    def collides_with_self(self, position: tuple[int, int]) -> bool:
        raise NotImplementedError
