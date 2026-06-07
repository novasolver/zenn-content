---
title: "Z変換の極が単位円の中なら安定 — デジタルフィルタの極零配置をJavaScriptで"
emoji: "🔢"
type: "tech"
topics: ["javascript", "信号処理", "DSP", "数学", "可視化"]
published: false
---

![Z変換と極零配置 — NovaSolver](/images/z-transform/cover.png)

## デジタルフィルタの安定性は「単位円」で決まる

連続系のラプラス変換に対応する、離散系（デジタル信号処理）の道具が **Z 変換**です。デジタルフィルタの伝達関数 $H(z)$ の**極**がどこにあるかで、フィルタが安定か発散するかが決まります。判定はとてもシンプル：**すべての極が単位円の内側にあれば安定**。z 平面に極（×）と零点（○）を打つだけで、フィルタの素性が見えてきます。

この記事では、IIR フィルタの極・零点と周波数応答を JavaScript で計算します。

🔢 **動くデモ**: [Z変換シミュレーター（NovaSolver）](https://novasolver.jp/tools/z-transform.html)

## 伝達関数と安定条件

差分方程式の係数 $b$（分子）・$a$（分母）から、Z 変換の伝達関数が得られます。

$$
H(z) = \frac{B(z)}{A(z)} = \frac{b_0 + b_1 z^{-1} + \cdots}{a_0 + a_1 z^{-1} + \cdots}
$$

分母 $A(z)$ の根が**極**、分子 $B(z)$ の根が**零点**です。**安定条件は「全極の絶対値 < 1（単位円の内側）」**。周波数応答は $z = e^{j\omega}$ を代入して得られます。

既定の 2 次ローパス IIR（$b = [0.0675, 0.135, 0.0675]$、$a = [1, -1.143, 0.4128]$）で計算すると、**極は $0.572 \pm 0.294j$、絶対値 $|p| = 0.642 < 1$ で安定**。零点は $z = -1$（2 重）にあり、これがナイキスト周波数（$\omega = \pi$）でゲインを深く落とすローパス特性を生みます。

![z平面の極零配置（左, 単位円内＝安定）と周波数応答（右）](/images/z-transform/charts-closeup.png)

## JavaScript 実装

複素数で周波数応答を評価し、極の絶対値で安定性を判定します。

```javascript
function freqResponse(b, a, omega) {
  const evalPoly = c => {
    let re = 0, im = 0;
    for (let k = 0; k < c.length; k++) {       // z^-k = e^-jkω
      re += c[k] * Math.cos(-k * omega);
      im += c[k] * Math.sin(-k * omega);
    }
    return { re, im };
  };
  const B = evalPoly(b), A = evalPoly(a);
  const d = A.re*A.re + A.im*A.im;             // 複素除算 B/A
  return Math.hypot((B.re*A.re + B.im*A.im)/d, (B.im*A.re - B.re*A.im)/d);
}
// 安定性：分母の根（極）の絶対値が全て < 1 か
const stable = poles.every(p => Math.hypot(p.re, p.im) < 1.0);
```

極を単位円に近づけるほど、その周波数で鋭いピークが立ちます。極が単位円を超えると応答が発散し、フィルタは不安定になります。

![極の半径を大きくすると単位円を超えて不安定になる](/images/z-transform/slider-anim.gif)

## ツールで遊ぶ

[Z変換シミュレーター](https://novasolver.jp/tools/z-transform.html)で試してほしい操作：

- **分子係数 b・分母係数 a** を編集し、極・零点が z 平面上で動くのを見る
- **「低域IIR」「高域」「微分器」「積分器」「移動平均」プリセット**で代表的フィルタを比較
- **安定性バッジ**で全極が単位円内（STABLE）か外（UNSTABLE）かを確認
- **極を単位円に近づけて**周波数応答に鋭いピークが立つのを観察
- **インパルス応答**で安定なら減衰、不安定なら発散するのを見る
- **周波数応答**でローパス／ハイパスの違いを読む

## まとめ

- Z 変換の伝達関数 $H(z) = B(z)/A(z)$、極＝分母の根
- 安定条件は**全極が単位円の内側**（$|p| < 1$）
- 既定 IIR は $|p| = 0.642$ で安定なローパス
- 周波数応答は $z = e^{j\omega}$ を代入して得る

デジタルフィルタ設計の基礎となる極零配置を、係数を変えながら体感してみてください。

🔢 **[Z変換シミュレーター（NovaSolver）](https://novasolver.jp/tools/z-transform.html)** で、極零と安定性の関係を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。信号処理では [ラプラス変換](https://novasolver.jp/tools/laplace-transform.html)、[標本化定理](https://novasolver.jp/tools/nyquist-sampling.html)、[FFTアナライザ](https://novasolver.jp/tools/fft-analyzer.html) もどうぞ。
