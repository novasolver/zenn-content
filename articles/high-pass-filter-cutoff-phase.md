---
title: "RCハイパスフィルタのカットオフと位相 — fc=1/(2πRC)をJavaScriptでボード線図に"
emoji: "🎚️"
type: "tech"
topics: ["javascript", "電気回路", "信号処理", "可視化", "数値計算"]
published: true
---

![ハイパスフィルタ — NovaSolver](/images/high-pass-filter/cover.png)

## 低い音をカットして高い音だけ通す回路

オーディオの「低音カット」、センサー信号の「直流ドリフト除去」、画像のエッジ強調――低周波を遮断して高周波を通すのが**ハイパスフィルタ**。最も基本的な RC ハイパスは、抵抗 $R$ とコンデンサ $C$ ふたつだけ。その振る舞いは**カットオフ周波数 $f_c$** ひとつで決まり、周波数特性（ボード線図）にきれいに表れます。

この記事では、RC ハイパスフィルタの周波数特性を JavaScript で計算します。

🎚️ **動くデモ**: [ハイパスフィルタシミュレーター（NovaSolver）](https://novasolver.jp/tools/high-pass-filter.html)

## 伝達関数とカットオフ周波数

RC ハイパスの伝達関数は、$\tau = RC$ として

$$
H(j\omega) = \frac{j\omega\tau}{1 + j\omega\tau},\qquad f_c = \frac{1}{2\pi RC}
$$

ゲイン（振幅特性）と位相は次式です。

$$
|H(f)|_{\mathrm{dB}} = 20\log_{10}\frac{f/f_c}{\sqrt{1+(f/f_c)^2}},\qquad
\phi = 90° - \arctan\!\frac{f}{f_c}
$$

カットオフ周波数 $f_c$ では振幅が $1/\sqrt2 \approx -3.01\,\mathrm{dB}$、位相が $+45°$ になります。$f_c$ より低い周波数では **−20 dB/decade**（10 倍ごとに 20 dB）で減衰し、高い周波数はそのまま通過（0 dB、位相 0°）します。

既定値 $R = 1\,\mathrm{k\Omega}$、$C = 100\,\mathrm{nF}$ で計算すると、時定数 $\tau = 100\,\mathrm{\mu s}$、**カットオフ周波数 $f_c = 1592\,\mathrm{Hz}$**。$f_c$ ちょうどの観測周波数では ゲイン $-3.01\,\mathrm{dB}$、位相 $+45°$。$f_c$ の 1/10（159 Hz）では $-20\,\mathrm{dB}$（10 分の 1 の振幅）まで落ちます。

![ボード線図：ゲイン特性（左）と位相特性（右）](/images/high-pass-filter/charts-closeup.png)

## JavaScript 実装

```javascript
function highpass(R, C, f) {
  const tau = R * C;
  const fc = 1 / (2 * Math.PI * tau);          // カットオフ周波数
  const ratio = f / fc;
  const gainDb = 20 * Math.log10(ratio / Math.sqrt(1 + ratio*ratio));
  const phaseDeg = 90 - Math.atan(ratio) * 180 / Math.PI;
  return { fc, gainDb, phaseDeg, tau };
}
// highpass(1000, 100e-9, 1592) → fc=1592Hz, gain=-3.01dB, phase=45°
```

カットオフ周波数は $R$ と $C$ の積だけで決まります。同じ $f_c$ なら $R$ を大きくして $C$ を小さくしても、逆でも構いません。これがフィルタ設計の自由度になります。

![C を変えるとカットオフ周波数が移動する](/images/high-pass-filter/slider-anim.gif)

## ツールで遊ぶ

[ハイパスフィルタシミュレーター](https://novasolver.jp/tools/high-pass-filter.html)で試してほしい操作：

- **抵抗 R・容量 C スライダー**を変え、カットオフ $f_c = 1/(2\pi RC)$ が移動するのを確認
- **観測周波数 f スライダー**を $f_c$ に合わせ、ゲイン −3 dB・位相 +45° になるのを見る
- $f$ を $f_c$ の 1/10 にして −20 dB（−20 dB/decade の傾き）を確認
- **「時定数 τ=RC」**でカットオフとの関係を読む
- **ボード線図**で低域の −20 dB/decade と高域の平坦部を観察
- **波形表示**で入出力の振幅・位相のずれを見る

## まとめ

- RC ハイパスのカットオフは $f_c = 1/(2\pi RC)$
- $f_c$ で −3.01 dB・位相 +45°、低域は −20 dB/decade で減衰
- 既定（R=1kΩ, C=100nF）で $f_c = 1592\,\mathrm{Hz}$、$\tau = 100\,\mathrm{\mu s}$
- カットオフは RC 積のみで決まる（設計の自由度）

電子回路の基本フィルタを、R・C を変えながらボード線図で体感してみてください。

🎚️ **[ハイパスフィルタシミュレーター（NovaSolver）](https://novasolver.jp/tools/high-pass-filter.html)** で、カットオフと位相特性を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。電気回路・信号処理では [RLC共振回路](https://novasolver.jp/tools/rlc-resonance.html)、[ボード線図](https://novasolver.jp/tools/bode-plot.html)、[FFTアナライザ](https://novasolver.jp/tools/fft-analyzer.html) もどうぞ。
