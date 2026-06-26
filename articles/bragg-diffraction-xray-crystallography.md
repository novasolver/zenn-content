---
title: "ブラッグの法則 2d sinθ = nλ — X線が結晶構造を「測る」しくみ"
emoji: "💎"
type: "tech"
topics: ["javascript", "物理", "結晶", "可視化", "材料工学"]
published: true
---

![ブラッグの法則 2d sinθ = nλ — NovaSolver](/images/bragg-diffraction/cover.png)

## ブラッグの法則とは

結晶は原子が規則正しく並び、何枚もの平行な「面」を作っています。そこへ X 線を当てると、隣り合う面で反射した波がある角度でだけ強め合い、鋭い回折ピークが観測されます。その条件が **ブラッグの法則** です：

$$
2d\sin\theta = n\lambda
$$

- $d$：結晶面の間隔（面間隔、単位 Å）
- $\theta$：ブラッグ角（X 線と「結晶面」のなす角）
- $n$：回折次数（1, 2, 3… の整数）
- $\lambda$：X 線の波長（Å）

1913 年に Bragg 父子が導き、ノーベル物理学賞につながった式です。たった 1 本の式で、X 線回折（XRD）による物質同定・残留応力測定・タンパク質構造解析まで支えています。

この記事では：

1. なぜ光路差が $2d\sin\theta$ になるのか
2. 20 行の JavaScript でピーク位置を計算する
3. 格子ひずみ $\varepsilon$ がピークをどう動かすか

