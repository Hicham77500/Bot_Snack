"""Auto AI mode — DQN agent plays Snake with visual feedback."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto AI Snake")
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--model", type=str, default="models/best_agent.pth")
    args = parser.parse_args()
    raise NotImplementedError


if __name__ == "__main__":
    main()
