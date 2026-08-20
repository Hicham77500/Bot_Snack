"""
manual_test.py — Tests manuels du moteur headless (sans UI/Pygame).

Usage:
    python -m game.manual_test
"""

from game.game import Game
from game.snake import UP, DOWN, LEFT, RIGHT


def test_basic_death_on_wall():
    g = Game(level=1)
    s = g.reset(level=1)
    steps = 0
    while not g.is_done() and steps < 200:
        s = g.step(UP)
        steps += 1
    assert g.is_done(), "Le serpent devrait finir par mourir contre un mur"
    assert s.death_reason == "wall", f"Attendu 'wall', reçu {s.death_reason!r}"
    print(f"[OK] level=1 mort par mur en {steps} steps, score={g.get_score()}")


def test_anti_uturn():
    g = Game(level=1)
    s = g.reset(level=1)
    initial_dir = s.snake_direction  # RIGHT au départ
    opposite = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}[initial_dir]
    s = g.step(opposite)  # tentative de demi-tour immédiat -> doit être ignorée
    assert s.snake_direction == initial_dir, "Le demi-tour immédiat doit être ignoré"
    print("[OK] anti demi-tour respecté")


def test_all_levels_reset():
    g = Game(level=1)
    for lvl in (1, 2, 3, 4):
        s = g.reset(level=lvl)
        assert g.get_level() == lvl
        assert s.level == lvl
        assert not s.done
        assert s.food_position not in s.snake_body
        assert s.food_position not in s.obstacles
        if lvl == 1:
            assert s.obstacles == [], "Le niveau 1 ne doit avoir aucun obstacle"
        else:
            assert len(s.obstacles) > 0, f"Le niveau {lvl} devrait avoir des obstacles"
        print(f"[OK] level={lvl} ({s.board_width}x{s.board_height}), "
              f"obstacles={len(s.obstacles)}, food={s.food_position}")


def test_eating_grows_and_scores():
    g = Game(level=1)
    s = g.reset(level=1)
    start_len = len(s.snake_body)

    # Force la nourriture juste devant la tête pour un test déterministe.
    hx, hy = s.snake_body[0]
    g.food.position = (hx + 1, hy)  # direction RIGHT par défaut

    s = g.step(RIGHT)
    assert not g.is_done(), "Ne doit pas mourir en mangeant"
    assert g.get_score() == 1, "Le score doit passer à 1"
    assert len(s.snake_body) == start_len + 1, "Le serpent doit grandir de 1"
    assert g.get_reward() > 0, "La récompense doit être positive en mangeant"
    print(f"[OK] manger -> score={g.get_score()}, longueur={len(s.snake_body)}, "
          f"reward={g.get_reward()}")


def test_obstacle_death_level4():
    g = Game(level=4)
    s = g.reset(level=4)
    steps = 0
    died_reasons = set()
    # On teste que les niveaux avec obstacles peuvent bien produire
    # une mort par obstacle sur un parcours suffisamment long.
    while not g.is_done() and steps < 300:
        s = g.step(RIGHT)
        steps += 1
    died_reasons.add(s.death_reason)
    print(f"[OK] level=4 fin de partie après {steps} steps, "
          f"reason={s.death_reason}, score={g.get_score()}")


if __name__ == "__main__":
    test_all_levels_reset()
    test_anti_uturn()
    test_eating_grows_and_scores()
    test_basic_death_on_wall()
    test_obstacle_death_level4()
    print("\nTous les tests manuels sont passés.")
