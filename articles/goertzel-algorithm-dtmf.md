---
title: "Goertzelアルゴリズム — FFTを使わず特定周波数だけ検出する（DTMF）"
emoji: "☎️"
type: "tech"
topics: ["javascript", "信号処理", "アルゴリズム", "DSP", "可視化"]
published: false
---

![Goertzelアルゴリズム — NovaSolver](/images/goertzel-algorithm/cover.png)

## プッシュホンの「ピポパ」を聞き分ける

固定電話のボタンを押すと「ピポパ」と鳴ります。あの音は **DTMF（Dual-Tone Multi-Frequency）**——低群（行）と高群（列）から 1 つずつ、合計 2 つの正弦波を重ねたものです。受信側は「どの 2 周波数が含まれるか」だけ分かればキーを特定できます。

ここで全周波数スペクトルを出す FFT は**過剰**です。必要な数個の周波数だけを安く調べたい——その答えが **Goertzel アルゴリズム**。1958 年に Gerald Goertzel が考案した、二次 IIR フィルタによる単一周波数検出法です。

☎️ **動くデモ**: [Goertzelアルゴリズム シミュレーター（NovaSolver）](https://novasolver.jp/tools/goertzel-algorithm.html)

## Goertzel の漸化式

目的の周波数に対応する DFT ビン $k = \mathrm{round}(f\cdot N/F_s)$ を決め、係数

$$
c = 2\cos\!\left(\frac{2\pi k}{N}\right)
$$

を使って、入力 $x[n]$ を二次の漸化式に通します。

$$
s_n = x_n + c\,s_{n-1} - s_{n-2}
$$

$N$ サンプル流し終えたら、最後の 2 状態から目的周波数のパワーが求まります。

$$
|X_k|^2 = s_{N-1}^2 + s_{N-2}^2 - c\,s_{N-1}\,s_{N-2}
$$

サインやコサインのテーブルも複素数も不要。**1 周波数あたり乗算 1 回／サンプル**という軽さです。

## なぜ FFT より速いのか

FFT は全 $N$ 個のビンを $O(N\log N)$ で一気に求めます。対して Goertzel は 1 ビンを $O(N)$ で求めるので、検出したい周波数が $M$ 個なら合計 $O(NM)$。**$M \ll \log N$ のときに Goertzel が有利**です。DTMF は行 4 ＋列 4 ＝ 8 周波数だけ見ればよいので、まさに Goertzel の独壇場。ツールの既定設定（$N=256$）では演算量は $N\times M = 256\times8 = 2048$ 回の乗算で済みます。

![DTMFキー'5'の信号と、8周波数のGoertzel検出結果](/images/goertzel-algorithm/charts-closeup.png)

## DTMF を実際に検出する

DTMF の周波数表は行 = {697, 770, 852, 941} Hz、列 = {1209, 1336, 1477, 1633} Hz。キー「5」は**行 770 Hz ＋列 1336 Hz** の組み合わせです。この 2 音を重ねた信号を 8 つの Goertzel フィルタに通すと、上図のように 770 Hz と 1336 Hz のバーだけが突出します。最強の行と列を読めば、押されたキーが「5」だと特定できます。

## JavaScript 実装

漸化式そのままで、驚くほど短く書けます。

```javascript
function goertzel(x, N, Fs, targetF) {
  const k = Math.round(targetF * N / Fs);
  const omega = 2 * Math.PI * k / N;
  const c = 2 * Math.cos(omega);             // 係数（事前計算可）
  let s1 = 0, s2 = 0;
  for (let n = 0; n < N; n++) {
    const s = x[n] + c * s1 - s2;            // 二次IIR：乗算1回/サンプル
    s2 = s1; s1 = s;
  }
  return s1*s1 + s2*s2 - c*s1*s2;            // |X_k|^2
}
// DTMF: 行4+列4=8周波数それぞれに適用し、最強の行・列からキーを判定
```

![DTMFキーを切り替えると検出される2周波数が変わる](/images/goertzel-algorithm/slider-anim.gif)

## ツールで遊ぶ

[Goertzelアルゴリズム シミュレーター](https://novasolver.jp/tools/goertzel-algorithm.html)で試してほしい操作：

- **DTMF キー番号スライダー**（0〜15）を動かし、**検出される行・列周波数**と 8 本のバーが変わるのを見る
- **計算結果**で「検出キー」「最強行周波数」「最強列周波数」「演算量 N·M」を確認
- **ノイズレベルスライダー**を上げ、雑音の中でも目的周波数のバーが立つ（耐雑音性）ことを観察
- **フレーム長 N スライダー**を変え、長いほど周波数分解能が上がる一方で演算量 $N\cdot M$ が増えることを確認
- **サンプリング Fs スライダー**を変え、ビン $k=\mathrm{round}(f N/F_s)$ がどう移るか見る
- 入力信号（上段）と Goertzel 出力（下段バー）を見比べ、2 音検出の仕組みを体感

## まとめ

- Goertzel は二次 IIR フィルタで**単一周波数のパワー**を求める：$s_n=x_n+c\,s_{n-1}-s_{n-2}$、$c=2\cos(2\pi k/N)$
- 1 周波数 $O(N)$、$M$ 周波数で $O(NM)$。**$M\ll\log N$ なら FFT より速い**
- DTMF（8 周波数検出）に最適。キー「5」は 770 Hz＋1336 Hz として検出される
- サイン表も複素数も不要で、組込み・低リソース環境に向く

電話・トーン検出・モールス受信などで現役の DSP 古典を、キーを押しながら体感してみてください。

☎️ **[Goertzelアルゴリズム シミュレーター（NovaSolver）](https://novasolver.jp/tools/goertzel-algorithm.html)** で、必要な周波数だけを安く拾う仕組みを見てみましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。信号処理系では [パーセバルの定理](https://novasolver.jp/tools/parsevals-theorem.html)、[ケプストラム分析](https://novasolver.jp/tools/cepstrum.html)、[FFTアナライザ](https://novasolver.jp/tools/fft-analyzer.html) なども揃えています。
