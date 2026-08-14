# バグ報告（Devinへの入力用サンプル）

実務でよくある「報告のされ方」を模したものです。そのままDevinに渡す練習に使ってください。

---

## BUG-1: タスクを削除した後に追加すると、IDが重複する

**環境**: main ブランチ / Python 3.11

**再現手順**
```bash
taskman --file ./bug1.json add "A"      # -> #1
taskman --file ./bug1.json add "B"      # -> #2
taskman --file ./bug1.json rm 1
taskman --file ./bug1.json add "C"      # -> #2 になる（Bと重複）
taskman --file ./bug1.json list
```

**期待**: 既存タスクとIDが重複しない（少なくとも過去に使ったIDを再利用しない）
**実際**: `#2` が2件表示され、`taskman done 2` がどちらか一方にしか効かない

**影響**: 完了・削除の対象が特定できない

---

## BUG-2: 当日が期限のタスクが「期限切れ」に出てくる

**再現手順**
```bash
taskman --file ./bug2.json add "本日締切" --due $(date +%F)
taskman --file ./bug2.json overdue
```

**期待**: `overdue()` のdocstringどおり、当日は期限内として扱われ表示されない
**実際**: 当日締切のタスクが期限切れとして表示される

---

## BUG-3: 大文字で検索するとヒットしない

**再現手順**
```bash
taskman --file ./bug3.json add "Deploy to staging" --tag Infra
taskman --file ./bug3.json search "deploy"   # 0件
taskman --file ./bug3.json search "inf"      # 0件（タグ部分一致もできない）
```

**期待**: 大文字小文字を区別せず、タイトル・タグの部分一致で検索できる
**実際**: どちらもヒットしない

---

## BUG-4: 保存中にプロセスが落ちるとJSONが壊れる

**状況**: `taskman add` の実行中にCtrl-Cすると、`tasks.json` が途中まで書かれた状態になり、
次回起動時に `json.decoder.JSONDecodeError` でCLIが一切使えなくなる。

**期待**: 保存が原子的に行われ、失敗時は前の状態が保たれる
