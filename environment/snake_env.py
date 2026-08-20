"""Gym-like RL environment wrapping the Snake game engine."""

import numpy as np

from environment.actions import NUM_ACTIONS
from environment.observation import OBSERVATION_SIZE, build_observation
from environment.reward import compute_reward
from game.game import Game


class SnakeEnv:
    """RL environment: reset() / step(action) interface."""

    def __init__(self, level: int = 1, max_level: int = 4):
        self.max_level = max_level
        self.level = level
        self.game = Game(level=level)
        self._last_state = None

    @property
    def observation_size(self) -> int:
        return OBSERVATION_SIZE

    @property
    def action_size(self) -> int:
        return NUM_ACTIONS

    def reset(self, level: int | None = None) -> np.ndarray:
        if level is not None:
            self.level = level
        self.game = Game(level=self.level)
        state = self.game.reset()
        self._last_state = state
        return build_observation(state, self.max_level)

    def step(self, action: int) -> tuple[np.ndarray, float, bool, dict]:
        state = self.game.step(int(action))
        self._last_state = state
        obs = build_observation(state, self.max_level)
        reward = compute_reward(state)
        done = state.done
        info = {
            "score": state.score,
            "level": state.level,
            "steps": state.steps,
            "reason": state.death_reason,
        }
        return obs, reward, done, info
