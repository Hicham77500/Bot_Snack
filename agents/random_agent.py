"""Random baseline agent for Snake."""

import random

import numpy as np


class RandomAgent:
    """Selects a random valid action at each step."""

    def __init__(self, action_size: int = 4, seed: int | None = None):
        self.action_size = action_size
        self.rng = random.Random(seed)

    def select_action(self, state: np.ndarray, training: bool = False) -> int:
        return self.rng.randint(0, self.action_size - 1)

    def save(self, path: str) -> None:
        pass

    def load(self, path: str) -> None:
        pass
