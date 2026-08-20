"""Main Snake game engine — headless, Pygame-free."""

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
    def __init__(self, level: int = 1):
        self._level = level

    def reset(self, level: int | None = None) -> GameState:
        raise NotImplementedError

    def step(self, action: int) -> GameState:
        raise NotImplementedError

    def get_state(self) -> GameState:
        raise NotImplementedError

    def get_reward(self) -> float:
        raise NotImplementedError

    def is_done(self) -> bool:
        raise NotImplementedError

    def get_score(self) -> int:
        raise NotImplementedError

    def get_level(self) -> int:
        raise NotImplementedError
