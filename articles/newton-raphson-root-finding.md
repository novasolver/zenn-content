---
title: "ニュートン・ラフソン法はなぜ3回で9桁合うのか — 2次収束をJavaScriptで体感"
emoji: "➗"
type: "tech"
topics: ["javascript", "数値計算", "アルゴリズム", "数学", "可視化"]
published: true
---

![ニュートン・ラフソン法 — NovaSolver](/images/newton-raphson/cover.png)

## 方程式を「接線で滑り降りて」解く

$x^3 - 2x - 5 = 0$ のような方程式は、公式では解けません。そこで使うのが**ニュートン・ラフソン法**。現在の点で接線を引き、その接線が x 軸と交わる点を次の推定値にする――これを繰り返すだけで、驚くほど速く根に到達します。その速さは**2 次収束**と呼ばれ、正しい桁数が反復ごとに倍々に増えます。

この記事では、ニュートン・ラフソン法を JavaScript で実装し、その収束の速さを確かめます。

➗ **動くデモ**: [ニュートン・ラフソン法シミュレーター（NovaSolver）](https://novasolver.jp/tools/newton-raphson.html)

## 接線の式と2次収束

関数 $f(x)$ の点 $x_n$ における接線が x 軸と交わる点が、次の推定値です。

$$
x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}
$$

根の近くでは誤差 $e_n = x_n - x^*$ について

$$
|e_{n+1}| \le \frac{|f''(x^*)|}{2|f'(x^*)|}\,|e_n|^2
$$

が成り立ちます。誤差が**二乗で縮む**ため、いったん近づくと有効桁数が一気に倍増します。

テスト関数 $f(x) = x^3 - 2x - 5$（$f'(x) = 3x^2 - 2$、真の根 $x^* \approx 2.094551482$）を初期値 $x_0 = 2.0$ から反復すると：

| 反復 | $x_n$ | $\lvert f(x_n)\rvert$ |
|---|---|---|
| 0 | 2.000000000 | 1.0 |
| 1 | 2.100000000 | 6.1×10⁻² |
| 2 | 2.094568121 | 1.86×10⁻⁴ |
| 3 | 2.094551482 | 1.74×10⁻⁹ |

わずか **3 反復で 9 桁**が一致します。$|f|$ が $10^{-2} \to 10^{-4} \to 10^{-9}$ と桁数がほぼ倍々で増えるのが 2 次収束の証拠です。

![f(x)と接線（左, 緑=根）と|f(x_n)|の2次収束（右）](/images/newton-raphson/charts-closeup.png)

## JavaScript 実装

```javascript
function f(x)  { return x*x*x - 2*x - 5; }
function fp(x) { return 3*x*x - 2; }        // 導関数
function newton(x0, tol, maxIter, omega) {
  let x = x0;
  for (let n = 0; n < maxIter; n++) {
    const fx = f(x), fpx = fp(x);
    if (Math.abs(fx) < tol) return { root: x, iters: n, converged: true };
    if (Math.abs(fpx) < 1e-14) break;       // 導関数が 0 → 破綻
    x = x - omega * fx / fpx;                // ω: 緩和係数（既定 1）
  }
  return { root: x, converged: false };
}
// newton(2.0, 1e-6, 20, 1.0) → root ≈ 2.094551482 (3 反復)
```

ただし万能ではありません。導関数が 0 に近い点（この関数なら $x = \pm\sqrt{2/3} \approx \pm0.816$）の近くでは接線がほぼ水平になり、推定値が遠くへ飛んで発散します。**緩和係数 $\omega$**（更新幅を $\omega$ 倍に抑える）で安定化できます。

![接線をたどって根へ収束していく様子](/images/newton-raphson/slider-anim.gif)

## ツールで遊ぶ

[ニュートン・ラフソン法シミュレーター](https://novasolver.jp/tools/newton-raphson.html)で試してほしい操作：

- **初期値 x₀ スライダー**を変え、収束する場合と発散する場合を比較（$x_0$ を $\pm0.816$ 付近にすると不安定）
- **許容差 1e⁻ⁿ スライダー**で収束判定の厳しさを変え、必要な反復回数を見る
- **最大反復回数 スライダー**で打ち切りの挙動を確認
- **緩和係数 ω スライダー**を 1 未満にして、発散しがちな初期値でも安定させる
- **関数グラフ**で接線（黄破線）が x 軸を切る点が次の推定になるのを読む
- **収束グラフ**で $|f(x_n)|$ が対数軸で急降下（2 次収束）するのを確認

## まとめ

- ニュートン・ラフソン法は $x_{n+1} = x_n - f(x_n)/f'(x_n)$ で接線をたどる
- 根の近くで 2 次収束：有効桁数が反復ごとに倍々
- $x^3-2x-5=0$ は $x_0=2$ から 3 反復で 9 桁一致（root≈2.0946）
- 導関数 0 付近では発散、緩和係数 ω で安定化できる

数値計算の定番アルゴリズムを、初期値や緩和係数を変えながら体感してみてください。

➗ **[ニュートン・ラフソン法シミュレーター（NovaSolver）](https://novasolver.jp/tools/newton-raphson.html)** で、2 次収束の速さを確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。数値計算では [二分法](https://novasolver.jp/tools/bisection-method.html)、[勾配降下法](https://novasolver.jp/tools/gradient-descent.html)、[ルンゲ・クッタ法](https://novasolver.jp/tools/runge-kutta.html) もどうぞ。
