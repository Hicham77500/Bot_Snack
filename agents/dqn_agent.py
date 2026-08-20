"""DQN agent — TODO: implement (Hicham Guendouz)."""

import numpy as np


class DQNAgent:
    def __init__(
        self,
        state_size: int,
        action_size: int,
        lr: float = 1e-3,
        gamma: float = 0.99,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.995,
        buffer_size: int = 10_000,
        batch_size: int = 64,
        target_update: int = 10,
        device: str | None = None,
    ):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = epsilon

    def select_action(self, state: np.ndarray, training: bool = False) -> int:
        raise NotImplementedError("Hicham: implement dqn_agent.select_action()")

    def remember(
        self,
        state: np.ndarray,
        action: int,
        reward: float,
        next_state: np.ndarray,
        done: bool,
    ) -> None:
        raise NotImplementedError("Hicham: implement dqn_agent.remember()")

    def train_step(self) -> float | None:
        raise NotImplementedError("Hicham: implement dqn_agent.train_step()")

    def save(self, path: str) -> None:
        raise NotImplementedError("Hicham: implement dqn_agent.save()")

    def load(self, path: str) -> None:
        raise NotImplementedError("Hicham: implement dqn_agent.load()")
