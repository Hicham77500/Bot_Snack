"""Discrete action space for Snake RL."""

from enum import IntEnum

NUM_ACTIONS = 4

ACTION_NAMES = ["UP", "DOWN", "LEFT", "RIGHT"]


class Action(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
