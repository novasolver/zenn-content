---
title: "テイラー級数で関数を多項式に変える — sin(x)が項を増やすほど一致する様子をJSで"
emoji: "📈"
type: "tech"
topics: ["javascript", "数学", "数値計算", "可視化", "アルゴリズム"]
published: false
---

![テイラー級数による近似 — NovaSolver](/images/taylor-series/cover.png)

## 電卓はどうやって sin や exp を計算しているのか

電卓やコンピュータは、$\sin(x)$ や $e^x$ を直接「知っている」わけではありません。これらを足し算と掛け算だけでできる**多項式**に変換して計算しています。その変換が**テイラー級数**。関数を展開点まわりの多項式で近似し、項を増やすほど元の関数に一致していきます。

この記事では、テイラー級数を JavaScript で実装し、近似が改善する様子を確かめます。

📈 **動くデモ**: [テイラー級数シミュレーター（NovaSolver）](https://novasolver.jp/tools/taylor-series.html)

## テイラー展開の式

関数 $f$ を点 $a$ のまわりで展開すると、$n$ 階微分係数を係数とする多項式になります。

$$
f(x) = \sum_{n=0}^{N} \frac{f^{(n)}(a)}{n!}(x-a)^n + R_N
$$

剰余項 $R_N = \frac{f^{(N+1)}(\xi)}{(N+1)!}(x-a)^{N+1}$ が打ち切り誤差です。例えば $\sin x$ を $a=0$ で展開すると、奇数次の項だけが残る有名な級数になります。

$$
\sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \cdots
$$

$\sin(0.5)$（厳密値 $0.4794255$）を次数を上げて近似すると、誤差は急速に小さくなります：**$N=3$ で $2.6\times10^{-4}$、$N=5$ で $1.5\times10^{-6}$、$N=7$ で $5.4\times10^{-9}$**。$\sin$ の収束半径は無限大なので、項を十分足せばどんな $x$ でも近似できます（ただし $x$ が大きいほど多くの項が必要）。

![sin(x)とテイラー多項式 N=1,3,5,7（左）と次数に対する誤差（右）](/images/taylor-series/charts-closeup.png)

## JavaScript 実装

```javascript
function factorial(n) { let r = 1; for (let i = 2; i <= n; i++) r *= i; return r; }
// sin(x) を点 a で展開した係数：sin(a), cos(a), -sin(a), -cos(a) が周期4で循環
function sinCoeff(n, a) {
  const base = [Math.sin(a), Math.cos(a), -Math.sin(a), -Math.cos(a)];
  return base[n % 4] / factorial(n);
}
function taylorSum(x, a, N, coeff) {
  let s = 0;
  for (let n = 0; n <= N; n++) s += coeff(n, a) * Math.pow(x - a, n);
  return s;
}
// taylorSum(0.5, 0, 5, sinCoeff) ≈ 0.479427（誤差 1.5e-6）
```

展開点 $a$ から離れるほど近似は崩れます。グラフで見ると、低次（$N=1$ なら直線）では展開点付近しか合いませんが、次数を上げるとぴったり一致する範囲がどんどん広がっていきます。

![項を増やすほどテイラー多項式が sin(x) に一致する範囲が広がる](/images/taylor-series/slider-anim.gif)

## ツールで遊ぶ

[テイラー級数シミュレーター](https://novasolver.jp/tools/taylor-series.html)で試してほしい操作：

- **関数の選択**（sin, cos, eˣ, ln(1+x), 1/(1−x), √(1+x)）を切り替えて級数の違いを見る
- **次数 N スライダー**を上げ、近似多項式（破線）が元の関数（実線）に近づくのを確認
- **展開点 a スライダー**を変え、その点付近で最もよく一致することを見る
- **「収束半径」**表示で、ln(1+x) や 1/(1−x) など有限の収束半径を持つ関数を確認
- **「各項」表示**で個々の項がどう寄与するかを見る
- **誤差グラフ**で次数を上げると誤差が急減するのを読む

## まとめ

- テイラー級数は関数を $\sum f^{(n)}(a)/n!\,(x-a)^n$ で多項式近似
- $\sin(0.5)$ は N=3 で誤差 2.6×10⁻⁴、N=7 で 5.4×10⁻⁹
- 剰余項が打ち切り誤差を与える
- 展開点付近が最も精度が高く、次数を上げると一致範囲が広がる

電卓の中身でもある関数近似を、関数・次数・展開点を変えながら体感してみてください。

📈 **[テイラー級数シミュレーター（NovaSolver）](https://novasolver.jp/tools/taylor-series.html)** で、多項式近似の収束を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。数学・数値計算では [数値積分](https://novasolver.jp/tools/numerical-integration.html)、[フーリエ級数とギブス現象](https://novasolver.jp/tools/fourier-series.html)、[ニュートン・ラフソン法](https://novasolver.jp/tools/newton-raphson.html) もどうぞ。
