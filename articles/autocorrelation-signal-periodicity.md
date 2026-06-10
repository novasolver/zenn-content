---
title: "自己相関でノイズに埋もれた周期を見つける — R(τ)=Σx(t)x(t+τ)をJavaScriptで"
emoji: "📡"
type: "tech"
topics: ["javascript", "信号処理", "DSP", "統計", "可視化"]
published: true
---

![自己相関と周期性検出 — NovaSolver](/images/autocorrelation/cover.png)

## ノイズだらけの信号から「隠れた周期」を取り出す

雑音まみれの信号を眺めても、そこに周期的な成分があるかどうかは目視では分かりません。そんなとき強力なのが**自己相関**。信号を自分自身の時間をずらしたコピーと掛け合わせることで、ノイズは打ち消し合い、周期成分だけが浮かび上がります。心拍のピッチ検出、音声の基本周波数推定、レーダー、地震波解析まで、周期性検出の定番です。

この記事では、自己相関を JavaScript で実装し、ノイズの中から周期を見つけます。

📡 **動くデモ**: [自己相関シミュレーター（NovaSolver）](https://novasolver.jp/tools/autocorrelation.html)

## 自己相関と周期検出

信号 $x[n]$ をラグ $k$ だけずらして掛け合わせ、平均したものが自己相関です（バイアス推定）。

$$
R_{xx}[k] = \frac{1}{N}\sum_{n=0}^{N-k-1} x[n]\,x[n+k],\qquad
\rho[k] = \frac{R_{xx}[k]}{R_{xx}[0]}
$$

$\rho[0] = 1$ で、周期 $T$ の成分があれば $\rho[k]$ は**ラグ $k = T$ で再びピーク**を作ります。ランダムなノイズはずらすと無相関になり打ち消えるため、周期成分だけが残るのです。

信号モデル $x[n] = A\sin(2\pi f_0 n) + \sigma\,\eta[n]$ の既定値（振幅 $A=1$、周波数 $f_0 = 0.05$、ノイズ $\sigma = 0.5$、$N=512$）で計算すると、SNR は $(A/\sigma)^2 = 4 = 6\,\mathrm{dB}$。生波形では周期が雑音に埋もれて見えませんが、自己相関を取ると**ラグ 20 サンプルに明瞭なピーク**が現れ、周期 $T = 1/f_0 = 20$ サンプルが正しく検出できます。

![ノイズ信号（上）と自己相関（下, ラグ20にピーク）](/images/autocorrelation/charts-closeup.png)

## JavaScript 実装

```javascript
function autocorr(x, N) {
  const K = Math.floor(N / 2);
  const R = new Float64Array(K + 1);
  for (let k = 0; k <= K; k++) {
    let s = 0;
    for (let n = 0; n < N - k; n++) s += x[n] * x[n + k];
    R[k] = s / N;                            // バイアス推定（N で割る）
  }
  const rho = R.map(v => v / R[0]);          // 正規化（ρ[0]=1）
  return rho;
}
// ピーク検出：最初のゼロ交差の後の最大値を周期とみなす
```

ピーク位置がそのまま周期になります。ノイズを強くしていっても（$\sigma$ を上げても）、周期成分があるかぎりラグ 20 のピークは残り続けます。これが「ノイズに強い」周期検出の威力です。

![ノイズを強くしても自己相関のピーク（周期20）は残る](/images/autocorrelation/slider-anim.gif)

## ツールで遊ぶ

[自己相関シミュレーター](https://novasolver.jp/tools/autocorrelation.html)で試してほしい操作：

- **信号周波数 f₀ スライダー**を変え、検出される周期（ピーク位置）が $1/f_0$ で動くのを確認
- **ノイズ標準偏差 σ スライダー**を上げ、生波形は乱れてもピークが残る（SNR 低下に強い）のを見る
- **信号振幅 A スライダー**で SNR が変わるのを確認（SNR=(A/σ)²）
- **サンプル数 N スライダー**を増やし、推定が安定するのを観察
- **「推定周期」「ρ(T)」「SNR」「R(0)」**の値を読む
- σ を極端に上げて、いつ周期検出が破綻するかを確かめる

## まとめ

- 自己相関 $R_{xx}[k] = \frac1N\sum x[n]x[n+k]$ で周期性を検出
- ノイズは打ち消え、周期成分はラグ $k=T$ にピークを作る
- 既定（f₀=0.05, σ=0.5, SNR=6dB）でラグ 20＝周期 20 を検出
- ピーク位置がそのまま周期になる

ノイズに埋もれた信号の周期を暴く DSP の基礎を、周波数やノイズを変えながら体感してみてください。

📡 **[自己相関シミュレーター（NovaSolver）](https://novasolver.jp/tools/autocorrelation.html)** で、隠れた周期の検出を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。信号処理では [FFTアナライザ](https://novasolver.jp/tools/fft-analyzer.html)、[ケプストラム分析](https://novasolver.jp/tools/cepstrum.html)、[フーリエ変換](https://novasolver.jp/tools/fourier-transform.html) もどうぞ。
