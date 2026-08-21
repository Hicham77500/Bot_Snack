"""Learning-curve visualization: Random vs DQN comparison.

Run:
    python -m ui.statistics --episodes 100 --model models/best_agent.pth

Plays the same number of episodes with the Random baseline and the DQN agent
(or a labelled heuristic stand-in when no trained model exists), then saves a
two-panel figure to ``results/curves/comparison.png``:
  - left  : score per episode (Random vs DQN)
  - right : mean score bar chart (Random vs Trained)
"""

from __future__ import annotations

import argparse
import os

import matplotlib

matplotlib.use("Agg")  # headless: write PNG without a display
import matplotlib.pyplot as plt
import numpy as np

from ui import engine_adapter as adapter

DEFAULT_OUTPUT = os.path.join("results", "curves", "comparison.png")
MAX_STEPS_PER_EPISODE = 1000  # safety cap so a looping policy still terminates


def _run_episodes(env, agent, episodes: int) -> list[int]:
    scores: list[int] = []
    for _ in range(episodes):
        obs = env.reset()
        done = False
        steps = 0
        score = 0
        while not done and steps < MAX_STEPS_PER_EPISODE:
            action = int(agent.select_action(obs, training=False))
            obs, _reward, done, info = env.step(action)
            score = info["score"]
            steps += 1
        scores.append(score)
    return scores


def collect_stats(
    episodes: int, level: int, model_path: str, seed: int = 42
) -> dict:
    """Return per-episode scores for Random and DQN over the same setup."""
    # Random baseline.
    env_r, _r_real, env_label = adapter.make_env(level, seed=seed)
    random_agent, _ra_real, _ = adapter.load_random_agent(
        action_size=env_r.action_size, seed=seed
    )
    random_scores = _run_episodes(env_r, random_agent, episodes)

    # DQN (or heuristic placeholder).
    env_d, _d_real, _ = adapter.make_env(level, seed=seed + 1)
    dqn_agent, dqn_real, dqn_label = adapter.load_dqn_agent(
        model_path, state_size=env_d.observation_size, action_size=env_d.action_size
    )
    dqn_scores = _run_episodes(env_d, dqn_agent, episodes)

    return {
        "random_scores": random_scores,
        "dqn_scores": dqn_scores,
        "dqn_real": dqn_real,
        "dqn_label": dqn_label,
        "env_label": env_label,
        "level": level,
    }


def _moving_average(values: list[int], window: int = 10) -> np.ndarray:
    if len(values) < 2:
        return np.array(values, dtype=float)
    window = min(window, len(values))
    kernel = np.ones(window) / window
    return np.convolve(values, kernel, mode="valid")


def plot_comparison(stats: dict, output: str = DEFAULT_OUTPUT) -> str:
    random_scores = stats["random_scores"]
    dqn_scores = stats["dqn_scores"]
    dqn_real = stats["dqn_real"]
    dqn_name = "DQN" if dqn_real else f"DQN* ({stats['dqn_label']})"
    episodes = range(1, len(random_scores) + 1)

    fig, (ax_curve, ax_bar) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(
        f"Snake — Random vs {dqn_name}  (level {stats['level']}, "
        f"{len(random_scores)} episodes, engine: {stats['env_label']})",
        fontsize=13,
    )

    # Left: per-episode score + smoothed trend.
    ax_curve.plot(episodes, random_scores, color="#888", alpha=0.35, label="Random (raw)")
    ax_curve.plot(episodes, dqn_scores, color="#4aa3ff", alpha=0.35, label=f"{dqn_name} (raw)")
    ma_r = _moving_average(random_scores)
    ma_d = _moving_average(dqn_scores)
    off = len(random_scores) - len(ma_r) + 1
    ax_curve.plot(range(off, off + len(ma_r)), ma_r, color="#555", lw=2, label="Random (avg)")
    ax_curve.plot(range(off, off + len(ma_d)), ma_d, color="#1670d6", lw=2, label=f"{dqn_name} (avg)")
    ax_curve.set_xlabel("Episode")
    ax_curve.set_ylabel("Score (food eaten)")
    ax_curve.set_title("Score per episode")
    ax_curve.grid(True, alpha=0.25)
    ax_curve.legend(fontsize=9)

    # Right: mean score bar chart.
    means = [float(np.mean(random_scores)), float(np.mean(dqn_scores))]
    errs = [float(np.std(random_scores)), float(np.std(dqn_scores))]
    labels = ["Random", dqn_name]
    bars = ax_bar.bar(labels, means, yerr=errs, capsize=6, color=["#888", "#4aa3ff"])
    for bar, m in zip(bars, means):
        ax_bar.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f"{m:.2f}", ha="center", va="bottom", fontsize=11,
        )
    ax_bar.set_ylabel("Mean score")
    ax_bar.set_title("Mean score (Random vs Trained)")
    ax_bar.grid(True, axis="y", alpha=0.25)

    if not dqn_real:
        fig.text(
            0.5, 0.01,
            "* DQN is a heuristic placeholder (no trained models/best_agent.pth yet)",
            ha="center", fontsize=9, color="#b06a00",
        )

    fig.tight_layout(rect=[0, 0.04, 1, 0.95])
    os.makedirs(os.path.dirname(output), exist_ok=True)
    fig.savefig(output, dpi=120)
    plt.close(fig)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot agent statistics")
    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--model", type=str, default="models/best_agent.pth")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    stats = collect_stats(args.episodes, args.level, args.model, args.seed)
    path = plot_comparison(stats, args.output)

    r_mean = np.mean(stats["random_scores"])
    d_mean = np.mean(stats["dqn_scores"])
    tag = "DQN" if stats["dqn_real"] else f"DQN placeholder ({stats['dqn_label']})"
    print(f"Episodes      : {args.episodes} (level {args.level})")
    print(f"Random  mean  : {r_mean:.2f}")
    print(f"{tag} mean  : {d_mean:.2f}")
    print(f"Saved figure  : {path}")


if __name__ == "__main__":
    main()
