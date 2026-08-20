"""Experiment logging utilities."""

import csv
from datetime import date
from pathlib import Path

EXPERIMENTS_FILE = Path("results/experiments.csv")


def log_experiment(
    exp_id: str,
    modification: str,
    mean_score: float,
    result: str,
    author: str,
) -> None:
    """Append one row to the experiments log."""
    file_exists = EXPERIMENTS_FILE.exists() and EXPERIMENTS_FILE.stat().st_size > 0

    with open(EXPERIMENTS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                ["Exp", "Modification", "Score_moyen", "Resultat", "Date", "Auteur"]
            )
        writer.writerow(
            [exp_id, modification, f"{mean_score:.2f}", result, date.today().isoformat(), author]
        )


if __name__ == "__main__":
    log_experiment("E0", "Random baseline", 0.0, "Baseline", "Khalil Jouani")
