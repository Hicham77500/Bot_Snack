"""Reward computation for Snake RL environment."""

from game.game import GameState

REWARD_FOOD = 10.0
REWARD_DEATH = -10.0
REWARD_SURVIVAL = 0.1


def compute_reward(state: GameState) -> float:
    raise NotImplementedError
