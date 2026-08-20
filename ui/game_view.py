"""Main Pygame game view with menu."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Snake game UI")
    parser.add_argument("--level", type=int, default=1)
    args = parser.parse_args()
    raise NotImplementedError


if __name__ == "__main__":
    main()
