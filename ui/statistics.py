"""Learning curve visualization and Random vs DQN comparison."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from agents.dqn_agent import DQNAgent
from agents.random_agent import RandomAgent
from environment.snake_env import SnakeEnv
from training.evaluate import evaluate_agent


def plot_comparison(
    random_scores: list[float],
    dqn_scores: list[float],
    output_path: str = "results/curves/comparison.png",
) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(random_scores, alpha=0.5, label="Random")
    axes[0].plot(dqn_scores, alpha=0.5, label="DQN")
    axes[0].set_xlabel("Episode")
    axes[0].set_ylabel("Score")
    axes[0].set_title("Score per Episode")
    axes[0].legend()

    labels = ["Random Agent", "Trained Agent"]
    means = [np.mean(random_scores), np.mean(dqn_scores)]
    axes[1].bar(labels, means, color=["#e74c3c", "#2ecc71"])
    axes[1].set_ylabel("Mean Score")
    axes[1].set_title("Random vs DQN")

    for i, v in enumerate(means):
        axes[1].text(i, v + 0.3, f"{v:.1f}", ha="center")

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved comparison plot to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot agent statistics")
    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--model", type=str, default="models/best_agent.pth")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    env = SnakeEnv(level=args.level)

    random_agent = RandomAgent(action_size=env.action_size, seed=args.seed)
    random_results = evaluate_agent(random_agent, env, episodes=args.episodes, level=args.level)

    dqn_agent = DQNAgent(
        state_size=env.observation_size,
        action_size=env.action_size,
    )
    try:
        dqn_agent.load(args.model)
        dqn_agent.epsilon = 0.0
        dqn_results = evaluate_agent(dqn_agent, env, episodes=args.episodes, level=args.level)
    except FileNotFoundError:
        print(f"Model not found: {args.model}. Skipping DQN comparison.")
        return

    plot_comparison(random_results["scores"], dqn_results["scores"])

    print(f"Random mean: {random_results['mean_score']:.2f}")
    print(f"DQN mean:    {dqn_results['mean_score']:.2f}")


if __name__ == "__main__":
    main()
