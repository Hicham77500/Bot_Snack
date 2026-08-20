"""DQN training loop for Snake."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from agents.dqn_agent import DQNAgent
from environment.snake_env import SnakeEnv


def train(
    episodes: int = 500,
    level: int = 1,
    model_path: str = "models/best_agent.pth",
    curve_path: str = "results/curves/training_curve.png",
    seed: int = 42,
) -> list[float]:
    np.random.seed(seed)
    env = SnakeEnv(level=level)
    agent = DQNAgent(
        state_size=env.observation_size,
        action_size=env.action_size,
    )

    scores: list[float] = []
    best_score = -1.0

    for episode in range(1, episodes + 1):
        state = env.reset(level=level)
        total_reward = 0.0
        done = False

        while not done:
            action = agent.select_action(state, training=True)
            next_state, reward, done, info = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            agent.train_step()
            state = next_state
            total_reward += reward

        score = info["score"]
        scores.append(float(score))

        if score > best_score:
            best_score = score
            agent.save(model_path)

        if episode % 50 == 0:
            avg = np.mean(scores[-50:])
            print(f"Episode {episode}/{episodes} | Avg score (50): {avg:.2f} | Best: {best_score:.0f}")

    Path(curve_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 5))
    plt.plot(scores, alpha=0.4, label="Score")
    window = min(50, len(scores))
    if window > 1:
        smoothed = np.convolve(scores, np.ones(window) / window, mode="valid")
        plt.plot(range(window - 1, len(scores)), smoothed, label=f"Avg {window}")
    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.title("DQN Training Progress")
    plt.legend()
    plt.tight_layout()
    plt.savefig(curve_path)
    plt.close()

    return scores


def main() -> None:
    parser = argparse.ArgumentParser(description="Train DQN on Snake")
    parser.add_argument("--episodes", type=int, default=500)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--model", type=str, default="models/best_agent.pth")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    train(
        episodes=args.episodes,
        level=args.level,
        model_path=args.model,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
