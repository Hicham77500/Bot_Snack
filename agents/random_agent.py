"""Random baseline agent (Khalil Jouani).

Agent de référence : il choisit une action **au hasard** parmi les 4
directions à chaque pas, sans jamais apprendre. C'est la baseline
officielle contre laquelle on compare l'agent entraîné (DQN) — l'objectif
du projet n'est pas d'avoir un beau score, mais d'apprendre *mieux que le
hasard*, mesuré sur le même nombre de parties.

Le serpent démarre à une longueur > 1, donc le moteur ignore de toute
façon les demi-tours immédiats : un tirage uniforme sur les 4 actions
donne bien une baseline « hasard pur » honnête.

Conforme au contrat Agent :
    select_action(state, training=False) -> int
    save(path) / load(path)
"""

import numpy as np


class RandomAgent:
    """Sélectionne une action aléatoire uniforme à chaque step."""

    def __init__(self, action_size: int = 4, seed: int | None = None):
        self.action_size = action_size
        # RNG dédié => baseline reproductible quand une seed est fournie.
        self._rng = np.random.default_rng(seed)

    def select_action(self, state: np.ndarray, training: bool = False) -> int:
        """Retourne une action aléatoire dans [0, action_size).

        ``state`` et ``training`` sont ignorés (agent sans mémoire), mais
        présents pour respecter l'interface commune des agents.
        """
        return int(self._rng.integers(self.action_size))

    def save(self, path: str) -> None:
        """Aucun poids à sauvegarder pour un agent aléatoire (no-op)."""
        return None

    def load(self, path: str) -> None:
        """Aucun poids à charger pour un agent aléatoire (no-op)."""
        return None
