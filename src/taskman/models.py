from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    priority: int = 3  # 1 (高) - 5 (低)
    due: date | None = None
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "priority": self.priority,
            "due": self.due.isoformat() if self.due else None,
            "tags": list(self.tags),
        }

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        return cls(
            id=int(data["id"]),
            title=data["title"],
            done=bool(data.get("done", False)),
            priority=int(data.get("priority", 3)),
            due=date.fromisoformat(data["due"]) if data.get("due") else None,
            tags=list(data.get("tags", [])),
        )
