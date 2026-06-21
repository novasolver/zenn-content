---
title: "二項分布をlog階乗でオーバーフローなく計算する — P(X=k)とモーメントをJSで"
emoji: "🎲"
type: "tech"
topics: ["javascript", "統計", "確率", "数学", "可視化"]
published: true
---

![二項分布 — NovaSolver](/images/binomial-distribution/cover.png)

## 「20回中ちょうど6回成功する確率は？」

コインを 20 回投げて表がちょうど 10 回出る確率、製品 100 個中の不良品数、世論調査での支持者数――「成功確率 $p$ の試行を $n$ 回繰り返したときの成功回数」は**二項分布**に従います。式は単純ですが、$n$ が大きいと二項係数 $\binom{n}{k}$ が天文学的な数になり、素朴に計算すると桁あふれします。これを **log 階乗**で回避するのが実装の勘どころです。

この記事では、二項分布の確率とモーメントを JavaScript で計算します。

🎲 **動くデモ**: [二項分布シミュレーター（NovaSolver）](https://novasolver.jp/tools/binomial-distribution.html)

## 確率質量関数とモーメント

$n$ 回中ちょうど $k$ 回成功する確率は次式です。

$$
P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}
$$

平均・分散・歪度はパラメータだけで決まります。

$$
\mu = np,\quad \sigma^2 = np(1-p),\quad \gamma_1 = \frac{1-2p}{\sqrt{np(1-p)}}
$$

既定値 $n=20$、$p=0.30$ で計算すると、平均 $\mu = 6$、標準偏差 $\sigma = 2.049$、歪度 $\gamma_1 = 0.195$（右に少し裾を引く）、最頻値 6。**ちょうど 6 回成功する確率 $P(X=6) = 0.1916$**、6 回以下の累積確率 $P(X \le 6) = 0.608$ です。$p = 0.5$（公平なコイン）なら左右対称になり、20 回中 10 回ちょうどの確率は $P(X=10) = 0.176$ になります。

![PMFと正規近似（左）と累積分布（右）](/images/binomial-distribution/charts-closeup.png)

## JavaScript 実装（log 階乗でオーバーフロー回避）

二項係数を直接計算すると $n!$ が巨大になるため、対数空間で和差にして指数で戻します。

```javascript
function logFactorial(n) {
  let s = 0;
  for (let i = 2; i <= n; i++) s += Math.log(i);
  return s;
}
function logBinom(n, k) {                 // log C(n,k)
  if (k < 0 || k > n) return -Infinity;
  return logFactorial(n) - logFactorial(k) - logFactorial(n - k);
}
function binomPMF(n, k, p) {               // P(X=k)
  if (k < 0 || k > n) return 0;
  const logP = logBinom(n, k) + k*Math.log(p) + (n - k)*Math.log(1 - p);
  return Math.exp(logP);                   // 最後に一度だけ exp で戻す
}
// 平均・分散
const mean = n * p, variance = n * p * (1 - p);
```

$n$ が大きく $p$ が中庸なら、二項分布は**正規分布 $\mathcal N(np, np(1-p))$ で近似**でき、$p$ が小さく $n$ が大きければ**ポアソン分布 $\mathrm{Poi}(np)$** で近似できます。シミュレーターでは両近似を重ねて比較できます。

![成功確率 p を変えると分布の形と位置が変わる](/images/binomial-distribution/slider-anim.gif)

## ツールで遊ぶ

[二項分布シミュレーター](https://novasolver.jp/tools/binomial-distribution.html)で試してほしい操作：

- **試行回数 n・成功確率 p スライダー**を変え、PMF の形（位置・幅・対称性）が変わるのを見る
- **k と演算子（=, ≤, ≥, <, >）**を選び、特定の確率 $P(X\,\text{op}\,k)$ を計算
- **「コイン」「不良品」「世論調査」「希少事象」プリセット**で実例を再現
- **「平均 μ=np」「標準偏差 σ」「歪度」「最頻値」**の統計量を読む
- **「近似」タブ**で正規近似（緑）とポアソン近似（橙破線）を二項の真値（青）と比較
- $p$ を 0.5 から離して分布が非対称（歪度が大きく）になるのを確認

## まとめ

- 二項分布は $P(X=k) = \binom{n}{k}p^k(1-p)^{n-k}$
- 二項係数は log 階乗でオーバーフローを回避して計算
- 既定（n=20, p=0.3）で μ=6, σ=2.049, P(X=6)=0.192, P(X≤6)=0.608
- 大 n では正規近似、小 p・大 n ではポアソン近似が有効

確率論の基礎となる二項分布を、試行回数と成功確率を変えながら体感してみてください。

🎲 **[二項分布シミュレーター（NovaSolver）](https://novasolver.jp/tools/binomial-distribution.html)** で、成功回数の確率を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。確率・統計では [正規分布](https://novasolver.jp/tools/normal-distribution.html)、[ビュフォンの針](https://novasolver.jp/tools/buffon-needle.html)、[マルコフ連鎖](https://novasolver.jp/tools/markov-chain.html) もどうぞ。
