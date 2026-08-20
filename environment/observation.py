"""Observation builder — TODO: implement (Khalil Jouani)."""

import numpy as np

from game.game import GameState

OBSERVATION_SIZE = 11


def build_observation(state: GameState, max_level: int = 4) -> np.ndarray:
    """Build 11-feature observation vector. See CONTRACT.md."""
    raise NotImplementedError("Khalil: implement build_observation()")
