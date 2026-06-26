---
title: "ビット誤り率（BER）入門 — Eb/N0と変調方式で決まる通信品質"
emoji: "📡"
type: "tech"
topics: ["javascript", "通信", "信号処理", "可視化", "アルゴリズム"]
published: true
---

![ビット誤り率（BER）— NovaSolver](/images/bit-error-rate/cover.png)

## ビット誤り率（BER）とは

デジタル通信で「送ったビットのうち、どれくらいが化けたか」を表すのが **ビット誤り率（Bit Error Rate, BER）** です。BER が $10^{-6}$ なら、100 万ビットに 1 個が反転する、という意味になります。

このビットの化けを引き起こす主犯は **雑音** です。受信機の熱雑音や宇宙からの電波など、避けられないランダムな揺らぎが信号に足し算されます。これをモデル化したのが AWGN（加法性白色ガウス雑音）で、最も基本的な通信路です。

ここで効いてくるのが、絶対的な信号の強さではなく **信号と雑音の比** ——具体的には 1 ビットあたりのエネルギー $E_b$ と雑音電力スペクトル密度 $N_0$ の比 $E_b/N_0$ です。AWGN 通信路では、BPSK（2 値位相変調）の BER は次の式で **解析的に** 求まります：

$$
\text{BER}_{\text{BPSK}} = Q\!\left(\sqrt{2\,E_b/N_0}\right) = \frac{1}{2}\,\mathrm{erfc}\!\left(\sqrt{E_b/N_0}\right)
$$

$Q(x)$ は標準正規分布の上側裾確率、$\mathrm{erfc}$ は相補誤差関数です。$E_b/N_0$ は真数（リニア）値で、dB からは $E_b/N_0[\text{lin}] = 10^{(E_b/N_0[\text{dB}])/10}$ で変換します。

この記事では：

1. BPSK と高次 QAM の BER 式、その差が何を意味するか
2. 20 行ほどの JavaScript による BER 計算の実装
3. 「ウォーターフォール曲線」がなぜ滝のように落ちるのか、数値で確かめる

## 高次変調のトレードオフ

1 シンボルにより多くのビットを載せれば、同じ帯域で速く送れます（スペクトル効率の向上）。しかし信号点（コンスタレーション）の間隔が狭くなり、雑音に弱くなります。高次 QAM の近似 BER は次のとおりです：

$$
\text{BER}_{16\text{-QAM}} \approx \frac{3}{8}\,Q\!\left(\sqrt{\tfrac{4}{5}E_b/N_0}\right),\qquad
\text{BER}_{64\text{-QAM}} \approx \frac{7}{24}\,Q\!\left(\sqrt{\tfrac{2}{7}E_b/N_0}\right)
$$

平方根の中の係数（BPSK の 2 に対し、16-QAM は 4/5、64-QAM は 2/7）が小さいほど、同じ $E_b/N_0$ で BER が悪化します。「速さ」と「強さ」は基本的にトレードオフ、という関係がここに現れています。

## JavaScript で BER を計算する

`erfc` を有理近似で実装すれば、BER 計算は短く書けます。NovaSolver のツールも同じロジックで動いています：

```javascript
// 相補誤差関数（Abramowitz-Stegun 近似, 精度 ~1e-7）
function erfc(x){
  const z = Math.abs(x), t = 1/(1+0.5*z);
  const ans = t*Math.exp(-z*z-1.26551223+t*(1.00002368+t*(0.37409196
    +t*(0.09678418+t*(-0.18628806+t*(0.27886807+t*(-1.13520398
    +t*(1.48851587+t*(-0.82215223+t*0.17087277)))))))));
  return x>=0 ? ans : 2-ans;
}
const Q = x => 0.5*erfc(x/Math.SQRT2);

// AWGN 通信路の理論 BER（ebn0Lin は真数）
function berOf(mod, ebn0Lin){
  if(mod==='bpsk' || mod==='qpsk') return Q(Math.sqrt(2*ebn0Lin));
  if(mod==='qam16') return (3/8)*Q(Math.sqrt((4/5)*ebn0Lin));
  if(mod==='qam64') return (7/24)*Q(Math.sqrt((2/7)*ebn0Lin));
}

// 例: Eb/N0 = 8 dB の BPSK
const ebn0Lin = Math.pow(10, 8/10);   // = 6.310
console.log(berOf('bpsk', ebn0Lin));  // 1.909e-4
```

8 dB（真数 6.31）の BPSK で BER は約 $1.9\times10^{-4}$。10 Mbps なら 1 秒あたり約 1,900 ビットが化ける計算です。

