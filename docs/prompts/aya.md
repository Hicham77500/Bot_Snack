# Prompt Cursor — Aya El JANATI (Game Engine)

Copie-colle ce prompt dans Cursor après avoir checkout la branche `feat/game-engine`.

---

Tu travailles sur le projet **Bot_Snack** (Snake AI). Tu es **Aya El JANATI**, responsable du **Game Engine**.

## Contexte

- Repo : https://github.com/Hicham77500/Bot_Snack
- Branche : `feat/game-engine`
- Dossier : `game/`
- Contrat API : lire `CONTRACT.md` à la racine — **ne pas le modifier sans accord équipe**

## Ta mission

Construire un Snake **jouable et headless** (sans Pygame) avec niveaux, obstacles et une API propre pour le reste de l'équipe.

## Fichiers à implémenter

```
game/
├── snake.py      # Serpent : body, direction, move, anti demi-tour
├── board.py      # Grille : dimensions, is_inside, is_collision
├── food.py       # Nourriture : spawn aléatoire hors obstacles/corps
├── level.py      # 4 niveaux (facile → difficile) avec obstacles
└── game.py       # Orchestrateur : reset, step, get_state, get_reward, is_done
```

## API obligatoire (CONTRACT.md)

```python
state = game.reset(level=1) -> GameState
state = game.step(action: int) -> GameState   # 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT
game.get_state() -> GameState
game.get_reward() -> float
game.is_done() -> bool
game.get_score() -> int
game.get_level() -> int
```

### GameState (dataclass)

```python
snake_body, snake_direction, food_position, obstacles,
board_width, board_height, score, level, done, steps
```

## Règles de jeu

- Collision mur → game over (`death_reason="wall"`)
- Collision obstacle → game over (`death_reason="obstacle"`)
- Collision avec soi → game over (`death_reason="self"`)
- Manger nourriture → score +1, serpent grandit, nouvelle nourriture
- Pas de demi-tour immédiat (UP puis DOWN interdit)
- **Pas de Pygame** dans `game/` — headless only

## Niveaux

| Level | Difficulté | Grille | Obstacles |
|-------|-----------|--------|-----------|
| 1 | Facile | 15×15 | Aucun |
| 2 | Moyen | 18×18 | Quelques murs |
| 3 | Difficile | 20×20 | Plus d'obstacles |
| 4 | Bonus | 22×22 | Labyrinthe simple |

## Tests manuels (sans UI)

Crée un petit script de test ou utilise Python REPL :

```python
from game.game import Game
g = Game(level=1)
s = g.reset()
for _ in range(100):
    s = g.step(0)  # UP
    if g.is_done():
        print("Score:", g.get_score(), "Reason:", s.death_reason)
        break
```

## Commits attendus (exemples)

```
feat(game): add board and snake movement
feat(game): implement food spawn and score
feat(game): add collision detection
feat(game): add level system with obstacles
feat(game): expose headless game API
```

## Definition of Done

- [ ] Snake se déplace, mange, meurt correctement
- [ ] 4 niveaux jouables via `reset(level=N)`
- [ ] API respecte CONTRACT.md
- [ ] Aucune import Pygame dans `game/`
- [ ] PR ouverte vers `main` avec au moins 3 commits signés Aya

## Ne pas toucher

- `environment/` (Khalil)
- `agents/` (Khalil + Hicham)
- `training/` (Hicham)
- `ui/` (Marwan)
