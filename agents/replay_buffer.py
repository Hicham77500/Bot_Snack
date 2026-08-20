"""Experience replay buffer — TODO: implement (Hicham Guendouz)."""

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
        raise NotImplementedError("Hicham: implement replay_buffer.push()")

    def sample(self, batch_size: int) -> tuple:
        raise NotImplementedError("Hicham: implement replay_buffer.sample()")

    def __len__(self) -> int:
        return 0
