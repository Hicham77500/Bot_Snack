"""Observation builder for the Snake RL environment (Khalil Jouani).

Transforme un ``GameState`` (fourni par le moteur d'Aya) en un vecteur
d'observation compact de **11 features float32**, conforme à CONTRACT.md.

Découpage des 11 features (indices) :

    0-3 : one-hot de la direction courante   (UP, DOWN, LEFT, RIGHT)
    4   : danger_front   (1.0 si collision droit devant, sinon 0.0)
    5   : danger_left    (1.0 si collision sur la gauche relative)
    6   : danger_right   (1.0 si collision sur la droite relative)
    7   : food_dx        (delta X normalisé tête -> nourriture)
    8   : food_dy        (delta Y normalisé tête -> nourriture)
    9   : level_norm     (level / max_level)
    10  : score_norm     (score / 100)

Note d'intégration : CONTRACT.md décrit ``snake_direction`` comme un tuple
(dx, dy), mais le moteur d'Aya l'expose sous forme d'entier (0-3). Cette
implémentation accepte **les deux formats** pour rester robuste quel que
soit le moteur mergé sur ``main``.
"""

from typing import Tuple

import numpy as np

OBSERVATION_SIZE = 11

# Deltas de déplacement par direction (convention grille : y vers le bas).
# 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT
_DELTAS = {
    0: (0, -1),   # UP
    1: (0, 1),    # DOWN
    2: (-1, 0),   # LEFT
    3: (1, 0),    # RIGHT
}

# Mapping inverse (delta -> index) pour le cas où le moteur renvoie un tuple.
_DELTA_TO_INDEX = {v: k for k, v in _DELTAS.items()}


def _direction_index(snake_direction) -> int:
    """Normalise ``snake_direction`` (int OU tuple) vers un index 0-3."""
    if isinstance(snake_direction, (int, np.integer)):
        return int(snake_direction)
    # tuple/list (dx, dy)
    dx, dy = snake_direction
    key = (int(np.sign(dx)), int(np.sign(dy)))
    return _DELTA_TO_INDEX.get(key, 3)  # défaut RIGHT si vecteur inattendu


def _is_blocked(
    cell: Tuple[int, int],
    board_width: int,
    board_height: int,
    obstacles: set,
    body: set,
) -> float:
    """Retourne 1.0 si ``cell`` est une collision (mur / obstacle / corps)."""
    x, y = cell
    if not (0 <= x < board_width and 0 <= y < board_height):
        return 1.0  # hors plateau
    if cell in obstacles:
        return 1.0  # obstacle du niveau
    if cell in body:
        return 1.0  # corps du serpent
    return 0.0


def build_observation(state, max_level: int = 4) -> np.ndarray:
    """Construit le vecteur d'observation à 11 features (float32).

    Args:
        state: ``GameState`` renvoyé par le moteur de jeu.
        max_level: nombre maximum de niveaux, pour normaliser ``level``.

    Returns:
        np.ndarray de shape (11,) et dtype float32.
    """
    body = list(state.snake_body)
    head = body[0]
    hx, hy = head

    dir_idx = _direction_index(state.snake_direction)
    dxf, dyf = _DELTAS[dir_idx]  # vecteur "devant"

    # Vecteurs relatifs gauche / droite par rapport au cap du serpent
    # (grille avec y vers le bas) :
    #   gauche = (dy, -dx)   droite = (-dy, dx)
    left_vec = (dyf, -dxf)
    right_vec = (-dyf, dxf)

    front_cell = (hx + dxf, hy + dyf)
    left_cell = (hx + left_vec[0], hy + left_vec[1])
    right_cell = (hx + right_vec[0], hy + right_vec[1])

    obstacles = set(map(tuple, state.obstacles))
    # Le corps compte comme danger (une case adjacente occupée par le corps
    # est mortelle).
    body_set = set(map(tuple, body))

    bw, bh = state.board_width, state.board_height

    danger_front = _is_blocked(front_cell, bw, bh, obstacles, body_set)
    danger_left = _is_blocked(left_cell, bw, bh, obstacles, body_set)
    danger_right = _is_blocked(right_cell, bw, bh, obstacles, body_set)

    # One-hot direction (indices 0-3)
    dir_onehot = [0.0, 0.0, 0.0, 0.0]
    dir_onehot[dir_idx] = 1.0

    # Position relative de la nourriture, normalisée par la taille du plateau
    fx, fy = state.food_position
    food_dx = (fx - hx) / bw
    food_dy = (fy - hy) / bh

    level_norm = state.level / max_level if max_level else 0.0
    score_norm = state.score / 100.0

    obs = np.array(
        [
            dir_onehot[0],
            dir_onehot[1],
            dir_onehot[2],
            dir_onehot[3],
            danger_front,
            danger_left,
            danger_right,
            food_dx,
            food_dy,
            level_norm,
            score_norm,
        ],
        dtype=np.float32,
    )
    return obs
