"""Auto AI mode — DQN agent plays Snake with visual feedback."""

import argparse
import sys

import pygame

from agents.dqn_agent import DQNAgent
from environment.snake_env import SnakeEnv
from ui.game_view import GameView, CELL_SIZE, COLORS, FPS


class AutoPlayView(GameView):
    def __init__(self, level: int = 1, model_path: str = "models/best_agent.pth"):
        super().__init__(level=level)
        self.env = SnakeEnv(level=level)
        self.agent = DQNAgent(
            state_size=self.env.observation_size,
            action_size=self.env.action_size,
        )
        try:
            self.agent.load(model_path)
            self.agent.epsilon = 0.0
        except FileNotFoundError:
            print(f"Model not found: {model_path}")
            print("Train first: python -m training.train")
            sys.exit(1)
        self.obs = self.env.reset(level=level)
        self.episode = 1
        self.best_score = 0

    def run(self) -> None:
        self.setup()
        self.mode = "auto"
        running = True
        step_delay = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if step_delay <= 0 and not self.state.done:
                action = self.agent.select_action(self.obs, training=False)
                self.obs, _, done, info = self.env.step(action)
                self.state = self.env.game.get_state()
                step_delay = 3
            elif self.state.done:
                if info["score"] > self.best_score:
                    self.best_score = info["score"]
                self.obs = self.env.reset(level=self.level)
                self.state = self.env.game.get_state()
                self.episode += 1
                step_delay = 30
            else:
                step_delay -= 1

            self._draw_auto_hud()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()

    def _draw_auto_hud(self) -> None:
        assert self.screen and self.small_font
        hud_x = self.state.board_width * CELL_SIZE + 30
        lines = [
            f"Episode: {self.episode}",
            f"Level: {self.state.level}",
            f"Score: {self.state.score}",
            f"Best: {self.best_score}",
            "Agent: DQN",
        ]
        for i, line in enumerate(lines):
            text = self.small_font.render(line, True, COLORS["text"])
            self.screen.blit(text, (hud_x, 20 + i * 28))


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto AI Snake")
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--model", type=str, default="models/best_agent.pth")
    args = parser.parse_args()

    view = AutoPlayView(level=args.level, model_path=args.model)
    view.run()


if __name__ == "__main__":
    main()
