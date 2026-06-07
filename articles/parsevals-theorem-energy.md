---
title: "パーセバルの定理 — 時間と周波数で「エネルギーが保存する」ことをDFTで確かめる"
emoji: "⚖️"
type: "tech"
topics: ["javascript", "信号処理", "フーリエ変換", "数学", "可視化"]
published: false
---

![パーセバルの定理 — NovaSolver](/images/parsevals-theorem/cover.png)

## フーリエ変換しても「総エネルギー」は変わらない

信号を時間領域で眺めても、フーリエ変換して周波数領域で眺めても、それは同じ信号の別の見方にすぎません。ならば「信号の総エネルギー」は、どちらの領域で測っても等しいはず——それを保証するのが**パーセバルの定理（Parseval's theorem）** です。フーリエ解析が「情報を失わない変換」であることの数学的な裏付けでもあります。

この記事ではパーセバルの定理を離散版（DFT）で定式化し、JavaScript で時間領域と周波数領域のエネルギーを実際に計算して、両者が一致することを確かめます。

⚖️ **動くデモ**: [パーセバルの定理シミュレーター（NovaSolver）](https://novasolver.jp/tools/parsevals-theorem.html)

## 離散版パーセバルの定理

長さ $N$ の離散信号 $x[n]$ とその離散フーリエ変換（DFT）$X[k]$ について、パーセバルの定理は次のように書けます。

$$
\sum_{n=0}^{N-1} |x[n]|^2 = \frac{1}{N}\sum_{k=0}^{N-1} |X[k]|^2
$$

左辺が時間領域の総エネルギー $E_t$、右辺が周波数領域の総エネルギー $E_f$。係数 $1/N$ は DFT の正規化に由来します（DFT を $X[k]=\sum_n x[n]e^{-j2\pi kn/N}$ と定義した場合）。

周波数ビンごとのエネルギー $|X[k]|^2/N$ は**パワースペクトル密度（PSD）** と呼ばれ、「どの周波数にエネルギーが集中しているか」を表します。

## 実際に計算してみる

ツールの既定値（正弦波 $x[n]=A\cos(2\pi f_0 n/N)$、$A=1$、$f_0=10$、$N=512$）で確かめます。正弦波の時間領域エネルギーは $\cos^2$ の平均が $1/2$ であることから理論的に

$$
E_t = \sum_{n=0}^{N-1}|x[n]|^2 = \frac{N A^2}{2} = \frac{512\times1}{2} = 256
$$

一方、周波数領域でも DFT を計算して $E_f = (1/N)\sum_k|X[k]|^2$ を求めると、**$E_f = 256$** でぴったり一致します。実際の数値計算での相対誤差は浮動小数点演算の丸め程度（$\sim10^{-12}$）に収まります。

![時間領域の信号と周波数領域のPSD、両者のエネルギーが一致](/images/parsevals-theorem/charts-closeup.png)

正弦波のエネルギーは、周波数領域では $\pm f_0$ の 2 本のスペクトル線に集中します（上図下段のピーク）。バラバラに散らばった時間波形のエネルギーが、周波数領域では一点に凝縮される——それでも総和は変わらない、というのがパーセバルの妙味です。

## JavaScript 実装

DFT と両領域のエネルギー和は素直に書けます。

```javascript
function dftMagSq(x) {                      // |X[k]|^2 を返す
  const N = x.length, magSq = new Float64Array(N);
  for (let k = 0; k < N; k++) {
    let re = 0, im = 0;
    for (let n = 0; n < N; n++) {
      const ang = -2 * Math.PI * k * n / N;
      re += x[n] * Math.cos(ang);
      im += x[n] * Math.sin(ang);
    }
    magSq[k] = re * re + im * im;
  }
  return magSq;
}
let Et = 0; for (let n = 0; n < N; n++) Et += x[n] * x[n];           // 時間領域
let sum = 0; for (let k = 0; k < N; k++) sum += magSq[k]; const Ef = sum / N;  // 周波数領域
// Parseval: Et ≈ Ef
```

![信号の周波数を変えてもエネルギーの等式は保たれる](/images/parsevals-theorem/slider-anim.gif)

## ツールで遊ぶ

[パーセバルの定理シミュレーター](https://novasolver.jp/tools/parsevals-theorem.html)で試してほしい操作：

- **計算結果**で「時間域エネルギー $E_t$」「周波数域エネルギー $E_f$」「相対誤差」を見て、$E_t=E_f$（誤差が丸め程度）を確認
- **周波数 f₀ スライダー**を動かし、PSD のピークが移動しても $E_t=E_f$ が保たれることを観察
- **信号タイプ**を「正弦」「矩形パルス」「ガウス」で切り替え、波形が変わってもエネルギー等式が成り立つことを確認
- **振幅 A スライダー**を上げると $E_t,E_f$ がともに $A^2$ で増えることを見る
- **サンプル数 N スライダー**を変え、正弦波で $E_t = NA^2/2$ になることを確かめる
- 時間波形（上段）と PSD（下段）を見比べ、エネルギーが「散らばる／集中する」対比を体感

## まとめ

- パーセバルの定理：$\sum_n|x[n]|^2 = \frac{1}{N}\sum_k|X[k]|^2$。時間と周波数で総エネルギーが等しい
- 正弦波（$A=1$、$N=512$）では $E_t=E_f=256=NA^2/2$。数値誤差は丸め程度
- $|X[k]|^2/N$ がパワースペクトル密度（PSD）。エネルギーの周波数分布を表す
- フーリエ変換が情報を失わない（ユニタリ的な）変換であることの保証

信号処理・通信・スペクトル解析の土台となるエネルギー保存則を、両領域の数値を見比べて確かめてみてください。

⚖️ **[パーセバルの定理シミュレーター（NovaSolver）](https://novasolver.jp/tools/parsevals-theorem.html)** で、時間と周波数のエネルギーが一致する瞬間を見てみましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。信号処理系では [フーリエ変換](https://novasolver.jp/tools/fourier-transform.html)、[フーリエ級数](https://novasolver.jp/tools/fourier-series.html)、[FFTアナライザ](https://novasolver.jp/tools/fft-analyzer.html) なども揃えています。
