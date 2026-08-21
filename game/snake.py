"""
snake.py — Le serpent : corps, direction, déplacement, anti demi-tour.

Directions (contrat) : 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT.
Convention grille : y augmente vers le bas (comme un écran).
"""

from typing import List, Tuple

Position = Tuple[int, int]

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

_DELTAS = {
    UP: (0, -1),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    RIGHT: (1, 0),
}

_OPPOSITE = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}


class Snake:
    """Corps du serpent. `body[0]` est la tête, le reste est la queue."""

    def __init__(self, start: Position, direction: int = RIGHT, length: int = 3):
        self.direction = direction
        dx, dy = _DELTAS[_OPPOSITE[direction]]
        # Construit le corps derrière la tête, dans le sens opposé au déplacement.
        self.body: List[Position] = [
            (start[0] + dx * i, start[1] + dy * i) for i in range(length)
        ]
        self._grow_pending = 0

    @property
    def head(self) -> Position:
        return self.body[0]

    def set_direction(self, direction: int) -> None:
        """
        Change la direction du serpent, sauf si c'est un demi-tour
        immédiat (ex: direction actuelle UP, interdiction de repartir
        directement DOWN). Ignore les valeurs invalides.
        """
        if direction not in _DELTAS:
            return
        if len(self.body) > 1 and direction == _OPPOSITE[self.direction]:
            return  # demi-tour interdit
        self.direction = direction

    def next_head(self) -> Position:
        """Calcule la position de la prochaine tête sans déplacer le serpent."""
        dx, dy = _DELTAS[self.direction]
        hx, hy = self.head
        return (hx + dx, hy + dy)

    def grow(self, amount: int = 1) -> None:
        """Programme une croissance du serpent au(x) prochain(s) move()."""
        self._grow_pending += amount

    def move(self) -> Position:
        """
        Avance le serpent d'une case dans `self.direction`.
        Retourne la nouvelle position de la tête.
        """
        new_head = self.next_head()
        self.body.insert(0, new_head)
        if self._grow_pending > 0:
            self._grow_pending -= 1
        else:
            self.body.pop()
        return new_head

    def collides_with_self(self, pos: Position = None) -> bool:
        """True si `pos` (par défaut la tête) touche le reste du corps."""
        pos = pos if pos is not None else self.head
        return pos in self.body[1:]
