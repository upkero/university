import json
from pathlib import Path

from .models import FairData


class DataStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> FairData:
        if not self.path.exists():
            return FairData.default()
        with self.path.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
        return FairData.from_dict(raw)

    def save(self, data: FairData) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        with temp_path.open("w", encoding="utf-8") as handle:
            json.dump(data.to_dict(), handle, indent=2, sort_keys=True)
        temp_path.replace(self.path)
