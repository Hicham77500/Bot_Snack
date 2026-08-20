"""Experience replay buffer for DQN."""

import numpy as np


class ReplayBuffer:
    def __init__(self, capacity: int = 10_000):
        self.capacity = capacity

    def push(
        self,
        state: np.ndarray,
        action: int,
        reward: float,
        next_state: np.ndarray,
        done: bool,
    ) -> None:
        raise NotImplementedError

    def sample(self, batch_size: int) -> tuple:
        raise NotImplementedError

    def __len__(self) -> int:
        return 0
