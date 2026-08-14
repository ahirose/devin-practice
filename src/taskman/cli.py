from __future__ import annotations

import argparse
from datetime import date

from .service import TaskService
from .storage import DEFAULT_PATH, JsonStorage


def _format(task) -> str:
    mark = "x" if task.done else " "
    due = task.due.isoformat() if task.due else "-"
    tags = ",".join(task.tags) if task.tags else "-"
    return f"[{mark}] #{task.id} (p{task.priority}) {task.title}  due:{due}  tags:{tags}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taskman", description="Devin学習用タスク管理CLI")
    parser.add_argument("--file", default=str(DEFAULT_PATH), help="保存先JSONファイル")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="タスクを追加")
    add.add_argument("title")
    add.add_argument("--priority", type=int, default=3)
    add.add_argument("--due", help="YYYY-MM-DD")
    add.add_argument("--tag", action="append", default=[])

    ls = sub.add_parser("list", help="タスク一覧")
    ls.add_argument("--open-only", action="store_true")

    done = sub.add_parser("done", help="タスクを完了")
    done.add_argument("task_id", type=int)

    rm = sub.add_parser("rm", help="タスクを削除")
    rm.add_argument("task_id", type=int)

    search = sub.add_parser("search", help="タスクを検索")
    search.add_argument("keyword")

    sub.add_parser("overdue", help="期限切れタスクを表示")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    service = TaskService(JsonStorage(args.file))

    if args.command == "add":
        due = date.fromisoformat(args.due) if args.due else None
        task = service.add(args.title, priority=args.priority, due=due, tags=args.tag)
        print(_format(task))
    elif args.command == "list":
        for task in service.list(include_done=not args.open_only):
            print(_format(task))
    elif args.command == "done":
        print(_format(service.complete(args.task_id)))
    elif args.command == "rm":
        service.delete(args.task_id)
        print(f"deleted #{args.task_id}")
    elif args.command == "search":
        for task in service.search(args.keyword):
            print(_format(task))
    elif args.command == "overdue":
        for task in service.overdue():
            print(_format(task))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
