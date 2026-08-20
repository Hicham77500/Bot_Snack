"""Gym-like RL environment wrapping the Snake game engine."""

import numpy as np

from environment.actions import NUM_ACTIONS
from environment.observation import OBSERVATION_SIZE


class SnakeEnv:
    def __init__(self, level: int = 1, max_level: int = 4):
        self.max_level = max_level
        self.level = level

    @property
    def observation_size(self) -> int:
        return OBSERVATION_SIZE

    @property
    def action_size(self) -> int:
        return NUM_ACTIONS

    def reset(self, level: int | None = None) -> np.ndarray:
        raise NotImplementedError

    def step(self, action: int) -> tuple[np.ndarray, float, bool, dict]:
        raise NotImplementedError
