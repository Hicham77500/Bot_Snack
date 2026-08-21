# Avancée — Interface UI (Marwan)

> Fichier de reprise. Si la session crash, relis ce fichier pour repartir au bon endroit.
> Dernière mise à jour : 2026-08-21 — branche `feat/ui`.

## TL;DR

L'interface Pygame + visualisation est **fonctionnellement terminée** et testée en headless.
Elle tourne **dès maintenant**, sans attendre les modules des autres (game/env/agents encore stubs),
grâce à un **moteur de secours** confiné à `ui/`. Dès que les vrais modules seront mergés, ils sont
utilisés automatiquement (aucune ligne d'UI à changer).

## Definition of Done (marwan.md)

- [x] Jeu jouable au clavier via `python -m ui.game_view`
- [x] Mode AUTO AI fonctionne (fallback heuristique tant que `best_agent.pth` absent, vrai DQN sinon)
- [x] Graphique Random vs DQN généré → `results/curves/comparison.png`
- [x] Bonus : panneau d'observation de l'agent (Front/Left/Right + Action)
- [ ] Commits signés Marwan + PR vers `main` **(reste à faire — voir "Prochaines étapes")**

## Fichiers `ui/`

| Fichier | Rôle | État |
|---------|------|------|
| `game_view.py` | Menu + jeu clavier (PLAY / AUTO AI / LEVEL SELECT) | ✅ complet |
| `auto_play.py` | Mode AUTO AI, agent joue seul, stats live + observation | ✅ complet |
| `statistics.py` | Courbes Random vs DQN (matplotlib, headless) | ✅ complet |
| `render.py` | Helpers de rendu Pygame (board, sidebar, HUD, banner) | ✅ complet |
| `engine_adapter.py` | Choisit le vrai module d'équipe, sinon le fallback | ✅ complet |
| `fallback_engine.py` | Moteur/env/agents de secours conformes à `CONTRACT.md` | ✅ complet |

## Architecture clé : le pattern adaptateur

`engine_adapter.py` renvoie toujours `(objet, is_real, label)` :
- il tente d'importer le vrai module (`game.Game`, `environment.SnakeEnv`, `agents.DQNAgent`,
  `agents.RandomAgent`) et le **sonde** (`reset()`, action valide…) ;
- si le module lève `NotImplementedError` ou échoue → **fallback** (`ui/fallback_engine.py`).

Conséquence : l'UI n'affiche **jamais** un placeholder comme s'il était le vrai DQN entraîné
(label "heuristic placeholder" / "fallback" visible à l'écran et sur le graphe).

## Contrat respecté (`CONTRACT.md`)

- Actions : `0=UP 1=DOWN 2=LEFT 3=RIGHT`
- Observation : vecteur 11 features float32 (`build_observation`)
- `GameState` : mêmes champs que le contrat
- Env gym-like : `reset(level)` / `step(action) -> (obs, reward, done, info)`
- Reward : +10 food / -10 mort / +0.1 survie

## Comment lancer / tester

```bash
# Jeu clavier (flèches/WASD, Esc = menu, R = restart après game over)
python -m ui.game_view
python -m ui.game_view --level 3

# Mode AUTO AI (agent joue seul)
python -m ui.auto_play --level 1 --model models/best_agent.pth

# Graphique Random vs DQN -> results/curves/comparison.png
python -m ui.statistics --episodes 100 --level 1
```

### Tests headless (sans écran, utile pour valider vite)

```bash
# Windows PowerShell : $env:SDL_VIDEODRIVER='dummy'; python -m ui.statistics --episodes 15
SDL_VIDEODRIVER=dummy python -m ui.statistics --episodes 15 --level 1
SDL_VIDEODRIVER=dummy python -c "from ui import auto_play; auto_play.run_auto(level=2, max_episodes=2)"
```

Dernier run headless OK (2026-08-21) : statistics + auto_play + init game_view → ✅.

## État git au moment de l'écriture

Non commité sur `feat/ui` :
- Modifiés : `ui/auto_play.py`, `ui/game_view.py`, `ui/statistics.py`
- Nouveaux : `ui/engine_adapter.py`, `ui/fallback_engine.py`, `ui/render.py`
- Ce fichier `ADVANCEMENT_UI.md`

## Prochaines étapes (par ordre)

1. **Commits signés Marwan** (voir messages attendus dans `marwan.md`), p.ex. :
   - `feat(ui): add pygame menu with play and level select`
   - `feat(ui): implement manual keyboard gameplay`
   - `feat(ui): add auto AI mode with DQN agent`
   - `feat(metrics): add learning curve comparison plot`
   - `feat(ui): display agent observation panel`
2. **PR `feat/ui` → `main`**.
3. Quand les vrais modules d'équipe sont mergés : relancer les 3 commandes ci-dessus
   et vérifier que les labels passent de "fallback"/"placeholder" à "game.Game"/"DQN".
4. Bonus vidéo : le panneau d'observation est déjà là ; envisager un mode ralenti pour la démo.

## Points d'attention / dette

- Le fallback est **volontairement** dans `ui/` uniquement — ne pas le fusionner dans `game/`.
- `render.CELL`/`SIDEBAR` fixent la taille fenêtre depuis les dimensions du board (20x15).
- Si un vrai module a une **signature différente** du contrat, l'adaptateur bascule en fallback
  silencieusement : penser à vérifier les labels à l'écran lors de l'intégration.
