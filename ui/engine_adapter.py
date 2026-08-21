"""Adapter that prefers the real team modules and falls back to ``ui`` stubs.

The UI depends on three packages owned by other members (``game/``,
``environment/``, ``agents/``). While those are still stubs raising
``NotImplementedError``, this adapter transparently substitutes the
self-contained fallback in :mod:`ui.fallback_engine`.

Each factory returns ``(object, is_real, label)`` so the views can display
exactly which engine/agent is live and never pass a placeholder off as the
real trained DQN.
"""

from __future__ import annotations

import os
from typing import Any

from ui import fallback_engine as fb


def _real_module_usable(make, *args, probe: str | None = None) -> Any | None:
    """Instantiate a real object and probe it; return None if it is a stub."""
    try:
        obj = make(*args)
        if probe is not None:
            getattr(obj, probe)()  # e.g. reset() — stubs raise NotImplementedError
        return obj
    except NotImplementedError:
        return None
    except Exception:
        # Missing symbol, signature mismatch, import error, etc. -> fallback.
        return None


def make_game(level: int = 1, seed: int | None = None) -> tuple[Any, bool, str]:
    """Return a Game-like object exposing reset/step/get_state."""
    try:
        from game.game import Game  # type: ignore

        real = _real_module_usable(lambda: Game(level=level), probe="reset")
        if real is not None:
            return real, True, "game.Game"
    except Exception:
        pass
    return fb.FallbackGame(level=level, seed=seed), False, "fallback"


def make_env(level: int = 1, seed: int | None = None) -> tuple[Any, bool, str]:
    """Return a gym-like env exposing reset/step and observation/action size."""
    try:
        from environment.snake_env import SnakeEnv  # type: ignore

        real = _real_module_usable(lambda: SnakeEnv(level=level), probe="reset")
        if real is not None:
            return real, True, "environment.SnakeEnv"
    except Exception:
        pass
    return fb.FallbackEnv(level=level, seed=seed), False, "fallback"


def load_dqn_agent(
    model_path: str, state_size: int, action_size: int
) -> tuple[Any, bool, str]:
    """Load the trained DQN agent, or a labelled heuristic placeholder."""
    if os.path.exists(model_path):
        try:
            from agents.dqn_agent import DQNAgent  # type: ignore

            agent = DQNAgent(state_size=state_size, action_size=action_size)
            agent.load(model_path)
            # Sanity probe: a real agent must return a valid action.
            action = agent.select_action(
                __import__("numpy").zeros(state_size, dtype="float32")
            )
            if isinstance(action, (int,)) or hasattr(action, "__int__"):
                return agent, True, "DQN"
        except NotImplementedError:
            pass
        except Exception:
            pass
    # No usable trained model -> heuristic stand-in, clearly labelled.
    return fb.HeuristicAgent(action_size=action_size), False, "heuristic placeholder"


def load_random_agent(action_size: int, seed: int | None = None) -> tuple[Any, bool, str]:
    """Return the real RandomAgent baseline if usable, else the fallback one."""
    try:
        from agents.random_agent import RandomAgent as RealRandom  # type: ignore

        agent = RealRandom(action_size=action_size, seed=seed)
        action = agent.select_action(
            __import__("numpy").zeros(1, dtype="float32")
        )
        if isinstance(action, int) or hasattr(action, "__int__"):
            return agent, True, "Random"
    except NotImplementedError:
        pass
    except Exception:
        pass
    return fb.RandomAgent(action_size=action_size, seed=seed), False, "Random"


def observation_from_state(state: Any, max_level: int = fb.MAX_LEVEL):
    """Build the 11-feature observation from a GameState-like object.

    Works whether ``state`` comes from the real game engine or the fallback,
    as long as it exposes the CONTRACT.md ``GameState`` attributes.
    """
    return fb.build_observation(state, max_level=max_level)
