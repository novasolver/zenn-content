# 1記事あたりの実行レシピ（品質ゲート）

このレシピは Claude Code セッションが **1記事を作るたびに必ず全工程を踏む**ための手順書。
量より質。1セッションあたり **最大8本**。`queue.json` の `status:"todo"` を `priority` 昇順で処理する。

参照テンプレート（既存の良質記事）:
`articles/lorenz-attractor-butterfly-effect.md` / `double-pendulum-chaos-lagrangian.md` / `fourier-epicycles-dft-drawing.md`

---

## STEP 0. 題材確定（捏造・重複の防止）
- `queue.json` から次の `todo` を1件取る。`status` を `drafting` に更新。
- **ツール実在確認**: `cae-archive/tools/<tool_slug>.html` が存在すること。無ければ skip して `status:"skipped"`＋理由をログ。
- **slug検査**: `article_slug` が `^[a-z0-9_-]{12,50}$`、かつ `articles/` に同名が無いこと。
- 既出ツール（`_done_tools`）と重複しないこと。

## STEP 1. ツールHTML精読（CTAを実機能に一致させる）★最重要
- `cae-archive/tools/<tool_slug>.html` を**全部読む**。以下を書き出す:
  - 実在するスライダー/セレクト/ボタン/プリセット（id とラベル）
  - 出力（stat-card のラベル）
  - canvas/Chart の有無と id、操作（ドラッグ/ズーム等）
  - 物理/数式（theory-box）と数値手法・刻み
- **CTAには実在する操作・出力しか書かない**（存在しない機能を案内しない）。
- 同時に**バグを探す**（後述 STEP 6）。

## STEP 2. 数値はPythonで実測してから書く ★最重要
- ツールの計算ロジックを Python で再現し、記事に載せる数値（臨界値・保存量・誤差・収束など）を**実際に計算**する。
- 手計算できる既知解があれば突き合わせる。**未検証の数値を本文に書かない**（ハルシネーション防止）。
- 例: Lorenz の ρc=24.74、二重振り子の全エネルギー14.72J＋ドリフト0.01%、楕円=2円(1.5/0.5)。

## STEP 3. 本文執筆
- 構成は参照テンプレに合わせる: 導入→定義→数式→JS実装(20〜40行)→可視化→定量的な山場→「ツールで遊ぶ」(実機能のCTA)→まとめ→関連リンク。
- frontmatter: `title / emoji / type:"tech" / topics(5個) / published: false`。
- 文字数 2500〜3500字、数式(MathJax `$...$`/`$$...$$`)・コード・表を含む。
- 強い断定は出典が無ければ弱める（[[feedback-medium-article-quality-gates]] 準拠）。
- 画像参照は `/images/<tool_slug>/cover.png`, `charts-closeup.png`, `slider-anim.gif` の3点。

## STEP 4. ビジュアル生成
- 既定: `pipeline/scripts/make_visuals_template.py <tool_slug> "<title1>" "<title2>" "<subtitle>" [<slider_id>]`
  - ライブサイト（novasolver.jp）を Selenium でキャプチャ → cover/charts-closeup/stats/slider-anim を生成。
  - Chrome対策: 同時実行1、失敗時は1回リトライ（[[project-audit-chrome-crash-chain]]）。
- **ツールの描画にバグがある／キャプチャが破綻する場合は matplotlib で正しい図を自作**する
  （例: fourier-epicycles は周波数折返しバグでトレースが破綻するため matplotlib 生成に切替えた）。

## STEP 5. 画像QA（自動）
- `python pipeline/scripts/qa_check.py <tool_slug> <article_slug>` を実行し **PASS** を確認。
  - cover/charts-closeup/slider-anim が存在し、非空白（情報量がある）こと
  - 記事 frontmatter が妥当・`published:false`・slug長OK・画像参照が揃っていること
- 失敗したら原因を直すか、その記事を skip（中途半端な記事を出さない）。
- 仕上げに画像を1枚ずつ目視（Readでの画像確認）して破綻が無いか確認。

## STEP 6. バグは別タスク化（記事完成優先 / Q3=B）
- STEP 1 で見つけたツールのバグは**修正せず**、`pipeline/bugs.md` に
  `tool_slug / 箇所(行) / 症状 / 想定修正` を追記。重大度も付ける。
- EN/ZH 版にも同症状の可能性が高い旨を併記。

## STEP 7. コミット（push はバッチ末尾でまとめて）
- `git add articles/<article_slug>.md images/<tool_slug>` → `git commit -m "Stock article #N (draft): <topic>"`
- `queue.json` の当該 `status` を `draft` に更新（同コミットでよい）。
- **published:false のまま**。公開は GitHub Actions の日次cronが1本/日で行う。
- バッチの全件完了後に **1回だけ** `git push origin main`。
- 末尾で「作成本数・skip・検出バグ件数」を要約報告。

---

### 絶対禁止
- スタブ/テンプレ使い回しの大量生成（CLAUDE.md §14）。
- 実在しないツール機能をCTAに書く。未検証数値を書く。
- 破綻画像・空白画像をそのまま出荷する。
- ツールのバグをその場で一括修正する（別タスク化）。
