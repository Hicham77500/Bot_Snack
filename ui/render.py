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
SIDEBAR = 260          # right-hand info panel width
MARGIN = 20

# --- Palette (modern dark / neon accent) ------------------------------------
COLOR_BG = (10, 12, 20)
COLOR_GRID = (28, 32, 48)
COLOR_GRID_ALT = (22, 26, 38)
COLOR_BOARD = (16, 20, 32)
COLOR_BOARD_BORDER = (48, 56, 80)
COLOR_PANEL = (18, 22, 36)
COLOR_PANEL_BORDER = (40, 48, 72)
COLOR_SNAKE_HEAD = (56, 255, 156)
COLOR_SNAKE_BODY = (32, 180, 110)
COLOR_SNAKE_TAIL = (20, 120, 78)
COLOR_FOOD = (255, 88, 108)
COLOR_FOOD_GLOW = (255, 88, 108, 60)
COLOR_OBSTACLE = (52, 58, 78)
COLOR_OBSTACLE_EDGE = (72, 80, 108)
COLOR_TEXT = (236, 240, 252)
COLOR_TEXT_DIM = (120, 128, 158)
COLOR_ACCENT = (100, 180, 255)
COLOR_ACCENT_GLOW = (100, 180, 255, 40)
COLOR_WARN = (255, 200, 80)
COLOR_DANGER = (255, 90, 110)
COLOR_SAFE = (56, 255, 156)
COLOR_MENU_SELECT = (24, 32, 52)
COLOR_MENU_SELECT_BORDER = (80, 140, 220)


def board_pixel_size(width: int, height: int) -> tuple[int, int]:
    """Full window size (board + sidebar) for a given board in cells."""
    w = MARGIN * 2 + width * CELL + SIDEBAR
    h = MARGIN * 2 + height * CELL
    return w, h


def _font(size: int, bold: bool = False) -> pygame.font.Font:
    return pygame.font.SysFont("sfmono-regular,consolas,menlo,monospace", size, bold=bold)


def _lerp_color(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = max(0.0, min(1.0, t))
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )


def _draw_rounded_panel(
    surface: pygame.Surface,
    rect: pygame.Rect,
    fill: tuple[int, int, int],
    border: tuple[int, int, int],
    radius: int = 10,
    border_width: int = 1,
) -> None:
    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    if border_width:
        pygame.draw.rect(surface, border, rect, width=border_width, border_radius=radius)


def _truncate_text(font: pygame.font.Font, text: str, max_width: int) -> str:
    """Shorten *text* with an ellipsis so it fits *max_width* pixels."""
    if max_width <= 0 or not text:
        return text
    if font.size(text)[0] <= max_width:
        return text
    ell = "…"
    trimmed = text
    while len(trimmed) > 1 and font.size(trimmed + ell)[0] > max_width:
        trimmed = trimmed[:-1]
    return trimmed + ell if trimmed else ell


FooterLine = str | tuple[str, tuple[int, int, int]]


