# Bot_Snack — Snake AI (Gaming Agent)

Projet de groupe — Agent capable de jouer au Snake à niveaux, avec comparaison objective contre un agent aléatoire.

## Équipe

| Membre | Rôle |
|--------|------|
| Hicham Guendouz | Lead AI & Architecture — DQN, entraînement, intégration |
| Aya El JANATI | Game Engine — Snake, niveaux, collisions |
| Khalil Jouani | Environment RL — observation, reward, Random Agent |
| Marwan Ghrairi | UI — Pygame, visualisation, monitoring |

**Nom d'équipe :** Bot_Snack

## Jeu choisi

**Snake à niveaux** (4 niveaux de difficulté croissante avec obstacles).

Critères de choix :
- Environnement opérationnel en moins de 30 minutes
- Score mesurable immédiatement
- Espace d'actions discret (4 directions)
- Entraînement rapide sans GPU

## Méthode d'apprentissage

**DQN (Deep Q-Network)**

Pourquoi DQN pour ce jeu :
- Actions discrètes (UP / DOWN / LEFT / RIGHT)
- Observations vectorielles compactes (11 features)
- Pas besoin de GPU pour converger sur une petite grille
- Replay buffer + target network = stabilité raisonnable en 2 jours

## Observation (v1)

L'agent observe un vecteur de **11 features** :

| Feature | Description |
|---------|-------------|
| dir_x, dir_y | Direction actuelle |
| danger_front | Collision devant (0/1) |
| danger_left | Collision à gauche (0/1) |
| danger_right | Collision à droite (0/1) |
| food_dx, food_dy | Direction vers la nourriture (normalisé) |
| level | Niveau actuel (normalisé) |
| score_norm | Score (normalisé) |

> Document complet : [CONTRACT.md](CONTRACT.md)

## Actions

| Index | Action |
|-------|--------|
| 0 | UP |
| 1 | DOWN |
| 2 | LEFT |
| 3 | RIGHT |

Les demi-tours immédiats sont bloqués par le moteur de jeu.

## Reward (v1)

| Événement | Valeur |
|-----------|--------|
| Manger une nourriture | +10.0 |
| Mort (mur / soi / obstacle) | -10.0 |
| Survie (chaque step) | +0.1 |

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Utilisation

```bash
python -m ui.game_view --level 1
python -m training.evaluate --agent random --episodes 100 --level 1
python -m training.train --episodes 500 --level 1
python -m training.evaluate --agent dqn --model models/best_agent.pth --episodes 100
python -m ui.auto_play --level 1 --model models/best_agent.pth
python -m ui.statistics --episodes 100 --model models/best_agent.pth
```

## Structure du projet

```text
├── game/           # Moteur Snake headless (Aya)
├── environment/    # Wrapper RL (Khalil)
├── agents/         # Random + DQN (Khalil + Hicham)
├── training/       # Entraînement + évaluation (Hicham)
├── ui/             # Pygame + graphiques (Marwan)
├── models/         # best_agent.pth (hors Git — lien externe)
├── results/        # experiments.csv + courbes
├── CONTRACT.md     # Contrat d'API équipe
└── README.md
```

## Carnet d'essais

Voir [results/experiments.csv](results/experiments.csv).

| Exp | Modification | Score moyen | Résultat |
|-----|-------------|------------:|----------|
| E0 | Random baseline (100 parties, level 1, seed 42) | 0.060 | Baseline |
| E1 | DQN initial | — | — |
| E2+ | À compléter | — | — |

## Résultats

| Agent | Score moyen | Score max | Parties |
|-------|------------:|----------:|--------:|
| Random | 0.060 | 2 | 100 |
| DQN | — | — | — |

> Baseline Random mesurée sur level 1, 100 parties, `--seed 42` (reproductible).
> Sur plusieurs seeds, le score moyen Random reste dans ~0.06–0.15 : le hasard
> ne mange quasiment jamais. C'est la référence à battre. Comparaison DQN vs
> Random à faire sur le **même nombre de parties**.

**Reproduire la baseline :**

```bash
python -m training.evaluate --agent random --episodes 100 --level 1 --seed 42
```

## Liens externes

- **Modèle entraîné** (`best_agent.pth`) : _à ajouter (Google Drive / release GitHub)_
- **Vidéo de présentation** (10-15 min) : _à ajouter_

## Convention de commits

```
feat(game): implement snake movement
feat(env): expose snake observation
feat(agent): implement random baseline
feat(ai): implement DQN network
feat(training): add replay buffer
feat(ui): add auto AI mode
feat(metrics): add learning curve
```

## Roadmap

### Jour 1
1. Snake fonctionnel
2. Environment + Random Agent
3. DQN + premier entraînement
4. Score Random vs DQN (même si DQN < Random)

### Jour 2
1. Tuning hyperparamètres
2. Save/Load best_agent.pth
3. Courbes + carnet d'essais
4. Auto AI visuel
5. Niveaux 2-3-4

## Checklist livrables

- [ ] Agent aléatoire jouable à tout moment
- [ ] Observation / Actions / Reward documentés
- [ ] DQN entraîné + modèle sauvegardé (lien externe)
- [ ] Courbe Random vs DQN
- [ ] Carnet d'essais complet
- [ ] Rechargement depuis script neuf (`evaluate.py`)
- [ ] 3 runs reproductibles
- [ ] Vidéo 10-15 min (lien dans README)
- [ ] Repo public

## Branches Git

| Branche | Responsable |
|---------|-------------|
| `main` | Hicham |
| `feat/game-engine` | Aya |
| `feat/environment` | Khalil |
| `feat/dqn-training` | Hicham |
| `feat/ui` | Marwan |
