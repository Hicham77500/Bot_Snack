"""Observation builder for Snake RL agent."""

import numpy as np

from game.game import GameState

OBSERVATION_SIZE = 11


def build_observation(state: GameState, max_level: int = 4) -> np.ndarray:
    raise NotImplementedError