📐 **動くデモ**: [ブラッグ回折シミュレーター（NovaSolver）](https://novasolver.jp/tools/bragg-diffraction.html)

## 光路差が 2d sinθ になる理由

上の面で反射する波と、間隔 $d$ だけ下の面で反射する波を比べると、下の波は「降りて戻る」分だけ余計に進みます。両方の波が結晶面となす角はともに $\theta$ なので、幾何学的に余分な距離は往復で $2d\sin\theta$ になります。

これがちょうど波長の整数倍 $n\lambda$ のとき、2 波の位相が揃い、建設的干渉で強いピークが出ます。整数倍からずれると位相が打ち消し合い、観測されません。だから回折は **離散的な次数 $n$ でしか起きない** のです。

実際に結晶が応力を受けて伸び縮みすると、面間隔が変わります。ツールでは実効面間隔 $d_\text{eff}$ を導入しています：

$$
d_\text{eff} = d(1+\varepsilon),\qquad \sin\theta = \frac{n\lambda}{2\,d_\text{eff}}
$$

また $\sin\theta \le 1$ という物理制約から、観測できる最大次数が決まります：

$$
n_\max = \left\lfloor \frac{2\,d_\text{eff}}{\lambda} \right\rfloor
$$

## 20 行の JavaScript 実装

ブラッグの法則は代数式なので、数値積分は不要です。角度を逆算するだけで実装できます：

```javascript
// 入力: d[Å], λ[Å], n(整数), ε(無次元ひずみ)
function bragg(d, lambda, n, eps) {
  const dEff = d * (1 + eps);             // 実効面間隔
  const sinTheta = (n * lambda) / (2 * dEff);
  const nMax = Math.floor((2 * dEff) / lambda);
  if (sinTheta > 1 || sinTheta < 0) {
    return { valid: false, nMax };        // 反射条件外
  }
  const theta = Math.asin(sinTheta) * 180 / Math.PI;  // 度
  return { dEff, sinTheta, theta, twoTheta: 2 * theta, nMax, valid: true };
}

// Cu Kα 線で d=2.5 Å の面を 1〜3 次まで
const lambda = 1.54;  // Å (Cu Kα)
for (let n = 1; n <= 3; n++) {
  const r = bragg(2.5, lambda, n, 0);
  console.log(`n=${n}: 2θ = ${r.twoTheta.toFixed(2)}°`);
}
// n=1: 2θ = 35.88°
// n=2: 2θ = 76.05°
// n=3: 2θ = 135.04°
```

`Math.asin` が `NaN` を返さないよう、`sinTheta > 1` で「反射条件外」を弾くのがポイントです。波長を長くしすぎたり次数を上げすぎると、すぐにこの制約に当たります。

## 多次数ピークを描く

同じ面（$d$ 一定）でも、次数 $n$ を上げると回折角 $2\theta$ が高角側へ移動します。標準パラメータ（$d=2.5$ Å、Cu Kα 線 $\lambda=1.54$ Å）での各ピーク位置を計算すると、次のようになります：

![Cu Kα・d=2.5Å の多次数回折ピークと格子ひずみシフト](/images/bragg-diffraction/charts-closeup.png)

| 次数 $n$ | $\sin\theta$ | ブラッグ角 $\theta$ | 回折角 $2\theta$ |
|---|---|---|---|
| 1 | 0.308 | 17.94° | 35.88° |
| 2 | 0.616 | 38.02° | 76.05° |
| 3 | 0.924 | 67.52° | 135.04° |
| 4 | 1.232 | — | （$\sin\theta>1$ で消失） |

$2\cdot2.5/1.54 = 3.247$ なので、整数部の **3 次までが観測限界**（$n_\max=3$）です。波長を短い Mo Kα 線（$\lambda=0.71$ Å）に替えると $2d/\lambda=7.04$ となり、最大 7 次まで観測できます。短波長ほど多くのピークが取れるのが、単結晶構造解析で Mo が好まれる理由です。

## 格子ひずみで残留応力を測る

X 線回折が工学で強力なのは、ピーク位置のわずかなずれから **内部応力** を読み取れるからです。引張ひずみ $\varepsilon>0$ では面間隔が広がり、$\sin\theta=n\lambda/(2d_\text{eff})$ が小さくなるため、ピークは低角側へ動きます。

標準条件（$d=2.5$ Å、$\lambda=1.54$ Å、$n=1$）で $\varepsilon$ を動かすと：

| ひずみ $\varepsilon$ | $d_\text{eff}$ | 回折角 $2\theta$ |
|---|---|---|
| $-0.01$（圧縮 1%） | 2.475 Å | 36.25° |
| $0$ | 2.500 Å | 35.88° |
| $+0.01$（引張 1%） | 2.525 Å | 35.51° |

1% のひずみで $2\theta$ が約 0.7° 動きます。実機ではこの微小シフトを多方向から測る $\sin^2\psi$ 法などで、結晶内部の応力を高い感度で評価できます。タービンブレードのショットピーニングや溶接残留応力の評価に使われている手法です。

## ツールで遊ぶ

NovaSolver のシミュレーターでは、結晶面の反射経路と多次数ピークを同時に見ながらパラメータを動かせます：

![λ をスイープすると回折ピークが移動する](/images/bragg-diffraction/slider-anim.gif)

試してほしい操作：

- **結晶面間隔 d スライダー**（1.0〜10.0 Å）を動かすと、模式図の経路差 $2d\sin\theta$ とピーク位置が連動します
- **X 線波長 λ スライダー**（0.1〜3.0 Å）：1.54 Å（Cu Kα）から 0.71 Å（Mo Kα）に下げると最大可能次数が 3 → 7 に増えます
- **回折次数 n**（1〜5）を変えて、黄色マーカーが各ピークへ移るのを確認
- **格子ひずみ ε スライダー**（−0.05〜+0.05）：ピークが低角／高角へシフトする残留応力測定の原理
- **「λ をスイープ」ボタン** で波長を自動掃引し、ピーク群が動くアニメーションを再生
- 計算結果カードに **ブラッグ角 θ・回折角 2θ・実効面間隔 d_eff・最大可能次数** が即時表示されます

## まとめ

- ブラッグの法則 $2d\sin\theta = n\lambda$ は、隣接面の光路差 $2d\sin\theta$ が波長の整数倍になる干渉条件
- 標準条件（$d=2.5$ Å、Cu Kα）では $\theta=17.94°$、$2\theta=35.88°$、最大 3 次まで観測可能
- 実装は `Math.asin` で角度を逆算するだけの 20 行。`sinθ>1` の反射条件外チェックが要
- 格子ひずみ $\varepsilon$ はピーク位置を動かし、残留応力測定（$\sin^2\psi$ 法など）の基礎になる

「規則正しい構造」と「波の干渉」というシンプルな組み合わせから、原子スケールの情報が読み取れる——これがブラッグの法則の面白さです。

📐 **[ブラッグ回折シミュレーター（NovaSolver）](https://novasolver.jp/tools/bragg-diffraction.html)** で、波長や格子ひずみを動かしてピークの動きを見てみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。波動・回折まわりでは [回折・ヤング二重スリット干渉](https://novasolver.jp/tools/diffraction.html)、[単スリット回折](https://novasolver.jp/tools/single-slit-diffraction.html)、[エアリーディスク](https://novasolver.jp/tools/airy-disk.html) なども揃えています。
