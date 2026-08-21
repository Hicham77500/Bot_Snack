"""
board.py — Grille de jeu pour Bot_Snack.

Représente le plateau (dimensions + obstacles) et fournit les
primitives de test utilisées par game.py : is_inside, is_obstacle,
is_collision. Headless, aucune dépendance graphique.
"""

import random
from typing import List, Tuple

Position = Tuple[int, int]


class Board:
    """Grille rectangulaire du jeu, avec une liste d'obstacles fixes."""

    def __init__(self, width: int, height: int, obstacles: List[Position] = None):
        self.width = width
        self.height = height
        self.obstacles: List[Position] = list(obstacles) if obstacles else []

    def is_inside(self, pos: Position) -> bool:
        """True si `pos` est à l'intérieur des limites du plateau."""
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def is_obstacle(self, pos: Position) -> bool:
        """True si `pos` correspond à un obstacle fixe du niveau."""
        return pos in self.obstacles

    def is_collision(self, pos: Position) -> bool:
        """
        True si `pos` est une collision "plateau" : hors grille ou
        sur un obstacle. Ne teste PAS la collision avec le corps du
        serpent (gérée dans snake.py / game.py).
        """
        return (not self.is_inside(pos)) or self.is_obstacle(pos)

    def random_free_cell(self, forbidden: List[Position]) -> Position:
        """Retourne une case libre aléatoire (hors `forbidden` + obstacles)."""
        forbidden_set = set(forbidden) | set(self.obstacles)
        free_cells = [
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if (x, y) not in forbidden_set
        ]
        if not free_cells:
            raise RuntimeError("Aucune case libre disponible sur le plateau.")
        return random.choice(free_cells)
