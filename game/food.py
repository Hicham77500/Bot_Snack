"""
food.py — Nourriture : spawn aléatoire hors obstacles/corps du serpent.
"""

from typing import List, Tuple

Position = Tuple[int, int]


class Food:
    """Position de la nourriture sur le plateau."""

    def __init__(self):
        self.position: Position = (0, 0)

    def spawn(self, board, snake_body: List[Position]) -> Position:
        """
        Place la nourriture sur une case libre aléatoire du plateau
        (ni sur le corps du serpent, ni sur un obstacle du niveau).
        """
        self.position = board.random_free_cell(forbidden=snake_body)
        return self.position
