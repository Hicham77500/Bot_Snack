"""
game.py — Orchestrateur headless du jeu Snake (Bot_Snack).

Expose l'API attendue par CONTRACT.md :
    game.reset(level=1)   -> GameState
    game.step(action)     -> GameState   (0=UP, 1=DOWN, 2=LEFT, 3=RIGHT)
    game.get_state()      -> GameState
    game.get_reward()     -> float
    game.is_done()        -> bool
    game.get_score()      -> int
    game.get_level()      -> int

Aucun import Pygame ici : moteur 100% headless, testable en pur Python.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional

from game.board import Board
from game.snake import Snake, RIGHT
from game.food import Food
from game.level import build_level

Position = Tuple[int, int]

# Récompenses par défaut pour l'agent RL (training/). Ajustable si l'équipe
# est d'accord, mais garder les noms/signes cohérents avec CONTRACT.md.
REWARD_FOOD = 10.0
REWARD_DEATH = -10.0
REWARD_STEP = -0.01  # légère pénalité pour pousser vers l'efficacité


@dataclass
class GameState:
    snake_body: List[Position]
    snake_direction: int
    food_position: Position
    obstacles: List[Position]
    board_width: int
    board_height: int
    score: int
    level: int
    done: bool
    steps: int
    death_reason: Optional[str] = None


class Game:
    """Orchestrateur : instancie Board/Snake/Food et gère la boucle de jeu."""

    def __init__(self, level: int = 1):
        self._level = level
        self.board: Optional[Board] = None
        self.snake: Optional[Snake] = None
        self.food: Optional[Food] = None
        self._score = 0
        self._steps = 0
        self._done = False
        self._death_reason: Optional[str] = None
        self._last_reward = 0.0
        self.reset(level=level)

    # ------------------------------------------------------------------
    # API CONTRACT.md
    # ------------------------------------------------------------------

    def reset(self, level: int = None) -> GameState:
        """Réinitialise une partie sur le niveau demandé (ou le niveau courant)."""
        if level is not None:
            self._level = level

        width, height, obstacles = build_level(self._level)

        # La tête démarre au centre ; on dégage une zone pour ne pas
        # faire spawn le serpent sur un obstacle du niveau.
        start = (width // 2, height // 2)
        clear_zone = {
            (start[0] + dx, start[1] + dy)
            for dx in range(-2, 3)
            for dy in range(-2, 3)
        }
        obstacles = [o for o in obstacles if o not in clear_zone]

        self.board = Board(width, height, obstacles)
        self.snake = Snake(start=start, direction=RIGHT, length=3)
        self.food = Food()
        self.food.spawn(self.board, self.snake.body)

        self._score = 0
        self._steps = 0
        self._done = False
        self._death_reason = None
        self._last_reward = 0.0

        return self.get_state()

    def step(self, action: int) -> GameState:
        """Avance le jeu d'un tick avec `action` (0=UP,1=DOWN,2=LEFT,3=RIGHT)."""
        if self._done:
            return self.get_state()

        self.snake.set_direction(action)
        new_head = self.snake.next_head()

        # --- Collisions (ordre : mur > obstacle > soi-même) ---
        if not self.board.is_inside(new_head):
            self._end_game("wall")
            return self.get_state()

        if self.board.is_obstacle(new_head):
            self._end_game("obstacle")
            return self.get_state()

        ate = new_head == self.food.position
        # Si on mange, la queue ne bouge pas (le serpent grandit) donc la
        # case de queue actuelle n'est pas "libérée" -> on l'inclut aussi.
        if self.snake.collides_with_self(new_head) and not ate:
            self._end_game("self")
            return self.get_state()
        if ate and new_head in self.snake.body:
            # Cas limite : manger correspondrait à re-rentrer dans son corps.
            self._end_game("self")
            return self.get_state()

        # --- Déplacement ---
        if ate:
            self.snake.grow(1)

        self.snake.move()
        self._steps += 1

        if ate:
            self._score += 1
            self._last_reward = REWARD_FOOD
            self.food.spawn(self.board, self.snake.body)
        else:
            self._last_reward = REWARD_STEP

        return self.get_state()

    def get_state(self) -> GameState:
        return GameState(
            snake_body=list(self.snake.body),
            snake_direction=self.snake.direction,
            food_position=self.food.position,
            obstacles=list(self.board.obstacles),
            board_width=self.board.width,
            board_height=self.board.height,
            score=self._score,
            level=self._level,
            done=self._done,
            steps=self._steps,
            death_reason=self._death_reason,
        )

    def get_reward(self) -> float:
        return self._last_reward

    def is_done(self) -> bool:
        return self._done

    def get_score(self) -> int:
        return self._score

    def get_level(self) -> int:
        return self._level

    # ------------------------------------------------------------------
    # Internes
    # ------------------------------------------------------------------

    def _end_game(self, reason: str) -> None:
        self._done = True
        self._death_reason = reason
        self._last_reward = REWARD_DEATH
