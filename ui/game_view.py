"""Pygame game view — TODO: implement (Marwan Ghrairi)."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Snake game UI")
    parser.add_argument("--level", type=int, default=1)
    args = parser.parse_args()
    raise NotImplementedError("Marwan: implement ui/game_view.py — see docs/prompts/marwan.md")


if __name__ == "__main__":
    main()
