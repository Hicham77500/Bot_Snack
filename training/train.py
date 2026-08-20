"""DQN training loop — TODO: implement (Hicham Guendouz)."""

import argparse


def train(
    episodes: int = 500,
    level: int = 1,
    model_path: str = "models/best_agent.pth",
    curve_path: str = "results/curves/training_curve.png",
    seed: int = 42,
) -> list[float]:
    raise NotImplementedError("Hicham: implement training loop")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train DQN on Snake")
    parser.add_argument("--episodes", type=int, default=500)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--model", type=str, default="models/best_agent.pth")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    train(episodes=args.episodes, level=args.level, model_path=args.model, seed=args.seed)


if __name__ == "__main__":
    main()
