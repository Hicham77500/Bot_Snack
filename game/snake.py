"""Snake entity."""

from dataclasses import dataclass, field

DIRECTIONS = {
    0: (0, -1),   # UP
    1: (0, 1),    # DOWN
    2: (-1, 0),   # LEFT
    3: (1, 0),    # RIGHT
}


@dataclass
class Snake:
    body: list[tuple[int, int]] = field(default_factory=list)
    direction: tuple[int, int] = (1, 0)

    def head(self) -> tuple[int, int]:
        return self.body[0]

    def set_direction(self, action: int) -> None:
        new_dir = DIRECTIONS[action]
        # Prevent 180-degree turn
        if (new_dir[0] + self.direction[0], new_dir[1] + self.direction[1]) == (0, 0):
            return
        self.direction = new_dir

    def move(self, grow: bool = False) -> tuple[int, int]:
        hx, hy = self.head()
        dx, dy = self.direction
        new_head = (hx + dx, hy + dy)
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()
        return new_head

    def collides_with_self(self, position: tuple[int, int]) -> bool:
        return position in self.body
