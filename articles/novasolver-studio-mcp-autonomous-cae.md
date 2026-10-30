---
title: "AIにCAEを任せたら「この数字で判断するな」と返ってきた──自律解析のためのMCPサーバ設計"
emoji: "🧪"
type: "tech"
topics: ["mcp", "ai", "cae", "python", "llm"]
published: true
published_at: "2026-11-02 08:00"
---

![](/images/studio/g_ask.gif)

AIエージェントに流体解析や構造解析を回させること自体は、もう珍しくありません。MCPで解析ソフトを操作する例も増えました。

ただ、エージェントに解析を任せて本当に困るのは「計算が回るか」ではありません。**出てきた数字を信じていいのか**です。人間の解析者なら、メッシュを細かくして答えが動かないかを確かめ、角の応力が発散していないかを疑います。エージェントにもそれをやらせたい。

NovaSolverでは、オープンソースの解析ソフト **NovaSolver Studio** を作っています。構造・熱・流れ・電気を解けて、28個のMCPツールを持っています。この記事では、エージェントが自分の答えを疑えるようにするために、ツール側でどんな設計をしたかを書きます。

## まず、実際のやりとり

角を丸めていないL字の金具（同梱のサンプル `l_bracket.step`）を読み込み、壁側の面を固定して、穴に下向き500 Nをかけました。以下は MCP クライアントから Studio を呼んだ実際の記録です（返答は原文から抜粋。ID や長い部分は「...」で省略し、ジョブの待ち合わせは1行にまとめています）。

なお最初の `run_simulation` は「計算に失敗しました: process ended」で終わりました。原因は記録用に書いたクライアントの側で、ツールを呼ぶたびに MCP サーバを終了させていたため、裏で動いていた計算ジョブが一緒に止まっていました。接続を保ったまま実行し直した2回目以降を載せています。

```text
>>> import_geometry(path="l_bracket.step", physics="structural", units="mm")
Imported l_bracket.step as c_20261031_010618_2990 (rev 1): 9 faces,
bounding box [0.0, 0.0, 0.0] - [80.0, 40.0, 60.0] mm. All faces start as 'free'.

>>> describe_case(case_id=..., detail="full")
l_bracket c_20261031_010618_2990 rev 1 | mode preview -> builtin-fem | ready=False
[error] 固定された面がありません。物体が浮いたままなので解けません。
[error] 荷重も圧力もかかっていません。結果がすべてゼロになります。
```

面は番号でしか分からないので、エージェントは画像で確かめます。

```text
>>> render_view(case_id=..., quantity="faces", view="iso_back")
面と境界条件の確認  [image]
```

![番号つきの面（裏側から）](/images/studio/faces_back.png)

壁に当たる裏面が `f1`、穴が `f9` だと分かったので、条件を入れます。画面を開いていれば、AIの操作はその場で画面にも反映されます。

![AIが条件を入れると、画面にもそのまま反映される](/images/studio/g2_ai_conditions.gif)

```text
>>> update_case(case_id=..., expected_revision=1, changes={
      "boundaries.f1.role": "fixed",
      "boundaries.f9.role": "load", "boundaries.f9.force": "500 N", "boundaries.f9.direction": "-z",
      "materials.solid.preset": "aluminium"})
rev 2. boundaries.f1.role: free -> fixed; boundaries.f9.role: free -> load; ...

>>> validate_case(case_id=...)
GREEN

>>> run_simulation(case_id=..., mode="final")      # CalculiX
Running as r_20261031_..._72f6. Call job_status after 5 s.

>>> job_status(job_id=...)        # 数回呼んで待つ
done 100% - 完了 | ran=yes / converged=yes / verified=no

>>> get_results(case_id=...)
ran=yes / converged=yes / verified=no
最大ミーゼス応力: 52.81 MPa
最大変位: 0.3101 mm
```

ここで止めると「最大52.8 MPa、アルミなら余裕」と報告してしまいます。しかし判定は `verified=no` なので、エージェントはメッシュ収束を確かめにいきます。

