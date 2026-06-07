---
title: "ケプストラム分析 — 「スペクトルのスペクトル」でピッチを当てる"
emoji: "🎙️"
type: "tech"
topics: ["javascript", "信号処理", "DSP", "可視化", "音声"]
published: false
---

![ケプストラム分析 — NovaSolver](/images/cepstrum/cover.png)

## スペクトルをもう一度フーリエ変換する

人の声や楽器の音は、基本周波数 $f_0$（ピッチ）とその整数倍の高調波が**櫛（くし）状**に並んだスペクトルを持ちます。この櫛の間隔から $f_0$ を読み取りたい——ところが高調波が多いと素朴なピーク検出では難しい。

そこで登場するのが**ケプストラム（cepstrum）**。スペクトルの対数をもう一度フーリエ変換した「スペクトルのスペクトル」です。名前は spectrum のアナグラム、横軸の単位は frequency をもじった **quefrency（ケフレンシ）**。この一風変わった変換が、ピッチ検出を驚くほど鮮やかにこなします。

🎙️ **動くデモ**: [ケプストラム分析シミュレーター（NovaSolver）](https://novasolver.jp/tools/cepstrum.html)

## ケプストラムの定義

実ケプストラム $c[n]$ は、信号 $x$ の DFT の**対数振幅**を逆フーリエ変換したものです。

$$
c[n] = \frac{1}{N}\sum_{k=0}^{N-1} \log|X[k]|\,\cos\!\left(\frac{2\pi k n}{N}\right)
$$

なぜ「対数」が効くのか。音声は「声帯の励振（周期パルス列）」と「声道の伝達特性（フォルマント）」の**畳み込み**でできています。フーリエ変換で畳み込みは掛け算になり、**対数をとると掛け算が足し算に変わります**。足し算なら、ゆっくり変化するフォルマント成分と、細かく振動する高調波成分を、quefrency 軸上で**分離**できるのです。これが**ホモモルフィック（準同型）信号処理**の核心です。

## ピッチは quefrency のピークに現れる

スペクトルの櫛の間隔（＝高調波間隔 $f_0$）は、ケプストラムでは quefrency $\tau$ の位置のピークとして現れます。基本周期に対応する quefrency は

$$
\tau_{\text{pitch}} = \frac{F_s}{f_0},\qquad \hat{f}_0 = \frac{F_s}{\tau_{\text{peak}}}
$$

ツールの既定値（$f_0=200\,\mathrm{Hz}$、$F_s=8000\,\mathrm{Hz}$）なら、ピッチピークは quefrency $= 8000/200 = 40$ サンプル（時間 $\tau = 40/8000 = 5\,\mathrm{ms}$）に立ち、そこから $\hat{f}_0 = F_s/\tau_{\text{peak}} \approx 200\,\mathrm{Hz}$ と推定されます（量子化により実際は 40〜41 サンプル付近）。

![時系列・対数スペクトル（高調波の櫛）・ケプストラム（quefrencyピーク）](/images/cepstrum/charts-closeup.png)

上図中段の対数スペクトルに見える等間隔の櫛が、下段のケプストラムでは 1 本のピークに凝縮されています。

## JavaScript 実装

DFT → 対数振幅 → 逆 DFT（コサイン変換）→ ピーク探索、という素直なパイプラインです。

```javascript
// 1. スペクトルの対数振幅
for (let k = 0; k < N; k++) logMag[k] = Math.log(mag[k] + 1e-10);
// 2. 逆フーリエ変換 = 実ケプストラム
function realCepstrum(logMag, Ncep) {
  const c = new Float64Array(Ncep);
  for (let n = 0; n < Ncep; n++) {
    let sum = 0;
    for (let k = 0; k < N; k++) sum += logMag[k] * Math.cos(2*Math.PI*n*k/N);
    c[n] = sum / N;
  }
  return c;
}
// 3. ピッチ帯(2-20ms)でピーク → f0 = Fs / peakIndex
```

![基本周波数を変えるとケプストラムのピーク位置が動く](/images/cepstrum/slider-anim.gif)

## ツールで遊ぶ

[ケプストラム分析シミュレーター](https://novasolver.jp/tools/cepstrum.html)で試してほしい操作：

- **基本周波数 f₀ スライダー**を動かし、ケプストラムのピーク（quefrency）が反比例に移動するのを見る
- **計算結果**で「ケプストラムピーク quefrency」「対応する時間 τ」「推定基本周波数 f₀」「推定誤差」を確認
- **高調波減衰率 α スライダー**を変え、高調波の櫛の濃さがケプストラムのピークの明瞭さに与える影響を観察
- **ノイズ σ スライダー**を上げ、雑音下でもピッチピークが残る頑健さを確認
- **サンプリング Fs スライダー**を変え、$\tau=F_s/f_0$ の関係でピーク位置が動くことを見る
- 3 段の表示（時系列・対数スペクトル・ケプストラム）で、櫛が 1 本のピークに凝縮される流れを追う

## まとめ

- ケプストラムは「対数振幅スペクトルの逆フーリエ変換」＝スペクトルのスペクトル
- 対数で畳み込みが足し算になり、励振（ピッチ）と伝達系（フォルマント）を quefrency 軸で分離できる
- ピッチは $\tau_{\text{pitch}}=F_s/f_0$ のピークに現れ、$\hat{f}_0=F_s/\tau_{\text{peak}}$ で推定（既定で 40 サンプル＝5 ms）
- 音声のピッチ／フォルマント分析、MFCC、回転機械の歯車欠陥診断などで現役

ホモモルフィック信号処理の代表選手を、声のピッチを当てながら体感してみてください。

🎙️ **[ケプストラム分析シミュレーター（NovaSolver）](https://novasolver.jp/tools/cepstrum.html)** で、スペクトルをもう一度変換する不思議を見てみましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。信号処理系では [Goertzelアルゴリズム](https://novasolver.jp/tools/goertzel-algorithm.html)、[パーセバルの定理](https://novasolver.jp/tools/parsevals-theorem.html)、[FFTアナライザ](https://novasolver.jp/tools/fft-analyzer.html) なども揃えています。
