---
title: "ラプラス変換のs平面で系の応答を読む — 極が左半面なら安定をJavaScriptで"
emoji: "🔣"
type: "tech"
topics: ["javascript", "信号処理", "制御工学", "数学", "可視化"]
published: true
---

![ラプラス変換とs平面 — NovaSolver](/images/laplace-transform/cover.png)

## 微分方程式を「代数」に変える魔法

ラプラス変換は、面倒な微分方程式を**代数方程式に変換**してしまう強力な道具です。制御工学では、システムの振る舞いを **s 平面**上の**極の位置**だけで読み取れます。極が左半面にあれば応答は減衰して安定、虚軸上なら持続振動、右半面なら発散――時間波形を解く前に、極の場所を見るだけで系の運命が分かります。

この記事では、ラプラス変換の変換対と s 平面の極を JavaScript で扱います。

🔣 **動くデモ**: [ラプラス変換シミュレーター（NovaSolver）](https://novasolver.jp/tools/laplace-transform.html)

## 定義と極の意味

ラプラス変換は時間関数 $f(t)$ を複素周波数 $s = \sigma + j\omega$ の関数 $F(s)$ に写します。

$$
F(s) = \mathcal{L}\{f(t)\} = \int_0^\infty f(t)\,e^{-st}\,dt
$$

代表的な変換対：減衰指数 $e^{-at} \leftrightarrow 1/(s+a)$、減衰正弦 $e^{-at}\sin(\omega t) \leftrightarrow \omega/((s+a)^2+\omega^2)$。後者の**極は $s = -a \pm j\omega$** にあります。極の**実部 $-a$ が減衰率**、**虚部 $\omega$ が振動周波数**を表します。

既定の $e^{-at}$（$a=1$）では、極は $s = -1$（左半面）にあり安定。**直流ゲイン $F(0) = 1/a = 1$**、最終値 $f(\infty) = 0$（最終値の定理 $\lim_{t\to\infty} f(t) = \lim_{s\to0} sF(s)$ より）。減衰正弦（$a=1, \omega=2$）なら極は $-1 \pm 2j$ で、左半面ゆえ振動しながら減衰します。

![s平面の極（左, 左半面＝安定）と時間応答（右）](/images/laplace-transform/charts-closeup.png)

## JavaScript 実装

部分分数分解で逆ラプラス変換を求めるのが基本です。分母の根（極）を解き、各極が時間領域の指数項に対応します。

```javascript
// F(s) = N(s)/D(s) の極（分母の根）を求める
function findRoots(coeffs) {           // 2次の例
  const [a, b, c] = coeffs;            // a s² + b s + c
  const disc = b*b - 4*a*c;
  if (disc >= 0) {
    const r = Math.sqrt(disc);
    return [{re:(-b+r)/(2*a), im:0}, {re:(-b-r)/(2*a), im:0}];
  }
  return [{re:-b/(2*a), im: Math.sqrt(-disc)/(2*a)},
          {re:-b/(2*a), im:-Math.sqrt(-disc)/(2*a)}];
}
// 各極 p_i は時間領域で A_i·e^(p_i·t) に対応
// 安定判定：全極の実部 Re(p) < 0（左半面）
```

極の実部が左へ行くほど（$a$ が大きいほど）応答は速く減衰します。極が虚軸を越えて右半面に入ると、応答は時間とともに発散します。

![極を左に動かす（aを増やす）と応答が速く減衰する](/images/laplace-transform/slider-anim.gif)

## ツールで遊ぶ

[ラプラス変換シミュレーター](https://novasolver.jp/tools/laplace-transform.html)で試してほしい操作：

- **変換対の表**から e^(-at)・減衰正弦・ステップなどを選び、s 平面の極と時間波形を比較
- **減衰係数 a スライダー**を変え、極の実部（横位置）と減衰の速さの関係を見る
- **角周波数 ω スライダー**で極の虚部（縦位置）と振動周波数の関係を確認
- **「DCゲイン F(0)」「最終値 f(∞)」**を読み、最終値の定理を確認
- **部分分数分解**で分子・分母係数を入力し、逆ラプラス変換を求める
- **s 平面の ROC**（収束領域）と極の位置関係を観察

## まとめ

- ラプラス変換 $F(s) = \int_0^\infty f(t)e^{-st}dt$ で微分方程式を代数化
- 極の実部＝減衰率、虚部＝振動周波数
- **極が左半面（Re<0）なら安定**、虚軸で持続振動、右半面で発散
- $e^{-at}$ は極 $s=-a$、$F(0)=1/a$、$f(\infty)=0$

制御・信号処理の共通言語であるラプラス変換を、極の位置を動かしながら体感してみてください。

🔣 **[ラプラス変換シミュレーター（NovaSolver）](https://novasolver.jp/tools/laplace-transform.html)** で、s 平面と応答の関係を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。信号処理・制御では [Z変換](https://novasolver.jp/tools/z-transform.html)、[ボード線図](https://novasolver.jp/tools/bode-plot.html)、[PID制御](https://novasolver.jp/tools/pid.html) もどうぞ。
