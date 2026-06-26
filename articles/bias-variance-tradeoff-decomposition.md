---
title: "バイアス・バリアンス トレードオフ — 汎化誤差を3つに分解する"
emoji: "🎯"
type: "tech"
topics: ["機械学習", "統計", "javascript", "過学習", "可視化"]
published: true
---

![バイアス・バリアンス トレードオフ — NovaSolver](/images/bias-variance-tradeoff/cover.png)

## バイアス・バリアンス トレードオフとは

「過学習に気をつけろ」とよく言われますが、なぜ複雑なモデルが新しいデータで外すのか。その答えが**バイアス・バリアンス分解**です。テスト点での期待二乗誤差は、きれいに3つの成分に分かれます。

$$
\mathbb{E}\big[(y-\hat f)^2\big]
= \underbrace{(\overline{\hat f}-f)^2}_{\text{バイアス}^2}
+ \underbrace{\mathbb{E}\big[(\hat f-\overline{\hat f})^2\big]}_{\text{バリアンス}}
+ \underbrace{\sigma^2}_{\text{ノイズ}}
$$

- **バイアス²**：平均予測 $\overline{\hat f}$ が真の関数 $f$ からどれだけ系統的にズレているか（単純すぎると大）
- **バリアンス**：学習データが変わると予測がどれだけ揺れるか（複雑すぎると大）
- **既約誤差** $\sigma^2$：観測ノイズの分散。どんなモデルでも消せない下限

この記事では、多項式回帰で各成分を Python で実測し、総誤差が複雑さに対して U 字を描くことを確かめます。

