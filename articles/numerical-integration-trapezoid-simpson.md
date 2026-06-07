---
title: "台形則とシンプソン則の誤差はどれだけ違う？ O(h²)とO(h⁴)をJavaScriptで"
emoji: "➕"
type: "tech"
topics: ["javascript", "数値計算", "アルゴリズム", "数学", "可視化"]
published: false
---

![数値積分（台形・シンプソン） — NovaSolver](/images/numerical-integration/cover.png)

## 解析的に積分できない関数を「面積」で求める

$\int_0^1 e^{-x^2}\,dx$ のように、原始関数が初等関数で書けない積分はたくさんあります。そんなときは曲線の下の面積を細い短冊に分けて足し合わせる**数値積分**の出番。最も基本的な**台形則**と、放物線で近似する**シンプソン則**――この 2 つは誤差の減り方（収束次数）がまるで違います。

この記事では、台形則とシンプソン則を JavaScript で実装し、誤差の差を確かめます。

➕ **動くデモ**: [数値積分シミュレーター（NovaSolver）](https://novasolver.jp/tools/numerical-integration.html)

## 台形則とシンプソン則

区間 $[a,b]$ を $n$ 等分（刻み $h = (b-a)/n$）します。**台形則**は各区間を台形で近似します（誤差 $O(h^2)$）。

$$
\int_a^b f\,dx \approx \frac{h}{2}\big[f(x_0) + 2f(x_1) + \cdots + 2f(x_{n-1}) + f(x_n)\big]
$$

**シンプソン則**は隣り合う 3 点を放物線で結んで近似します（$n$ は偶数、誤差 $O(h^4)$）。

$$
\int_a^b f\,dx \approx \frac{h}{3}\big[f(x_0) + 4f(x_1) + 2f(x_2) + \cdots + 4f(x_{n-1}) + f(x_n)\big]
$$

$\int_0^1 \sin x\,dx$（厳密値 $1 - \cos 1 = 0.459698$）を $n=10$ で計算すると、**台形則の誤差は $3.8\times10^{-4}$**、**シンプソン則の誤差は $2.6\times10^{-7}$** とすでに約 1000 倍の差。さらに $n$ を倍にすると、台形則の誤差は**約 1/4**（$O(h^2)$）、シンプソン則は**約 1/16〜1/64**（$O(h^4)$）に減ります。同じ計算量でシンプソン則が圧倒的に有利です。

![sin(x)を台形で近似（左）と分割数 n に対する誤差（右, 対数）](/images/numerical-integration/charts-closeup.png)

## JavaScript 実装

```javascript
function trapezoid(f, a, b, n) {
  const h = (b - a) / n;
  let s = (f(a) + f(b)) / 2;
  for (let i = 1; i < n; i++) s += f(a + i*h);
  return h * s;
}
function simpson(f, a, b, n) {
  if (n % 2 !== 0) n++;                        // n は偶数に
  const h = (b - a) / n;
  let s = f(a) + f(b);
  for (let i = 1; i < n; i++) s += (i % 2 === 0 ? 2 : 4) * f(a + i*h);
  return h * s / 3;                            // 端1, 奇数4, 偶数2
}
// simpson(Math.sin, 0, 1, 10) ≈ 0.459698（誤差 2.6e-7）
```

シンプソン則の重みパターン「1, 4, 2, 4, …, 4, 1」が放物線近似の本質です。なめらかな関数なら、わずか数分割で実用精度に達します。

![分割数 n を増やすと台形近似が真の面積に近づく](/images/numerical-integration/slider-anim.gif)

## ツールで遊ぶ

[数値積分シミュレーター](https://novasolver.jp/tools/numerical-integration.html)で試してほしい操作：

- **被積分関数**（sin, eˣ, x³−2x+1, e^(−x²) など）を切り替え、各手法の精度を比較
- **分割数 n スライダー**を増やし、台形則とシンプソン則の誤差の減り方の違いを見る
- **下限 a・上限 b スライダー**で積分区間を変える
- **結果テーブル**で台形・シンプソン・ガウス・ロンベルクなど多数の手法を一度に比較
- **誤差グラフ（対数）**で台形 $O(h^2)$ とシンプソン $O(h^4)$ の傾きの違いを読む
- e^(−x²) のような原始関数を持たない関数で数値積分の威力を確認

## まとめ

- 台形則は誤差 $O(h^2)$、シンプソン則は $O(h^4)$
- $\int_0^1\sin x\,dx$（n=10）で台形 3.8×10⁻⁴、シンプソン 2.6×10⁻⁷
- n を倍にすると台形は誤差 1/4、シンプソンは 1/16 以上
- なめらかな関数ならシンプソン則が少ない計算で高精度

解析的に解けない積分を数値で攻略する基礎を、関数や分割数を変えながら体感してみてください。

➕ **[数値積分シミュレーター（NovaSolver）](https://novasolver.jp/tools/numerical-integration.html)** で、台形則とシンプソン則の精度差を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。数値計算では [ルンゲ・クッタ法](https://novasolver.jp/tools/runge-kutta.html)、[テイラー級数](https://novasolver.jp/tools/taylor-series.html)、[モンテカルロ法でπ推定](https://novasolver.jp/tools/monte-carlo-pi.html) もどうぞ。