```text
>>> check_convergence(case_id=...)      # 粗い・標準・細かいの3段で解き直す
Running as ...
>>> job_status(job_id=...)
done 100% - 完了 | ran=yes / converged=yes / verified=no

>>> get_results(case_id=...)
最大ミーゼス応力: 59.86 MPa
WARNING: 最大応力はメッシュを細かくするほど上がり続けています（49 → 53 → 60 MPa）。
鋭い角や完全固定した面の縁など、理想化した形・拘束による応力特異性の可能性があり、
この最大値そのものは強度の判断に使えません。実物どおりの丸みや支え方をモデル化するか、
評価する場所を決めて、そこでの応力が収束するかを確かめてください。

>>> verify_case(case_id=...)
メッシュ収束（最大変位、GCI）: ... error +7.97% (tolerance 5.0%) -> FAIL
```

![最大応力は内側の角と固定した縁に集まる](/images/studio/bracket_vm.png)

応力が高いのは、丸みのない内側の角と、完全固定した面の縁でした。どちらも、メッシュを細かくするほど値が大きくなりやすい場所です。

この警告は、3段のメッシュでピーク応力が増え続け、最後の増分が3%を超えたときに出る検出則です。特異性を証明するものではなく「疑わしい」という合図ですが、エージェントにとっては「この最大値をそのまま報告するな」という十分な手がかりになります。

エージェントの次の手は2つです。角と穴のまわりだけメッシュを細かくすることと、評価する場所を特異点から離すことです。

```text
>>> update_case(case_id=..., expected_revision=3, changes={
      "mesh.refine.f6": "1.5 mm", "mesh.refine.f7": "1.5 mm", "mesh.refine.f9": "1 mm"})
rev 4. ... [warn] 形状か粗さが変わったので、メッシュを作り直す必要があります。

>>> check_convergence(case_id=...)
Running as ...
>>> job_status(job_id=...)
done 100% - 完了 | ran=yes / converged=yes / verified=yes

>>> get_results(case_id=...)
最大変位: 0.3188 mm
WARNING: 最大応力はメッシュを細かくするほど上がり続けています（74 → 88 → 105 MPa）。...

>>> verify_case(case_id=...)
メッシュ収束（最大変位、GCI）: ... error +1.83% (tolerance 5.0%) -> PASS

>>> probe_results(case_id=..., faces=["f9"])
f9 (251.3 mm2) mean: ... vm 7.2102 MPa ...; max: ... vm 16.725 MPa ...
```

結果は次のようにまとまりました。

| 量 | 値 | 判定 |
|---|---|---|
| 最大変位 | 0.319 mm | GCI 1.83%。この量について検証済み |
| 角の最大応力 | 74 → 88 → 105 MPa と増え続ける | 特異性が疑われる。この値では判断しない |
| 穴の面の最大応力 | 16.69 → 16.73 MPa（局所細分化の前後） | 変化は0.22%。ただし3段の収束評価はしていない |

エージェントがユーザーに返すべき答えは「最大105 MPa」ではありません。たとえば次のような答えです。

> このモデルの最大変位は 0.32 mm で、メッシュによる誤差の見積もり（GCI）は 1.8% です。荷重のかかる穴の面の応力は約17 MPa で、局所的にメッシュを細かくしてもほとんど変わりませんでした。内側の角は特異性が疑われ、このピーク値の収束は確認できていません。実物の丸み（R）を入れて評価し直す必要があります。

そう言えるだけの材料が、ツールの返答の中にそろっています。なお「検証済み」は、対象量について、参照値との照合またはメッシュによる誤差推定が所定の基準を満たしたことを示します。真の誤差の上限や、材料・拘束のモデル化が実物と合っていること、安全性までは保証しません。

## 設計1：判定を3段に分けて、毎回返す

![AIも人も、同じ道具を同じ規則で使う](/images/studio/fig_arch.png)

すべての結果に `ran / converged / verified` の3つのゲートをつけ、計算系のツールは毎回この行を返します。

| ゲート | 意味 |
|---|---|
| ran | ソルバが最後まで走った |
| converged | 解析の種類ごとの収束基準を満たした（非線形は反復の収束、外部流れは抗力係数の安定など） |
| verified | 解析解・文献値と許容範囲内で一致した。任意形状では、追跡する量（構造は最大変位、外部流れは抗力係数）について、3段のメッシュで GCI ≤ 5%、全段が収束、段ごとに要素数1.3倍以上、値の変化が落ち着く傾向にある、をすべて満たした |

