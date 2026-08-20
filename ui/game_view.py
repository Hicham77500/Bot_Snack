"""Main Pygame game view with menu."""

import argparse
import sys

import pygame

from game.game import Game
from environment.actions import ACTION_NAMES

CELL_SIZE = 24
FPS = 10

COLORS = {
    "bg": (20, 20, 30),
    "grid": (40, 40, 55),
    "snake": (50, 200, 80),
    "snake_head": (80, 255, 120),
    "food": (220, 60, 60),
    "obstacle": (100, 100, 120),
    "text": (230, 230, 240),
    "menu_bg": (30, 30, 45),
    "button": (60, 60, 90),
    "button_hover": (80, 80, 120),
}


class GameView:
    def __init__(self, level: int = 1):
        self.level = level
        self.game = Game(level=level)
        self.state = self.game.reset(level=level)
        self.mode = "menu"  # menu | play | auto
        self.clock = pygame.time.Clock()
        self.font = None
        self.small_font = None
        self.screen: pygame.Surface | None = None

    def setup(self) -> None:
        pygame.init()
        w = self.state.board_width * CELL_SIZE + 200
        h = max(self.state.board_height * CELL_SIZE + 40, 400)
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption("Bot_Snack — Snake AI")
        self.font = pygame.font.SysFont("arial", 24)
        self.small_font = pygame.font.SysFont("arial", 16)

    def run(self) -> None:
        self.setup()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.mode == "play" and not self.state.done:
                        key_map = {
                            pygame.K_UP: 0,
                            pygame.K_DOWN: 1,
                            pygame.K_LEFT: 2,
                            pygame.K_RIGHT: 3,
                        }
                        if event.key in key_map:
                            self.state = self.game.step(key_map[event.key])
                    elif event.key == pygame.K_r and self.state.done:
                        self.state = self.game.reset(level=self.level)
                elif event.type == pygame.MOUSEBUTTONDOWN and self.mode == "menu":
                    self._handle_menu_click(event.pos)

            if self.mode == "play" and not self.state.done:
                pass  # wait for key input

            self._draw()
            self.clock.tick(FPS)

        pygame.quit()

    def _handle_menu_click(self, pos: tuple[int, int]) -> None:
        if not self.screen:
            return
        buttons = self._menu_buttons()
        for label, rect, action in buttons:
            if rect.collidepoint(pos):
                action()

    def _menu_buttons(self) -> list:
        assert self.screen
        sw = self.screen.get_width()
        labels = [
            ("PLAY", lambda: self._start_play()),
            ("AUTO AI", lambda: self._start_auto()),
            ("LEVEL SELECT", lambda: self._cycle_level()),
        ]
        buttons = []
        y = 180
        for label, action in labels:
            rect = pygame.Rect(sw - 180, y, 160, 40)
            buttons.append((label, rect, action))
            y += 60
        return buttons

    def _start_play(self) -> None:
        self.mode = "play"
        self.state = self.game.reset(level=self.level)

    def _start_auto(self) -> None:
        print("AUTO AI mode: load model via ui/auto_play.py (Marwan)")

    def _cycle_level(self) -> None:
        self.level = (self.level % 4) + 1
        self.game = Game(level=self.level)
        self.state = self.game.reset(level=self.level)

    def _draw(self) -> None:
        assert self.screen and self.font and self.small_font
        self.screen.fill(COLORS["bg"])

        if self.mode == "menu":
            self._draw_menu()
        else:
            self._draw_board()
            self._draw_hud()

        pygame.display.flip()

    def _draw_menu(self) -> None:
        assert self.screen and self.font
        title = self.font.render("SNAKE AI — Bot_Snack", True, COLORS["text"])
        self.screen.blit(title, (20, 40))

        for label, rect, _ in self._menu_buttons():
            color = COLORS["button"]
            pygame.draw.rect(self.screen, color, rect, border_radius=6)
            text = self.small_font.render(label, True, COLORS["text"])
            self.screen.blit(text, (rect.x + 20, rect.y + 10))

        level_text = self.small_font.render(f"Level: {self.level}", True, COLORS["text"])
        self.screen.blit(level_text, (20, 120))

    def _draw_board(self) -> None:
        assert self.screen
        for x in range(self.state.board_width):
            for y in range(self.state.board_height):
                rect = pygame.Rect(x * CELL_SIZE + 10, y * CELL_SIZE + 10, CELL_SIZE - 1, CELL_SIZE - 1)
                pygame.draw.rect(self.screen, COLORS["grid"], rect)

        for ox, oy in self.state.obstacles:
            rect = pygame.Rect(ox * CELL_SIZE + 10, oy * CELL_SIZE + 10, CELL_SIZE - 1, CELL_SIZE - 1)
            pygame.draw.rect(self.screen, COLORS["obstacle"], rect)

        fx, fy = self.state.food_position
        food_rect = pygame.Rect(fx * CELL_SIZE + 10, fy * CELL_SIZE + 10, CELL_SIZE - 1, CELL_SIZE - 1)
        pygame.draw.rect(self.screen, COLORS["food"], food_rect)

        for i, (sx, sy) in enumerate(self.state.snake_body):
            color = COLORS["snake_head"] if i == 0 else COLORS["snake"]
            rect = pygame.Rect(sx * CELL_SIZE + 10, sy * CELL_SIZE + 10, CELL_SIZE - 1, CELL_SIZE - 1)
            pygame.draw.rect(self.screen, color, rect)

    def _draw_hud(self) -> None:
        assert self.screen and self.small_font
        sw = self.screen.get_width()
        hud_x = self.state.board_width * CELL_SIZE + 30
        lines = [
            f"Level: {self.state.level}",
            f"Score: {self.state.score}",
            f"Steps: {self.state.steps}",
            f"Mode: {self.mode.upper()}",
        ]
        if self.state.done:
            lines.append(f"GAME OVER ({self.state.death_reason})")
            lines.append("Press R to restart")

        for i, line in enumerate(lines):
            text = self.small_font.render(line, True, COLORS["text"])
            self.screen.blit(text, (hud_x, 20 + i * 28))


def main() -> None:
    parser = argparse.ArgumentParser(description="Snake game UI")
    parser.add_argument("--level", type=int, default=1)
    args = parser.parse_args()

    view = GameView(level=args.level)
    view.run()


if __name__ == "__main__":
    main()
