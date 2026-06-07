---
title: "RK4はなぜEulerより桁違いに正確か — 4次のルンゲ・クッタ法をJavaScriptで"
emoji: "🧮"
type: "tech"
topics: ["javascript", "数値計算", "アルゴリズム", "数学", "可視化"]
published: false
---

![ルンゲ・クッタ法（ODE解法） — NovaSolver](/images/runge-kutta/cover.png)

## 微分方程式を「数値で解く」標準手法

物理シミュレーションの心臓部は、微分方程式 $dy/dx = f(x,y)$ を時間ステップごとに積分することです。最も素朴な**オイラー法**は実装が簡単ですが精度が低い。実用で広く使われるのが **4 次のルンゲ・クッタ法（RK4）**で、同じ刻み幅でもオイラー法より**桁違いに正確**です。その秘密は「1 ステップ内で 4 つの傾きを測り、加重平均する」ことにあります。

この記事では、両手法を JavaScript で実装し、精度の違いを確かめます。

🧮 **動くデモ**: [ルンゲ・クッタ法シミュレーター（NovaSolver）](https://novasolver.jp/tools/runge-kutta.html)

## オイラー法とRK4

テスト方程式は減衰 $dy/dx = -ky$（厳密解 $y(x) = y_0 e^{-kx}$）。**オイラー法**は始点の傾きだけで一歩進みます（全体誤差 $O(h)$）。

$$
y_{n+1} = y_n + h\,f(x_n, y_n)
$$

**RK4** は 4 つの傾きをシンプソン重み（1:2:2:1）で平均します（全体誤差 $O(h^4)$）。

$$
\begin{aligned}
k_1 &= h\,f(x_n, y_n),\quad k_2 = h\,f(x_n+\tfrac h2, y_n+\tfrac{k_1}2)\\
k_3 &= h\,f(x_n+\tfrac h2, y_n+\tfrac{k_2}2),\quad k_4 = h\,f(x_n+h, y_n+k_3)\\
y_{n+1} &= y_n + \tfrac16(k_1 + 2k_2 + 2k_3 + k_4)
\end{aligned}
$$

既定値 $k=0.5$、$h=0.1$、$y_0=10$ で $x=4$ まで積分すると、厳密解は $y(4) = 10e^{-2} = 1.3534$。**オイラー法は 1.2851（相対誤差 −5.04%）**、**RK4 は 1.353353（相対誤差わずか 1.1×10⁻⁵%）**。同じ刻み幅 $h=0.1$ なのに、RK4 の誤差はオイラー法の **約 10⁵ 分の 1** です。

![解の比較（左, 厳密/RK4/Euler）と累積誤差（右, 対数）](/images/runge-kutta/charts-closeup.png)

## JavaScript 実装

```javascript
function fEval(k, y) { return -k * y; }       // dy/dx = -k·y
function integrate(k, h, xend, y0) {
  let yE = y0, yR = y0;                        // Euler, RK4
  const n = Math.round(xend / h);
  for (let i = 0; i < n; i++) {
    yE = yE + h * fEval(k, yE);                // Euler: 始点の傾きのみ
    const k1 = h * fEval(k, yR);              // RK4: 4つの傾き
    const k2 = h * fEval(k, yR + k1/2);
    const k3 = h * fEval(k, yR + k2/2);
    const k4 = h * fEval(k, yR + k3);
    yR = yR + (k1 + 2*k2 + 2*k3 + k4) / 6;   // 加重平均（1:2:2:1）
  }
  return { yEuler: yE, yRK4: yR, exact: y0 * Math.exp(-k * xend) };
}
```

誤差の次数（$O(h)$ vs $O(h^4)$）の意味は劇的です。刻み幅を半分にすると、オイラー法の誤差は約 1/2 にしかならないのに、RK4 の誤差は約 1/16 に減ります。だから少ない計算量で高精度が得られるのです。

![刻み幅 h を大きくするとオイラー法が崩れる](/images/runge-kutta/slider-anim.gif)

## ツールで遊ぶ

[ルンゲ・クッタ法シミュレーター](https://novasolver.jp/tools/runge-kutta.html)で試してほしい操作：

- **ステップ幅 h スライダー**を大きくし、オイラー法（赤）が厳密解から大きくずれ、RK4（青）はぴったり追従するのを確認
- **減衰率 k スライダー**を変え、解の減衰の速さが変わるのを見る
- **「Euler 相対誤差」**の値が h とともに増減するのを読む
- **初期値 y₀・終端 x_end スライダー**で問題設定を変える
- **「h をスイープ」ボタン**で刻み幅の影響を連続的に観察
- **誤差グラフ（対数）**で RK4 と Euler の誤差が桁違いであることを確認

## まとめ

- オイラー法は $y_{n+1}=y_n+hf$、全体誤差 $O(h)$ で低精度
- RK4 は 4 つの傾きを 1:2:2:1 で平均、全体誤差 $O(h^4)$
- 既定（h=0.1）で Euler 誤差 −5.04%、RK4 誤差 1.1×10⁻⁵%
- 刻み半減で Euler は誤差 1/2、RK4 は 1/16

物理シミュレーションを支える数値積分の精度を、刻み幅を変えながら体感してみてください。

🧮 **[ルンゲ・クッタ法シミュレーター（NovaSolver）](https://novasolver.jp/tools/runge-kutta.html)** で、RK4 と Euler の精度差を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。数値計算では [数値積分](https://novasolver.jp/tools/numerical-integration.html)、[ニュートン・ラフソン法](https://novasolver.jp/tools/newton-raphson.html)、[二分法](https://novasolver.jp/tools/bisection-method.html) もどうぞ。
