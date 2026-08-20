"""Gym-like RL environment — TODO: implement (Khalil Jouani)."""

import numpy as np

from environment.actions import NUM_ACTIONS
from environment.observation import OBSERVATION_SIZE


class SnakeEnv:
    """RL environment: reset() / step(action) interface. See CONTRACT.md."""

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
        raise NotImplementedError("Khalil: implement env.reset()")

    def step(self, action: int) -> tuple[np.ndarray, float, bool, dict]:
        raise NotImplementedError("Khalil: implement env.step()")
