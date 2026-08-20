"""Evaluate agents — standalone script to reload and test best model."""

import argparse


def evaluate_agent(agent, env, episodes: int = 100, level: int = 1) -> dict:
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Snake agents")
    parser.add_argument("--agent", choices=["random", "dqn"], default="random")
    parser.add_argument("--model", type=str, default="models/best_agent.pth")
    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    raise NotImplementedError


if __name__ == "__main__":
    main()
