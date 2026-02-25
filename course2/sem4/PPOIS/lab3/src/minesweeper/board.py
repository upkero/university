from __future__ import annotations

import random


class Board:
    def __init__(self, rows: int, cols: int, mines: int, rng: random.Random) -> None:
        self.rng = rng
        self.reset(rows, cols, mines)

    def reset(self, rows: int, cols: int, mines: int) -> None:
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.mines_placed = False
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flags = [[False for _ in range(cols)] for _ in range(rows)]
        self.revealed_count = 0

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r: int, c: int) -> list[tuple[int, int]]:
        out = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if self.in_bounds(nr, nc):
                    out.append((nr, nc))
        return out

    def place_mines(self, exclude: tuple[int, int]) -> None:
        safe_zone = set(self.neighbors(*exclude))
        safe_zone.add(exclude)
        cells = [(r, c) for r in range(self.rows) for c in range(self.cols) if (r, c) not in safe_zone]
        if len(cells) < self.mines:
            cells = [(r, c) for r in range(self.rows) for c in range(self.cols) if (r, c) != exclude]
        self.rng.shuffle(cells)
        for r, c in cells[: self.mines]:
            self.grid[r][c] = -1
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == -1:
                    continue
                count = 0
                for nr, nc in self.neighbors(r, c):
                    if self.grid[nr][nc] == -1:
                        count += 1
                self.grid[r][c] = count
        self.mines_placed = True

    def reveal(self, r: int, c: int) -> tuple[list[tuple[int, int]], bool]:
        if not self.in_bounds(r, c) or self.flags[r][c] or self.revealed[r][c]:
            return [], False
        if not self.mines_placed:
            self.place_mines((r, c))
        if self.grid[r][c] == -1:
            self.revealed[r][c] = True
            self.revealed_count += 1
            return [(r, c)], True
        revealed_cells: list[tuple[int, int]] = []
        queue = [(r, c)]
        while queue:
            cr, cc = queue.pop()
            if not self.in_bounds(cr, cc) or self.flags[cr][cc] or self.revealed[cr][cc]:
                continue
            self.revealed[cr][cc] = True
            self.revealed_count += 1
            revealed_cells.append((cr, cc))
            if self.grid[cr][cc] == 0:
                for nr, nc in self.neighbors(cr, cc):
                    if not self.revealed[nr][nc] and not self.flags[nr][nc]:
                        queue.append((nr, nc))
        return revealed_cells, False

    def chord(self, r: int, c: int) -> tuple[list[tuple[int, int]], bool]:
        if not self.in_bounds(r, c) or not self.revealed[r][c] or self.grid[r][c] <= 0:
            return [], False
        flag_count = 0
        for nr, nc in self.neighbors(r, c):
            if self.flags[nr][nc]:
                flag_count += 1
        if flag_count != self.grid[r][c]:
            return [], False
        revealed_cells: list[tuple[int, int]] = []
        hit_mine = False
        for nr, nc in self.neighbors(r, c):
            if not self.revealed[nr][nc] and not self.flags[nr][nc]:
                cells, mine = self.reveal(nr, nc)
                revealed_cells.extend(cells)
                if mine:
                    hit_mine = True
        return revealed_cells, hit_mine

    def toggle_flag(self, r: int, c: int) -> None:
        if self.in_bounds(r, c) and not self.revealed[r][c]:
            self.flags[r][c] = not self.flags[r][c]

    def is_win(self) -> bool:
        return self.revealed_count >= (self.rows * self.cols - self.mines)

    def reveal_all_mines(self) -> None:
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == -1:
                    self.revealed[r][c] = True