📐 **動くデモ**: [バイアス・バリアンス トレードオフ シミュレーター（NovaSolver）](https://novasolver.jp/tools/bias-variance-tradeoff.html)

## 実験の設定

真の関数を $f(x)=\sin(2\pi x)$ とし、観測値を $y = f(x) + \varepsilon$（$\varepsilon \sim \mathcal{N}(0,\sigma^2)$）で生成します。これを独立に何セットも作り、各セットで次数 $d$ の多項式を最小二乗フィットします。テストグリッド上で平均したのが、

$$
\text{Bias}^2 = \frac{1}{N}\sum_x\big(\overline{\hat f}(x)-f(x)\big)^2, \qquad
\text{Var} = \frac{1}{N}\sum_x\mathbb{E}_D\big[(\hat f_D(x)-\overline{\hat f}(x))^2\big]
$$

です。$\hat f_D$ はデータセット $D$ で学習したモデル、$\overline{\hat f}$ はその平均。本ツールはデータ生成にノイズ $\sigma$ を直接乗せているので、既約誤差はちょうど $\sigma^2$ になります。

## 30 行の JavaScript 実装

正規方程式を解いて多項式をフィットし、複数データセットで分解します（微小なリッジ $\lambda=10^{-6}$ で数値安定化）。

```javascript
function trueFn(x) { return Math.sin(2*Math.PI*x); }

// ヴァンデルモンド行列で最小二乗フィット（w を返す）
function fitPoly(xs, ys, deg) { /* (XtX + λI) w = Xty を解く */ }
function evalPoly(w, x) { let v=0,p=1; for(const c of w){v+=c*p;p*=x;} return v; }

function decompose(deg, nSamples, sigma, nDatasets) {
  const TEST_X = [...Array(60)].map((_,i)=>i/59);
  const preds = [];
  for (let d = 0; d < nDatasets; d++) {
    const xs = [], ys = [];
    for (let s = 0; s < nSamples; s++) {
      const x = Math.random();
      xs.push(x);
      ys.push(trueFn(x) + sigma * gauss());   // 真の値 + ガウスノイズ
    }
    const w = fitPoly(xs, ys, deg);
    preds.push(TEST_X.map(x => evalPoly(w, x)));
  }
  const mean = TEST_X.map((_,i)=> preds.reduce((s,p)=>s+p[i],0)/nDatasets);
  let bias2 = 0, variance = 0;
  TEST_X.forEach((x,i) => {
    bias2 += (mean[i] - trueFn(x))**2;
    variance += preds.reduce((s,p)=>s+(p[i]-mean[i])**2,0)/nDatasets;
  });
  bias2 /= 60; variance /= 60;
  return { bias2, variance, noise: sigma*sigma, total: bias2+variance+sigma*sigma };
}
```

## 分解曲線を描く

NovaSolver のツールは次数 1〜12 について分解を計算し、バイアス²（右肩下がり）・バリアンス（右肩上がり）・総誤差（U 字）を重ねて描きます。

![バイアス・バリアンス分解と U 字カーブ](/images/bias-variance-tradeoff/charts-closeup.png)

- 太い基準線が真の関数 $f(x)$
- 細い曲線群がデータセットごとの当てはめ（広がり＝バリアンス）
- 太い線が平均予測（真の関数との差＝バイアス）

## U 字を数値で確かめる

デフォルト設定（$\sigma=0.25$, $n=25$, データセット 20 個）で次数を 1 から 12 まで動かすと、総誤差がはっきり U 字を描きます。

| 次数 $d$ | バイアス² | バリアンス | 総誤差 |
|---|---|---|---|
| 1 | 0.2154 | 0.0213 | 0.2991 |
| 2 | 0.2304 | 0.0756 | 0.3685 |
| **3** | **0.0083** | **0.0203** | **0.0910** |
| 5 | 0.0021 | 0.0301 | 0.0947 |
| 8 | 0.0009 | 0.0377 | 0.1011 |
| 10 | 0.0047 | 0.0851 | 0.1523 |
| 12 | 0.0223 | 0.2632 | 0.3480 |

次数 1〜2 は**学習不足**（バイアス²が支配的、$\sin$ を低次多項式で表せない）。次数 12 は**過学習**（バリアンスが $0.26$ まで爆発）。U 字の底は**次数 3** で、総誤差 $0.0910$ が最小です。

ここで効いてくるのが既約誤差です。$\sigma=0.25$ なら $\sigma^2 = 0.0625$。U 字の底（$0.0910$）でも、その $0.0625$ は決して下回れません。総誤差から $0.0625$ を引いた $0.0285$ が、モデル選択で削れるバイアス²＋バリアンスの最小値です。ノイズ $\sigma$ を $0$ にすると、この下駄が消えて U 字が地面まで届きます。

> 注意：バイアスとバリアンスを別々に出せるのは、真の関数 $f$ を知っていて独立データセットを何個も作れる「神の視点」だからです。実データでは $f$ は不明で、トレードオフは交差検証によるテスト誤差で間接的に扱います。

## ツールで遊ぶ

NovaSolver のツールでは、5 つのパラメータでトレードオフを体感できます。

![次数を動かすと U 字の現在地が動く](/images/bias-variance-tradeoff/slider-anim.gif)

試してほしい操作：

- **多項式モデルの次数スライダー**を 12 まで上げると、当てはめ曲線群が暴れ出す（高バリアンス）
- 次数を 1 にすると曲線群がほぼ同じ直線に固まる（高バイアス・低バリアンス）
- **ノイズ標準偏差スライダー**を 0 にして、U 字の「下駄」（既約誤差）が消える様子を見る
- **1データセットの点数スライダー**を増やすと、バリアンスだけが下がる（バイアスは不変）
- **真の関数セレクト**を「三次関数」に切り替えると、最適次数が変わる
- **計算結果カード**でバイアス²・バリアンス・既約誤差・期待総誤差・状態判定を読む

## まとめ

- 期待二乗誤差 ＝ バイアス² ＋ バリアンス ＋ 既約誤差 $\sigma^2$
- 次数を上げるとバイアスは下がりバリアンスは上がり、総誤差は U 字を描く
- デフォルト設定では次数 3 が底（総誤差 0.0910、うち消せないノイズ 0.0625）
- データを増やすとバリアンスは下がるがバイアスには効かない——支配的な成分を見極めて対策を選ぶ

決定木の深さ、ニューラルネットの層数、正則化の強さ——どれも本質的にはこのトレードオフを動かすつまみです。「複雑なモデルほど良い」が幻想である理由を、U 字が教えてくれます。

📐 **[バイアス・バリアンス トレードオフ シミュレーター（NovaSolver）](https://novasolver.jp/tools/bias-variance-tradeoff.html)** で、次数を動かして U 字の底を探してみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。機械学習・統計では [決定木の不純度指標](https://novasolver.jp/tools/decision-tree-impurity.html)、[混同行列と評価指標](https://novasolver.jp/tools/confusion-matrix-metrics.html)、[正規分布](https://novasolver.jp/tools/normal-distribution.html) なども揃えています。

<!-- redeploy 2026-06-26 -->
