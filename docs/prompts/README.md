# Prompts par développeur — Bot_Snack

Ce dépôt contient **uniquement le scaffold** (structure + contrat d'API).  
Chaque membre de l'équipe développe **sa partie sur sa branche** avec son propre `git log`.

## Ordre de démarrage

1. **Aya** — `feat/game-engine` (bloquant pour les autres)
2. **Khalil** — `feat/environment` (dépend du game engine)
3. **Hicham** — `feat/dqn-training` (dépend de l'environnement)
4. **Marwan** — `feat/ui` (dépend du game engine, peut commencer en parallèle de Khalil)

## Comment utiliser

1. Cloner le repo : `git clone git@github.com:Hicham77500/Bot_Snack.git`
2. Lire [CONTRACT.md](../../CONTRACT.md)
3. Ouvrir **votre prompt** ci-dessous dans Cursor
4. Checkout **votre branche** et coder
5. Commits fréquents avec le bon préfixe (`feat(game):`, etc.)
6. Ouvrir une PR vers `main` quand votre livrable est prêt

## Prompts

| Dev | Branche | Prompt |
|-----|---------|--------|
| Aya El JANATI | `feat/game-engine` | [aya.md](aya.md) |
| Khalil Jouani | `feat/environment` | [khalil.md](khalil.md) |
| Hicham Guendouz | `feat/dqn-training` | [hicham.md](hicham.md) |
| Marwan Ghrairi | `feat/ui` | [marwan.md](marwan.md) |

## Setup commun

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
