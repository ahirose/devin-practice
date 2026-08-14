# devin-practice — Devin学習用の練習プロジェクト

学習プラン（`docs/LEARNING_PLAN.md`）の演習で使う小さなPythonプロジェクトです。
題材は **タスク管理CLI（taskman）**。意図的に「バグ」「未実装関数」「テスト不足」を仕込んであり、
Devinに投げる練習素材になります。

## 前提
- Python 3.9 以上
- pip

## セットアップ

```bash
cd devin-practice
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## 実行方法

```bash
# 追加
taskman --file ./tasks.json add "設計レビュー" --priority 1 --tag work
taskman --file ./tasks.json add "請求書提出" --due 2020-01-01 --tag admin

# 一覧（優先度順）
taskman --file ./tasks.json list
taskman --file ./tasks.json list --open-only

# 完了 / 削除
taskman --file ./tasks.json done 1
taskman --file ./tasks.json rm 2

# 検索 / 期限切れ
taskman --file ./tasks.json search "レビュー"
taskman --file ./tasks.json overdue
```

`--file` を省略すると `~/.taskman.json` を使います。
インストールせずに実行する場合は `PYTHONPATH=src python3 -m taskman.cli ...`。

## テスト / Lint

```bash
pytest -q              # ユニットテスト
ruff check .           # Lint
ruff check . --fix     # 自動修正
```

現状のベースラインは **6件すべてグリーン / Lintもクリーン** です。
演習を始める前に必ずこの状態を確認してください（Devinの変更を検証する基準になります）。

## ディレクトリ構成

```
devin-practice/
├── src/taskman/
│   ├── models.py     # Task データクラス（JSON変換）
│   ├── storage.py    # JSON永続化
│   ├── service.py    # ビジネスロジック ← 演習の主戦場（バグ・未実装あり）
│   └── cli.py        # argparse ベースのCLI
├── tests/test_service.py
└── docs/
    ├── LEARNING_PLAN.md   # 4週間の学習プラン
    ├── EXERCISES.md       # 週別の演習と、そのままコピペできるプロンプト
    ├── BUG_REPORTS.md     # 実務っぽいバグ報告（Devinへの入力用）
    ├── blueprint.sample.yaml
    ├── knowledge.sample.md
    └── playbook.sample.md
```

## 使い方の流れ（推奨）
1. このディレクトリをGitHubリポジトリとしてpushする（DevinはPRベースで作業するため）
2. `docs/EXERCISES.md` の Week 1 から順に、プロンプトをDevinに渡す
3. 出てきたPRを自分でレビューし、`pytest` / `ruff` で検証する
4. うまくいった指示・つまずいた点を `docs/knowledge.sample.md` に追記し、Devinのナレッジへ登録する
