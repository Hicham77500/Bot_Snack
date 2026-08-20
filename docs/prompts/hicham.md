# Prompt Cursor — Hicham Guendouz (DQN + Training + Intégration)

Copie-colle ce prompt dans Cursor après avoir checkout la branche `feat/dqn-training`.

---

Tu travailles sur le projet **Bot_Snack** (Snake AI). Tu es **Hicham Guendouz**, Lead AI — responsable du **DQN**, de l'**entraînement** et de l'**intégration**.

## Contexte

- Repo : https://github.com/Hicham77500/Bot_Snack
- Branche : `feat/dqn-training`
- Dossiers : `agents/dqn_agent.py`, `agents/network.py`, `agents/replay_buffer.py`, `training/`
- Contrat API : lire `CONTRACT.md`
- **Prérequis** : environnement RL de Khalil mergé sur `main`

## Ta mission

Implémenter un agent DQN qui apprend à jouer au Snake, l'entraîner, sauvegarder le meilleur modèle, et prouver qu'il bat (ou non) le Random Agent de façon mesurée.

## Fichiers à implémenter

```
agents/
├── network.py        # DQNNetwork (MLP PyTorch)
├── replay_buffer.py  # Experience replay
└── dqn_agent.py      # select_action, remember, train_step, save, load

training/
├── train.py          # Boucle d'entraînement + sauvegarde best_agent.pth
├── evaluate.py       # Script indépendant : reload + test (Random ET DQN)
└── experiments.py    # log_experiment() -> results/experiments.csv
```

## DQN — composants obligatoires

- Neural Network (input=11, output=4)
- Replay Buffer (capacity ~10000)
- Epsilon-greedy (decay)
- Target Network (update périodique)
- Training loop

## Hyperparamètres de départ

```python
lr=1e-3, gamma=0.99, epsilon=1.0, epsilon_min=0.01,
epsilon_decay=0.995, batch_size=64, target_update=10
```

## Entraînement

```bash
python -m training.train --episodes 500 --level 1
# Sauvegarde : models/best_agent.pth (hors Git — .gitignore)
```

## Validation (exigence prof)

1. **Rechargement depuis script neuf** :

```bash
python -m training.evaluate --agent dqn --model models/best_agent.pth --episodes 100
```

2. **Comparaison Random vs DQN** — même nombre de parties :

```bash
python -m training.evaluate --agent random --episodes 100
python -m training.evaluate --agent dqn --model models/best_agent.pth --episodes 100
```

3. **Carnet d'essais** — une amélioration à la fois :

```
E0 Random baseline (Khalil)
E1 DQN initial
E2 Reward modifiée
E3 Epsilon tuning
...
```

4. **3 runs reproductibles** avec seeds différentes — analyser variance des courbes

## Courbe de progression

Sauvegarder dans `results/curves/training_curve.png` (hors Git ou lien externe).

## Commits attendus

```
feat(ai): implement DQN network
feat(training): add replay buffer
feat(ai): implement DQN agent with epsilon greedy
feat(training): add training loop with model checkpoint
feat(training): add standalone evaluate script
feat(metrics): log E1 DQN baseline experiment
```

## Definition of Done

- [ ] DQN s'entraîne sans crash (même si score faible au début)
- [ ] `models/best_agent.pth` sauvegardé et rechargé via `evaluate.py`
- [ ] Score Random vs DQN documenté (README + experiments.csv)
- [ ] Courbe de progression tracée
- [ ] Merge des PRs Aya/Khalil/Marwan sur `main`
- [ ] PR DQN vers `main`

## Rôle Lead

- Valider les PRs des autres
- Ne pas coder à leur place — review + merge
- Garder `main` stable

## Ne pas toucher

- `game/` (Aya)
- `environment/observation.py` sauf accord (Khalil)
- `ui/` (Marwan)
