---
title: "正規分布の確率を誤差関数erfで計算する — 68-95-99.7ルールをJavaScriptで"
emoji: "📊"
type: "tech"
topics: ["javascript", "統計", "確率", "数学", "可視化"]
published: false
---

![正規分布（ガウス分布） — NovaSolver](/images/normal-distribution/cover.png)

## あらゆるところに現れる「ベルカーブ」

身長、テストの点数、測定誤差――自然界や社会のばらつきの多くは、左右対称の釣鐘型「正規分布（ガウス分布）」に従います。「平均 ± 標準偏差の範囲に約 68% が入る」という **68-95-99.7 ルール**は統計の基本ですが、では「平均より 1σ 下を下回る確率は？」のような任意の確率はどう計算するのでしょうか。鍵は**誤差関数 erf** です。

この記事では、正規分布の確率を JavaScript で計算します。

📊 **動くデモ**: [正規分布シミュレーター（NovaSolver）](https://novasolver.jp/tools/normal-distribution.html)

## 確率密度と累積分布

正規分布の確率密度関数（PDF）は次式です。

$$
f(x) = \frac{1}{\sigma\sqrt{2\pi}}\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
$$

「ある値以下になる確率」を与える累積分布関数（CDF）は、初等関数では書けず、**誤差関数 erf** を使って表します。

$$
\Phi(x) = \frac{1}{2}\left[1 + \mathrm{erf}\!\left(\frac{x-\mu}{\sigma\sqrt{2}}\right)\right]
$$

標準正規分布（$\mu=0$, $\sigma=1$）で計算すると、$\Phi(-1) = 0.1587$、つまり **$P(X < -1) = 15.87\%$**。±1σ・±2σ・±3σ の範囲に入る確率はそれぞれ **68.27%・95.45%・99.73%**（これが 68-95-99.7 ルール）。応用例として、IQ（$\mu=100$, $\sigma=15$）で 115〜130 に入る確率は $\Phi(130)-\Phi(115) = 13.59\%$ と求まります。

![PDFと裾の確率P(X<-1)（左）とCDF（右）](/images/normal-distribution/charts-closeup.png)

## JavaScript 実装（erf 近似）

erf は初等関数でないので、Abramowitz & Stegun の有理多項式近似（誤差 < 1.5×10⁻⁷）を使います。

```javascript
function erf(x) {
  const a1=0.254829592, a2=-0.284496736, a3=1.421413741,
        a4=-1.453152027, a5=1.061405429, p=0.3275911;
  const sign = x < 0 ? -1 : 1;
  x = Math.abs(x);
  const t = 1 / (1 + p*x);
  const y = 1 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*Math.exp(-x*x);
  return sign * y;
}
function pdf(x, mu, s) { return Math.exp(-0.5*((x-mu)/s)**2) / (s*Math.sqrt(2*Math.PI)); }
function cdf(x, mu, s) { return 0.5 * (1 + erf((x-mu)/(s*Math.sqrt(2)))); }
// P(a < X < b) = Φ(b) − Φ(a),  z-score = (x − μ)/σ
```

標準化（z スコア $z = (x-\mu)/\sigma$）すれば、どんな正規分布も標準正規分布に変換でき、erf ひとつで全ての確率が計算できます。

![境界 a を動かすと裾の確率 P(X<a) が変わる](/images/normal-distribution/slider-anim.gif)

## ツールで遊ぶ

[正規分布シミュレーター](https://novasolver.jp/tools/normal-distribution.html)で試してほしい操作：

- **平均 μ・標準偏差 σ スライダー**を変え、ベルカーブの位置と幅が変わるのを見る
- **「P(X<a)」「P(a<X<b)」「P(X>a)」モード**を切り替え、対応する領域が陰影表示されるのを確認
- **a・b の値**を変えて「確率 P」がリアルタイムに計算されるのを見る
- **「標準正規」「IQスコア」「身長分布」プリセット**で実例の確率を計算
- **z スコア計算**で X から z と累積確率を求める
- **CDF グラフ**で S 字曲線が 0 から 1 へ単調増加するのを読む

## まとめ

- 正規分布の確率は CDF $\Phi(x) = \frac{1}{2}[1 + \mathrm{erf}((x-\mu)/\sigma\sqrt2)]$ で計算
- erf は有理多項式近似で高精度に実装できる
- 68-95-99.7 ルール：±1σ/±2σ/±3σ で 68.27%/95.45%/99.73%
- z スコアで任意の正規分布を標準化できる

統計の土台となる正規分布を、平均・標準偏差を変えながら体感してみてください。

📊 **[正規分布シミュレーター（NovaSolver）](https://novasolver.jp/tools/normal-distribution.html)** で、確率と 68-95-99.7 ルールを確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。確率・統計では [二項分布](https://novasolver.jp/tools/binomial-distribution.html)、[マルコフ連鎖](https://novasolver.jp/tools/markov-chain.html)、[モンテカルロ法でπ推定](https://novasolver.jp/tools/monte-carlo-pi.html) もどうぞ。
