"""Évaluation des agents Snake (partie Random : Khalil ; partie DQN : Hicham).

Rejoue un agent sur ``N`` parties et calcule des métriques agrégées
(score moyen / max / min, écart-type, longueur moyenne des parties). C'est
l'outil qui produit les **deux chiffres côte à côte** demandés par l'énoncé :
score de l'agent aléatoire vs score de l'agent entraîné, sur le même nombre
de parties.

Exemples :
    python -m training.evaluate --agent random --episodes 100 --level 1
    python -m training.evaluate --agent random --episodes 100 --level 1 --log
    python -m training.evaluate --agent dqn --model models/best_agent.pth --episodes 100

``evaluate_agent`` est volontairement générique : elle fonctionne avec
n'importe quel agent respectant le contrat ``select_action(state, training)``,
donc elle sert aussi bien la baseline Random que le DQN d'Hicham.
"""

import argparse
import csv
import os
import random
from datetime import date

import numpy as np

from environment.snake_env import SnakeEnv


def evaluate_agent(agent, env: SnakeEnv, episodes: int = 100, level: int = 1) -> dict:
    """Évalue ``agent`` sur ``episodes`` parties et retourne des métriques.

    Args:
        agent: objet avec ``select_action(state, training=False) -> int``.
        env: instance de ``SnakeEnv``.
        episodes: nombre de parties.
        level: niveau sur lequel évaluer.

    Returns:
        dict : {mean_score, max_score, min_score, std_score,
                mean_steps, mean_reward, episodes, level, scores}
    """
    scores: list[int] = []
    steps_list: list[int] = []
    rewards_list: list[float] = []

    for _ in range(episodes):
        state = env.reset(level=level)
        done = False
        total_reward = 0.0
        info = {"score": 0, "steps": 0}

        while not done:
            action = agent.select_action(state, training=False)
            state, reward, done, info = env.step(action)
            total_reward += reward

        scores.append(info["score"])
        steps_list.append(info["steps"])
        rewards_list.append(total_reward)

    scores_arr = np.array(scores, dtype=np.float64)
    return {
        "mean_score": float(scores_arr.mean()),
        "max_score": int(scores_arr.max()),
        "min_score": int(scores_arr.min()),
        "std_score": float(scores_arr.std()),
        "mean_steps": float(np.mean(steps_list)),
        "mean_reward": float(np.mean(rewards_list)),
        "episodes": episodes,
        "level": level,
        "scores": scores,
    }


def _print_report(agent_name: str, metrics: dict) -> None:
    print("=" * 44)
    print(f"  Évaluation — agent {agent_name!r}")
    print("=" * 44)
    print(f"  Parties            : {metrics['episodes']} (level {metrics['level']})")
    print(f"  Score moyen        : {metrics['mean_score']:.3f}")
    print(f"  Score max / min    : {metrics['max_score']} / {metrics['min_score']}")
    print(f"  Écart-type score   : {metrics['std_score']:.3f}")
    print(f"  Steps moyen/partie : {metrics['mean_steps']:.1f}")
    print(f"  Reward moyen       : {metrics['mean_reward']:.2f}")
    print("=" * 44)


def _log_experiment(exp_id: str, label: str, mean_score: float,
                    result: str, author: str,
                    csv_path: str = "results/experiments.csv") -> None:
    """Ajoute une ligne au carnet d'essais (results/experiments.csv)."""
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    header = ["Exp", "Modification", "Score_moyen", "Resultat", "Date", "Auteur"]
    file_exists = os.path.exists(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow([
            exp_id, label, f"{mean_score:.3f}", result, date.today().isoformat(), author,
        ])
    print(f"[metrics] {exp_id} loggé dans {csv_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Snake agents")
    parser.add_argument("--agent", choices=["random", "dqn"], default="random")
    parser.add_argument("--model", type=str, default="models/best_agent.pth")
    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--log", action="store_true",
                        help="Écrire le résultat dans results/experiments.csv")
    args = parser.parse_args()

    # Reproductibilité : le moteur place la nourriture via le module
    # `random` du stdlib. On le seed ici pour que la baseline soit
    # rejouable à l'identique avec la même commande (3 runs reproductibles).
    random.seed(args.seed)
    np.random.seed(args.seed)

    env = SnakeEnv(level=args.level)

    if args.agent == "random":
        from agents.random_agent import RandomAgent
        agent = RandomAgent(action_size=env.action_size, seed=args.seed)
        metrics = evaluate_agent(agent, env, episodes=args.episodes, level=args.level)
        _print_report("random", metrics)
        if args.log:
            _log_experiment(
                "E0", "Random baseline", metrics["mean_score"],
                "Baseline", "Khalil Jouani",
            )

    elif args.agent == "dqn":
        # Partie DQN : complétée par Hicham (chargement du modèle entraîné).
        from agents.dqn_agent import DQNAgent
        agent = DQNAgent(
            state_size=env.observation_size,
            action_size=env.action_size,
        )
        agent.load(args.model)
        metrics = evaluate_agent(agent, env, episodes=args.episodes, level=args.level)
        _print_report("dqn", metrics)


if __name__ == "__main__":
    main()
