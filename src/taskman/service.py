from __future__ import annotations

from datetime import date

from .models import Task
from .storage import JsonStorage


class TaskService:
    def __init__(self, storage: JsonStorage) -> None:
        self.storage = storage

    def _next_id(self, tasks: list[Task]) -> int:
        return len(tasks) + 1

    def add(self, title: str, priority: int = 3, due: date | None = None,
            tags: list[str] | None = None) -> Task:
        tasks = self.storage.load()
        task = Task(
            id=self._next_id(tasks),
            title=title,
            priority=priority,
            due=due,
            tags=tags or [],
        )
        tasks.append(task)
        self.storage.save(tasks)
        return task

    def list(self, include_done: bool = True) -> list[Task]:
        tasks = self.storage.load()
        if not include_done:
            tasks = [t for t in tasks if not t.done]
        return sorted(tasks, key=lambda t: t.priority)

    def complete(self, task_id: int) -> Task:
        tasks = self.storage.load()
        for task in tasks:
            if task.id == task_id:
                task.done = True
                self.storage.save(tasks)
                return task
        raise KeyError(f"task {task_id} not found")

    def delete(self, task_id: int) -> None:
        tasks = self.storage.load()
        remaining = [t for t in tasks if t.id != task_id]
        if len(remaining) == len(tasks):
            raise KeyError(f"task {task_id} not found")
        self.storage.save(remaining)

    def search(self, keyword: str) -> list[Task]:
        """タイトルとタグをキーワードで検索する（大文字小文字を区別しない）。"""
        tasks = self.storage.load()
        return [t for t in tasks if keyword in t.title or keyword in t.tags]

    def overdue(self, today: date | None = None) -> list[Task]:
        """期限を過ぎた未完了タスクを返す（当日は期限内として扱う）。"""
        today = today or date.today()
        tasks = self.storage.load()
        return [t for t in tasks if t.due and t.due <= today and not t.done]

    def summary(self) -> dict:
        """タスクの件数サマリを返す。

        Week 2の演習で実装する（total / done / open / overdue / by_tag を返す想定）。
        """
        raise NotImplementedError("Week 2の演習: summary() を実装する")
