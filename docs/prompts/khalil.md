# Prompt Cursor — Khalil Jouani (Environment RL + Random Agent)

Copie-colle ce prompt dans Cursor après avoir checkout la branche `feat/environment`.

---

Tu travailles sur le projet **Bot_Snack** (Snake AI). Tu es **Khalil Jouani**, responsable de l'**Environnement RL** et du **Random Agent** (baseline).

## Contexte

- Repo : https://github.com/Hicham77500/Bot_Snack
- Branche : `feat/environment`
- Dossiers : `environment/`, `agents/random_agent.py`
- Contrat API : lire `CONTRACT.md`
- **Prérequis** : le game engine d'Aya doit être mergé sur `main` (ou rebase ta branche sur `main`)

## Ta mission

Wrapper le moteur Snake dans un environnement RL exploitable par l'IA, définir observation/reward, et produire la **baseline Random** officielle.

## Fichiers à implémenter

```
environment/
├── actions.py       # Déjà défini : UP=0, DOWN=1, LEFT=2, RIGHT=3
├── observation.py   # build_observation(state) -> np.ndarray (11 features)
├── reward.py        # compute_reward(state) -> float
└── snake_env.py     # reset() / step(action) gym-like

agents/
└── random_agent.py  # Baseline aléatoire + métriques
```

## API obligatoire

```python
env = SnakeEnv(level=1)
obs = env.reset(level=1)                          # np.ndarray shape (11,)
obs, reward, done, info = env.step(action)        # info = {score, level, steps, reason}
```

## Observation v1 (11 features float32)

Voir CONTRACT.md :
- Direction (dir_x, dir_y)
- danger_front, danger_left, danger_right (0.0 ou 1.0)
- food_dx, food_dy (normalisés)
- level / max_level
- score / 100

## Reward v1

| Événement | Valeur |
|-----------|--------|
| Nourriture | +10.0 |
| Mort | -10.0 |
| Survie (step) | +0.1 |

## Random Agent

```python
class RandomAgent:
    def select_action(self, state, training=False) -> int: ...
```

Produire les métriques baseline sur **100 parties** level 1 :

```bash
python -m training.evaluate --agent random --episodes 100 --level 1
```

Noter dans `results/experiments.csv` :

```
E0,Random baseline,<score_moyen>,Baseline,<date>,Khalil Jouani
```

## Script evaluate.py

Tu peux implémenter ou compléter `training/evaluate.py` pour la partie Random (Hicham complétera la partie DQN).

## Commits attendus

```
feat(env): wrap game engine in SnakeEnv
feat(env): implement 11-feature observation
feat(env): implement reward function
feat(agent): implement random baseline agent
feat(metrics): log E0 random baseline in experiments.csv
```

## Definition of Done

- [ ] `env.reset()` / `env.step()` fonctionnent avec le game engine d'Aya
- [ ] Observation = vecteur 11 features conforme CONTRACT.md
- [ ] Random Agent joue 100 parties sans crash
- [ ] Score moyen Random noté dans README et experiments.csv (E0)
- [ ] PR vers `main` avec commits signés Khalil

## Ne pas toucher

- `game/` (Aya)
- `agents/dqn_*` (Hicham)
- `ui/` (Marwan)