エージェントは「完了」という言葉に引きずられがちです。そこで「計算は終わったが、まだ信じてはいけない」状態を、文字列で明示しています。さらに、降伏応力を設定した線形の構造解析では、降伏応力を超えた結果に「線形解析の前提が崩れている」と警告します（弾塑性モデルや複数材料のケースなど、出ない条件もあります）。**verified は安全という意味ではない**ことを、ツール側から伝える仕組みです。

## 設計2：型つきツールだけ。シェルもソルバの辞書も渡さない

28個のツールは、すべて引数の型が決まっています。シェル実行やコード実行のツールはありません。

OpenFOAM の辞書や CalculiX の入力ファイルを、エージェントに直接書かせることもしません。エージェントが埋めるのは、`boundaries.f9.force = "500 N"` のような、**ドット区切りのパスと単位つきの値**だけです。ソルバの入力は Studio が生成します。

こうしておくと、間違いが「エラーメッセージ付きで弾かれる」形で表に出ます。

```text
>>> describe_case(case_id=..., detail="faces")
Error executing tool describe_case: 1 validation error
detail  Input should be 'concise' or 'full'
```

## 設計3：数字は文字で返し、画像は確認用にする

`render_view` のツール説明には、**"Read numbers from get_results, not pictures."** と書いています。

画像は「どの面を固定したか」を人と確かめるためのもの、数値は `get_results` や `probe_results` の文字で読むもの、と役割を分けています。マルチモーダルなモデルでも、カラーバーの色から値を読ませると読み違えるおそれがあるためです。

## 設計4：人とAIが同じケースを触っても壊れない

Studio の画面とエージェントは、同じケースを同時に開けます。変更には `expected_revision` を付けさせ、ずれていれば書き換えを拒否します。今回の作業でも、実際に一度弾かれました。直前の `run_simulation(mode="final")` で実行モードが書き換わり、版が上がっていたのを見落としていたためです。

```text
>>> update_case(case_id=..., expected_revision=2, changes={"mesh.refine.f6": "1.5 mm", ...})
ケースは別の操作で更新されています（現在の revision は 3）。
describe_case で最新を読み、expected_revision=3 で再度呼んでください。
```

エラー文に「次に何をすればよいか」まで書いておくと、エージェントは自分で読み直して再試行します。

ほかにも、人とAIの協調のために次の仕組みがあります。

- **共通の Undo/Redo**：画面と AI の変更が同じ履歴に入る。Ctrl+Z で AI の変更も戻せる。
- **`get_gui_selection`**：人が画面で選んだ面を AI が読める。「選んだ面を固定して」が通じる。

## 設計5：重い計算はジョブにする

`run_simulation` は約20秒だけ待ち、終わらなければ `job_id` を返します。エージェントは `job_status` を呼んで進み具合と残り時間を見ます。MCP の1回の呼び出しで数分ブロックすると、クライアントによってはタイムアウトするためです。

## 検証の土台

「verified」を名乗る以上、基準が要ります。配布物には、解析解・文献値・近似式と比べた21の検証例を同梱しています。

![同梱の検証例21問](/images/studio/fig_bench21.png)

全問が許容範囲内で、最大は塑性崩壊荷重の +2.44% です。`list_examples` と `open_example` で、エージェントからも開けます。

## 使ってみる

Claude Desktop なら、Releases の `.mcpb` を開くだけで入ります。Python があれば、次の設定でも動きます。

```json
{
  "mcpServers": {
    "novasolver-studio": { "command": "uvx", "args": ["novasolver-studio", "mcp"] }
  }
}
```

あとは、たとえばこう頼みます。

> bracket.step を読み込んで、底の面を固定、上の面に 500 N。計算して、結果が検証済みかどうか教えて

## おわりに

エージェントに解析を任せるとき、ツールに求めるべきは「速く解ける」ことより「間違いを言ってくれる」ことだと思っています。

- GitHub：https://github.com/novasolver/novasolver-studio
- 紹介ページ：https://novasolver.jp/studio/

GPL-3.0 です。MCPまわりの設計に意見があれば、Issue や Discord（https://novasolver.jp/community/ ）でぜひ。
