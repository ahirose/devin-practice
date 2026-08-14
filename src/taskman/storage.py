from __future__ import annotations

import json
from pathlib import Path

from .models import Task

DEFAULT_PATH = Path.home() / ".taskman.json"


class JsonStorage:
    """タスクをJSONファイルに永続化する。"""

    def __init__(self, path: Path | str = DEFAULT_PATH) -> None:
        self.path = Path(path)

    def load(self) -> list[Task]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [Task.from_dict(item) for item in raw]

    def save(self, tasks: list[Task]) -> None:
        payload = [task.to_dict() for task in tasks]
        self.path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
