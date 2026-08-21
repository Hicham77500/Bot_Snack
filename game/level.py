"""
level.py — Définition des 4 niveaux (facile → difficile).

| Level | Difficulté | Grille | Obstacles          |
|-------|-----------|--------|--------------------|
| 1     | Facile    | 15x15  | Aucun              |
| 2     | Moyen     | 18x18  | Quelques murs      |
| 3     | Difficile | 20x20  | Plus d'obstacles   |
| 4     | Bonus     | 22x22  | Labyrinthe simple  |
"""

from typing import List, Tuple

Position = Tuple[int, int]


def _level_1_obstacles(w: int, h: int) -> List[Position]:
    return []


def _level_2_obstacles(w: int, h: int) -> List[Position]:
    """Quelques murs isolés, symétriques, loin des bords."""
    obstacles: List[Position] = []
    obstacles += [(4, y) for y in range(3, 7)]
    obstacles += [(w - 5, y) for y in range(h - 7, h - 3)]
    return obstacles


def _level_3_obstacles(w: int, h: int) -> List[Position]:
    """Davantage d'obstacles, dont une ligne médiane trouée."""
    obstacles: List[Position] = []
    obstacles += [(4, y) for y in range(2, 9)]
    obstacles += [(w - 5, y) for y in range(h - 9, h - 2)]
    mid = h // 2
    obstacles += [(x, mid) for x in range(6, w - 6) if x % 3 != 0]  # ligne trouée
    return obstacles


def _level_4_obstacles(w: int, h: int) -> List[Position]:
    """Labyrinthe simple en peigne (couloirs alternés)."""
    obstacles: List[Position] = []
    row = 4
    toggle = 0
    while row < h - 4:
        if toggle % 2 == 0:
            obstacles += [(x, row) for x in range(2, w - 4)]
        else:
            obstacles += [(x, row) for x in range(4, w - 2)]
        row += 4
        toggle += 1
    return obstacles


LEVELS = {
    1: {"name": "Facile", "width": 15, "height": 15, "obstacles_fn": _level_1_obstacles},
    2: {"name": "Moyen", "width": 18, "height": 18, "obstacles_fn": _level_2_obstacles},
    3: {"name": "Difficile", "width": 20, "height": 20, "obstacles_fn": _level_3_obstacles},
    4: {"name": "Bonus", "width": 22, "height": 22, "obstacles_fn": _level_4_obstacles},
}


def build_level(level: int):
    """Retourne (width, height, obstacles) pour le niveau demandé (1 à 4)."""
    if level not in LEVELS:
        raise ValueError(f"Niveau invalide: {level}. Attendu: {sorted(LEVELS)}")
    cfg = LEVELS[level]
    obstacles = cfg["obstacles_fn"](cfg["width"], cfg["height"])
    return cfg["width"], cfg["height"], obstacles
