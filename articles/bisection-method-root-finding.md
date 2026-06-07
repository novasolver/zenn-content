---
title: "二分法は遅いが絶対に裏切らない — 区間を半分ずつ詰める求根をJavaScriptで"
emoji: "🔍"
type: "tech"
topics: ["javascript", "数値計算", "アルゴリズム", "数学", "可視化"]
published: false
---

![二分法による求根 — NovaSolver](/images/bisection-method/cover.png)

## 速さより確実性 — 必ず根にたどり着くアルゴリズム

ニュートン法は速いけれど、初期値が悪いと発散することがあります。一方**二分法（bisection）**は遅い代わりに、条件さえ満たせば**必ず**根に収束する安心のアルゴリズムです。原理は中学生でも分かる単純さ：「符号が変わる区間を、半分に切り続ける」だけ。中間値の定理が収束を保証してくれます。

この記事では、二分法を JavaScript で実装し、その確実な収束を確かめます。

🔍 **動くデモ**: [二分法シミュレーター（NovaSolver）](https://novasolver.jp/tools/bisection-method.html)

## 中点と符号判定

区間 $[a, b]$ の両端で関数の符号が異なれば（$f(a)\cdot f(b) < 0$）、その間に必ず根があります。中点 $c = (a+b)/2$ を取り、根がどちらの半分にあるかを符号で判定して区間を狭めます。

$$
c_n = \frac{a_n+b_n}{2},\qquad
[a_{n+1}, b_{n+1}] = \begin{cases}[a_n, c_n] & f(a_n)f(c_n) < 0 \\ [c_n, b_n] & \text{それ以外}\end{cases}
$$

区間幅は毎回ちょうど半分になるので、誤差は $1/2$ ずつ縮みます（**線形収束**）。許容差 $\varepsilon$ に達するのに必要な反復回数は

$$
N \ge \log_2\frac{b_0-a_0}{\varepsilon}
$$

テスト関数 $f(x) = x^3 - 2x - 5$ を区間 $[1, 3]$ から探します。$f(1) = -6 < 0$、$f(3) = 16 > 0$ で符号が異なるので根が挟まれています。許容差 $10^{-6}$ で実行すると、**21 反復**で区間幅が $9.5\times10^{-7}$ まで縮み、根 $x \approx 2.0946$ が得られます。理論式 $\log_2(2/10^{-6}) \approx 20.9$ とぴたり一致します。

![区間[a,b]が半分ずつ縮む様子（左）と区間幅の線形収束（右）](/images/bisection-method/charts-closeup.png)

## JavaScript 実装

```javascript
function f(x) { return x*x*x - 2*x - 5; }
function bisection(a, b, tol, maxIter) {
  if (f(a) * f(b) > 0) return null;          // 符号が同じ → 根を挟めない
  for (let n = 0; n < maxIter; n++) {
    const c = (a + b) / 2;                    // 中点
    const fc = f(c);
    if (Math.abs(fc) < tol) return { root: c, iters: n };
    if (f(a) * fc < 0) b = c;                 // 根は [a, c] 側
    else a = c;                               // 根は [c, b] 側
    if ((b - a) < tol) return { root: (a+b)/2, iters: n+1 };
  }
  return { root: (a + b) / 2, converged: false };
}
// bisection(1, 3, 1e-6, 50) → root ≈ 2.0946 (21 反復)
```

ニュートン法が 3 反復で済むのに対し二分法は 21 反復。1 反復で得られる桁数は $\log_{10}2 \approx 0.3$ 桁だけ。それでも**初期値に依存せず確実に収束する**頑健さが、二分法が今も使われ続ける理由です。

![区間を半分に詰めながら根へ収束していく](/images/bisection-method/slider-anim.gif)

## ツールで遊ぶ

[二分法シミュレーター](https://novasolver.jp/tools/bisection-method.html)で試してほしい操作：

- **初期区間 a・b スライダー**を変え、符号が異なる区間を設定（同符号だと「同符号エラー」）
- **許容差 1e⁻ⁿ スライダー**を厳しくして、必要な反復回数が増えるのを確認
- **最大反復回数 スライダー**で打ち切りの挙動を見る
- **「反復スイープ」ボタン**で区間が半分ずつ狭まる様子をアニメーションで観察
- **収束グラフ**で区間幅が対数軸上を直線的に下る（線形収束）のを読む
- **関数グラフ**で中点（黄点）が根に近づくのを見る

## まとめ

- 二分法は符号が変わる区間を半分ずつ詰める求根法
- 中間値の定理により $f(a)f(b)<0$ なら**必ず収束**
- 線形収束：誤差は毎回 1/2、必要反復は $N \ge \log_2((b_0-a_0)/\varepsilon)$
- $x^3-2x-5=0$ は $[1,3]$ から 21 反復で根 2.0946

速さのニュートン法、確実さの二分法――両者を比べながら数値解法の使い分けを体感してみてください。

🔍 **[二分法シミュレーター（NovaSolver）](https://novasolver.jp/tools/bisection-method.html)** で、確実に収束する求根を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。数値計算では [ニュートン・ラフソン法](https://novasolver.jp/tools/newton-raphson.html)、[数値積分](https://novasolver.jp/tools/numerical-integration.html)、[ルンゲ・クッタ法](https://novasolver.jp/tools/runge-kutta.html) もどうぞ。
