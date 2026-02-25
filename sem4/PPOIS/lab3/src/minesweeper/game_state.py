from __future__ import annotations

import random

from .board import Board


class GameState:
    def __init__(self, rows: int, cols: int, mines: int, mode: str, time_limit_sec: int, rng: random.Random) -> None:
        self.board = Board(rows, cols, mines, rng)
        self.mode = mode
        self.time_limit_sec = time_limit_sec
        self.status = "playing"
        self.start_time: float | None = None
        self.end_time: float | None = None
        self.reveal_anims: dict[tuple[int, int], float] = {}
        self.particles: list[dict] = []
        self.last_mine_cell: tuple[int, int] | None = None

    def elapsed(self, now: float) -> float:
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time is not None else now
        return max(0.0, end - self.start_time)

    def time_left(self, now: float) -> float:
        return self.time_limit_sec - self.elapsed(now)
