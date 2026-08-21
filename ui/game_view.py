"""Main Pygame game view: menu + manual keyboard gameplay.

Run:
    python -m ui.game_view              # start on the menu
    python -m ui.game_view --level 3    # preselect a level

Menu:
    [ PLAY ]         -> manual keyboard game
    [ AUTO AI ]      -> DQN agent plays on its own (ui.auto_play)
    [ LEVEL SELECT ] -> cycle levels 1..4
"""

from __future__ import annotations

import argparse

import pygame

from ui import engine_adapter as adapter
from ui import render
from ui.fallback_engine import (
    ACTION_VECTORS,
    DOWN,
    LEFT,
    MAX_LEVEL,
    RIGHT,
    UP,
)

FPS_PLAY = 8  # snake steps per second in manual mode

MENU_ITEMS = ["PLAY", "AUTO AI", "LEVEL SELECT"]


class GameView:
    def __init__(self, level: int = 1):
        pygame.init()
        pygame.display.set_caption("SNAKE AI — Bot_Snack")
        self.level = max(1, min(level, MAX_LEVEL))
        self.best_score = 0
        self.last_score = 0
        # A game instance drives the window size (board dimensions).
        self.game, self.engine_real, self.engine_label = adapter.make_game(self.level)
        state = self.game.get_state()
        self.window_size = render.board_pixel_size(state.board_width, state.board_height)
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.selected = 0

    # -- top-level loop ------------------------------------------------------
    def run(self) -> None:
        running = True
        while running:
            running = self.menu_loop()
        pygame.quit()

    # -- menu ----------------------------------------------------------------
    def menu_loop(self) -> bool:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        return False
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.selected = (self.selected - 1) % len(MENU_ITEMS)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.selected = (self.selected + 1) % len(MENU_ITEMS)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        action = MENU_ITEMS[self.selected]
                        if action == "PLAY":
                            self.play_loop()
                        elif action == "AUTO AI":
                            self._launch_auto()
                        elif action == "LEVEL SELECT":
                            self._cycle_level()
            self._draw_menu()
            self.clock.tick(30)

    def _cycle_level(self) -> None:
        self.level = self.level % MAX_LEVEL + 1
        self.game, self.engine_real, self.engine_label = adapter.make_game(self.level)

    def _launch_auto(self) -> None:
        # Import lazily to keep manual play independent of auto mode.
        from ui import auto_play

        auto_play.run_auto(
            level=self.level,
            model_path="models/best_agent.pth",
            screen=self.screen,
            clock=self.clock,
            show_observation=True,
        )
        # Re-assert our caption/window after the auto session returns.
        pygame.display.set_caption("SNAKE AI — Bot_Snack")

    def _draw_menu(self) -> None:
        self.screen.fill(render.COLOR_BG)
        cx = self.window_size[0] // 2

        title = render._font(48, bold=True).render("SNAKE AI", True, render.COLOR_SNAKE_HEAD)
        self.screen.blit(title, (cx - title.get_width() // 2, 60))
        sub = render._font(22).render("Bot_Snack", True, render.COLOR_TEXT_DIM)
        self.screen.blit(sub, (cx - sub.get_width() // 2, 118))

        y = 200
        for i, item in enumerate(MENU_ITEMS):
            selected = i == self.selected
            label = f"[ {item} ]"
            if item == "LEVEL SELECT":
                label = f"[ LEVEL SELECT: {self.level} ]"
            color = render.COLOR_ACCENT if selected else render.COLOR_TEXT
            surf = render._font(30, bold=selected).render(label, True, color)
            self.screen.blit(surf, (cx - surf.get_width() // 2, y))
            y += 56

        info = [
            f"Level: {self.level}",
            f"Score: {self.last_score}",
            f"Best:  {self.best_score}",
        ]
        iy = y + 24
        for line in info:
            surf = render._font(20).render(line, True, render.COLOR_TEXT_DIM)
            self.screen.blit(surf, (cx - surf.get_width() // 2, iy))
            iy += 28

        eng = render._font(15).render(
            f"engine: {self.engine_label}", True,
            render.COLOR_WARN if not self.engine_real else render.COLOR_SAFE,
        )
        self.screen.blit(eng, (cx - eng.get_width() // 2, self.window_size[1] - 60))
        hint = render._font(15).render(
            "↑/↓ select   Enter confirm   Esc quit", True, render.COLOR_TEXT_DIM
        )
        self.screen.blit(hint, (cx - hint.get_width() // 2, self.window_size[1] - 34))
        pygame.display.flip()

    # -- manual play ---------------------------------------------------------
    def play_loop(self) -> None:
        state = self.game.reset(self.level)
        pending_action: int | None = None
        game_over = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # back to menu
                    if game_over and event.key == pygame.K_r:
                        state = self.game.reset(self.level)
                        game_over = False
                        pending_action = None
                    key_map = {
                        pygame.K_UP: UP, pygame.K_w: UP,
                        pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
                        pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
                        pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT,
                    }
                    if not game_over and event.key in key_map:
                        pending_action = key_map[event.key]

            if not game_over:
                action = pending_action if pending_action is not None else _dir_to_action(
                    state.snake_direction
                )
                state = self.game.step(action)
                if state.done:
                    game_over = True
                    self.last_score = state.score
                    self.best_score = max(self.best_score, state.score)

            self._draw_play(state, game_over)
            self.clock.tick(FPS_PLAY if not game_over else 30)

    def _draw_play(self, state, game_over: bool) -> None:
        render.draw_board(self.screen, state)
        render.draw_sidebar(
            self.screen,
            state,
            title="PLAY",
            stats=[
                ("Level", state.level),
                ("Score", state.score),
                ("Steps", state.steps),
                ("Best", self.best_score),
            ],
            footer=[
                f"engine: {self.engine_label}",
                "Arrows/WASD to move",
                "Esc: menu",
            ],
        )
        if game_over:
            render.draw_center_banner(
                self.screen,
                state,
                [
                    ("GAME OVER", render.COLOR_DANGER),
                    (f"Score {state.score}", render.COLOR_TEXT),
                    ("Press R to restart", render.COLOR_TEXT_DIM),
                ],
            )
        pygame.display.flip()


def _dir_to_action(direction: tuple[int, int]) -> int:
    for action, vec in ACTION_VECTORS.items():
        if vec == direction:
            return action
    return RIGHT


def main() -> None:
    parser = argparse.ArgumentParser(description="Snake game UI")
    parser.add_argument("--level", type=int, default=1)
    args = parser.parse_args()
    GameView(level=args.level).run()


if __name__ == "__main__":
    main()
