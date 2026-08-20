"""Reward computation for Snake RL environment."""

from game.game import GameState

REWARD_FOOD = 10.0
REWARD_DEATH = -10.0
REWARD_SURVIVAL = 0.1


def compute_reward(state: GameState) -> float:
    """Return reward for the last transition based on game state."""
    if state.done:
        if state.death_reason:
            return REWARD_DEATH
    if state.last_reward >= REWARD_FOOD:
        return REWARD_FOOD
    return REWARD_SURVIVAL
