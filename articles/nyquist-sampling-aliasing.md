---
title: "標本化定理とエイリアシング — なぜ600Hzが400Hzに化ける？ 折り返しをJSで"
emoji: "📶"
type: "tech"
topics: ["javascript", "信号処理", "DSP", "可視化", "数値計算"]
published: false
---

![標本化定理とエイリアシング — NovaSolver](/images/nyquist-sampling/cover.png)

## デジタル化で高い音が「別の音」に化ける

アナログ信号をデジタル化（標本化）するとき、サンプリング周波数が低すぎると**高い周波数が低い周波数に化けて**しまいます。これが**エイリアシング（折り返し雑音）**。動画で車輪が逆回転して見える「ワゴンホイール効果」も同じ現象です。これを防ぐ指針が**標本化定理（ナイキスト定理）**：「信号の最高周波数の 2 倍より速くサンプリングせよ」。

この記事では、エイリアシングと折り返しを JavaScript で計算します。

📶 **動くデモ**: [標本化定理シミュレーター（NovaSolver）](https://novasolver.jp/tools/nyquist-sampling.html)

## ナイキスト周波数と折り返し

サンプリング周波数 $f_s$ の半分が**ナイキスト周波数** $f_N = f_s/2$。信号周波数 $f$ がこれを超えると、見かけの周波数（エイリアス）に折り返されます。

$$
f_N = \frac{f_s}{2},\qquad
f_{\text{alias}} = \bigl|\,f - \mathrm{round}(f/f_s)\cdot f_s\,\bigr|
$$

正しく再構成できる条件は $f_s \ge 2 f_{\max}$（標本化定理）。

既定値 $f = 600\,\mathrm{Hz}$、$f_s = 1000\,\mathrm{Hz}$ では、ナイキスト周波数 $f_N = 500\,\mathrm{Hz}$。信号が $f_N$ を超えているため、**見かけの周波数は $|600 - 1\times1000| = 400\,\mathrm{Hz}$** に化けます。サンプル点だけ見ると、元の 600 Hz と 400 Hz の波形は完全に一致してしまい、区別できません。量子化ビット数 $N=8$ なら量子化 SNR は $6.02N + 1.76 = 49.92\,\mathrm{dB}$ です。

![原信号・サンプル点・見かけ波形（上）と折り返しの三角波（下）](/images/nyquist-sampling/charts-closeup.png)

## JavaScript 実装

```javascript
function nyquist(f, fs, bits) {
  const fN = fs / 2;                                  // ナイキスト周波数
  const k = Math.round(f / fs);
  const fAlias = Math.abs(f - k * fs);               // 折り返し後の見かけ周波数
  const aliasing = f > fN;                            // 標本化定理を満たすか
  const snrDb = 6.02 * bits + 1.76;                   // 量子化 SNR
  return { fN, fAlias, aliasing, snrDb };
}
// nyquist(600, 1000, 8) → fN=500Hz, fAlias=400Hz, aliasing=true, SNR=49.92dB
```

折り返しの様子は三角波（のこぎり波）になります。信号周波数を上げていくと、見かけの周波数は $0 \to f_N$ を行き来し、$f_s$ ごとに同じパターンを繰り返します。だからアンチエイリアシングフィルタで $f_N$ 以上を事前に除去するのが、正しいデジタル化の鉄則です。

![サンプリング周波数を下げるとエイリアシングが発生する](/images/nyquist-sampling/slider-anim.gif)

## ツールで遊ぶ

[標本化定理シミュレーター](https://novasolver.jp/tools/nyquist-sampling.html)で試してほしい操作：

- **信号周波数 f スライダー**を上げ、$f > f_s/2$ で「エイリアシング」表示になるのを確認
- **サンプリング周波数 f_s スライダー**を上げ、$f_s \ge 2f$ で「正常」に戻るのを見る
- **「ナイキスト周波数」「見かけ周波数」**の値を読む
- **波形表示**で原信号（橙）と見かけ波形（黄）がサンプル点で一致するのを観察
- **折り返しグラフ**で見かけ周波数が三角波状に折り返すのを見る
- **量子化ビット数 N スライダー**で SNR の変化を確認

## まとめ

- ナイキスト周波数 $f_N = f_s/2$、標本化定理は $f_s \ge 2f_{\max}$
- $f > f_N$ で見かけ周波数 $f_{\text{alias}} = |f - \mathrm{round}(f/f_s)f_s|$ に化ける
- 既定（f=600, fs=1000）で見かけ 400 Hz、量子化 SNR 49.92 dB
- 防止にはアンチエイリアシングフィルタで $f_N$ 以上を除去

デジタル信号処理の最重要概念を、信号・サンプリング周波数を変えながら体感してみてください。

📶 **[標本化定理シミュレーター（NovaSolver）](https://novasolver.jp/tools/nyquist-sampling.html)** で、エイリアシングと折り返しを確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。信号処理では [FFTアナライザ](https://novasolver.jp/tools/fft-analyzer.html)、[自己相関](https://novasolver.jp/tools/autocorrelation.html)、[フーリエ変換](https://novasolver.jp/tools/fourier-transform.html) もどうぞ。
