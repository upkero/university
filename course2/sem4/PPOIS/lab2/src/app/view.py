from __future__ import annotations

import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk
from typing import Callable

from .model import Page

POSITIONS = ("Вратарь", "Защитник", "Полузащитник", "Нападающий")
SQUADS = ("Основной", "Запасной", "Молодежный")


class DateInput(ttk.Frame):
    def __init__(self, master, *, optional: bool) -> None:
        super().__init__(master)
        today = date.today()
        self.optional = optional
        self.enabled_var = tk.BooleanVar(value=not optional)
        self.day_var = tk.StringVar(value=f"{today.day:02d}")
        self.month_var = tk.StringVar(value=f"{today.month:02d}")
        self.year_var = tk.StringVar(value=str(today.year))

        if optional:
            ttk.Checkbutton(self, text="Учитывать дату", variable=self.enabled_var, command=self._sync_state).pack(
                side=tk.LEFT, padx=(0, 8)
            )

        self.day_spin = ttk.Spinbox(self, from_=1, to=31, width=3, textvariable=self.day_var, format="%02.0f")
        self.month_spin = ttk.Spinbox(self, from_=1, to=12, width=3, textvariable=self.month_var, format="%02.0f")
        self.year_spin = ttk.Spinbox(self, from_=1900, to=2100, width=5, textvariable=self.year_var)
        self.day_spin.pack(side=tk.LEFT)
        ttk.Label(self, text=".").pack(side=tk.LEFT)
        self.month_spin.pack(side=tk.LEFT)
        ttk.Label(self, text=".").pack(side=tk.LEFT)
        self.year_spin.pack(side=tk.LEFT)
        self._sync_state()

    def _sync_state(self) -> None:
        state = "normal" if self.enabled_var.get() else "disabled"
        if not self.optional:
            state = "normal"
        for widget in (self.day_spin, self.month_spin, self.year_spin):
            widget.configure(state=state)

    def get_date(self) -> date | None:
        if self.optional and not self.enabled_var.get():
            return None
        try:
            return date(int(self.year_var.get()), int(self.month_var.get()), int(self.day_var.get()))
        except ValueError as exc:
            raise ValueError("Некорректная дата.") from exc


class PaginationControls(ttk.Frame):
    def __init__(
        self,
        master,
        *,
        on_first: Callable[[], None],
        on_prev: Callable[[], None],
        on_next: Callable[[], None],
        on_last: Callable[[], None],
        on_page_size: Callable[[int], None],
    ) -> None:
        super().__init__(master)
        self._on_page_size = on_page_size
        self.page_size_var = tk.StringVar(value="10")
        self.meta_var = tk.StringVar(value="Страница 1/1 | На странице: 0 | Всего: 0")

        self.first_btn = ttk.Button(self, text="|<", width=4, command=on_first)
        self.prev_btn = ttk.Button(self, text="<", width=4, command=on_prev)
        self.next_btn = ttk.Button(self, text=">", width=4, command=on_next)
        self.last_btn = ttk.Button(self, text=">|", width=4, command=on_last)

        self.first_btn.pack(side=tk.LEFT, padx=2)
        self.prev_btn.pack(side=tk.LEFT, padx=2)
        self.next_btn.pack(side=tk.LEFT, padx=2)
        self.last_btn.pack(side=tk.LEFT, padx=2)

        ttk.Label(self, text="Записей на странице:").pack(side=tk.LEFT, padx=(10, 4))
        size_box = ttk.Combobox(self, width=4, state="readonly", textvariable=self.page_size_var, values=("5", "10", "20", "50"))
        size_box.bind("<<ComboboxSelected>>", self._on_size_changed)
        size_box.pack(side=tk.LEFT)

        ttk.Label(self, textvariable=self.meta_var).pack(side=tk.LEFT, padx=(10, 0))

    def _on_size_changed(self, _event=None) -> None:
        self._on_page_size(int(self.page_size_var.get()))

    def render(self, page: Page) -> None:
        self.meta_var.set(
            f"Страница {page.current_page}/{page.total_pages} | На странице: {page.current_page_count} | Всего: {page.total_items}"
        )
        self.first_btn.configure(state="disabled" if page.current_page <= 1 else "normal")
        self.prev_btn.configure(state="disabled" if page.current_page <= 1 else "normal")
        self.next_btn.configure(state="disabled" if page.current_page >= page.total_pages else "normal")
        self.last_btn.configure(state="disabled" if page.current_page >= page.total_pages else "normal")


