# Codex への指示：Claude Code を起動して Zenn 記事を積み増す

**Codex の役割は「起動とスケジューリングだけ」。記事の判断・執筆・数値検証・画像生成は一切せず、すべて Claude Code に任せる。**
（理由: 実行は Claude Code に一本化済み — [[feedback-role-split-codex]]。Codex に内容を作らせない。）

## 基本方針
- **1セッション=最大8本**（品質維持のため。コンテキスト枯渇を避ける）。
- **「一気に1000本」はやらない**。素材は実在ツール（約824本）に限られ、薄い大量生成は CLAUDE.md §14 違反・Zennスパムリスク・SEO逆効果。
  目標は良質 60〜80 本（`queue.json` の `_policy.max_total_target`）。公開は日次cronで1本/日。
- すべて `published: false`（下書き）で蓄積。Codex は**公開フラグを触らない**。

## 起動コマンド（1セッション分）
作業ディレクトリで Claude Code をヘッドレス実行し、セッションプロンプトを渡す:

```bash
cd /e/NovaSolver/zenn-content
claude -p "$(cat pipeline/SESSION_PROMPT.md)" \
  --permission-mode acceptEdits \
  --add-dir /e/NovaSolver/cae-archive/tools \
  --allowedTools "Read,Edit,Write,Glob,Grep,Bash"
```

- **`--add-dir` は必須**: ツールHTML（`E:\NovaSolver\cae-archive\tools\<slug>.html`）は repo の外にあり、これが無いと STEP1（ツール精読）で読み取り権限不足になり停止する。
- 無人実行で権限プロンプトを避けたい場合のみ `--dangerously-skip-permissions` に置換（Bash/python/git push を伴うため）。利用は自己責任で。`-p` 無人モードでは確認プロンプトに答えられず停止するので、必要な権限は起動フラグで先に与えること。
- Windows ネイティブで回すなら PowerShell から同等に: `claude -p (Get-Content -Raw pipeline/SESSION_PROMPT.md) --permission-mode acceptEdits --add-dir E:\NovaSolver\cae-archive\tools`。
- 1コマンド=1バッチ(最大8本)。Claude Code 側がキューを読み、レシピに従い、最後に1回 push して要約を返す。

## 連続運用（複数バッチ）
キューが尽きるか目標本数に達するまで、**1バッチずつ順番に**起動する（並列起動しない＝Chromeクラッシュ連鎖回避）。バッチ間にレビューを挟むのが安全:

```bash
# 例: 最大5バッチを順次。各バッチ後に queue.json の残 todo 件数を見て継続判断
for i in 1 2 3 4 5; do
  cd /e/NovaSolver/zenn-content
  remaining=$(python -c "import json;print(sum(1 for q in json.load(open('pipeline/queue.json'))['queue'] if q['status']=='todo'))")
  [ "$remaining" -eq 0 ] && { echo "queue empty"; break; }
  claude -p "$(cat pipeline/SESSION_PROMPT.md)" --permission-mode acceptEdits --add-dir /e/NovaSolver/cae-archive/tools
  echo "=== batch $i done; remaining todo: $remaining ==="
done
```

## Codex が守ること（チェックリスト）
- [ ] バッチサイズ8を超えさせない（プロンプトに明記済み。超えそうなら停止）。
- [ ] バッチは**直列**実行（同時に複数 Claude Code を走らせない）。
- [ ] 各バッチ後に Claude Code の要約（作成数/skip/検出バグ/総下書き数）を保存・確認。
- [ ] `queue.json` の todo が 0、または総下書き数が目標(80)に達したら停止。
- [ ] 公開（published:true 化）は日次cron に任せ、Codex も Claude Code も一括公開しない。
- [ ] バッチでエラー/低品質が続いたら自動継続を止め、人間に報告。

## 人間レビューの推奨
下書きは公開前にバッファとして溜まる（1日1本公開）。数バッチごとに `articles/` の新規分と `pipeline/bugs.md` をスポット確認し、問題があれば該当 draft を直す or 削除する。これが大量自動生成の安全網。
