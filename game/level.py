"""Level configuration with obstacles."""

from dataclasses import dataclass, field


@dataclass
class Level:
    number: int
    board_width: int = 20
    board_height: int = 20
    obstacles: list[tuple[int, int]] = field(default_factory=list)
    tick_speed: float = 0.15

    @classmethod
    def from_number(cls, level: int) -> "Level":
        raise NotImplementedError
