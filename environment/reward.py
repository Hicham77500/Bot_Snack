"""Reward computation — TODO: implement (Khalil Jouani)."""

from game.game import GameState

REWARD_FOOD = 10.0
REWARD_DEATH = -10.0
REWARD_SURVIVAL = 0.1


def compute_reward(state: GameState) -> float:
    """Return reward for the last transition. See CONTRACT.md."""
    raise NotImplementedError("Khalil: implement compute_reward()")
