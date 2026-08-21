"""Auto AI mode — the DQN agent plays Snake with live visual feedback.

Run:
    python -m ui.auto_play --level 1 --model models/best_agent.pth

If a trained model exists and the real agent/env are available, they are used.
Otherwise the UI falls back to its self-contained engine and a clearly
labelled heuristic stand-in, so the mode is always demonstrable.
"""

from __future__ import annotations

import argparse

import pygame

from ui import engine_adapter as adapter
from ui import render
from ui.fallback_engine import (
    ACTION_NAMES,
    MAX_LEVEL,
    ObservationInfo,
    build_observation,
)

FPS_AUTO = 12  # agent steps per second


def _observation_info(state, action: int) -> ObservationInfo:
    obs = build_observation(state)
    return ObservationInfo(
        danger_front=obs[4] > 0.5,
        danger_left=obs[5] > 0.5,
        danger_right=obs[6] > 0.5,
        action=action,
    )


def run_auto(
    level: int = 1,
    model_path: str = "models/best_agent.pth",
    screen: pygame.Surface | None = None,
    clock: pygame.time.Clock | None = None,
    show_observation: bool = True,
    max_episodes: int | None = None,
) -> None:
    """Run the AUTO AI loop. Reuses an existing window when given one."""
    owns_pygame = screen is None
    if owns_pygame:
        pygame.init()
        pygame.display.set_caption("SNAKE AI — AUTO")

    env, env_real, env_label = adapter.make_env(level)
    obs = env.reset(level)
    state = env.state if hasattr(env, "state") else env.game.get_state()

    agent, agent_real, agent_label = adapter.load_dqn_agent(
        model_path, state_size=env.observation_size, action_size=env.action_size
    )

    win = render.board_pixel_size(state.board_width, state.board_height)
    if screen is None:
        screen = pygame.display.set_mode(win)
    if clock is None:
        clock = pygame.time.Clock()

    episode = 1
    best = 0
    last_action = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if owns_pygame:
                    pygame.quit()
                    return
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        last_action = int(agent.select_action(obs, training=False))
        obs, _reward, done, info = env.step(last_action)
        state = env.state if hasattr(env, "state") else env.game.get_state()

        if done:
            best = max(best, info["score"])
            episode += 1
            if max_episodes is not None and episode > max_episodes:
                running = False
            obs = env.reset(level)
            state = env.state if hasattr(env, "state") else env.game.get_state()

        obs_info = _observation_info(state, last_action) if show_observation else None
        _draw(
            screen, state, episode, best, agent_label, agent_real,
            env_label, obs_info,
        )
        clock.tick(FPS_AUTO)

    if owns_pygame:
        pygame.quit()


def _draw(
    screen, state, episode, best, agent_label, agent_real, env_label, obs_info
) -> None:
    render.draw_board(screen, state)
    obs_lines = obs_info.as_lines() if obs_info is not None else ()
    agent_display = "DQN" if agent_real else f"DQN? ({agent_label})"
    render.draw_sidebar(
        screen,
        state,
        title="AUTO AI",
        stats=[
            ("Episode", episode),
            ("Level", state.level),
            ("Score", state.score),
            ("Best", best),
            ("Agent", agent_display),
        ],
        footer=[
            f"engine: {env_label}",
            f"agent : {'DQN (trained)' if agent_real else agent_label}",
            "Esc: back",
        ],
        observation_lines=obs_lines,
    )
    if not agent_real:
        warn = render._font(14).render(
            "placeholder policy — no trained model", True, render.COLOR_WARN
        )
        screen.blit(warn, (render.MARGIN, screen.get_height() - 22))
    pygame.display.flip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto AI Snake")
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--model", type=str, default="models/best_agent.pth")
    parser.add_argument(
        "--no-observation", action="store_true", help="hide the observation panel"
    )
    args = parser.parse_args()
    run_auto(
        level=args.level,
        model_path=args.model,
        show_observation=not args.no_observation,
    )


if __name__ == "__main__":
    main()
