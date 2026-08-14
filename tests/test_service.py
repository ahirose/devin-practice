from datetime import date, timedelta

import pytest

from taskman.service import TaskService
from taskman.storage import JsonStorage


@pytest.fixture
def service(tmp_path):
    return TaskService(JsonStorage(tmp_path / "tasks.json"))


def test_add_and_list(service):
    service.add("設計レビュー", priority=1)
    service.add("テスト追加", priority=2)
    titles = [t.title for t in service.list()]
    assert titles == ["設計レビュー", "テスト追加"]


def test_complete(service):
    task = service.add("デプロイ")
    service.complete(task.id)
    assert service.list()[0].done is True


def test_complete_missing_id(service):
    with pytest.raises(KeyError):
        service.complete(999)


def test_delete(service):
    task = service.add("不要タスク")
    service.delete(task.id)
    assert service.list() == []


def test_open_only(service):
    a = service.add("A")
    service.add("B")
    service.complete(a.id)
    assert [t.title for t in service.list(include_done=False)] == ["B"]


def test_overdue_returns_past_due_tasks(service):
    yesterday = date.today() - timedelta(days=1)
    service.add("期限切れ", due=yesterday)
    service.add("期限内", due=date.today() + timedelta(days=3))
    assert [t.title for t in service.overdue()] == ["期限切れ"]
