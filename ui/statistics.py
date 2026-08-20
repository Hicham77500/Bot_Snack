"""Learning curve visualization — TODO: implement (Marwan Ghrairi)."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot agent statistics")
    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--model", type=str, default="models/best_agent.pth")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    raise NotImplementedError("Marwan: implement ui/statistics.py")


if __name__ == "__main__":
    main()
