---
title: "RC ローパスフィルタの直感 — カットオフ周波数と位相遅れを JavaScript で可視化する"
emoji: "⚡"
type: "tech"
topics: ["javascript", "数学", "電気回路", "信号処理", "可視化"]
published: false
---

![RC ローパスフィルタ — NovaSolver](/images/low-pass-filter/cover.png)

## RC ローパスとは

抵抗 $R$ とコンデンサ $C$ を直列接続し、$C$ の両端から出力を取り出す **最も基本的なローパスフィルタ** です。

オーディオの高域カット、AD コンバータ前段のアンチエイリアシング、PWM 電圧の平滑化、センサー信号のノイズ除去——とにかく現場で **死ぬほど使われる**回路です。

この記事では：

1. 伝達関数とカットオフ周波数の定義
2. ゲイン・位相のボード線図
3. JavaScript で実装した周波数応答計算

📐 **動くデモ**: [RC ローパスフィルタ（NovaSolver）](https://novasolver.jp/tools/low-pass-filter.html)

## 伝達関数

入力 $V_\text{in}$、出力 $V_\text{out}$ とすると、複素インピーダンス分割で：

$$
H(j\omega) = \frac{V_\text{out}}{V_\text{in}} = \frac{1/(j\omega C)}{R + 1/(j\omega C)} = \frac{1}{1 + j\omega RC}
$$

$\tau = RC$ を **時定数** と呼びます。これが回路の応答速度を支配する唯一のパラメータです。

## カットオフ周波数

ゲインの絶対値は：

$$
|H(j\omega)| = \frac{1}{\sqrt{1 + (\omega \tau)^2}}
$$

$\omega \tau = 1$、つまり $\omega_c = 1/\tau = 1/(RC)$ のとき **ゲイン = $1/\sqrt{2} \approx 0.707$（= -3 dB）** になります。これを **カットオフ周波数** と定義します。

通常 Hz 表記すると：

$$
f_c = \frac{1}{2\pi RC}
$$

「$f_c$ 以下はそのまま通す、$f_c$ 以上は徐々に減衰させる」というのが直感です。$f_c$ より十分高い周波数では **-20 dB/decade**（周波数 10 倍で 1/10）の傾きで落ちます。

## 位相遅れ

位相は：

$$
\angle H(j\omega) = -\arctan(\omega \tau)
$$

- $\omega \to 0$: 位相 $\to 0°$
- $\omega = \omega_c$: 位相 = $-45°$
- $\omega \to \infty$: 位相 $\to -90°$

カットオフ周波数で必ず **-45° 遅れる**。これは制御工学的に重要で、PID 制御のループに入れると位相余裕を食う原因になります。

## 50 行の JavaScript で実装

```javascript
function rcResponse(R, C, freqHz) {
  const tau = R * C;
  const omega = 2 * Math.PI * freqHz;
  const wTau = omega * tau;
  return {
    gainDb: 20 * Math.log10(1 / Math.sqrt(1 + wTau * wTau)),
    phaseDeg: -Math.atan(wTau) * 180 / Math.PI,
  };
}

function bodeData(R, C, fMin = 1, fMax = 1e5, points = 200) {
  const out = [];
  const logMin = Math.log10(fMin), logMax = Math.log10(fMax);
  for (let i = 0; i < points; i++) {
    const f = Math.pow(10, logMin + (logMax - logMin) * i / (points - 1));
    const { gainDb, phaseDeg } = rcResponse(R, C, f);
    out.push({ f, gainDb, phaseDeg });
  }
  return out;
}

// 例: R = 1kΩ, C = 100nF → fc = 1/(2π·1000·100e-9) ≈ 1.59 kHz
console.log(rcResponse(1000, 100e-9, 1590));
// → { gainDb: -3.01, phaseDeg: -45.0 }
```

カットオフ周波数で確かに -3 dB / -45° が出ます。

## 入力・出力波形を見る

時間波形で見ると、サイン波入力が **振幅減衰 + 位相遅れ** で出てくる様子が直感的に理解できます：

![RC ローパスの入力波形（青）と出力波形（橙）の比較](/images/low-pass-filter/charts-closeup.png)

カットオフ近辺の周波数では、橙色（出力）が青（入力）に対して **遅れて、かつ小さく** なっているのがわかります。

## R を動かして体感する

NovaSolver のツールで R スライダーを動かすと、ボード線図のカットオフ周波数が右にずれます：

![R スライダーでカットオフ周波数が変化](/images/low-pass-filter/slider-anim.gif)

$R$ を小さくする → $\tau$ 小 → $f_c$ 高 → 高周波まで通る、という関係が体で覚えられます。

## ゲインと位相の数値表示

カットオフ周波数の真上で、|H| = 0.707、φ = -45° となるのが見て確認できます：

![ゲインと位相の数値表示](/images/low-pass-filter/stats.png)

## 実用上の注意点

1. **負荷インピーダンスの影響**: 出力側に低インピーダンス負荷が付くと特性が崩れる。バッファアンプを挟むのが定石
2. **コンデンサの ESR**: 実物のコンデンサは等価直列抵抗を持ち、高周波で理論通りにならない
3. **デジタル実装**: マイコンでは離散時間版（IIR 1次フィルタ）で実装、$\alpha = \Delta t / (RC + \Delta t)$ で `y[n] = α·x[n] + (1-α)·y[n-1]`

「ローパス入れたら勝手にノイズが消える」と思いがちですが、**位相遅れと共に消える**のが本質です。

## まとめ

- RC ローパスは $\tau = RC$ で特性が決まる 1 パラメータ系
- カットオフ周波数 $f_c = 1/(2\pi RC)$ で -3 dB、-45°
- 高周波側は -20 dB/decade、位相は最終的に -90°
- 制御系の中に入れる場合は位相遅れが効くので注意

回路の基本中の基本ですが、**周波数応答の感覚** はここでつけておくと後が楽です。

📐 **[RC ローパスフィルタ（NovaSolver）](https://novasolver.jp/tools/low-pass-filter.html)** で R・C を動かしてみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。フィルタ系では他にも [ハイパスフィルタ](https://novasolver.jp/tools/high-pass-filter.html)、[バンドパスフィルタ](https://novasolver.jp/tools/band-pass-filter.html)、[FIRフィルタ設計](https://novasolver.jp/tools/fir-filter-design.html) などを揃えています。
