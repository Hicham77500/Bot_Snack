"""Self-contained fallback Snake engine for the UI.

This module lets the UI (PLAY / AUTO AI / statistics) run *before* the real
``game/``, ``environment/`` and ``agents/`` modules are implemented and merged
by the rest of the team. It is confined to ``ui/`` and never touches those
packages: it only mirrors the interfaces frozen in ``CONTRACT.md`` so the real
implementations can drop in later without changing a line of UI code.

Provided here:
- :class:`FallbackGame`   -> mirrors the ``game.Game`` / ``GameState`` contract
- :func:`build_observation` -> the 11-feature vector from ``CONTRACT.md``
- :class:`FallbackEnv`    -> gym-like wrapper (reset/step) over FallbackGame
- :class:`RandomAgent`    -> uniform-random baseline
- :class:`HeuristicAgent` -> a "smart" stand-in used *in place of* a trained DQN
  when ``models/best_agent.pth`` does not exist yet.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

import numpy as np

# --- Contract constants -----------------------------------------------------
# Action indices (CONTRACT.md > Actions)
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
ACTION_NAMES = {UP: "UP", DOWN: "DOWN", LEFT: "LEFT", RIGHT: "RIGHT"}
# (dx, dy) with y growing downward, as used for board coordinates.
ACTION_VECTORS: dict[int, tuple[int, int]] = {
    UP: (0, -1),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    RIGHT: (1, 0),
}
OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

NUM_ACTIONS = 4
OBSERVATION_SIZE = 11
MAX_LEVEL = 4


@dataclass
class GameState:
    """Mirror of the ``GameState`` dataclass in CONTRACT.md."""

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


# --- Level design -----------------------------------------------------------
# Board is fixed; obstacle density grows with the level (1..4).
BOARD_WIDTH = 20
BOARD_HEIGHT = 15


def _border_obstacles(w: int, h: int) -> list[tuple[int, int]]:
    cells = set()
    for x in range(w):
        cells.add((x, 0))
        cells.add((x, h - 1))
    for y in range(h):
        cells.add((0, y))
        cells.add((w - 1, y))
    return sorted(cells)


def build_obstacles(level: int, w: int, h: int, rng: random.Random) -> list[tuple[int, int]]:
    """Walls scale with the level. Level 1 = open field (walls only)."""
    obstacles = set(_border_obstacles(w, h))
    if level >= 2:
        # A couple of short interior bars.
        for x in range(4, 8):
            obstacles.add((x, h // 2))
    if level >= 3:
        for y in range(3, h - 3):
            obstacles.add((w // 2, y))
    if level >= 4:
        for x in range(w - 8, w - 4):
            obstacles.add((x, h // 3))
        for x in range(4, 8):
            obstacles.add((x, 2 * h // 3))
    return sorted(obstacles)


class FallbackGame:
    """Headless Snake engine following the ``game.Game`` contract."""

    def __init__(self, level: int = 1, seed: int | None = None):
        self._level = max(1, min(level, MAX_LEVEL))
        self._rng = random.Random(seed)
        self.board_width = BOARD_WIDTH
        self.board_height = BOARD_HEIGHT
        self.reset(self._level)

    # -- contract API --------------------------------------------------------
    def reset(self, level: int | None = None) -> GameState:
        if level is not None:
            self._level = max(1, min(level, MAX_LEVEL))
        w, h = self.board_width, self.board_height
        self._obstacles = build_obstacles(self._level, w, h, self._rng)
        cx, cy = w // 2, h // 2
        # Snake of length 3 heading right, placed in the clear center.
        self._snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self._direction = ACTION_VECTORS[RIGHT]
        self._score = 0
        self._steps = 0
        self._done = False
        self._last_reward = 0.0
        self._death_reason = None
        self._food = self._spawn_food()
        return self.get_state()

    def step(self, action: int) -> GameState:
        if self._done:
            return self.get_state()

        # Filter immediate 180° turn: keep current direction instead.
        desired = ACTION_VECTORS.get(action, self._direction)
        if desired == (-self._direction[0], -self._direction[1]):
            desired = self._direction
        self._direction = desired

        head_x, head_y = self._snake[0]
        new_head = (head_x + desired[0], head_y + desired[1])

        self._steps += 1
        reward = 0.1  # survival (CONTRACT.md reward)

        # Collision checks.
        if (
            new_head in self._obstacles
            or not (0 <= new_head[0] < self.board_width)
            or not (0 <= new_head[1] < self.board_height)
        ):
            self._death_reason = "obstacle" if new_head in self._obstacles else "wall"
            reward = -10.0
            self._finish(reward)
            return self.get_state()

        if new_head in self._snake[:-1]:  # tail cell is about to move away
            self._death_reason = "self"
            reward = -10.0
            self._finish(reward)
            return self.get_state()

        # Move.
        self._snake.insert(0, new_head)
        if new_head == self._food:
            self._score += 1
            reward = 10.0
            self._death_reason = "food"  # transient info for this step
            self._food = self._spawn_food()
            if self._food is None:  # board full = win
                self._finish(reward)
                return self.get_state()
        else:
            self._snake.pop()
            self._death_reason = None

        self._last_reward = reward
        return self.get_state()

    def get_state(self) -> GameState:
        return GameState(
            snake_body=list(self._snake),
            snake_direction=self._direction,
            food_position=self._food if self._food is not None else (-1, -1),
            obstacles=list(self._obstacles),
            board_width=self.board_width,
            board_height=self.board_height,
            score=self._score,
            level=self._level,
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
        return self._level

    # -- internals -----------------------------------------------------------
    def _finish(self, reward: float) -> None:
        self._last_reward = reward
        self._done = True

    def _spawn_food(self) -> tuple[int, int] | None:
        free = [
            (x, y)
            for x in range(self.board_width)
            for y in range(self.board_height)
            if (x, y) not in self._obstacles and (x, y) not in self._snake
        ]
        if not free:
            return None
        return self._rng.choice(free)


# --- Observation (CONTRACT.md v1, 11 features) ------------------------------
def _direction_vector(snake_direction) -> tuple[int, int]:
    """Accept int action index (0-3) or (dx, dy) tuple from GameState."""
    if isinstance(snake_direction, (int, np.integer)):
        return ACTION_VECTORS[int(snake_direction)]
    dx, dy = snake_direction
    return int(dx), int(dy)


def build_observation(state: GameState, max_level: int = MAX_LEVEL) -> np.ndarray:
    """Build the 11-feature float32 observation described in CONTRACT.md."""
    dx, dy = _direction_vector(state.snake_direction)
    head_x, head_y = state.snake_body[0]

    # Local frame: left / right relative to heading.
    left_vec = (dy, -dx)
    right_vec = (-dy, dx)

    def is_danger(vec: tuple[int, int]) -> float:
        nx, ny = head_x + vec[0], head_y + vec[1]
        if not (0 <= nx < state.board_width) or not (0 <= ny < state.board_height):
            return 1.0
        if (nx, ny) in state.obstacles:
            return 1.0
        if (nx, ny) in state.snake_body[:-1]:
            return 1.0
        return 0.0

    fx, fy = state.food_position
    denom_x = max(1, state.board_width)
    denom_y = max(1, state.board_height)

    obs = np.array(
        [
            float(dx),
            float(dy),
            1.0 if dx != 0 else 0.0,  # one-hot-ish horizontal
            1.0 if dy != 0 else 0.0,  # one-hot-ish vertical
            is_danger((dx, dy)),      # danger front
            is_danger(left_vec),      # danger left
            is_danger(right_vec),     # danger right
            (fx - head_x) / denom_x,  # food dx normalized
            (fy - head_y) / denom_y,  # food dy normalized
            state.level / max_level,  # level normalized
            state.score / 100.0,      # score normalized
        ],
        dtype=np.float32,
    )
    return obs


@dataclass
class ObservationInfo:
    """Human-readable observation, for the bonus panel / video."""

    danger_front: bool
    danger_left: bool
    danger_right: bool
    action: int

    def as_lines(self) -> list[str]:
        def tag(v: bool) -> str:
            return "danger" if v else "safe"

        return [
            f"Front : {tag(self.danger_front)}",
            f"Left  : {tag(self.danger_left)}",
            f"Right : {tag(self.danger_right)}",
            f"Action: {ACTION_NAMES.get(self.action, '?')}",
        ]


# --- Gym-like environment wrapper ------------------------------------------
class FallbackEnv:
    """Minimal gym-like env over :class:`FallbackGame`, for AUTO AI + stats."""

    def __init__(self, level: int = 1, max_level: int = MAX_LEVEL, seed: int | None = None):
        self.max_level = max_level
        self.level = level
        self.game = FallbackGame(level=level, seed=seed)
        self._state: GameState = self.game.get_state()

    @property
    def observation_size(self) -> int:
        return OBSERVATION_SIZE

    @property
    def action_size(self) -> int:
        return NUM_ACTIONS

    def reset(self, level: int | None = None) -> np.ndarray:
        self._state = self.game.reset(level if level is not None else self.level)
        return build_observation(self._state, self.max_level)

    def step(self, action: int) -> tuple[np.ndarray, float, bool, dict]:
        self._state = self.game.step(action)
        obs = build_observation(self._state, self.max_level)
        reward = self._state.last_reward
        done = self._state.done
        info = {
            "score": self._state.score,
            "level": self._state.level,
            "steps": self._state.steps,
            "reason": self._state.death_reason,
        }
        return obs, reward, done, info

    @property
    def state(self) -> GameState:
        return self._state


# --- Fallback agents --------------------------------------------------------
class RandomAgent:
    """Uniform random baseline (mirrors agents.random_agent contract)."""

    def __init__(self, action_size: int = NUM_ACTIONS, seed: int | None = None):
        self.action_size = action_size
        self._rng = random.Random(seed)

    def select_action(self, state: np.ndarray, training: bool = False) -> int:
        return self._rng.randrange(self.action_size)

    def save(self, path: str) -> None:  # pragma: no cover - parity only
        pass

    def load(self, path: str) -> None:  # pragma: no cover - parity only
        pass


class HeuristicAgent:
    """Greedy toward food while avoiding immediate danger.

    Stand-in for a trained DQN when no ``best_agent.pth`` exists yet, so the
    Random-vs-"DQN" comparison and the AUTO AI demo show a clear gap. It is
    *not* a learned policy and is always labelled as a placeholder in the UI.
    """

    label = "heuristic placeholder"

    def __init__(self, action_size: int = NUM_ACTIONS, seed: int | None = None):
        self.action_size = action_size
        self._rng = random.Random(seed)

    def select_action(self, state: np.ndarray, training: bool = False) -> int:
        # state layout (real env): [one-hot dir x4, dgr_front, dgr_left, dgr_right,
        #                           food_dx, food_dy, level, score]
        danger = {"front": state[4], "left": state[5], "right": state[6]}
        food_dx, food_dy = state[7], state[8]

        heading = _heading_from_obs(state)
        dx, dy = heading
        left_vec = (dy, -dx)
        right_vec = (-dy, dx)

        # Rank candidate directions by how much they reduce food distance.
        candidates = {
            "front": (heading, danger["front"]),
            "left": (left_vec, danger["left"]),
            "right": (right_vec, danger["right"]),
        }

        def score(vec: tuple[int, int]) -> float:
            # Higher is better: alignment of move with the food direction.
            return vec[0] * food_dx + vec[1] * food_dy

        safe = [(name, vec) for name, (vec, dgr) in candidates.items() if dgr < 0.5]
        pool = safe if safe else [(n, v) for n, (v, _d) in candidates.items()]
        best_name, best_vec = max(pool, key=lambda nv: score(nv[1]))

        return _vec_to_action(best_vec)


def _vec_to_action(vec: tuple[int, int]) -> int:
    for action, v in ACTION_VECTORS.items():
        if v == vec:
            return action
    return RIGHT


def _heading_from_obs(obs: np.ndarray) -> tuple[int, int]:
    """Decode the snake heading from an 11-feature observation vector.

    ``environment/observation.py`` uses a one-hot direction at ``obs[0:4]``.
    The legacy fallback layout stores ``(dx, dy)`` at ``obs[0]`` and ``obs[1]``.
    """
    o = obs[0:4]
    if np.count_nonzero(o >= 0.5) == 1 and np.all(o >= 0):
        return ACTION_VECTORS[int(np.argmax(o))]
    dx, dy = int(round(obs[0])), int(round(obs[1]))
    if (dx, dy) in ACTION_VECTORS.values():
        return (dx, dy)
    return ACTION_VECTORS[RIGHT]
