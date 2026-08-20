"""Observation builder for Snake RL agent."""

import numpy as np

from game.game import GameState
from game.snake import DIRECTIONS

OBSERVATION_SIZE = 11


def _danger_at(state: GameState, direction: tuple[int, int]) -> float:
    hx, hy = state.snake_body[0]
    dx, dy = direction
    nx, ny = hx + dx, hy + dy
    if nx < 0 or nx >= state.board_width or ny < 0 or ny >= state.board_height:
        return 1.0
    if (nx, ny) in state.obstacles:
        return 1.0
    if (nx, ny) in state.snake_body:
        return 1.0
    return 0.0


def _relative_direction(state: GameState) -> tuple[int, int]:
    dx, dy = state.snake_direction
    return dx, dy


def build_observation(state: GameState, max_level: int = 4) -> np.ndarray:
    """Build 11-feature observation vector (see CONTRACT.md)."""
    hx, hy = state.snake_body[0]
    fx, fy = state.food_position

    dir_x, dir_y = _relative_direction(state)
    front = (dir_x, dir_y)
    left = (-dir_y, dir_x)
    right = (dir_y, -dir_x)

    food_dx = (fx - hx) / max(state.board_width, 1)
    food_dy = (fy - hy) / max(state.board_height, 1)

    obs = np.array(
        [
            float(dir_x),
            float(dir_y),
            _danger_at(state, front),
            _danger_at(state, left),
            _danger_at(state, right),
            food_dx,
            food_dy,
            float(state.level) / max_level,
            float(state.score) / 100.0,
            float(len(state.snake_body)) / (state.board_width * state.board_height),
            float(state.steps) / 1000.0,
        ],
        dtype=np.float32,
    )
    return obs
