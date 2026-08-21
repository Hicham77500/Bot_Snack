"""Reward computation for the Snake RL environment (Khalil Jouani).

Fonction de récompense **v1** conforme à CONTRACT.md :

    | Événement                 | Valeur |
    |---------------------------|--------|
    | Manger une nourriture     | +10.0  |
    | Mort (mur / soi / obstacle) | -10.0 |
    | Survie (chaque step)      | +0.1   |

Volontairement simple : on ne complexifie pas la reward tant que les
baselines Random et DQN ne sont pas fonctionnelles (garde-fou de l'énoncé).

Détail d'implémentation : détecter "manger" nécessite de comparer le score
avant/après le step. ``SnakeEnv`` fournit donc ``prev_score``. La signature
reste compatible avec le contrat (``state`` en premier argument) ; si
``prev_score`` n'est pas fourni, on retombe sur un mode dégradé
mort/survie uniquement.
"""

REWARD_FOOD = 10.0
REWARD_DEATH = -10.0
REWARD_SURVIVAL = 0.1


def compute_reward(state, prev_score: int | None = None) -> float:
    """Récompense de la dernière transition.

    Args:
        state: ``GameState`` après application de l'action.
        prev_score: score AVANT le step (permet de détecter la prise de
            nourriture). Optionnel pour rester conforme au contrat.

    Returns:
        float : la récompense de la transition.
    """
    # La mort prime sur tout le reste.
    if state.done:
        return REWARD_DEATH

    # Nourriture mangée : le score a augmenté durant ce step.
    if prev_score is not None and state.score > prev_score:
        return REWARD_FOOD

    # Sinon : petite récompense de survie.
    return REWARD_SURVIVAL
