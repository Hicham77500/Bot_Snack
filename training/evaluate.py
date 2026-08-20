"""Evaluate agents — TODO: implement (Khalil + Hicham)."""

import argparse


def evaluate_agent(agent, env, episodes: int = 100, level: int = 1) -> dict:
    raise NotImplementedError("Implement evaluate_agent() — Random: Khalil, DQN: Hicham")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Snake agents")
    parser.add_argument("--agent", choices=["random", "dqn"], default="random")
    parser.add_argument("--model", type=str, default="models/best_agent.pth")
    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    raise NotImplementedError("Implement evaluate main()")


if __name__ == "__main__":
    main()
