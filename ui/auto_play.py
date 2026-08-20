"""Auto AI mode — TODO: implement (Marwan Ghrairi)."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto AI Snake")
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--model", type=str, default="models/best_agent.pth")
    args = parser.parse_args()
    raise NotImplementedError("Marwan: implement ui/auto_play.py")


if __name__ == "__main__":
    main()
