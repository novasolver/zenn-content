---
title: "回る円だけで絵を描く — フーリエ・エピサイクルとDFTの仕組み"
emoji: "🎡"
type: "tech"
topics: ["javascript", "数学", "フーリエ変換", "可視化", "信号処理"]
published: false
---

![フーリエ・エピサイクルとDFT — NovaSolver](/images/fourier-epicycles/cover.png)

## エピサイクルとは

大きな円の上でもう一つの円が回り、その上でさらに小さな円が回る——この **入れ子の回転円（エピサイクル／周転円）** を重ねていくと、ハートでも星でも、好きな閉曲線をペン先でなぞれます。

種明かしはフーリエ解析です。**任意の周期的な閉曲線は、半径・回転速度・初期角度の異なる回転ベクトルの重ね合わせで表せる**。古代の天文学者が惑星の逆行運動を周転円で説明しようとしたのと、数学的には同じ仕組みです。

この記事では：

1. 閉曲線を複素数の信号として扱う考え方
2. 離散フーリエ変換（DFT）で円の「設計図」を求める JavaScript 実装
3. 円の数 N と近似精度（＝どこまで細部を再現できるか）の関係

📐 **動くデモ**: [フーリエ円（エピサイクル）シミュレーター（NovaSolver）](https://novasolver.jp/tools/fourier-epicycles.html)

## 曲線を複素数で表す

平面上の点 $(x, y)$ を、1 個の複素数 $z = x + iy$ とみなします。閉曲線を $N$ 点でサンプリングすれば、複素数の数列 $z_0, z_1, \dots, z_{N-1}$ になります。

すると **回転ベクトル** が複素指数で素直に書けます：

$$
c\, e^{i(\omega t + \phi)}
$$

- $|c|$ … 円の半径（振幅）
- $\omega$ … 回転の角速度
- $\phi$ … スタート時の角度（位相）

エピサイクルの合成とは、こうした回転ベクトルの **足し算** に他なりません。

## DFTで円の設計図を求める

各円の半径・速度・位相は、**離散フーリエ変換（DFT）** で一発で求まります：

$$
X_k = \sum_{n=0}^{N-1} z_n\, e^{-i 2\pi k n / N}
$$

$k$ 番目の成分 $X_k$ が、そのまま 1 個のエピサイクルに対応します。$|X_k|/N$ が半径、$k$ が回転速度（基本周波数の整数倍）、$\arg(X_k)$ が初期位相です。JavaScript なら素朴な二重ループで書けます：

```javascript
function computeDFT(points) {           // points: [{x, y}, ...]
  const N = points.length;
  // 重心を原点へ
  const mx = points.reduce((s,p)=>s+p.x,0) / N;
  const my = points.reduce((s,p)=>s+p.y,0) / N;
  const re = points.map(p => p.x - mx);
  const im = points.map(p => p.y - my);

  const circles = [];
  for (let k = 0; k < N; k++) {
    let sr = 0, si = 0;
    for (let n = 0; n < N; n++) {
      const a = -2 * Math.PI * k * n / N;
      sr += re[n]*Math.cos(a) - im[n]*Math.sin(a);
      si += re[n]*Math.sin(a) + im[n]*Math.cos(a);
    }
    sr /= N; si /= N;
    circles.push({
      freq: k,
      amp: Math.hypot(sr, si),   // 半径
      phase: Math.atan2(si, sr), // 初期角度
    });
  }
  // 半径の大きい順 = 効く順に並べる
  circles.sort((a, b) => b.amp - a.amp);
  return circles;
}
```

ポイントは最後の **振幅順ソート**。半径の大きい円ほど形の大枠を担うので、大きい順に並べておけば「上位 N 個だけ使う」近似がそのまま作れます。

描画は、円を順に足しながらペン先を進めるだけです：

```javascript
let x = cx, y = cy;
for (let i = 0; i < used; i++) {
  const { freq, amp, phase } = circles[i];
  const a = freq * t + phase;       // t はアニメーション時刻
  x += amp * Math.cos(a);
  y += amp * Math.sin(a);
}
// (x, y) が今のペン先 → tracePath に追加して線を引く
```

## まず一番きれいな例：円と楕円

直感をつかむのにうってつけなのが楕円です。半長軸 $a$・半短軸 $b$ の楕円 $z = a\cos t + i\, b\sin t$ は、オイラーの公式で展開すると

$$
z = \underbrace{\frac{a+b}{2}}_{\text{半径}} e^{it} + \underbrace{\frac{a-b}{2}}_{\text{半径}} e^{-it}
$$

つまり **ちょうど 2 個の円**——正方向に回る大きい円と、逆方向に回る小さい円——の和です。$a=2,\ b=1$ で DFT にかけると、振幅は理論どおり $1.5$ と $0.5$ の 2 つだけが立ち、それ以外はゼロ：

| 成分 | 振幅 |
|---|---|
| $+1$ 回転 | 1.500 |
| $-1$ 回転 | 0.500 |
| その他 | 0.000 |

**円なら 1 個、楕円なら 2 個**で完全再現。残りの複雑な形は、ここに高周波の小さな円を足していくだけです。

## 円の数と近似精度

NovaSolver のツールは、近似の「誤差」を次のように定義しています：

$$
\text{近似誤差} = \left(1 - \frac{\text{使った円の振幅合計}}{\text{全円の振幅合計}}\right) \times 100\%
$$

「ハート」プリセット（256 点）で、使う円の数 $N$ を増やしたときの誤差を実測すると：

| 円の数 $N$ | 近似誤差 |
|---|---|
| 1 | 43.5% |
| 3 | 29.0% |
| 5 | 19.0% |
| 10 | 8.9% |
| 20 | 4.3% |
| 50 | 1.5% |

数個の円で大枠（低周波）が決まり、円を足すほど細部（高周波）が乗っていくのがわかります。下のスライダー操作では、この「ざっくり → 精密」の移り変わりがそのまま見えます：

![円の数を増やすと近似が精密になる](/images/fourier-epicycles/slider-anim.gif)

角のある形（星や矩形）は、鋭い角を再現するために高周波成分が多く必要で、円を増やしても角の付近に小さな波打ち（**ギブス現象**）が残ります。

![エピサイクルが曲線をなぞる様子](/images/fourier-epicycles/charts-closeup.png)

## ツールで遊ぶ

[フーリエ円シミュレーター](https://novasolver.jp/tools/fourier-epicycles.html)で試してほしい操作：

- **マウスやタッチで自由に曲線を描く**と、即座に DFT 分解されてエピサイクルが回り始める
- **プリセット**「星形」「ハート」「矩形波」をワンクリックで読み込む
- **「円の数 N」スライダー**（1〜200）を動かして、近似誤差がどう減るかを観察
- **「速度」スライダー**で再生スピードを変える（各円の相対速度比は固定。整数倍の関係は崩れない）
- **「描画／再生」モード**を切り替えて、描き直しと再生を行き来する

## まとめ

- 平面の閉曲線を複素数列 $z_n = x_n + i y_n$ として扱う
- DFT $X_k = \sum z_n e^{-i2\pi kn/N}$ の各成分が 1 個のエピサイクル（半径・速度・位相）になる
- 振幅順に並べて上位 N 個を使えば、N で近似精度が調整できる（円=1個、楕円=2個で完全再現）
- 同じ DFT が音声圧縮・JPEG・振動診断・デジタルフィルタの土台

「複雑な形＝単純な回転の重ね合わせ」というフーリエの発想を、ペン先の軌跡として目で見られるのがこのツールの魅力です。

📐 **[フーリエ円（エピサイクル）シミュレーター（NovaSolver）](https://novasolver.jp/tools/fourier-epicycles.html)** で、自分の描いた曲線が回る円に分解される様子を見てみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。フーリエ・信号処理系では [フーリエ級数シミュレーター](https://novasolver.jp/tools/fourier-series.html)、[FFT アナライザ](https://novasolver.jp/tools/fourier-transform.html)、[パーセバルの定理](https://novasolver.jp/tools/parsevals-theorem.html) なども揃えています。
