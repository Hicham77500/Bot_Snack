"""Learning curve visualization and Random vs DQN comparison."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot agent statistics")
    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--model", type=str, default="models/best_agent.pth")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    raise NotImplementedError


if __name__ == "__main__":
    main()
