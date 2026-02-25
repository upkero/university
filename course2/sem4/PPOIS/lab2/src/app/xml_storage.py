from __future__ import annotations

from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Final
from xml.dom import minidom
from xml.sax import ContentHandler, parse, parseString

from .model import Player

PLAYER_FIELDS: Final[tuple[str, ...]] = (
    "last_name",
    "first_name",
    "middle_name",
    "birth_date",
    "team",
    "home_city",
    "squad",
    "position",
)


def save_players_dom(players: list[Player], file_path: str | Path) -> None:
    doc = minidom.Document()
    root = doc.createElement("players")
    doc.appendChild(root)

    for player in players:
        player_element = doc.createElement("player")
        root.appendChild(player_element)
        payload = asdict(player)
        payload["birth_date"] = player.birth_date.isoformat()
        for field_name in PLAYER_FIELDS:
            element = doc.createElement(field_name)
            element.appendChild(doc.createTextNode(str(payload[field_name])))
            player_element.appendChild(element)

    target_path = Path(file_path)
    xml_bytes = doc.toprettyxml(indent="  ", encoding="utf-8")
    target_path.write_bytes(xml_bytes)


def load_players_sax(file_path: str | Path) -> list[Player]:
    path = Path(file_path)
    handler = _PlayerSaxHandler()
    try:
        parse(str(path), handler)
        return handler.players
    except Exception as first_error:  # noqa: BLE001
        raw = path.read_bytes()
        for encoding in ("utf-8-sig", "cp1251", "windows-1251"):
            try:
                text = raw.decode(encoding)
            except UnicodeDecodeError:
                continue
            try:
                fallback_handler = _PlayerSaxHandler()
                parseString(text, fallback_handler)
                return fallback_handler.players
            except Exception:  # noqa: BLE001
                continue
        raise ValueError(
            "Не удалось прочитать XML. Проверьте, что файл сохранен в UTF-8 или CP1251 и не содержит поврежденных символов."
        ) from first_error


class _PlayerSaxHandler(ContentHandler):
    def __init__(self) -> None:
        super().__init__()
        self.players: list[Player] = []
        self._current: dict[str, str] = {}
        self._tag: str | None = None
        self._text_chunks: list[str] = []

    def startElement(self, name: str, attrs) -> None:
        if name == "player":
            self._current = {}
            return
        if name in PLAYER_FIELDS:
            self._tag = name
            self._text_chunks = []

    def characters(self, content: str) -> None:
        if self._tag is not None:
            self._text_chunks.append(content)

    def endElement(self, name: str) -> None:
        if name == "player":
            self.players.append(_player_from_dict(self._current))
            self._current = {}
            return
        if self._tag == name:
            self._current[name] = "".join(self._text_chunks).strip()
            self._tag = None
            self._text_chunks = []


def _player_from_dict(raw: dict[str, str]) -> Player:
    missing = [field_name for field_name in PLAYER_FIELDS if field_name not in raw]
    if missing:
        raise ValueError(f"В XML отсутствуют поля: {', '.join(missing)}")
    return Player(
        last_name=raw["last_name"],
        first_name=raw["first_name"],
        middle_name=raw["middle_name"],
        birth_date=date.fromisoformat(raw["birth_date"]),
        team=raw["team"],
        home_city=raw["home_city"],
        squad=raw["squad"],
        position=raw["position"],
    )
