---
title: "ショックレーのダイオード式 — 「0.7Vで導通」の正体を指数関数で読む"
emoji: "🔌"
type: "tech"
topics: ["javascript", "電子工作", "半導体", "物理シミュレーション", "可視化"]
published: false
---

![ショックレーのダイオード式 — NovaSolver](/images/shockley-diode/cover.png)

## 「ダイオードは0.7Vで導通」は近似にすぎない

電子回路を学ぶと、まず「シリコンダイオードは順方向に 0.7 V かけると流れる」と教わります。便利な近似ですが、実際の電流と電圧の関係はもっと滑らかで、**指数関数**で記述されます。それを与えるのが **ショックレーのダイオード式** です：

$$
I = I_S\left(\exp\!\frac{qV}{nkT} - 1\right) = I_S\left(\exp\!\frac{V}{nV_T} - 1\right)
$$

ここで $I_S$ は飽和電流、$V$ は印加電圧、$n$ は理想率、$V_T = kT/q$ は熱電圧です。この式から見ると、$0.7\,\mathrm{V}$ という値は「電流が数百 mA に達する動作点での目安」であって、固定された閾値ではありません。実際、$V = 0.4\,\mathrm{V}$ でもすでに mA オーダーの電流が流れています。

この記事では：

1. 熱電圧 $V_T = kT/q$ がなぜ「室温で約 26 mV」なのか
2. 理想率 $n$ と「半対数グラフの傾き 60 mV/桁」の関係
3. 動的抵抗 $r_d = nV_T/I$ と、20 数行の JavaScript 実装