## ウォーターフォール曲線

横軸に $E_b/N_0$ [dB]、縦軸に BER を対数目盛で取ると、ある領域から BER が滝のように急峻に落ちます。これが「ウォーターフォール曲線」です：

![BERウォーターフォール曲線とコンスタレーション](/images/bit-error-rate/charts-closeup.png)

BPSK の BER を $E_b/N_0$ ごとに並べると、その急峻さがよく分かります：

| $E_b/N_0$ [dB] | BER (BPSK) | BER (16-QAM) | BER (64-QAM) |
|---|---|---|---|
| 4 | $1.3\times10^{-2}$ | $2.9\times10^{-2}$ | $5.8\times10^{-2}$ |
| 8 | $1.9\times10^{-4}$ | $4.6\times10^{-3}$ | $2.6\times10^{-2}$ |
| 10 | $3.9\times10^{-6}$ | $8.8\times10^{-4}$ | $1.3\times10^{-2}$ |
| 11 | $2.6\times10^{-7}$ | $2.8\times10^{-4}$ | $8.4\times10^{-3}$ |
| 12 | $9.0\times10^{-9}$ | $6.9\times10^{-5}$ | $4.9\times10^{-3}$ |

BPSK では $E_b/N_0$ を 8 dB から 11 dB に **3 dB（電力で 2 倍）** 上げるだけで、BER が $1.9\times10^{-4}$ から $2.6\times10^{-7}$ へと **3 桁近く** 改善します。逆に言えば、ぎりぎりの設計では少しの劣化で一気に品質が崩れるということです。

設計の目安として、BER $= 10^{-6}$ を満たすのに必要な $E_b/N_0$ を変調方式ごとに比べると、BPSK/QPSK で約 **10.5 dB**、16-QAM で約 **14.1 dB**、64-QAM で約 **18.5 dB**。高次になるほど多くの $E_b/N_0$ を要求します。

![変調方式ごとの必要Eb/N0が変化する様子](/images/bit-error-rate/slider-anim.gif)

## ツールで遊ぶ

NovaSolver の [ビット誤り率（BER）シミュレーター](https://novasolver.jp/tools/bit-error-rate.html) では、スライダーを動かすと結果がその場で更新されます：

- **Eb/N0 スライダー** を 8 dB → 5 dB に下げて、BER が桁違いに悪化する様子を見る
- **変調方式** を BPSK / QPSK / 16-QAM / 64-QAM に切り替え、コンスタレーション図で信号点の間隔と受信シンボルの散らばりを比べる
- **誤り訂正符号化利得** を上げると、実効 Eb/N0 が底上げされ、ウォーターフォール曲線上の動作点が左へ動く
- **ビットレート** を変えて、1 秒あたりの誤りビット数がどう変わるか確認する

「計算結果」カードには BER・1 秒あたりの誤りビット数・スペクトル効率・必要 Eb/N0・実効 Eb/N0・通信品質判定が並び、ウォーターフォール曲線と「変調方式ごとの必要 Eb/N0」グラフも同時に更新されます。

## まとめ

- BER は「化けたビットの割合」。AWGN では BPSK の BER は $Q(\sqrt{2E_b/N_0})$ で解析的に求まる
- 高次 QAM はスペクトル効率が高い一方、同じ BER に必要な $E_b/N_0$ が大きい（速さと強さのトレードオフ）
- BER は $E_b/N_0$ に非常に敏感で、わずか数 dB の差が桁違いの品質差になる（ウォーターフォール曲線）
- BER $=10^{-6}$ の必要 $E_b/N_0$ は BPSK 約 10.5 dB、16-QAM 約 14.1 dB、64-QAM 約 18.5 dB

ここで扱ったのは AWGN という理想通信路の理論値です。実際の無線回線ではフェージングや実装損失で BER は理論値より悪化するため、設計では数 dB のマージンを見込むのが一般的です。

📡 **[ビット誤り率（BER）シミュレーター（NovaSolver）](https://novasolver.jp/tools/bit-error-rate.html)** で、Eb/N0 と変調方式を動かして「滝」の急峻さを体感してみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。信号処理・通信系では [FFTアナライザ](https://novasolver.jp/tools/fft-analyzer.html)、[ナイキストサンプリングとエイリアシング](https://novasolver.jp/tools/nyquist-sampling.html)、[正規分布（ガウス分布）](https://novasolver.jp/tools/normal-distribution.html) なども揃えています。

<!-- redeploy 2026-06-26 -->