def draw_board(surface: pygame.Surface, state: Any) -> None:
    """Render the play area from a GameState-like object."""
    surface.fill(COLOR_BG)
    ox, oy = MARGIN, MARGIN
    bw, bh = state.board_width, state.board_height
    board_w, board_h = bw * CELL, bh * CELL

    # Board frame
    frame = pygame.Rect(ox - 3, oy - 3, board_w + 6, board_h + 6)
    _draw_rounded_panel(surface, frame, COLOR_BOARD_BORDER, COLOR_BOARD_BORDER, radius=8)

    board_rect = pygame.Rect(ox, oy, board_w, board_h)
    _draw_rounded_panel(surface, board_rect, COLOR_BOARD, COLOR_BOARD, radius=6)

    # Subtle checker / grid
    for cy in range(bh):
        for cx in range(bw):
            if (cx + cy) % 2 == 0:
                r = pygame.Rect(ox + cx * CELL, oy + cy * CELL, CELL, CELL)
                pygame.draw.rect(surface, COLOR_GRID_ALT, r)
    for x in range(bw + 1):
        pygame.draw.line(
            surface, COLOR_GRID, (ox + x * CELL, oy), (ox + x * CELL, oy + board_h)
        )
    for y in range(bh + 1):
        pygame.draw.line(
            surface, COLOR_GRID, (ox, oy + y * CELL), (ox + board_w, oy + y * CELL)
        )

    def cell_rect(cx: int, cy: int, pad: int = 1) -> pygame.Rect:
        return pygame.Rect(
            ox + cx * CELL + pad, oy + cy * CELL + pad, CELL - 2 * pad, CELL - 2 * pad
        )

    # Obstacles — beveled blocks
    for ox_, oy_ in state.obstacles:
        r = cell_rect(ox_, oy_, 1)
        pygame.draw.rect(surface, COLOR_OBSTACLE, r, border_radius=5)
        pygame.draw.rect(surface, COLOR_OBSTACLE_EDGE, r, width=1, border_radius=5)
        highlight = r.inflate(-4, -4)
        highlight.height = 3
        pygame.draw.rect(surface, (68, 74, 98), highlight, border_radius=2)

    # Food — glow + core
    fx, fy = state.food_position
    if fx >= 0 and fy >= 0:
        center = (ox + fx * CELL + CELL // 2, oy + fy * CELL + CELL // 2)
        glow = pygame.Surface((CELL * 2, CELL * 2), pygame.SRCALPHA)
        for radius, alpha in ((22, 35), (16, 55), (10, 80)):
            pygame.draw.circle(glow, (*COLOR_FOOD[:3], alpha), (CELL, CELL), radius)
        surface.blit(glow, (center[0] - CELL, center[1] - CELL))
        food_r = cell_rect(fx, fy, 5)
        pygame.draw.rect(surface, COLOR_FOOD, food_r, border_radius=8)
        inner = food_r.inflate(-6, -6)
        pygame.draw.rect(surface, (255, 140, 150), inner, border_radius=4)

    # Snake — gradient head → tail
    body_len = max(len(state.snake_body), 1)
    for i, (sx, sy) in enumerate(state.snake_body):
        if i == 0:
            color = COLOR_SNAKE_HEAD
            pad = 0
            radius = 7
        else:
            t = i / max(body_len - 1, 1)
            color = _lerp_color(COLOR_SNAKE_BODY, COLOR_SNAKE_TAIL, t)
            pad = 1
            radius = 5
        r = cell_rect(sx, sy, pad)
        pygame.draw.rect(surface, color, r, border_radius=radius)
        if i == 0:
            # Eyes on head
            hx, hy = r.centerx, r.centery
            pygame.draw.circle(surface, (12, 18, 28), (hx - 4, hy - 3), 3)
            pygame.draw.circle(surface, (12, 18, 28), (hx + 4, hy - 3), 3)
            pygame.draw.circle(surface, (220, 255, 240), (hx - 5, hy - 4), 1)
            pygame.draw.circle(surface, (220, 255, 240), (hx + 3, hy - 4), 1)


def draw_sidebar(
    surface: pygame.Surface,
    state: Any,
    title: str,
    stats: Sequence[tuple[str, str | int]],
    footer: Sequence[FooterLine] = (),
    observation_lines: Sequence[str] = (),
) -> None:
    """Render the info panel: title, key/value stats, footer, observation."""
    bw = state.board_width
    panel_x = MARGIN * 2 + bw * CELL + 8
    panel_y = MARGIN - 3
    panel_h = state.board_height * CELL + 6
    panel_w = SIDEBAR - 16
    inner_w = panel_w - 32

    panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
    _draw_rounded_panel(surface, panel_rect, COLOR_PANEL, COLOR_PANEL_BORDER, radius=10)

    prev_clip = surface.get_clip()
    surface.set_clip(panel_rect)

    x = panel_x + 16
    y = panel_y + 16

    # Accent bar under title
    title_surf = _font(24, bold=True).render(title, True, COLOR_ACCENT)
    surface.blit(title_surf, (x, y))
    y += 32
    pygame.draw.line(surface, COLOR_ACCENT, (x, y), (x + inner_w, y), 2)
    y += 16

    label_font = _font(16)
    value_font = _font(18, bold=True)
    for label, value in stats:
        label_surf = label_font.render(label, True, COLOR_TEXT_DIM)
        surface.blit(label_surf, (x, y))
        max_val_w = inner_w - label_surf.get_width() - 10
        val_text = _truncate_text(value_font, str(value), max(0, max_val_w))
        val_surf = value_font.render(val_text, True, COLOR_TEXT)
        surface.blit(val_surf, (panel_x + panel_w - 16 - val_surf.get_width(), y - 1))
        y += 28

    if observation_lines:
        y += 8
        obs_title = _font(16, bold=True).render("Observation", True, COLOR_ACCENT)
        surface.blit(obs_title, (x, y))
        y += 24
        mono = _font(15)
        for line in observation_lines:
            color = COLOR_TEXT
            if line.endswith("danger"):
                color = COLOR_DANGER
            elif line.endswith("safe"):
                color = COLOR_SAFE
            line_text = _truncate_text(mono, line, inner_w)
            line_surf = mono.render(line_text, True, color)
            if line.endswith(("danger", "safe")):
                pill = line_surf.get_rect(topleft=(x, y))
                pill.inflate_ip(8, 4)
                bg = (40, 20, 28) if line.endswith("danger") else (16, 36, 28)
                pygame.draw.rect(surface, bg, pill, border_radius=4)
            surface.blit(line_surf, (x, y))
            y += 22

    if footer:
        fy = panel_y + panel_h - 16 - len(footer) * 18
        small = _font(13)
        for line in footer:
            if isinstance(line, tuple):
                text, color = line
            else:
                text, color = line, COLOR_TEXT_DIM
            text = _truncate_text(small, text, inner_w)
            surface.blit(small.render(text, True, color), (x, fy))
            fy += 18

    surface.set_clip(prev_clip)


def draw_center_banner(
    surface: pygame.Surface, state: Any, lines: Sequence[tuple[str, tuple[int, int, int]]]
) -> None:
    """Translucent overlay with centered lines (e.g. GAME OVER)."""
    bw, bh = state.board_width, state.board_height
    board_w, board_h = bw * CELL, bh * CELL
    ox, oy = MARGIN, MARGIN

    overlay = pygame.Surface((board_w, board_h), pygame.SRCALPHA)
    overlay.fill((6, 8, 16, 210))
    surface.blit(overlay, (ox, oy))

    total_h = len(lines) * 44 + 24
    card_w = min(board_w - 40, 320)
    card_h = total_h
    card = pygame.Rect(ox + (board_w - card_w) // 2, oy + (board_h - card_h) // 2, card_w, card_h)
    _draw_rounded_panel(surface, card, (22, 28, 44), COLOR_PANEL_BORDER, radius=12, border_width=2)

    cx = card.centerx
    y = card.y + 16
    for text, color in lines:
        surf = _font(32, bold=True).render(text, True, color)
        surface.blit(surf, (cx - surf.get_width() // 2, y))
        y += 44


def draw_menu_item(
    surface: pygame.Surface,
    text: str,
    center_x: int,
    y: int,
    selected: bool,
) -> None:
    """Draw a single menu entry with optional selection highlight."""
    font = _font(28, bold=selected)
    surf = font.render(text, True, COLOR_ACCENT if selected else COLOR_TEXT)
    rect = surf.get_rect(center=(center_x, y + surf.get_height() // 2))
    rect.inflate_ip(32, 14)

    if selected:
        glow = pygame.Surface((rect.width + 8, rect.height + 8), pygame.SRCALPHA)
        pygame.draw.rect(glow, COLOR_ACCENT_GLOW, glow.get_rect(), border_radius=10)
        surface.blit(glow, (rect.x - 4, rect.y - 4))
        _draw_rounded_panel(surface, rect, COLOR_MENU_SELECT, COLOR_MENU_SELECT_BORDER, radius=8, border_width=2)

    surface.blit(surf, (center_x - surf.get_width() // 2, y))


def menu_stats_card_height(stat_count: int) -> int:
    """Vertical size of the menu stats card (stats rows + engine footer)."""
    row_h = 26
    pad_top = 14
    sep_gap = 8
    engine_h = 16
    pad_bottom = 12
    return pad_top + stat_count * row_h + sep_gap + engine_h + pad_bottom


def draw_menu_stats_card(
    surface: pygame.Surface,
    center_x: int,
    top_y: int,
    stats: Sequence[tuple[str, str]],
    engine_label: str,
    engine_real: bool,
) -> int:
    """Draw the menu stats panel with an engine line inside. Returns bottom y."""
    card_w = 240
    row_h = 26
    pad_top = 14
    sep_gap = 8
    engine_h = 16
    pad_bottom = 12
    card_h = pad_top + len(stats) * row_h + sep_gap + engine_h + pad_bottom

    card = pygame.Rect(center_x - card_w // 2, top_y, card_w, card_h)
    _draw_rounded_panel(surface, card, COLOR_PANEL, COLOR_PANEL_BORDER, radius=10)

    sy = card.y + pad_top
    label_font = _font(15)
    value_font = _font(17, bold=True)
    for label, val in stats:
        surface.blit(label_font.render(label, True, COLOR_TEXT_DIM), (card.x + 16, sy))
        val_surf = value_font.render(val, True, COLOR_TEXT)
        surface.blit(val_surf, (card.right - 16 - val_surf.get_width(), sy))
        sy += row_h

    sep_y = sy + 2
    pygame.draw.line(
        surface,
        COLOR_PANEL_BORDER,
        (card.x + 16, sep_y),
        (card.right - 16, sep_y),
        1,
    )

    eng_color = COLOR_SAFE if engine_real else COLOR_WARN
    eng = _font(12).render(f"engine: {engine_label}", True, eng_color)
    eng_y = sep_y + sep_gap
    surface.blit(eng, (center_x - eng.get_width() // 2, eng_y))

    return card.bottom
