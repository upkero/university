import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from dataclasses import dataclass, field
from typing import List, Optional


ALTERNATIVES = [
    ("a1", "Обновить текущую пожарную систему"),
    ("a2", "Выдать в каждую комнату огнетушитель"),
    ("a3", "Установить новую противопожарную систему"),
    ("a4", "Проверить готовность студентов к ЧС (обучение/тренировки)"),
]


@dataclass
class SurveyState:
    alternatives_keys: List[str] = field(default_factory=lambda: [k for k, _ in ALTERNATIVES])
    alternatives_labels: dict = field(default_factory=lambda: {k: v for k, v in ALTERNATIVES})
    experts_count: int = 0
    rankings: List[List[str]] = field(default_factory=list)  # список порядков для каждого эксперта

    def reset(self):
        self.experts_count = 0
        self.rankings = []


class StartFrame(ttk.Frame):
    def __init__(self, master, state: SurveyState, on_start):
        super().__init__(master, padding=15)
        self.state = state
        self.on_start = on_start

        ttk.Label(self, text="Метод Кондорсе", font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, sticky="w")
        desc = (
            "Задача: выбрать наилучшую альтернативу для повышения эффективности\n"
            "пожарной безопасности в общежитии на основе ранжирований экспертов.\n\n"
            "Альтернативы:\n"
            "1) Обновить текущую пожарную систему\n"
            "2) Выдать в каждую комнату огнетушитель\n"
            "3) Установить новую противопожарную систему\n"
            "4) Проверить готовность студентов к ЧС"
        )
        ttk.Label(self, text=desc, justify="left").grid(row=1, column=0, pady=(6, 12), sticky="w")

        box = ttk.Frame(self)
        box.grid(row=2, column=0, sticky="w")
        ttk.Label(box, text="Шаг 1 — Количество экспертов:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.var = tk.StringVar(value="3")
        self.entry = ttk.Entry(box, textvariable=self.var, width=6)
        self.entry.grid(row=0, column=1, sticky="w")
        ttk.Button(box, text="Начать опрос", command=self._start).grid(row=0, column=2, padx=(10, 0))

        self.columnconfigure(0, weight=1)

    def _start(self):
        try:
            n = int(self.var.get())
            if n <= 0 or n > 1000:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите положительное целое число экспертов.")
            return
        self.state.reset()
        self.state.experts_count = n
        self.on_start()


class RankingFrame(ttk.Frame):
    def __init__(self, master, state: SurveyState, on_finish_all, on_cancel):
        super().__init__(master, padding=15)
        self.state = state
        self.on_finish_all = on_finish_all
        self.on_cancel = on_cancel

        self.title = ttk.Label(self, text="", font=("TkDefaultFont", 12, "bold"))
        self.title.grid(row=0, column=0, sticky="w")

        ttk.Label(self, text="Шаг 2 — Упорядочите альтернативы по предпочтению (сверху — лучший вариант).").grid(
            row=1, column=0, sticky="w", pady=(6, 6)
        )

        body = ttk.Frame(self)
        body.grid(row=2, column=0, sticky="nsew")
        self.listbox = tk.Listbox(body, height=len(self.state.alternatives_keys), activestyle="dotbox")
        for k in self.state.alternatives_keys:
            self.listbox.insert(tk.END, self.state.alternatives_labels[k])
        self.listbox.grid(row=0, column=0, rowspan=4, sticky="nsew")

        btns = ttk.Frame(body)
        btns.grid(row=0, column=1, padx=(10, 0), sticky="n")
        ttk.Button(btns, text="↑ Вверх", command=self.move_up).grid(row=0, column=0, sticky="ew", pady=(0, 5))
        ttk.Button(btns, text="↓ Вниз", command=self.move_down).grid(row=1, column=0, sticky="ew")

        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)

        ctl = ttk.Frame(self)
        ctl.grid(row=3, column=0, pady=(12, 0), sticky="e")
        ttk.Button(ctl, text="Сохранить мнение", command=self.save_ranking).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(ctl, text="Отмена", command=self.on_cancel).grid(row=0, column=1)

        self.columnconfigure(0, weight=1)
        self._refresh_title()

    def _refresh_title(self):
        i = len(self.state.rankings) + 1
        self.title.configure(text=f"Мнение эксперта №{i} (эксперт {i} из {self.state.experts_count})")

    def _current_list_keys(self) -> List[str]:
        # сопоставляем текущий порядок видимых подписей с ключами альтернатив
        visible = [self.listbox.get(i) for i in range(self.listbox.size())]
        inv = {v: k for k, v in self.state.alternatives_labels.items()}
        return [inv[v] for v in visible]

    def move_up(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        i = sel[0]
        if i == 0:
            return
        text = self.listbox.get(i)
        self.listbox.delete(i)
        self.listbox.insert(i - 1, text)
        self.listbox.selection_set(i - 1)

    def move_down(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        i = sel[0]
        if i == self.listbox.size() - 1:
            return
        text = self.listbox.get(i)
        self.listbox.delete(i)
        self.listbox.insert(i + 1, text)
        self.listbox.selection_set(i + 1)

    def save_ranking(self):
        order = self._current_list_keys()
        if sorted(order) != sorted(self.state.alternatives_keys):
            messagebox.showerror("Ошибка", "Ранжирование должно содержать все альтернативы без повторов.")
            return
        self.state.rankings.append(order)
        if len(self.state.rankings) < self.state.experts_count:
            # подготовить список заново для следующего эксперта
            self.listbox.delete(0, tk.END)
            for k in self.state.alternatives_keys:
                self.listbox.insert(tk.END, self.state.alternatives_labels[k])
            self._refresh_title()
        else:
            self.on_finish_all()


class ResultFrame(ttk.Frame):
    def __init__(self, master, state: SurveyState, on_restart, on_exit):
        super().__init__(master, padding=15)
        self.state = state
        self.on_restart = on_restart
        self.on_exit = on_exit

        ttk.Label(self, text="Результаты метода Кондорсе", font=("TkDefaultFont", 12, "bold")).grid(
            row=0, column=0, sticky="w"
        )

        self.result_label = ttk.Label(self, text="", font=("TkDefaultFont", 10))
        self.result_label.grid(row=1, column=0, pady=(6, 10), sticky="w")

        # Таблица попарных сравнений
        self.tree = ttk.Treeview(self, show="headings", height=len(self.state.alternatives_keys))
        cols = [""] + self.state.alternatives_keys
        self.tree["columns"] = cols
        for c in cols:
            hdr = c if c else " "
            self.tree.heading(c, text=hdr.upper())
            self.tree.column(c, width=80, anchor="center")
        self.tree.grid(row=2, column=0, sticky="nsew")

        # Блок парных сравнений
        self.pairs_text = tk.Text(self, height=8, wrap="none")
        self.pairs_text.grid(row=3, column=0, sticky="nsew", pady=(10, 0))

        # Кнопки
        ctl = ttk.Frame(self)
        ctl.grid(row=4, column=0, sticky="e", pady=(10, 0))
        ttk.Button(ctl, text="Сохранить отчёт", command=self.save_report).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(ctl, text="Начать заново", command=self.on_restart).grid(row=0, column=1, padx=(0, 6))
        ttk.Button(ctl, text="Выход", command=self.on_exit).grid(row=0, column=2)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        # Рассчитать и показать
        self.M = self.build_pairwise_matrix()
        winner = self.condorcet_winner(self.M)
        if winner is None:
            self.result_label.configure(text="Победитель: нет абсолютного победителя по принципу Кондорсе.")
        else:
            self.result_label.configure(
                text=f"Победитель: {self.state.alternatives_labels[winner]}"
            )
        self.fill_table(self.M)
        self.fill_pairs(self.M)

    # ---------- Логика Кондорсе ----------
    def build_pairwise_matrix(self):
        keys = self.state.alternatives_keys
        idx = {a: i for i, a in enumerate(keys)}
        n = len(keys)
        M = [[0] * n for _ in range(n)]
        for ranking in self.state.rankings:
            pos = {a: i for i, a in enumerate(ranking)}
            for i, a in enumerate(keys):
                for j, b in enumerate(keys):
                    if i == j:
                        continue
                    if pos[a] < pos[b]:
                        M[i][j] += 1
        return M

    def condorcet_winner(self, M) -> Optional[str]:
        keys = self.state.alternatives_keys
        n = len(keys)
        for i in range(n):
            if all(i == j or M[i][j] > M[j][i] for j in range(n)):
                return keys[i]
        return None

    # ---------- Отрисовка ----------
    def fill_table(self, M):
        self.tree.delete(*self.tree.get_children())
        keys = self.state.alternatives_keys
        for i, a in enumerate(keys):
            row = [a.upper()] + M[i]
            self.tree.insert("", "end", values=row)

    def fill_pairs(self, M):
        self.pairs_text.configure(state="normal")
        self.pairs_text.delete("1.0", tk.END)
        keys = self.state.alternatives_keys
        lab = self.state.alternatives_labels
        n = len(keys)
        for i in range(n):
            for j in range(i + 1, n):
                left = M[i][j]
                right = M[j][i]
                if left > right:
                    line = f"{lab[keys[i]]} ≻ {lab[keys[j]]}: {left} против {right}\n"
                elif right > left:
                    line = f"{lab[keys[j]]} ≻ {lab[keys[i]]}: {right} против {left}\n"
                else:
                    line = f"{lab[keys[i]]} ~ {lab[keys[j]]}: {left} = {right}\n"
                self.pairs_text.insert(tk.END, line)
        self.pairs_text.configure(state="disabled")

    def save_report(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt")],
            title="Сохранить отчёт"
        )
        if not path:
            return
        keys = self.state.alternatives_keys
        lab = self.state.alternatives_labels
        winner = self.condorcet_winner(self.M)
        with open(path, "w", encoding="utf-8") as f:
            f.write("Результаты метода Кондорсе\n\n")
            if winner is None:
                f.write("Победитель: нет абсолютного победителя\n\n")
            else:
                f.write(f"Победитель: {lab[winner]}\n\n")
            f.write("Матрица попарных сравнений (строка против столбца):\n")
            header = ["   "] + [k.upper() for k in keys]
            f.write("\t".join(header) + "\n")
            for i, a in enumerate(keys):
                f.write("\t".join([a.upper()] + [str(x) for x in self.M[i]]) + "\n")
            f.write("\nПары:\n")
            f.write(self.pairs_text.get("1.0", tk.END))
        messagebox.showinfo("Готово", "Отчёт сохранён.")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Метод Кондорсе — Пожарная безопасность")
        self.state = SurveyState()

        self.style = ttk.Style(self)
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.current = None
        self.show_start()

    def _swap(self, frame_ctor, *args):
        if self.current:
            self.current.destroy()
        self.current = frame_ctor(self.container, *args)
        self.current.pack(fill="both", expand=True)

    def show_start(self):
        self._swap(StartFrame, self.state, self.show_ranking)

    def show_ranking(self):
        self._swap(RankingFrame, self.state, self.show_results, self.show_start)
    
    def show_results(self):
        self._swap(ResultFrame, self.state, self.show_start, self.destroy)


if __name__ == "__main__":
    App().mainloop()

