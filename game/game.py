"""Main Snake game engine — headless, Pygame-free."""

from dataclasses import dataclass

from game.board import Board
from game.food import Food
from game.level import Level
from game.snake import Snake


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
    REWARD_FOOD = 10.0
    REWARD_DEATH = -10.0
    REWARD_SURVIVAL = 0.1

    def __init__(self, level: int = 1):
        self._level_config = Level.from_number(level)
        self._board = Board(self._level_config.board_width, self._level_config.board_height)
        self._snake = Snake()
        self._food: Food | None = None
        self._score = 0
        self._steps = 0
        self._done = False
        self._last_reward = 0.0
        self._death_reason: str | None = None

    def reset(self, level: int | None = None) -> GameState:
        if level is not None:
            self._level_config = Level.from_number(level)
            self._board = Board(
                self._level_config.board_width,
                self._level_config.board_height,
            )

        cx = self._board.width // 2
        cy = self._board.height // 2
        self._snake = Snake(
            body=[(cx, cy), (cx - 1, cy), (cx - 2, cy)],
            direction=(1, 0),
        )
        self._score = 0
        self._steps = 0
        self._done = False
        self._last_reward = 0.0
        self._death_reason = None
        self._spawn_food()
        return self.get_state()

    def step(self, action: int) -> GameState:
        if self._done:
            return self.get_state()

        self._snake.set_direction(action)
        head = self._snake.move(grow=False)
        self._steps += 1
        self._last_reward = self.REWARD_SURVIVAL

        if self._board.is_collision(*head):
            self._done = True
            self._last_reward = self.REWARD_DEATH
            self._death_reason = "wall"
        elif head in self._level_config.obstacles:
            self._done = True
            self._last_reward = self.REWARD_DEATH
            self._death_reason = "obstacle"
        elif self._snake.collides_with_self(head):
            self._done = True
            self._last_reward = self.REWARD_DEATH
            self._death_reason = "self"
        elif self._food and head == self._food.position:
            self._snake.move(grow=True)
            self._score += 1
            self._last_reward = self.REWARD_FOOD
            self._spawn_food()

        return self.get_state()

    def get_state(self) -> GameState:
        return GameState(
            snake_body=list(self._snake.body),
            snake_direction=self._snake.direction,
            food_position=self._food.position if self._food else (0, 0),
            obstacles=list(self._level_config.obstacles),
            board_width=self._board.width,
            board_height=self._board.height,
            score=self._score,
            level=self._level_config.number,
            done=self._done,
            steps=self._steps,
            last_reward=self._last_reward,
            death_reason=self._death_reason,
        )

    def get_reward(self) -> float:
        return self._last_reward

    def is_done(self) -> bool:
        return self._done

    def get_score(self) -> int:
        return self._score

    def get_level(self) -> int:
        return self._level_config.number

    def _spawn_food(self) -> None:
        occupied = set(self._snake.body) | set(self._level_config.obstacles)
        self._food = Food.spawn(
            self._board.width,
            self._board.height,
            occupied,
        )
