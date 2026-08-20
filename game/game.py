"""Main Snake game engine — TODO: implement (Aya El JANATI).

Headless only — no Pygame imports allowed in this module.
See CONTRACT.md and docs/prompts/aya.md
"""

from dataclasses import dataclass


@dataclass
class GameState:
    snake_body: list[tuple[int, int]]
    snake_direction: tuple[int, int]
    food_position: tuple[int, int]
    obstacles: list[tuple[int, int]]
    board_width: int
    board_height: int
    score: int
    level: int
    done: bool
    steps: int
    last_reward: float = 0.0
    death_reason: str | None = None


class Game:
    """Snake game engine. Must work without any UI."""

    def __init__(self, level: int = 1):
        self._level = level

    def reset(self, level: int | None = None) -> GameState:
        raise NotImplementedError("Aya: implement game.reset()")

    def step(self, action: int) -> GameState:
        raise NotImplementedError("Aya: implement game.step()")

    def get_state(self) -> GameState:
        raise NotImplementedError("Aya: implement game.get_state()")

    def get_reward(self) -> float:
        raise NotImplementedError("Aya: implement game.get_reward()")

    def is_done(self) -> bool:
        raise NotImplementedError("Aya: implement game.is_done()")

    def get_score(self) -> int:
        raise NotImplementedError("Aya: implement game.get_score()")

    def get_level(self) -> int:
        raise NotImplementedError("Aya: implement game.get_level()")
