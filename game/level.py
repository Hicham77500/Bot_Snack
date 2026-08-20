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
        configs = {
            1: cls(number=1, board_width=15, board_height=15, obstacles=[]),
            2: cls(
                number=2,
                board_width=18,
                board_height=18,
                obstacles=[(9, 5), (9, 6), (9, 7), (9, 13), (9, 14), (9, 15)],
            ),
            3: cls(
                number=3,
                board_width=20,
                board_height=20,
                obstacles=[
                    (5, 5), (5, 6), (5, 7),
                    (14, 12), (14, 13), (14, 14),
                    (10, 9), (10, 10), (10, 11),
                ],
            ),
            4: cls(
                number=4,
                board_width=22,
                board_height=22,
                obstacles=[
                    (x, 11) for x in range(4, 18)
                ] + [(11, y) for y in range(4, 18)],
                tick_speed=0.10,
            ),
        }
        return configs.get(level, configs[1])
