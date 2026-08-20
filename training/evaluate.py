"""Evaluate agents — standalone script to reload and test best model."""

import argparse

import numpy as np

from agents.dqn_agent import DQNAgent
from agents.random_agent import RandomAgent
from environment.snake_env import SnakeEnv


def evaluate_agent(
    agent,
    env: SnakeEnv,
    episodes: int = 100,
    level: int = 1,
) -> dict:
    scores = []
    survival_count = 0

    for _ in range(episodes):
        state = env.reset(level=level)
        done = False
        while not done:
            action = agent.select_action(state, training=False)
            state, _, done, info = env.step(action)
        scores.append(info["score"])
        if info["score"] > 0:
            survival_count += 1

    return {
        "mean_score": float(np.mean(scores)),
        "max_score": float(np.max(scores)),
        "episodes": episodes,
        "survival_rate": survival_count / episodes,
        "scores": scores,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Snake agents")
    parser.add_argument("--agent", choices=["random", "dqn"], default="random")
    parser.add_argument("--model", type=str, default="models/best_agent.pth")
    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    env = SnakeEnv(level=args.level)

    if args.agent == "random":
        agent = RandomAgent(action_size=env.action_size, seed=args.seed)
    else:
        agent = DQNAgent(
            state_size=env.observation_size,
            action_size=env.action_size,
        )
        agent.load(args.model)
        agent.epsilon = 0.0

    results = evaluate_agent(agent, env, episodes=args.episodes, level=args.level)

    print(f"Agent: {args.agent.upper()}")
    print(f"Episodes: {results['episodes']}")
    print(f"Mean score: {results['mean_score']:.2f}")
    print(f"Max score: {results['max_score']:.0f}")
    print(f"Survival rate: {results['survival_rate']:.1%}")


if __name__ == "__main__":
    main()
