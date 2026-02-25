from __future__ import annotations

from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox

from .model import Page, Player, PlayerRepository, SearchQuery, paginate
from .xml_storage import load_players_sax, save_players_dom


class AppController:
    def __init__(self, repository: PlayerRepository) -> None:
        self.repository = repository
        self.page_size = 10
        self.current_page = 1
        self._view = None

    def bind_view(self, view) -> None:
        self._view = view
        self.refresh_main()

    def run(self) -> None:
        if self._view is None:
            raise RuntimeError("View is not bound")
        self._view.mainloop()

    def add_player(self, data: dict[str, str | date]) -> None:
        player = Player(
            last_name=str(data["last_name"]).strip(),
            first_name=str(data["first_name"]).strip(),
            middle_name=str(data["middle_name"]).strip(),
            birth_date=data["birth_date"],  # type: ignore[arg-type]
            team=str(data["team"]).strip(),
            home_city=str(data["home_city"]).strip(),
            squad=str(data["squad"]).strip(),
            position=str(data["position"]).strip(),
        )
        self.repository.add(player)
        self.current_page = paginate(self.repository.all(), 10**9, self.page_size).current_page
        self.refresh_main()

    def load_xml(self) -> None:
        path = filedialog.askopenfilename(
            title="Загрузить XML",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
        )
        if not path:
            return
        players = load_players_sax(path)
        self.repository.replace_all(players)
        self.current_page = 1
        self.refresh_main()
        messagebox.showinfo("Загрузка", f"Загружено записей: {len(players)}")

    def save_xml(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Сохранить XML",
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
        )
        if not path:
            return
        save_players_dom(self.repository.all(), Path(path))
        messagebox.showinfo("Сохранение", f"Сохранено записей: {len(self.repository.all())}")

    def delete_by_query(self, query: SearchQuery) -> int:
        query.validate(require_non_empty=True)
        deleted_count = self.repository.delete(query)
        self.current_page = 1
        self.refresh_main()
        return deleted_count

    def search_by_query(self, query: SearchQuery) -> list[Player]:
        query.validate(require_non_empty=False)
        return self.repository.search(query) if query.has_any_condition else self.repository.all()

    def refresh_main(self) -> None:
        if self._view is None:
            return
        page = paginate(self.repository.all(), self.current_page, self.page_size)
        self.current_page = page.current_page
        self._view.render_main_page(page)

    def set_main_page_size(self, page_size: int) -> None:
        self.page_size = max(1, page_size)
        self.current_page = 1
        self.refresh_main()

    def go_main_first(self) -> None:
        self.current_page = 1
        self.refresh_main()

    def go_main_prev(self) -> None:
        self.current_page -= 1
        self.refresh_main()

    def go_main_next(self) -> None:
        self.current_page += 1
        self.refresh_main()

    def go_main_last(self) -> None:
        page = paginate(self.repository.all(), 10**9, self.page_size)
        self.current_page = page.total_pages
        self.refresh_main()

    @staticmethod
    def build_query(raw: dict[str, str | date | None]) -> SearchQuery:
        return SearchQuery(
            last_name=str(raw.get("last_name", "") or ""),
            first_name=str(raw.get("first_name", "") or ""),
            middle_name=str(raw.get("middle_name", "") or ""),
            birth_date=raw.get("birth_date"),  # type: ignore[arg-type]
            team=str(raw.get("team", "") or ""),
            home_city=str(raw.get("home_city", "") or ""),
            squad=str(raw.get("squad", "") or ""),
            position=str(raw.get("position", "") or ""),
        )

    @staticmethod
    def page_for(items: list[Player], page: int, page_size: int) -> Page:
        return paginate(items, page, page_size)
