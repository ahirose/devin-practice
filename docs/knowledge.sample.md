# Knowledgeノート サンプル（devin-practice）

> Devinの Knowledge に登録する内容の下書き。スコープは「repo: devin-practice」を想定。
> トリガー説明の例: 「devin-practice リポジトリで作業するとき」

## ディレクトリの責務
- `src/taskman/models.py` — `Task` データクラスとJSON変換のみ。ロジックを置かない
- `src/taskman/storage.py` — 永続化のみ。ビジネスルールを持たせない
- `src/taskman/service.py` — ビジネスロジックの置き場所。新機能は基本ここに追加する
- `src/taskman/cli.py` — argparseの引数定義と表示整形のみ。ロジックは `service.py` に置く

## コーディング規約
- `ruff check .` がクリーンであること（設定は `pyproject.toml`、行長100、ルール E/F/I/UP）
- 型ヒントは必須。`from __future__ import annotations` を先頭に置く
- 依存パッケージは原則追加しない（標準ライブラリで実装する）
- 例外は具体的な型で投げる（存在しないIDは `KeyError`）

## テストの書き方
- `pytest`。テストは `tests/` に置き、`service` フィクスチャ（`tmp_path` ベース）を使う
- ホームディレクトリの `~/.taskman.json` を絶対に触らない
- バグ修正では「先に失敗するテストを追加してから直す」

## PRの粒度
- 1PR = 1つの論点。無関係なフォーマット変更を混ぜない
- PR説明には「変更理由」と「検証方法（実行したコマンド）」を書く

## よくある落とし穴
- `pip install -e ".[dev]"` を忘れると `taskman` コマンドが無い（`PYTHONPATH=src python3 -m taskman.cli` で代替可）
- タスクIDは `_next_id()` の実装に依存するため、ID採番を変えるときは既存JSONとの互換性を確認する