class QueryForm(ttk.LabelFrame):
    def __init__(self, master) -> None:
        super().__init__(master, text="Условия")
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)

        self.last_name_var = tk.StringVar()
        self.first_name_var = tk.StringVar()
        self.middle_name_var = tk.StringVar()
        self.team_var = tk.StringVar()
        self.city_var = tk.StringVar()
        self.squad_var = tk.StringVar()
        self.position_var = tk.StringVar()

        ttk.Label(self, text="Фамилия:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        ttk.Entry(self, textvariable=self.last_name_var).grid(row=0, column=1, sticky="ew", padx=6, pady=4)
        ttk.Label(self, text="Имя:").grid(row=0, column=2, sticky="w", padx=6, pady=4)
        ttk.Entry(self, textvariable=self.first_name_var).grid(row=0, column=3, sticky="ew", padx=6, pady=4)

        ttk.Label(self, text="Отчество:").grid(row=1, column=0, sticky="w", padx=6, pady=4)
        ttk.Entry(self, textvariable=self.middle_name_var).grid(row=1, column=1, sticky="ew", padx=6, pady=4)
        ttk.Label(self, text="Дата рождения:").grid(row=1, column=2, sticky="w", padx=6, pady=4)
        self.birth_date_input = DateInput(self, optional=True)
        self.birth_date_input.grid(row=1, column=3, sticky="w", padx=6, pady=4)

        ttk.Label(self, text="Позиция:").grid(row=2, column=0, sticky="w", padx=6, pady=4)
        ttk.Combobox(self, state="readonly", values=("",) + POSITIONS, textvariable=self.position_var).grid(
            row=2, column=1, sticky="ew", padx=6, pady=4
        )
        ttk.Label(self, text="Состав:").grid(row=2, column=2, sticky="w", padx=6, pady=4)
        ttk.Combobox(self, state="readonly", values=("",) + SQUADS, textvariable=self.squad_var).grid(
            row=2, column=3, sticky="ew", padx=6, pady=4
        )

        ttk.Label(self, text="Команда:").grid(row=3, column=0, sticky="w", padx=6, pady=4)
        ttk.Entry(self, textvariable=self.team_var).grid(row=3, column=1, sticky="ew", padx=6, pady=4)
        ttk.Label(self, text="Домашний город:").grid(row=3, column=2, sticky="w", padx=6, pady=4)
        ttk.Entry(self, textvariable=self.city_var).grid(row=3, column=3, sticky="ew", padx=6, pady=4)

        ttk.Label(self, text="Для ФИО заполняйте только один элемент.").grid(
            row=4, column=0, columnspan=4, sticky="w", padx=6, pady=(2, 6)
        )

    def get_payload(self) -> dict[str, object]:
        return {
            "last_name": self.last_name_var.get(),
            "first_name": self.first_name_var.get(),
            "middle_name": self.middle_name_var.get(),
            "birth_date": self.birth_date_input.get_date(),
            "team": self.team_var.get(),
            "home_city": self.city_var.get(),
            "squad": self.squad_var.get(),
            "position": self.position_var.get(),
        }


class AddDialog(tk.Toplevel):
    def __init__(self, master, *, on_submit: Callable[[dict[str, object]], None]) -> None:
        super().__init__(master)
        self.title("Добавить запись")
        self.resizable(False, False)
        self._on_submit = on_submit
        self.columnconfigure(1, weight=1)

        self.last_name_var = tk.StringVar()
        self.first_name_var = tk.StringVar()
        self.middle_name_var = tk.StringVar()
        self.team_var = tk.StringVar()
        self.city_var = tk.StringVar()
        self.squad_var = tk.StringVar(value=SQUADS[0])
        self.position_var = tk.StringVar(value=POSITIONS[0])

        ttk.Label(self, text="Фамилия:").grid(row=0, column=0, sticky="w", padx=8, pady=4)
        ttk.Entry(self, textvariable=self.last_name_var).grid(row=0, column=1, sticky="ew", padx=8, pady=4)
        ttk.Label(self, text="Имя:").grid(row=1, column=0, sticky="w", padx=8, pady=4)
        ttk.Entry(self, textvariable=self.first_name_var).grid(row=1, column=1, sticky="ew", padx=8, pady=4)
        ttk.Label(self, text="Отчество:").grid(row=2, column=0, sticky="w", padx=8, pady=4)
        ttk.Entry(self, textvariable=self.middle_name_var).grid(row=2, column=1, sticky="ew", padx=8, pady=4)

        ttk.Label(self, text="Дата рождения:").grid(row=3, column=0, sticky="w", padx=8, pady=4)
        self.birth_date = DateInput(self, optional=False)
        self.birth_date.grid(row=3, column=1, sticky="w", padx=8, pady=4)

        ttk.Label(self, text="Команда:").grid(row=4, column=0, sticky="w", padx=8, pady=4)
        ttk.Entry(self, textvariable=self.team_var).grid(row=4, column=1, sticky="ew", padx=8, pady=4)
        ttk.Label(self, text="Домашний город:").grid(row=5, column=0, sticky="w", padx=8, pady=4)
        ttk.Entry(self, textvariable=self.city_var).grid(row=5, column=1, sticky="ew", padx=8, pady=4)

        ttk.Label(self, text="Состав:").grid(row=6, column=0, sticky="w", padx=8, pady=4)
        ttk.Combobox(self, state="readonly", values=SQUADS, textvariable=self.squad_var).grid(
            row=6, column=1, sticky="ew", padx=8, pady=4
        )
        ttk.Label(self, text="Позиция:").grid(row=7, column=0, sticky="w", padx=8, pady=4)
        ttk.Combobox(self, state="readonly", values=POSITIONS, textvariable=self.position_var).grid(
            row=7, column=1, sticky="ew", padx=8, pady=4
        )

        buttons = ttk.Frame(self)
        buttons.grid(row=8, column=0, columnspan=2, sticky="e", padx=8, pady=8)
        ttk.Button(buttons, text="Добавить", command=self._submit).pack(side=tk.LEFT, padx=4)
        ttk.Button(buttons, text="Отмена", command=self.destroy).pack(side=tk.LEFT, padx=4)

        self.transient(master)
        self.grab_set()

    def _submit(self) -> None:
        try:
            payload = {
                "last_name": self.last_name_var.get().strip(),
                "first_name": self.first_name_var.get().strip(),
                "middle_name": self.middle_name_var.get().strip(),
                "birth_date": self.birth_date.get_date(),
                "team": self.team_var.get().strip(),
                "home_city": self.city_var.get().strip(),
                "squad": self.squad_var.get().strip(),
                "position": self.position_var.get().strip(),
            }
            if not payload["last_name"] or not payload["first_name"]:
                raise ValueError("Нужно заполнить фамилию и имя.")
            if not payload["team"] or not payload["home_city"]:
                raise ValueError("Нужно заполнить команду и домашний город.")
            self._on_submit(payload)
            self.destroy()
        except Exception as exc:  # noqa: BLE001
            raise_show("Ошибка", str(exc))


class SearchDialog(tk.Toplevel):
    def __init__(self, master, *, on_search: Callable[[dict[str, object]], list], page_builder: Callable) -> None:
        super().__init__(master)
        self.title("Поиск")
        self.geometry("1000x560")
        self._on_search = on_search
        self._page_builder = page_builder
        self._results: list = []
        self._page = 1
        self._page_size = 10

        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.form = QueryForm(self)
        self.form.grid(row=0, column=0, sticky="ew", padx=8, pady=8)

        header = ttk.Frame(self)
        header.grid(row=1, column=0, sticky="ew", padx=8)
        self.status_var = tk.StringVar(value="Результаты: 0")
        ttk.Button(header, text="Найти", command=self._search).pack(side=tk.LEFT)
        ttk.Label(header, textvariable=self.status_var).pack(side=tk.LEFT, padx=(10, 0))

        columns = ("fio", "birth_date", "team", "city", "squad", "position")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        for key, title, width in (
            ("fio", "ФИО игрока", 220),
            ("birth_date", "Дата рождения", 120),
            ("team", "Футбольная команда", 180),
            ("city", "Домашний город", 160),
            ("squad", "Состав", 110),
            ("position", "Позиция", 120),
        ):
            self.tree.heading(key, text=title)
            self.tree.column(key, width=width, anchor="center")
        self.tree.grid(row=2, column=0, sticky="nsew", padx=8, pady=8)

        self.pager = PaginationControls(
            self,
            on_first=self._go_first,
            on_prev=self._go_prev,
            on_next=self._go_next,
            on_last=self._go_last,
            on_page_size=self._set_page_size,
        )
        self.pager.grid(row=3, column=0, sticky="ew", padx=8, pady=(0, 8))

        self.transient(master)
        self.grab_set()

    def _search(self) -> None:
        try:
            self._results = self._on_search(self.form.get_payload())
            self.status_var.set(f"Результаты: {len(self._results)}")
            self._page = 1
            self._render()
        except Exception as exc:  # noqa: BLE001
            raise_show("Ошибка", str(exc))

    def _set_page_size(self, value: int) -> None:
        self._page_size = value
        self._page = 1
        self._render()

    def _go_first(self) -> None:
        self._page = 1
        self._render()

    def _go_prev(self) -> None:
        self._page -= 1
        self._render()

    def _go_next(self) -> None:
        self._page += 1
        self._render()

    def _go_last(self) -> None:
        page = self._page_builder(self._results, 10**9, self._page_size)
        self._page = page.total_pages
        self._render()

    def _render(self) -> None:
        page = self._page_builder(self._results, self._page, self._page_size)
        self._page = page.current_page
        for item in self.tree.get_children():
            self.tree.delete(item)
        for player in page.items:
            self.tree.insert("", tk.END, values=player.to_row())
        self.pager.render(page)


class DeleteDialog(tk.Toplevel):
    def __init__(self, master, *, on_delete: Callable[[dict[str, object]], int]) -> None:
        super().__init__(master)
        self.title("Удаление")
        self.resizable(False, False)
        self._on_delete = on_delete
        self.columnconfigure(0, weight=1)

        self.form = QueryForm(self)
        self.form.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        ttk.Button(self, text="Удалить", command=self._delete).grid(row=1, column=0, sticky="e", padx=8, pady=(0, 8))

        self.transient(master)
        self.grab_set()

    def _delete(self) -> None:
        try:
            deleted_count = self._on_delete(self.form.get_payload())
            if deleted_count:
                messagebox.showinfo("Удаление", f"Удалено записей: {deleted_count}")
            else:
                messagebox.showinfo("Удаление", "Записи по заданным условиям не найдены.")
            self.destroy()
        except Exception as exc:  # noqa: BLE001
            raise_show("Ошибка", str(exc))


class MainView(tk.Tk):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.title("Футбольные игроки")
        self.geometry("1050x620")
        self.minsize(980, 520)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self._build_menu()
        self._build_toolbar()
        self._build_table()
        self._build_pager()

    def _build_menu(self) -> None:
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label="Загрузить XML", command=self._guard(self.controller.load_xml))
        file_menu.add_command(label="Сохранить XML", command=self._guard(self.controller.save_xml))
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.destroy)

        action_menu = tk.Menu(menu, tearoff=False)
        action_menu.add_command(label="Добавить", command=self._guard(self.open_add))
        action_menu.add_command(label="Поиск", command=self._guard(self.open_search))
        action_menu.add_command(label="Удаление", command=self._guard(self.open_delete))

        menu.add_cascade(label="Файл", menu=file_menu)
        menu.add_cascade(label="Действия", menu=action_menu)
        self.config(menu=menu)

    def _build_toolbar(self) -> None:
        toolbar = ttk.Frame(self)
        toolbar.grid(row=0, column=0, sticky="ew", padx=8, pady=6)
        ttk.Button(toolbar, text="Добавить", command=self._guard(self.open_add)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Поиск", command=self._guard(self.open_search)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Удаление", command=self._guard(self.open_delete)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Загрузить XML", command=self._guard(self.controller.load_xml)).pack(side=tk.LEFT, padx=10)
        ttk.Button(toolbar, text="Сохранить XML", command=self._guard(self.controller.save_xml)).pack(side=tk.LEFT, padx=2)

    def _build_table(self) -> None:
        columns = ("fio", "birth_date", "team", "city", "squad", "position")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for key, title, width in (
            ("fio", "ФИО игрока", 220),
            ("birth_date", "Дата рождения", 120),
            ("team", "Футбольная команда", 180),
            ("city", "Домашний город", 170),
            ("squad", "Состав", 120),
            ("position", "Позиция", 130),
        ):
            self.tree.heading(key, text=title)
            self.tree.column(key, width=width, anchor="center")
        self.tree.grid(row=1, column=0, sticky="nsew", padx=8, pady=6)

    def _build_pager(self) -> None:
        self.pager = PaginationControls(
            self,
            on_first=self.controller.go_main_first,
            on_prev=self.controller.go_main_prev,
            on_next=self.controller.go_main_next,
            on_last=self.controller.go_main_last,
            on_page_size=self.controller.set_main_page_size,
        )
        self.pager.grid(row=2, column=0, sticky="ew", padx=8, pady=(0, 8))

    def render_main_page(self, page: Page) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for player in page.items:
            self.tree.insert("", tk.END, values=player.to_row())
        self.pager.render(page)

    def open_add(self) -> None:
        AddDialog(self, on_submit=self.controller.add_player)

    def open_search(self) -> None:
        SearchDialog(self, on_search=self._search_payload, page_builder=self.controller.page_for)

    def open_delete(self) -> None:
        DeleteDialog(self, on_delete=self._delete_payload)

    def _search_payload(self, payload: dict[str, object]) -> list:
        query = self.controller.build_query(payload)
        return self.controller.search_by_query(query)

    def _delete_payload(self, payload: dict[str, object]) -> int:
        query = self.controller.build_query(payload)
        return self.controller.delete_by_query(query)

    def _guard(self, callback: Callable[[], None]) -> Callable[[], None]:
        def wrapped() -> None:
            try:
                callback()
            except Exception as exc:  # noqa: BLE001
                raise_show("Ошибка", str(exc))

        return wrapped


def raise_show(title: str, text: str) -> None:
    messagebox.showerror(title, text)
