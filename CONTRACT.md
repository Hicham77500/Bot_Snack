# Contrat d'API — Bot_Snack

Document figé en Phase 0. Toute modification doit être validée par l'équipe avant implémentation.

## Responsabilités

| Membre | Dossiers | Rôle |
|--------|----------|------|
| Hicham Guendouz | `agents/dqn_*`, `training/` | Lead AI, DQN, entraînement, intégration |
| Aya El JANATI | `game/` | Game engine, niveaux, collisions |
| Khalil Jouani | `environment/`, `agents/random_agent.py` | Environnement RL, baseline, métriques |
| Marwan Ghrairi | `ui/` | Interface, visualisation, monitoring |

## Contrat Environment (Khalil)

Interface gym-like obligatoire :

```python
state = env.reset(level: int = 1) -> np.ndarray
next_state, reward, done, info = env.step(action: int) -> tuple
```

### Actions (`environment/actions.py`)

Espace discret, 4 actions :

| Index | Nom |
|-------|-----|
| 0 | UP |
| 1 | DOWN |
| 2 | LEFT |
| 3 | RIGHT |

Les actions interdites (demi-tour immédiat) sont filtrées par l'environnement ou le game engine.

### Observation v1 (`environment/observation.py`)

Vecteur de **11 features** (float32) :

| Index | Feature | Description |
|-------|---------|-------------|
| 0-3 | dir_x, dir_y, one-hot direction | Direction actuelle du serpent |
| 4 | danger_front | 1.0 si collision devant, sinon 0.0 |
| 5 | danger_left | 1.0 si collision à gauche, sinon 0.0 |
| 6 | danger_right | 1.0 si collision à droite, sinon 0.0 |
| 7 | food_dx | Delta X normalisé vers la nourriture |
| 8 | food_dy | Delta Y normalisé vers la nourriture |
| 9 | level | Niveau actuel normalisé (level / max_level) |
| 10 | score_norm | Score normalisé (score / 100) |

### Reward v1 (`environment/reward.py`)

| Événement | Valeur |
|-----------|--------|
| Manger une nourriture | +10.0 |
| Mort (collision) | -10.0 |
| Survie (chaque step) | +0.1 |

Ne pas complexifier avant d'avoir une baseline Random + DQN fonctionnelle.

### Info dict

```python
info = {
    "score": int,
    "level": int,
    "steps": int,
    "reason": str | None,  # "food", "wall", "self", "obstacle"
}
```

## Contrat Game Engine (Aya)

Le moteur de jeu **ne dépend pas de Pygame**. Il doit tourner en mode headless.

```python
class Game:
    def reset(self, level: int = 1) -> GameState: ...
    def step(self, action: int) -> GameState: ...
    def get_state(self) -> GameState: ...
    def get_reward(self) -> float: ...
    def is_done(self) -> bool: ...
    def get_score(self) -> int: ...
    def get_level(self) -> int: ...
```

### GameState

```python
@dataclass
class GameState:
    snake_body: list[tuple[int, int]]
    snake_direction: tuple[int, int]
    food_position: tuple[int, int]
    obstacles: list[tuple[int, int]]
    board_width: int
    board_height: int
    score: int
    level: int
    done: bool
    steps: int
```

## Contrat Agents

```python
class Agent:
    def select_action(self, state: np.ndarray, training: bool = False) -> int: ...
    def save(self, path: str) -> None: ...
    def load(self, path: str) -> None: ...
```

## Contrat Training (Hicham)

- Sauvegarde du meilleur modèle : `models/best_agent.pth`
- Rechargement depuis un script indépendant : `training/evaluate.py`
- Comparaison Random vs DQN sur le **même nombre de parties**

## Convention de commits

```
feat(game): ...
feat(env): ...
feat(agent): ...
feat(ai): ...
feat(training): ...
feat(ui): ...
feat(metrics): ...
fix(...): ...
docs(...): ...
```

## Branches

| Branche | Responsable |
|---------|-------------|
| `main` | Hicham (merge) |
| `feat/game-engine` | Aya |
| `feat/environment` | Khalil |
| `feat/dqn-training` | Hicham |
| `feat/ui` | Marwan |
