from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from math import ceil

FIO_PART_RE = re.compile(r"^[A-Za-zА-Яа-яЁё]+$")


def normalize_fio_part(value: str) -> str:
    text = value.strip()
    if not text:
        return ""
    return text[0].upper() + text[1:].lower()


def validate_fio_part(value: str, *, field_label: str, required: bool) -> str:
    normalized = normalize_fio_part(value)
    if not normalized:
        if required:
            raise ValueError(f"Поле '{field_label}' обязательно.")
        return ""
    if not FIO_PART_RE.fullmatch(normalized):
        raise ValueError(f"Поле '{field_label}' должно содержать только кириллические или латинские буквы.")
    return normalized


@dataclass(slots=True)
class Player:
    last_name: str
    first_name: str
    middle_name: str
    birth_date: date
    team: str
    home_city: str
    squad: str
    position: str

    def __post_init__(self) -> None:
        self.last_name = validate_fio_part(self.last_name, field_label="Фамилия", required=True)
        self.first_name = validate_fio_part(self.first_name, field_label="Имя", required=True)
        self.middle_name = validate_fio_part(self.middle_name, field_label="Отчество", required=False)
        self.team = self.team.strip()
        self.home_city = self.home_city.strip()
        self.squad = self.squad.strip()
        self.position = self.position.strip()

    @property
    def full_name(self) -> str:
        return " ".join(part for part in (self.last_name, self.first_name, self.middle_name) if part)

    def to_row(self) -> tuple[str, str, str, str, str, str]:
        return (
            self.full_name,
            self.birth_date.isoformat(),
            self.team,
            self.home_city,
            self.squad,
            self.position,
        )


@dataclass(slots=True)
class SearchQuery:
    last_name: str = ""
    first_name: str = ""
    middle_name: str = ""
    birth_date: date | None = None
    team: str = ""
    home_city: str = ""
    squad: str = ""
    position: str = ""

    def normalized(self) -> SearchQuery:
        return SearchQuery(
            last_name=normalize_fio_part(self.last_name),
            first_name=normalize_fio_part(self.first_name),
            middle_name=normalize_fio_part(self.middle_name),
            birth_date=self.birth_date,
            team=self.team.strip().casefold(),
            home_city=self.home_city.strip().casefold(),
            squad=self.squad.strip().casefold(),
            position=self.position.strip().casefold(),
        )

    def validate(self, require_non_empty: bool) -> None:
        normalized = self.normalized()
        for field_label, value in (
            ("Фамилия", normalized.last_name),
            ("Имя", normalized.first_name),
            ("Отчество", normalized.middle_name),
        ):
            if value and not FIO_PART_RE.fullmatch(value):
                raise ValueError(f"Поле '{field_label}' должно содержать только кириллические или латинские буквы.")
        filled_fio = sum(bool(value) for value in (normalized.last_name, normalized.first_name, normalized.middle_name))
        if filled_fio > 1:
            raise ValueError("Для ФИО можно заполнить только один элемент: фамилию, имя или отчество.")
        if require_non_empty and not normalized.has_any_condition:
            raise ValueError("Нужно указать хотя бы одно условие.")

    @property
    def has_any_condition(self) -> bool:
        return any(
            (
                self.last_name.strip(),
                self.first_name.strip(),
                self.middle_name.strip(),
                self.birth_date is not None,
                self.team.strip(),
                self.home_city.strip(),
                self.squad.strip(),
                self.position.strip(),
            )
        )

    def matches(self, player: Player) -> bool:
        q = self.normalized()

        group_fio_birth: list[bool] = []
        if q.last_name:
            group_fio_birth.append(player.last_name.casefold() == q.last_name.casefold())
        if q.first_name:
            group_fio_birth.append(player.first_name.casefold() == q.first_name.casefold())
        if q.middle_name:
            group_fio_birth.append(player.middle_name.casefold() == q.middle_name.casefold())
        if q.birth_date is not None:
            group_fio_birth.append(player.birth_date == q.birth_date)
        group_fio_birth_ok = all(group_fio_birth) if group_fio_birth else True

        group_position_squad: list[bool] = []
        if q.position:
            group_position_squad.append(player.position.casefold() == q.position)
        if q.squad:
            group_position_squad.append(player.squad.casefold() == q.squad)
        group_position_squad_ok = any(group_position_squad) if group_position_squad else True

        group_team_city: list[bool] = []
        if q.team:
            group_team_city.append(player.team.casefold() == q.team)
        if q.home_city:
            group_team_city.append(player.home_city.casefold() == q.home_city)
        group_team_city_ok = any(group_team_city) if group_team_city else True

        return group_fio_birth_ok and group_position_squad_ok and group_team_city_ok


@dataclass(slots=True)
class Page:
    items: list[Player]
    total_items: int
    total_pages: int
    current_page: int
    page_size: int
    current_page_count: int


def paginate(items: list[Player], page: int, page_size: int) -> Page:
    safe_page_size = max(1, page_size)
    total_items = len(items)
    total_pages = max(1, ceil(total_items / safe_page_size))
    current_page = min(max(1, page), total_pages)
    start = (current_page - 1) * safe_page_size
    chunk = items[start : start + safe_page_size]
    return Page(
        items=chunk,
        total_items=total_items,
        total_pages=total_pages,
        current_page=current_page,
        page_size=safe_page_size,
        current_page_count=len(chunk),
    )


@dataclass(slots=True)
class PlayerRepository:
    _players: list[Player] = field(default_factory=list)

    def add(self, player: Player) -> None:
        self._players.append(player)

    def all(self) -> list[Player]:
        return list(self._players)

    def replace_all(self, players: list[Player]) -> None:
        self._players = list(players)

    def search(self, query: SearchQuery) -> list[Player]:
        return [player for player in self._players if query.matches(player)]

    def delete(self, query: SearchQuery) -> int:
        before = len(self._players)
        self._players = [player for player in self._players if not query.matches(player)]
        return before - len(self._players)
