"""Random baseline agent for Snake."""

import numpy as np


class RandomAgent:
    def __init__(self, action_size: int = 4, seed: int | None = None):
        self.action_size = action_size

    def select_action(self, state: np.ndarray, training: bool = False) -> int:
        raise NotImplementedError

    def save(self, path: str) -> None:
        pass

    def load(self, path: str) -> None:
        pass
