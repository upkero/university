from __future__ import annotations

from pathlib import Path

from .utils import load_json, resolve_path, save_json


class RecordStore:
    def __init__(self, cfg: dict, base_dir: Path) -> None:
        records_cfg = cfg.get("records", {})
        self.path = resolve_path(records_cfg.get("path", "config/records.json"), base_dir)
        self.max_entries = int(records_cfg.get("max_entries", 5))
        self.default_name = records_cfg.get("default_name", "N/A")
        self.default_time = int(records_cfg.get("default_time_sec", 9999))
        self.modes = list(cfg.get("modes", {}).keys())
        self.levels = list(cfg.get("levels", {}).keys())
        self._data = self._load()

    def _default_entry(self) -> dict:
        return {"name": self.default_name, "time_sec": self.default_time}

    def _load(self) -> dict:
        if self.path.exists():
            try:
                data = load_json(self.path)
            except Exception:
                data = {}
        else:
            data = {}

        for mode in self.modes:
            data.setdefault(mode, {})
            for level in self.levels:
                data[mode].setdefault(level, [])
                entries = data[mode][level]
                if not isinstance(entries, list):
                    entries = []
                entries = sorted(entries, key=lambda e: e.get("time_sec", self.default_time))
                data[mode][level] = entries[: self.max_entries]

        save_json(self.path, data)
        return data

    def save(self) -> None:
        save_json(self.path, self._data)

    def entries(self, mode: str, level: str) -> list[dict]:
        return self._data[mode][level]

    def best(self, mode: str, level: str) -> float:
        entries = self._data[mode][level]
        if not entries:
            return float(self.default_time)
        return float(entries[0].get("time_sec", self.default_time))

    def visible_entries(self, mode: str, level: str) -> list[dict]:
        return [e for e in self._data[mode][level] if e.get("time_sec", self.default_time) < self.default_time]

    def insert(self, mode: str, level: str, name: str, time_sec: float) -> None:
        entries = self._data[mode][level]
        entries.append({"name": name, "time_sec": int(time_sec)})
        entries.sort(key=lambda e: e.get("time_sec", self.default_time))
        self._data[mode][level] = entries[: self.max_entries]
        self.save()
