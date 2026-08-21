"""Gym-like RL environment for Snake (Khalil Jouani).

``SnakeEnv`` enveloppe le moteur de jeu headless d'Aya (``game.Game``) et
expose l'interface gym-like attendue par les agents et l'entraînement :

    env = SnakeEnv(level=1)
    obs = env.reset(level=1)                     # np.ndarray shape (11,)
    obs, reward, done, info = env.step(action)   # info = {score, level, steps, reason}

Responsabilités de cette couche (contrat Khalil) :
  * traduire ``GameState`` -> vecteur d'observation (via ``build_observation``)
  * calculer la récompense v1 (via ``compute_reward``)
  * fournir un ``info`` propre et un garde-fou anti-boucle (``max_steps``)

Le moteur de jeu reste la source de vérité pour la logique Snake ; on ne
duplique pas ses règles ici.
"""

import numpy as np

from environment.actions import NUM_ACTIONS
from environment.observation import OBSERVATION_SIZE, build_observation
from environment.reward import compute_reward
from game.game import Game


class SnakeEnv:
    """Environnement RL : interface reset() / step(action). Voir CONTRACT.md."""

    def __init__(self, level: int = 1, max_level: int = 4, max_steps: int | None = None):
        """
        Args:
            level: niveau de départ (1 à 4).
            max_level: nombre total de niveaux (normalisation de l'observation).
            max_steps: nombre max de pas par épisode avant arrêt forcé
                (garde-fou anti-boucle infinie). Si None, une valeur par
                défaut proportionnelle à la taille du plateau est utilisée
                au premier reset.
        """
        self.max_level = max_level
        self.level = level
        self._max_steps = max_steps

        self.game = Game(level=level)
        self._prev_score = 0
        self._last_obs: np.ndarray | None = None

    @property
    def observation_size(self) -> int:
        return OBSERVATION_SIZE

    @property
    def action_size(self) -> int:
        return NUM_ACTIONS

    # ------------------------------------------------------------------
    # API gym-like
    # ------------------------------------------------------------------

    def reset(self, level: int | None = None) -> np.ndarray:
        """Réinitialise l'environnement et retourne l'observation initiale."""
        if level is not None:
            self.level = level

        state = self.game.reset(level=self.level)
        self._prev_score = state.score

        # Garde-fou anti-boucle : par défaut, ~ (largeur * hauteur) pas.
        if self._max_steps is None:
            self._max_steps = state.board_width * state.board_height * 4

        self._last_obs = build_observation(state, max_level=self.max_level)
        return self._last_obs

    def step(self, action: int) -> tuple[np.ndarray, float, bool, dict]:
        """Applique une action et retourne (obs, reward, done, info)."""
        prev_score = self._prev_score

        state = self.game.step(action)
        obs = build_observation(state, max_level=self.max_level)
        reward = compute_reward(state, prev_score=prev_score)

        done = bool(state.done)
        reason = state.death_reason

        # Garde-fou anti-boucle : on coupe l'épisode s'il traîne trop.
        if not done and state.steps >= self._max_steps:
            done = True
            reason = reason or "max_steps"

        info = {
            "score": state.score,
            "level": state.level,
            "steps": state.steps,
            "reason": reason,
        }

        self._prev_score = state.score
        self._last_obs = obs
        return obs, reward, done, info
