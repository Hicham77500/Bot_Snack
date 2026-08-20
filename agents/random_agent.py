"""Random baseline agent — TODO: implement (Khalil Jouani)."""

import numpy as np


class RandomAgent:
    """Selects a random valid action at each step."""

    def __init__(self, action_size: int = 4, seed: int | None = None):
        self.action_size = action_size

    def select_action(self, state: np.ndarray, training: bool = False) -> int:
        raise NotImplementedError("Khalil: implement random_agent.select_action()")

    def save(self, path: str) -> None:
        pass

    def load(self, path: str) -> None:
        pass
