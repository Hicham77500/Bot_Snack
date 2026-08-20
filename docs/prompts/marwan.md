# Prompt Cursor — Marwan Ghrairi (UI + Visualisation)

Copie-colle ce prompt dans Cursor après avoir checkout la branche `feat/ui`.

---

Tu travailles sur le projet **Bot_Snack** (Snake AI). Tu es **Marwan Ghrairi**, responsable de l'**interface Pygame** et de la **visualisation**.

## Contexte

- Repo : https://github.com/Hicham77500/Bot_Snack
- Branche : `feat/ui`
- Dossier : `ui/`
- Contrat API : lire `CONTRACT.md`
- **Prérequis** : game engine d'Aya mergé sur `main`

## Ta mission

Construire l'interface visible du projet : menu, jeu manuel, mode Auto AI, graphiques d'apprentissage.

## Fichiers à implémenter

```
ui/
├── game_view.py    # Menu + jeu clavier
├── auto_play.py    # Mode AUTO AI (charge best_agent.pth)
└── statistics.py   # Courbes Random vs DQN (matplotlib)
```

## Écran menu

```
SNAKE AI — Bot_Snack

[ PLAY ]          → mode clavier
[ AUTO AI ]       → charge models/best_agent.pth, agent joue seul
[ LEVEL SELECT ]  → cycle niveaux 1-4

Level: 1
Score: 42
Best: 58
```

## Mode PLAY

- Flèches = actions (UP/DOWN/LEFT/RIGHT)
- Afficher grille, serpent, nourriture, obstacles
- HUD : Level, Score, Steps
- Game Over → touche R pour restart

## Mode AUTO AI

Afficher en temps réel :

```
Episode: 1245
Level: 3
Score: 42
Best: 58
Agent: DQN
```

Brancher sur `agents/dqn_agent.py` + `environment/snake_env.py` (disponibles après merge Hicham/Khalil).

```bash
python -m ui.auto_play --level 1 --model models/best_agent.pth
```

## Visualisation apprentissage (`statistics.py`)

Graphique :

- Courbe score par épisode (Random vs DQN)
- Bar chart : score moyen Random vs Trained

```bash
python -m ui.statistics --episodes 100 --model models/best_agent.pth
```

Sauvegarder dans `results/curves/comparison.png`.

## Bonus (si le temps le permet)

Afficher ce que l'agent **perçoit** :

```
Observation:
Front : danger
Left  : safe
Right : safe
Action: RIGHT
```

Très utile pour la vidéo de présentation (10-15 min).

## Commits attendus

```
feat(ui): add pygame menu with play and level select
feat(ui): implement manual keyboard gameplay
feat(ui): add auto AI mode with DQN agent
feat(metrics): add learning curve comparison plot
feat(ui): display agent observation panel
```

## Definition of Done

- [ ] Jeu jouable au clavier via `python -m ui.game_view`
- [ ] Mode AUTO AI fonctionne avec modèle entraîné
- [ ] Graphique Random vs DQN généré
- [ ] PR vers `main` avec commits signés Marwan

## Priorité (Jour 1 vs Jour 2)

**Jour 1** : ne pas bloquer l'équipe sur l'UI — l'entraînement passe avant.  
**Jour 2** : polish UI + graphiques + bonus observation.

## Ne pas toucher

- `game/` (Aya) — consommer l'API seulement
- `environment/` (Khalil)
- `agents/dqn_*` (Hicham) — importer seulement
