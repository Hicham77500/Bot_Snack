"""Snake game engine — headless, no Pygame dependency."""

from game.game import Game, GameState
from game.snake import Snake
from game.board import Board
from game.food import Food
from game.level import Level

__all__ = ["Game", "GameState", "Snake", "Board", "Food", "Level"]
