"""RL environment layer for Snake."""

from environment.snake_env import SnakeEnv
from environment.observation import build_observation
from environment.reward import compute_reward
from environment.actions import Action, NUM_ACTIONS, ACTION_NAMES

__all__ = [
    "SnakeEnv",
    "build_observation",
    "compute_reward",
    "Action",
    "NUM_ACTIONS",
    "ACTION_NAMES",
]
