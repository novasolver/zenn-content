---
title: "ブラウザだけで動く Bode 線図ジェネレーター — 伝達関数から制御系の安定性を直感する"
emoji: "📐"
type: "tech"
topics: ["javascript", "数学", "制御工学", "可視化", "chartjs"]
published: true
---

![Bode 線図ジェネレーター — NovaSolver](/images/bode-plot/cover.png)

## なぜ Bode 線図か

制御工学を学んでいると必ず登場するのが Bode 線図です。教科書では手計算が前提ですが、伝達関数を変えるたびに描き直すのは骨が折れます。実は **数十行の JavaScript** で十分実用的なものが書けます。

この記事では：

1. 伝達関数 G(s) → 周波数応答の数学を最小限おさらい
2. ブラウザだけで動く Bode 線図ジェネレーターを 50 行で実装
3. ゲイン余裕・位相余裕で安定性を判定する実例

最後に、これを完成形にした実装（PID プリセット付き）を NovaSolver に置いてあるので、自分の手で動かして確かめてみてください。

📐 **動くデモ**: [Bode 線図ジェネレーター（NovaSolver）](https://novasolver.jp/tools/bode-plot.html)

## 伝達関数と周波数応答

線形時不変システムの伝達関数 $G(s)$ に $s = j\omega$ を代入すると、**周波数応答** $G(j\omega)$ が得られます：

$$
G(j\omega) = |G(j\omega)| e^{j \angle G(j\omega)}
$$

Bode 線図はこの絶対値と位相を、$\omega$ を対数軸にとって描いたものです：

- **ゲイン線図**: $20 \log_{10} |G(j\omega)|$ [dB] vs $\log \omega$
- **位相線図**: $\angle G(j\omega)$ [deg] vs $\log \omega$

たとえば一次遅れ系 $G(s) = \dfrac{1}{1+Ts}$ なら：

$$
|G(j\omega)| = \frac{1}{\sqrt{1+(T\omega)^2}}, \quad \angle G(j\omega) = -\arctan(T\omega)
$$

折点周波数 $\omega = 1/T$ で -3 dB、-45° になる定番の形ですね。

実際にプロットするとこんな見た目になります（NovaSolver で二次遅れ系 $G(s) = 1/(s^2 + s + 1)$ を描画）：

![Bode 線図のゲイン・位相プロット](/images/bode-plot/charts-closeup.png)

ゲイン線図の青の破線は **0 dB の基準線**、位相線図の灰色破線は **-180° の基準線**。あとで安定性判定に使います。

## 実装：50 行の JavaScript

伝達関数を分子・分母多項式の係数配列で表現し、各周波数で複素数評価します。

```javascript
// 複素数演算（最小限）
const cmul = (a, b) => ({ re: a.re*b.re - a.im*b.im, im: a.re*b.im + a.im*b.re });
const cadd = (a, b) => ({ re: a.re + b.re, im: a.im + b.im });

// 多項式 poly[i] * s^i を s = jω で評価
function evalPoly(poly, omega) {
  let result = { re: 0, im: 0 };
  let sPow = { re: 1, im: 0 };
  const jOmega = { re: 0, im: omega };
  for (let i = 0; i < poly.length; i++) {
    result = cadd(result, cmul(sPow, { re: poly[i], im: 0 }));
    sPow = cmul(sPow, jOmega);
  }
  return result;
}

// 周波数応答 G(jω) = num(jω) / den(jω)
function frequencyResponse(num, den, omega) {
  const n = evalPoly(num, omega);
  const d = evalPoly(den, omega);
  const dMag2 = d.re*d.re + d.im*d.im;
  return {
    re: (n.re*d.re + n.im*d.im) / dMag2,
    im: (n.im*d.re - n.re*d.im) / dMag2,
  };
}

// Bode 線図用データ生成
function bodeData(num, den, wMin = 0.01, wMax = 100, points = 200) {
  const data = [];
  const logMin = Math.log10(wMin), logMax = Math.log10(wMax);
  for (let i = 0; i < points; i++) {
    const omega = Math.pow(10, logMin + (logMax - logMin) * i / (points - 1));
    const G = frequencyResponse(num, den, omega);
    const mag = Math.sqrt(G.re*G.re + G.im*G.im);
    data.push({
      omega,
      gainDb: 20 * Math.log10(mag),
      phaseDeg: Math.atan2(G.im, G.re) * 180 / Math.PI,
    });
  }
  return data;
}

// 例: G(s) = 1 / (s^2 + 2s + 1)
const data = bodeData([1], [1, 2, 1]);
console.log(data.slice(0, 5));
```

これだけ。あとは [Chart.js](https://www.chartjs.org/) なり SVG なりで描けば完成です。

:::message
**位相のアンラップ（unwrap）**: 上のコードは `atan2` でそのまま位相を出していますが、Bode 線図では実用上「連続な位相」が欲しいので、隣接サンプル間で ±360° のジャンプを検出して補正するのが定番です。本実装では省略していますが、実装時の注意点として覚えておくと良いです。
:::

## ゲイン余裕と位相余裕で安定性を判定する

実用上の本題はここからです。**安定性判定**を Bode 線図から読み取ります：

- **位相交差周波数** $\omega_{pc}$ : 位相が -180° を切る周波数
- **ゲイン交差周波数** $\omega_{gc}$ : ゲインが 0 dB を切る周波数

そこから：

$$
GM = -20 \log_{10} |G(j\omega_{pc})| \, \text{[dB]}, \quad PM = 180° + \angle G(j\omega_{gc})
$$

経験則として、**PM ≥ 45°、GM ≥ 6 dB** あれば実用上の安定マージンは確保できる、と覚えておくと現場で困りません。

```javascript
function stabilityMargins(data) {
  // ω_gc: ゲインが 0 dB を下から横切る点
  let pmIdx = -1;
  for (let i = 1; i < data.length; i++) {
    if (data[i-1].gainDb > 0 && data[i].gainDb <= 0) { pmIdx = i; break; }
  }
  // ω_pc: 位相が -180° を下から横切る点
  let gmIdx = -1;
  for (let i = 1; i < data.length; i++) {
    if (data[i-1].phaseDeg > -180 && data[i].phaseDeg <= -180) { gmIdx = i; break; }
  }
  return {
    pm: pmIdx >= 0 ? 180 + data[pmIdx].phaseDeg : null,
    gm: gmIdx >= 0 ? -data[gmIdx].gainDb : null,
  };
}
```

これで PID ゲインをいじりながら「いま PM 何度？」を即座に見られます。実機調整ではこれが効きます。

NovaSolver の Bode 線図ジェネレーターでは、結果を 4 つの数値カードで常時表示しています：

![ゲイン余裕・位相余裕・交差周波数の表示](/images/bode-plot/stats.png)

PM が ∞ ということは、位相が -180° に達していない＝この系は十分に安定、という読み方になります。

## 実際に動かしてみる

ここまでの数式・コードを完成版に仕上げたものを NovaSolver に置いてあります：

📐 **[Bode 線図ジェネレーター（NovaSolver）](https://novasolver.jp/tools/bode-plot.html)**

- **PID プリセット**: $K_p, K_i, K_d$ をスライダーで動かして PM の変化を観察
- **代表的伝達関数を一発切り替え**: RC ローパス、二次遅れ、むだ時間付き、PID 補償器など
- **Chart.js でリアルタイム描画**: パラメータを変えた瞬間に再計算

二次遅れ系で減衰係数 $\zeta$ をスライダーで動かすと、ゲインと位相がリアルタイムに変化します：

![ζ スライダーを動かすと Bode 線図がリアルタイム変化](/images/bode-plot/slider-anim.gif)

$\zeta$ が小さくなると共振ピークが立ち上がり、ゲイン線図に大きな山ができるのが見えます。「PI 制御で $K_i$ を強くしすぎると PM が落ちて発振しそうになる」という古典の挙動も、実際に **スライダーを動かして体感** できます。教科書を読むのとは別の次元で頭に入ります。

## まとめ

- Bode 線図は伝達関数 → 周波数応答 → 対数軸プロットで作れる
- 50 行の JavaScript で十分実用的なものが書ける
- ゲイン余裕 / 位相余裕の自動検出も簡単
- 触って学ぶには [NovaSolver の Bode 線図ジェネレーター](https://novasolver.jp/tools/bode-plot.html) が便利

制御工学に限らず、**シミュレーター × ブラウザ** は「教科書で詰まった瞬間にすぐ確かめられる」という強い相性があります。手元で動かして、自分なりの直感を作ってみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。気になるトピックがあれば覗いてみてください。
