from __future__ import annotations

import math
import random
import time

import pygame

from .audio import AudioManager, ensure_sound_files
from .game_state import GameState
from .paths import BASE_DIR, CONFIG_PATH, HELP_PATH
from .records import RecordStore
from .utils import format_time, load_json, mix_color, strip_markdown, wrap_text


class App:
    def __init__(self) -> None:
        self.cfg = load_json(CONFIG_PATH)
        self.colors = {k: tuple(v) for k, v in self.cfg.get("colors", {}).items()}
        self.number_colors = {int(k): tuple(v) for k, v in self.cfg.get("number_colors", {}).items()}
        self.ui = self.cfg.get("ui", {})
        self.hints = self.ui.get("hints", {})
        self.modes = list(self.cfg.get("modes", {}).keys())
        self.levels = list(self.cfg.get("levels", {}).keys())
        self.menu_items = ["начать игру", "таблица рекордов", "справка", "выход"]
        self.menu_index = 0
        self.mode_index = 0
        self.level_index = 0
        self.selected_mode = self.modes[self.mode_index]
        self.selected_level = self.levels[self.level_index]
        self.state = "menu"
        self.running = True
        self.game: GameState | None = None
        self.rng = random.Random()
        self.record_input = ""
        self.pending_record_time: float | None = None
        self.menu_item_rects: list[pygame.Rect] = []

        pygame.init()
        ensure_sound_files(self.cfg, BASE_DIR)
        self.audio = AudioManager(self.cfg, BASE_DIR)
        self.screen = self._set_menu_mode()
        pygame.display.set_caption(self.cfg.get("window", {}).get("caption", "Minesweeper"))
        self.clock = pygame.time.Clock()

        font_name = self.ui.get("font_name") or None
        self.font = pygame.font.Font(font_name, 22)
        self.font_small = pygame.font.Font(font_name, 18)
        self.font_large = pygame.font.Font(font_name, 32)

        self.records = RecordStore(self.cfg, BASE_DIR)

        self.help_text = ""
        if HELP_PATH.exists():
            self.help_text = HELP_PATH.read_text(encoding="utf-8-sig")

    def _play_sfx(self, key: str) -> None:
        self.audio.play(key)

    def _set_menu_mode(self) -> pygame.Surface:
        size = self.cfg.get("window", {}).get("menu_size", [800, 600])
        return pygame.display.set_mode(size)

    def _set_game_mode(self, rows: int, cols: int) -> pygame.Surface:
        cell = int(self.ui.get("cell_size", 28))
        margin = int(self.ui.get("margin", 16))
        top_bar = int(self.ui.get("top_bar", 64))
        width = cols * cell + margin * 2
        height = rows * cell + top_bar + margin
        return pygame.display.set_mode((width, height))

    def _start_game(self) -> None:
        level_cfg = self.cfg.get("levels", {})[self.selected_level]
        rows = int(level_cfg["rows"])
        cols = int(level_cfg["cols"])
        mines = int(level_cfg["mines"])
        time_limit = int(level_cfg.get("time_limit_sec", 0))
        if self.selected_mode == "timed":
            timed_cfg = self.cfg.get("modes", {}).get("timed", {})
            time_limits = timed_cfg.get("time_limits", {})
            if self.selected_level in time_limits:
                time_limit = int(time_limits[self.selected_level])
        else:
            time_limit = 0
        self.game = GameState(rows, cols, mines, self.selected_mode, time_limit, self.rng)
        self.screen = self._set_game_mode(rows, cols)
        self.state = "game"

    def _cell_from_pos(self, pos: tuple[int, int]) -> tuple[int, int] | None:
        if not self.game:
            return None
        cell = int(self.ui.get("cell_size", 28))
        margin = int(self.ui.get("margin", 16))
        top_bar = int(self.ui.get("top_bar", 64))
        x, y = pos
        if y < top_bar:
            return None
        col = (x - margin) // cell
        row = (y - top_bar) // cell
        if 0 <= row < self.game.board.rows and 0 <= col < self.game.board.cols:
            return int(row), int(col)
        return None

    def _new_particles(self, cell: tuple[int, int]) -> None:
        if not self.game:
            return
        cell_size = int(self.ui.get("cell_size", 28))
        margin = int(self.ui.get("margin", 16))
        top_bar = int(self.ui.get("top_bar", 64))
        r, c = cell
        cx = margin + c * cell_size + cell_size / 2
        cy = top_bar + r * cell_size + cell_size / 2
        for _ in range(30):
            angle = self.rng.random() * math.tau
            speed = 80 + self.rng.random() * 160
            self.game.particles.append(
                {
                    "x": cx,
                    "y": cy,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": 0.6 + self.rng.random() * 0.6,
                }
            )

    def _handle_reveal(self, cells: list[tuple[int, int]], hit_mine: bool) -> None:
        if not self.game:
            return
        for cell in cells:
            self.game.reveal_anims[cell] = 0.0
        if cells and not hit_mine:
            self._play_sfx("reveal")

    def _win_game(self) -> None:
        if not self.game or self.game.status != "playing":
            return
        self.game.status = "won"
        now = time.perf_counter()
        self.game.end_time = now
        self._play_sfx("win")
        elapsed = self.game.elapsed(now)
        best = self.records.best(self.selected_mode, self.selected_level)
        if elapsed < best:
            self.pending_record_time = elapsed
            self.record_input = ""
            self.state = "record_input"

    def _lose_game(self, reason: str = "mine") -> None:
        if not self.game or self.game.status != "playing":
            return
        self.game.status = "lost"
        now = time.perf_counter()
        self.game.end_time = now
        self.game.board.reveal_all_mines()
        if reason == "mine" and self.game.last_mine_cell:
            self._new_particles(self.game.last_mine_cell)
            self._play_sfx("boom")
        else:
            self._play_sfx("lose")

    def _update_game(self, dt: float) -> None:
        if not self.game:
            return
        now = time.perf_counter()
        if self.game.status == "playing" and self.game.start_time is not None:
            if self.game.mode == "timed" and self.game.time_left(now) <= 0:
                self._lose_game("time")
        for cell in list(self.game.reveal_anims.keys()):
            self.game.reveal_anims[cell] += dt
            if self.game.reveal_anims[cell] >= 0.2:
                del self.game.reveal_anims[cell]
        for particle in list(self.game.particles):
            particle["life"] -= dt
            particle["x"] += particle["vx"] * dt
            particle["y"] += particle["vy"] * dt
            particle["vy"] += 120 * dt
            if particle["life"] <= 0:
                self.game.particles.remove(particle)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(int(self.ui.get("fps", 60))) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.state == "menu":
                    self._handle_menu_event(event)
                elif self.state == "select":
                    self._handle_select_event(event)
                elif self.state == "records":
                    self._handle_records_event(event)
                elif self.state == "help":
                    self._handle_help_event(event)
                elif self.state == "game":
                    self._handle_game_event(event)
                elif self.state == "record_input":
                    self._handle_record_input_event(event)

            if self.state in ("game", "record_input"):
                self._update_game(dt)

            self._draw()

        pygame.quit()

    def _handle_menu_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.menu_index = (self.menu_index - 1) % len(self.menu_items)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.menu_index = (self.menu_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                self._activate_menu_item(self.menu_index)
            elif event.key == pygame.K_ESCAPE:
                self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, rect in enumerate(self.menu_item_rects):
                if rect.collidepoint(event.pos):
                    self._activate_menu_item(idx)
                    break

    def _activate_menu_item(self, idx: int) -> None:
        item = self.menu_items[idx]
        if item == "начать игру":
            self.state = "select"
        elif item == "таблица рекордов":
            self.state = "records"
        elif item == "справка":
            self.state = "help"
        elif item == "выход":
            self.running = False

    def _handle_select_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.mode_index = (self.mode_index - 1) % len(self.modes)
            self.selected_mode = self.modes[self.mode_index]
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.mode_index = (self.mode_index + 1) % len(self.modes)
            self.selected_mode = self.modes[self.mode_index]
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.level_index = (self.level_index - 1) % len(self.levels)
            self.selected_level = self.levels[self.level_index]
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.level_index = (self.level_index + 1) % len(self.levels)
            self.selected_level = self.levels[self.level_index]
        elif event.key == pygame.K_RETURN:
            self._start_game()
        elif event.key == pygame.K_ESCAPE:
            self.state = "menu"

    def _handle_records_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.mode_index = (self.mode_index - 1) % len(self.modes)
            self.selected_mode = self.modes[self.mode_index]
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.mode_index = (self.mode_index + 1) % len(self.modes)
            self.selected_mode = self.modes[self.mode_index]
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.level_index = (self.level_index - 1) % len(self.levels)
            self.selected_level = self.levels[self.level_index]
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.level_index = (self.level_index + 1) % len(self.levels)
            self.selected_level = self.levels[self.level_index]
        elif event.key == pygame.K_ESCAPE:
            self.state = "menu"

    def _handle_help_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = "menu"

    def _handle_game_event(self, event: pygame.event.Event) -> None:
        if not self.game:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = "menu"
                self.screen = self._set_menu_mode()
            if self.game.status != "playing" and event.key == pygame.K_RETURN:
                self._start_game()
            return
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if self.game.status != "playing":
            return
        cell = self._cell_from_pos(event.pos)
        if cell is None:
            return
        r, c = cell
        if event.button == 1:
            if self.game.start_time is None:
                self.game.start_time = time.perf_counter()
            if self.game.board.revealed[r][c]:
                cells, hit_mine = self.game.board.chord(r, c)
            else:
                cells, hit_mine = self.game.board.reveal(r, c)
            self._handle_reveal(cells, hit_mine)
            if hit_mine:
                self.game.last_mine_cell = (r, c)
                self._lose_game("mine")
            elif self.game.board.is_win():
                self._win_game()
        elif event.button == 3:
            self.game.board.toggle_flag(r, c)
            self._play_sfx("flag")

    def _handle_record_input_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.state = "menu"
            self.screen = self._set_menu_mode()
            return
        if event.key == pygame.K_RETURN:
            name = self.record_input.strip() or "Player"
            if self.pending_record_time is not None:
                self.records.insert(self.selected_mode, self.selected_level, name, self.pending_record_time)
            self.pending_record_time = None
            self.state = "records"
            self.screen = self._set_menu_mode()
            return
        if event.key == pygame.K_BACKSPACE:
            self.record_input = self.record_input[:-1]
            return
        if event.unicode and len(self.record_input) < 12 and event.unicode.isprintable():
            self.record_input += event.unicode

    def _draw(self) -> None:
        if self.state == "menu":
            self._draw_menu()
        elif self.state == "select":
            self._draw_select()
        elif self.state == "records":
            self._draw_records()
        elif self.state == "help":
            self._draw_help()
        elif self.state == "game":
            self._draw_game()
        elif self.state == "record_input":
            self._draw_game()
            self._draw_record_input()
        pygame.display.flip()

    def _draw_menu(self) -> None:
        self.screen.fill(self.colors.get("bg", (30, 30, 30)))
        title = self.font_large.render("САПЁР", True, self.colors.get("text", (230, 230, 230)))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 80))

        self.menu_item_rects = []
        start_y = 200
        for idx, item in enumerate(self.menu_items):
            color = self.colors.get("accent", (120, 200, 255)) if idx == self.menu_index else self.colors.get(
                "text", (230, 230, 230)
            )
            text = self.font.render(item, True, color)
            rect = text.get_rect(center=(self.screen.get_width() // 2, start_y + idx * 50))
            self.menu_item_rects.append(rect)
            self.screen.blit(text, rect.topleft)

        hint_text = self.hints.get("menu", "W/S - выбор, Enter - выбрать, Esc - выход")
        hint = self.font_small.render(hint_text, True, self.colors.get("text", (230, 230, 230)))
        self.screen.blit(hint, (self.screen.get_width() // 2 - hint.get_width() // 2, self.screen.get_height() - 50))

    def _draw_select(self) -> None:
        self.screen.fill(self.colors.get("bg", (30, 30, 30)))
        title = self.font_large.render("Выбор режима и сложности", True, self.colors.get("text", (230, 230, 230)))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 70))

        mode_label = self.cfg.get("modes", {})[self.selected_mode]["label"]
        level_label = self.cfg.get("levels", {})[self.selected_level]["label"]

        mode_text = self.font.render(f"Режим: {mode_label}", True, self.colors.get("accent", (120, 200, 255)))
        level_text = self.font.render(
            f"Сложность: {level_label}", True, self.colors.get("accent", (120, 200, 255))
        )

        self.screen.blit(mode_text, (self.screen.get_width() // 2 - mode_text.get_width() // 2, 200))
        self.screen.blit(level_text, (self.screen.get_width() // 2 - level_text.get_width() // 2, 260))

        hint_text = self.hints.get("select", "A/D режим, W/S сложность, Enter - старт, Esc - назад")
        hint = self.font_small.render(hint_text, True, self.colors.get("text", (230, 230, 230)))
        self.screen.blit(hint, (self.screen.get_width() // 2 - hint.get_width() // 2, self.screen.get_height() - 60))

    def _draw_records(self) -> None:
        self.screen.fill(self.colors.get("bg", (30, 30, 30)))
        title = self.font_large.render("Таблица рекордов", True, self.colors.get("text", (230, 230, 230)))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 60))

        mode_label = self.cfg.get("modes", {})[self.selected_mode]["label"]
        level_label = self.cfg.get("levels", {})[self.selected_level]["label"]
        header = self.font.render(f"{mode_label} / {level_label}", True, self.colors.get("accent", (120, 200, 255)))
        self.screen.blit(header, (self.screen.get_width() // 2 - header.get_width() // 2, 130))

        entries = self.records.visible_entries(self.selected_mode, self.selected_level)
        start_y = 190
        if entries:
            for i, entry in enumerate(entries, start=1):
                name = entry.get("name", "N/A")
                time_sec = entry.get("time_sec", 9999)
                line = self.font.render(
                    f"{i}. {name} — {format_time(time_sec)}", True, self.colors.get("text", (230, 230, 230))
                )
                self.screen.blit(line, (self.screen.get_width() // 2 - line.get_width() // 2, start_y + i * 35))
        else:
            line = self.font.render("Пока нет рекордов", True, self.colors.get("text", (230, 230, 230)))
            self.screen.blit(line, (self.screen.get_width() // 2 - line.get_width() // 2, start_y + 35))

        hint_text = self.hints.get("records", "A/D режим, W/S сложность, Esc - назад")
        hint = self.font_small.render(hint_text, True, self.colors.get("text", (230, 230, 230)))
        self.screen.blit(hint, (self.screen.get_width() // 2 - hint.get_width() // 2, self.screen.get_height() - 50))

    def _draw_help(self) -> None:
        self.screen.fill(self.colors.get("bg", (30, 30, 30)))
        title = self.font_large.render("Справка", True, self.colors.get("text", (230, 230, 230)))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 40))

        max_width = self.screen.get_width() - 80
        y = 110
        for raw_line in self.help_text.splitlines():
            line = strip_markdown(raw_line)
            if not line:
                y += 12
                continue
            for wrapped in wrap_text(line, self.font_small, max_width):
                text = self.font_small.render(wrapped, True, self.colors.get("text", (230, 230, 230)))
                self.screen.blit(text, (40, y))
                y += 24

        hint_text = self.hints.get("help", "Esc - назад")
        hint = self.font_small.render(hint_text, True, self.colors.get("text", (230, 230, 230)))
        self.screen.blit(hint, (self.screen.get_width() // 2 - hint.get_width() // 2, self.screen.get_height() - 50))

    def _draw_game(self) -> None:
        if not self.game:
            return
        self.screen.fill(self.colors.get("bg", (30, 30, 30)))
        cell = int(self.ui.get("cell_size", 28))
        margin = int(self.ui.get("margin", 16))
        top_bar = int(self.ui.get("top_bar", 64))

        bar_rect = pygame.Rect(0, 0, self.screen.get_width(), top_bar)
        pygame.draw.rect(self.screen, self.colors.get("panel", (45, 45, 50)), bar_rect)

        now = time.perf_counter()
        if self.game.mode == "timed":
            timer_value = max(0, int(self.game.time_left(now)))
            timer_label = f"Время: {format_time(timer_value)}"
        else:
            timer_label = f"Время: {format_time(self.game.elapsed(now))}"
        mines_left = self.game.board.mines - sum(sum(1 for c in row if c) for row in self.game.board.flags)
        mines_label = f"Мины: {mines_left}"

        timer_text = self.font.render(timer_label, True, self.colors.get("text", (230, 230, 230)))
        mines_text = self.font.render(mines_label, True, self.colors.get("text", (230, 230, 230)))
        self.screen.blit(timer_text, (margin, 18))
        self.screen.blit(mines_text, (self.screen.get_width() - mines_text.get_width() - margin, 18))

        for r in range(self.game.board.rows):
            for c in range(self.game.board.cols):
                x = margin + c * cell
                y = top_bar + r * cell
                rect = pygame.Rect(x, y, cell, cell)
                revealed = self.game.board.revealed[r][c]
                flagged = self.game.board.flags[r][c]
                if revealed:
                    color = self.colors.get("cell_revealed", (180, 180, 190))
                    if (r, c) in self.game.reveal_anims:
                        t = 1 - (self.game.reveal_anims[(r, c)] / 0.2)
                        color = mix_color(color, self.colors.get("accent", (120, 200, 255)), t * 0.5)
                    pygame.draw.rect(self.screen, color, rect)
                    if self.game.board.grid[r][c] > 0:
                        num = self.game.board.grid[r][c]
                        num_color = self.number_colors.get(num, self.colors.get("text", (230, 230, 230)))
                        text = self.font.render(str(num), True, num_color)
                        self.screen.blit(
                            text, (x + cell / 2 - text.get_width() / 2, y + cell / 2 - text.get_height() / 2)
                        )
                    if self.game.board.grid[r][c] == -1:
                        pygame.draw.circle(self.screen, self.colors.get("mine", (10, 10, 10)), rect.center, cell // 4)
                else:
                    color = self.colors.get("cell_hidden", (90, 90, 100))
                    pygame.draw.rect(self.screen, color, rect)
                    if flagged:
                        flag_color = self.colors.get("flag", (220, 60, 60))
                        points = [
                            (x + cell * 0.3, y + cell * 0.2),
                            (x + cell * 0.7, y + cell * 0.45),
                            (x + cell * 0.3, y + cell * 0.7),
                        ]
                        pygame.draw.polygon(self.screen, flag_color, points)
                        pygame.draw.line(
                            self.screen,
                            flag_color,
                            (x + cell * 0.3, y + cell * 0.2),
                            (x + cell * 0.3, y + cell * 0.85),
                            2,
                        )
                pygame.draw.rect(self.screen, self.colors.get("cell_border", (50, 50, 58)), rect, 1)

        for particle in self.game.particles:
            pygame.draw.circle(
                self.screen, self.colors.get("lose", (220, 70, 70)), (int(particle["x"]), int(particle["y"])), 3
            )

        if self.game.status == "won":
            label = self.font_large.render("Победа!", True, self.colors.get("win", (80, 200, 120)))
            hint = self.font_small.render(
                "Enter - сыграть ещё, Esc - меню", True, self.colors.get("text", (230, 230, 230))
            )
            self.screen.blit(label, (self.screen.get_width() // 2 - label.get_width() // 2, top_bar + 10))
            self.screen.blit(hint, (self.screen.get_width() // 2 - hint.get_width() // 2, top_bar + 50))
        elif self.game.status == "lost":
            label = self.font_large.render("Поражение", True, self.colors.get("lose", (220, 70, 70)))
            hint = self.font_small.render(
                "Enter - сыграть ещё, Esc - меню", True, self.colors.get("text", (230, 230, 230))
            )
            self.screen.blit(label, (self.screen.get_width() // 2 - label.get_width() // 2, top_bar + 10))
            self.screen.blit(hint, (self.screen.get_width() // 2 - hint.get_width() // 2, top_bar + 50))

    def _draw_record_input(self) -> None:
        if not self.game:
            return
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        title = self.font_large.render("Новый рекорд!", True, self.colors.get("accent", (120, 200, 255)))
        prompt = self.font.render("Введите имя:", True, self.colors.get("text", (230, 230, 230)))
        name = self.font.render(self.record_input + "_", True, self.colors.get("text", (230, 230, 230)))
        box_w = max(300, name.get_width() + 40)
        box_h = 180
        box = pygame.Rect(
            self.screen.get_width() // 2 - box_w // 2,
            self.screen.get_height() // 2 - box_h // 2,
            box_w,
            box_h,
        )
        pygame.draw.rect(self.screen, self.colors.get("panel", (45, 45, 50)), box)
        pygame.draw.rect(self.screen, self.colors.get("accent", (120, 200, 255)), box, 2)
        self.screen.blit(title, (box.centerx - title.get_width() // 2, box.y + 16))
        self.screen.blit(prompt, (box.centerx - prompt.get_width() // 2, box.y + 70))
        self.screen.blit(name, (box.centerx - name.get_width() // 2, box.y + 105))
