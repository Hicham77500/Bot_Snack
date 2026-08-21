"""Shared Pygame rendering helpers for the Snake UI.

Draws the board, snake, food, obstacles, a HUD and the bonus observation
panel from a CONTRACT.md ``GameState``-like object. Kept UI-only so the
game engine stays Pygame-free.
"""

from __future__ import annotations

from typing import Any, Sequence

import pygame

# --- Layout -----------------------------------------------------------------
CELL = 28              # pixel size of one board cell
SIDEBAR = 240          # right-hand info panel width
MARGIN = 16

# --- Palette ----------------------------------------------------------------
COLOR_BG = (18, 18, 24)
COLOR_GRID = (32, 34, 44)
COLOR_BOARD = (24, 26, 34)
COLOR_SNAKE_HEAD = (80, 220, 120)
COLOR_SNAKE_BODY = (52, 168, 96)
COLOR_FOOD = (235, 90, 90)
COLOR_OBSTACLE = (70, 74, 92)
COLOR_TEXT = (230, 232, 240)
COLOR_TEXT_DIM = (150, 154, 170)
COLOR_ACCENT = (120, 170, 255)
COLOR_WARN = (240, 190, 90)
COLOR_DANGER = (235, 90, 90)
COLOR_SAFE = (80, 220, 120)


def board_pixel_size(width: int, height: int) -> tuple[int, int]:
    """Full window size (board + sidebar) for a given board in cells."""
    w = MARGIN * 2 + width * CELL + SIDEBAR
    h = MARGIN * 2 + height * CELL
    return w, h


def _font(size: int, bold: bool = False) -> pygame.font.Font:
    return pygame.font.SysFont("consolas,menlo,monospace", size, bold=bold)


def draw_board(surface: pygame.Surface, state: Any) -> None:
    """Render the play area from a GameState-like object."""
    surface.fill(COLOR_BG)
    ox, oy = MARGIN, MARGIN
    bw, bh = state.board_width, state.board_height

    pygame.draw.rect(
        surface, COLOR_BOARD, (ox, oy, bw * CELL, bh * CELL)
    )
    for x in range(bw + 1):
        pygame.draw.line(
            surface, COLOR_GRID, (ox + x * CELL, oy), (ox + x * CELL, oy + bh * CELL)
        )
    for y in range(bh + 1):
        pygame.draw.line(
            surface, COLOR_GRID, (ox, oy + y * CELL), (ox + bw * CELL, oy + y * CELL)
        )

    def cell_rect(cx: int, cy: int, pad: int = 1) -> pygame.Rect:
        return pygame.Rect(
            ox + cx * CELL + pad, oy + cy * CELL + pad, CELL - 2 * pad, CELL - 2 * pad
        )

    for ox_, oy_ in state.obstacles:
        pygame.draw.rect(surface, COLOR_OBSTACLE, cell_rect(ox_, oy_, 0))

    fx, fy = state.food_position
    if fx >= 0 and fy >= 0:
        pygame.draw.rect(surface, COLOR_FOOD, cell_rect(fx, fy, 4), border_radius=6)

    for i, (sx, sy) in enumerate(state.snake_body):
        color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
        pygame.draw.rect(surface, color, cell_rect(sx, sy, 1), border_radius=4)


def draw_sidebar(
    surface: pygame.Surface,
    state: Any,
    title: str,
    stats: Sequence[tuple[str, str]],
    footer: Sequence[str] = (),
    observation_lines: Sequence[str] = (),
) -> None:
    """Render the info panel: title, key/value stats, footer, observation."""
    bw = state.board_width
    x = MARGIN * 2 + bw * CELL + 12
    y = MARGIN

    title_surf = _font(26, bold=True).render(title, True, COLOR_ACCENT)
    surface.blit(title_surf, (x, y))
    y += 44

    label_font = _font(18)
    value_font = _font(20, bold=True)
    for label, value in stats:
        surface.blit(label_font.render(label, True, COLOR_TEXT_DIM), (x, y))
        surface.blit(value_font.render(str(value), True, COLOR_TEXT), (x + 130, y - 1))
        y += 30

    if observation_lines:
        y += 14
        surface.blit(_font(18, bold=True).render("Observation", True, COLOR_ACCENT), (x, y))
        y += 26
        mono = _font(17)
        for line in observation_lines:
            color = COLOR_TEXT
            if line.endswith("danger"):
                color = COLOR_DANGER
            elif line.endswith("safe"):
                color = COLOR_SAFE
            surface.blit(mono.render(line, True, color), (x, y))
            y += 22

    if footer:
        fy = MARGIN + state.board_height * CELL - len(footer) * 20
        small = _font(15)
        for line in footer:
            surface.blit(small.render(line, True, COLOR_TEXT_DIM), (x, fy))
            fy += 20


def draw_center_banner(
    surface: pygame.Surface, state: Any, lines: Sequence[tuple[str, tuple[int, int, int]]]
) -> None:
    """Translucent overlay with centered lines (e.g. GAME OVER)."""
    bw, bh = state.board_width, state.board_height
    overlay = pygame.Surface((bw * CELL, bh * CELL), pygame.SRCALPHA)
    overlay.fill((10, 10, 16, 200))
    surface.blit(overlay, (MARGIN, MARGIN))

    cx = MARGIN + bw * CELL // 2
    cy = MARGIN + bh * CELL // 2
    total_h = len(lines) * 40
    y = cy - total_h // 2
    for text, color in lines:
        surf = _font(34, bold=True).render(text, True, color)
        surface.blit(surf, (cx - surf.get_width() // 2, y))
        y += 46