📐 **動くデモ**: [ショックレーダイオード シミュレーター（NovaSolver）](https://novasolver.jp/tools/shockley-diode.html)

## 熱電圧 V_T はなぜ約 26 mV なのか

熱電圧 $V_T$ は、ボルツマン定数 $k$・素電荷 $q$・絶対温度 $T$ だけで決まる、半導体物理の基本量です：

$$
V_T = \frac{kT}{q}
$$

「電子 1 個が持つ熱エネルギー $kT$ を電圧に換算したもの」と覚えると直感的です。$k = 1.381\times10^{-23}\,\mathrm{J/K}$、$q = 1.602\times10^{-19}\,\mathrm{C}$ を代入すると：

| 温度 | $T$ (K) | $V_T$ |
|---|---|---|
| $-40\,^\circ\mathrm{C}$ | 233.15 | 20.1 mV |
| $25\,^\circ\mathrm{C}$ | 298.15 | 25.7 mV |
| $27\,^\circ\mathrm{C}$（室温） | 300 | 25.85 mV |
| $125\,^\circ\mathrm{C}$ | 398.15 | 34.3 mV |

慣習的には「室温で約 26 mV」と覚えます。$V_T$ は式の分母に来るので、I-V カーブの「立ち上がりの急峻さ」が温度の関数になります。

## 60 mV/桁 — 半対数グラフの傾き

ショックレー式を順方向（$V \gg nV_T$ で $-1$ を無視）について対数を取ると：

$$
\log_{10} I = \log_{10} I_S + \frac{V}{n V_T \ln 10}
$$

つまり**半対数プロット上で I-V は直線**になり、電流を 1 桁（1 decade）増やすのに必要な電圧は

$$
\Delta V = n\,V_T \ln 10
$$

です。$n=1$、$25\,^\circ\mathrm{C}$ では $\Delta V = 1 \times 0.0257 \times 2.3026 \approx 59\,\mathrm{mV}$、慣用的に **「60 mV/decade」** と呼ばれる値です。$n=2$ ならその倍の約 118 mV/decade になり、立ち上がりが緩やかになります。理想率 $n$ は電流の運ばれ方を表す経験パラメータで、拡散電流支配なら $n\approx 1$、空乏層中の再結合電流支配なら $n\approx 2$ を取ります。

![n=1とn=2の半対数I-V特性、および温度による曲線シフト](/images/shockley-diode/charts-closeup.png)

左図は $n=1$（青）と $n=2$（桃）の半対数 I-V 特性です。傾きが $n$ 倍違うのがわかります。右図は同じダイオードを $T=25/75/125\,^\circ\mathrm{C}$ で比較したもので、高温ほど $V_T$ が増えて曲線が左へずれます（同じ電圧でより大きな電流が流れる）。

## 20 数行の JavaScript 実装

ショックレー式そのものは初等関数なので、数値積分すら不要です。NovaSolver のツールもこの式を実時間で評価しているだけです：

```javascript
const K_BOLTZ = 1.380649e-23;   // ボルツマン定数 [J/K]
const Q_ELEC  = 1.602176634e-19; // 素電荷 [C]

// 熱電圧 V_T = kT/q（T は摂氏）
function thermalVoltage(Tc) {
  return K_BOLTZ * (Tc + 273.15) / Q_ELEC;
}

// ショックレー式 I = I_S (exp(V / (n V_T)) - 1)
function diodeCurrent(V, IS, n, Tc) {
  const vt = thermalVoltage(Tc);
  let arg = V / (n * vt);
  if (arg > 700) arg = 700;        // exp のオーバーフロー対策
  return IS * (Math.exp(arg) - 1);
}

// 動作点での補助量：動的抵抗 r_d = n V_T / I、消費電力 P = V I
function operatingPoint(V, IS, n, Tc) {
  const vt = thermalVoltage(Tc);
  const I  = diodeCurrent(V, IS, n, Tc);
  const rd = I > 0 ? (n * vt / I) : Infinity;
  return { vt, I, rd, P: V * I };
}
```

既定値 $I_S = 1\,\mathrm{nA}$、$V_F = 0.40\,\mathrm{V}$、$n = 1.0$、$T = 25\,^\circ\mathrm{C}$ で実行すると：

```javascript
const op = operatingPoint(0.40, 1e-9, 1.0, 25);
// op.vt = 0.02569 V   → V_T ≈ 25.69 mV
// op.I  = 0.005773 A  → I   ≈ 5.77 mA
// op.rd = 4.45 Ω
// op.P  = 0.002309 W  → P   ≈ 2.31 mW
```

注意点は **`Math.exp` のオーバーフロー対策** だけです。$V = 1\,\mathrm{V}$、$n=1$、$V_T \approx 26\,\mathrm{mV}$ なら指数の引数は約 39 で問題ありませんが、$V_T$ を極端に小さくしたり $V$ を上げすぎると `Math.exp` が `Infinity` を返します。引数を上限でクランプしておくと安全です。

## 動的抵抗 r_d — 直流抵抗との違い

動作点での **動的抵抗（微分抵抗）** は I-V カーブの傾きの逆数で、次のきれいな形になります：

$$
r_d = \frac{dV}{dI} = \frac{nV_T}{I}
$$

ここで重要なのは、これが **オームの法則の直流抵抗 $V/I$ とは別物** だということです。既定動作点では直流抵抗が $V/I = 0.40 / 0.00577 \approx 69\,\Omega$ なのに対し、動的抵抗は $r_d \approx 4.5\,\Omega$ と一桁以上小さい。$r_d$ は「微小信号に対するインピーダンス」で、定電流バイアスしたダイオードがどれだけ電圧をクランプするかを表します。

| 量 | 式 | 既定値での値 |
|---|---|---|
| 熱電圧 | $V_T = kT/q$ | 25.7 mV |
| 順方向電流 | $I = I_S(e^{V/nV_T}-1)$ | 5.77 mA |
| 直流抵抗 | $V/I$ | 69 Ω |
| 動的抵抗 | $r_d = nV_T/I$ | 4.5 Ω |
| 消費電力 | $P = V\cdot I$ | 2.31 mW |

$r_d = nV_T/I$ という形は、バイポーラトランジスタのエミッタ小信号抵抗 $r_e = V_T/I_E$ とまったく同じです。LED 駆動の電流制限抵抗の選定や、検波・ミキサ回路の整合設計など、$r_d$ は実務で繰り返し登場します。

## ツールで遊ぶ

NovaSolver のツールでは、**順方向電圧 $V_F$ スライダー** を動かすと動作点マーカーが指数カーブを駆け上がり、電流が桁単位で変化する様子をその場で体感できます：

![V_F スライダーを動かすと動作点が指数カーブを上る](/images/shockley-diode/slider-anim.gif)

試してほしい操作：

- **「$V_F$ をスイープ」ボタン** で 0 → 1 V を自動往復させ、半対数 I-V カーブと動作点の動きを観察
- **理想率 $n$ スライダー** を 1.0 → 2.0 に動かし、曲線の立ち上がり（傾き 60 → 120 mV/桁）が緩くなるのを確認
- **温度 $T$ スライダー** を $-40 \to 150\,^\circ\mathrm{C}$ に動かし、熱電圧 $V_T$ と「温度比較（25/75/125°C）」グラフの曲線シフトを比べる
- **飽和電流 $\log_{10} I_S$ スライダー** で素子の種類（小信号ダイオードからパワーダイオードまで）を切り替え、同じ $V_F$ での電流が変わるのを見る

計算結果カードには $I$・$V_T$・$r_d$・$P$ の 4 値がリアルタイムで表示されます。

## まとめ

- ショックレー式 $I = I_S(e^{V/nV_T}-1)$ は pn 接合の I-V を表す理想式。「0.7 V で導通」はこの曲線上の一点の近似にすぎない
- 熱電圧 $V_T = kT/q$ は室温で約 26 mV。半対数 I-V の傾きは $nV_T\ln 10 \approx n\times 60\,\mathrm{mV}/\text{桁}$
- 既定値（$I_S=1\,\mathrm{nA}$, $V_F=0.40\,\mathrm{V}$, $n=1$, $25\,^\circ\mathrm{C}$）で $V_T\approx25.7\,\mathrm{mV}$, $I\approx5.77\,\mathrm{mA}$, $r_d\approx4.5\,\Omega$, $P\approx2.31\,\mathrm{mW}$
- 動的抵抗 $r_d = nV_T/I$ は直流抵抗 $V/I$ とは別物で、小信号設計の基本量

ただしショックレー式は理想モデルです。実機では大電流域での体抵抗、逆方向のリーク・降伏、$I_S$ 自体の強い温度依存（おおむね $10\,^\circ\mathrm{C}$ で倍増し、順方向電圧 $V_F$ が約 $-2\,\mathrm{mV/K}$ で低下）といった効果が加わります。それらの「ずれ」を知るうえでも、まず理想式を体で覚えるのが近道です。

📐 **[ショックレーダイオード シミュレーター（NovaSolver）](https://novasolver.jp/tools/shockley-diode.html)** で、$V_F$・$n$・$T$ を動かして指数カーブの正体を確かめてみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。電子回路・半導体まわりでは [PN接合ダイオード I-V特性](https://novasolver.jp/tools/semiconductor-pn.html)、[直列RLC共振回路](https://novasolver.jp/tools/rlc-resonance.html)、[NTCサーミスタ](https://novasolver.jp/tools/thermistor-ntc.html) なども揃えています。
