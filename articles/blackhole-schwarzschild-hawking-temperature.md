---
title: "ブラックホールの事象の地平面 — Schwarzschild 半径と Hawking 温度"
emoji: "🕳️"
type: "tech"
topics: ["javascript", "物理", "天文学", "相対論", "物理シミュレーション"]
published: false
---

![ブラックホールの事象の地平面 — NovaSolver](/images/blackhole-event-horizon/cover.png)

## 事象の地平面とは

ブラックホールの「光すら脱出できない境界」が **事象の地平面（Event Horizon）**です。地球の地平線の向こうが見えないのと同じで、この境界より内側で起きた出来事の情報は、外の宇宙に一切届きません。

その半径を与えるのが、1916 年に Karl Schwarzschild が一般相対論の方程式を解いて得た **Schwarzschild 半径**です。質量 $M$ の物体をこの半径まで圧縮すると、表面からの脱出速度が光速に達します。

この記事では：

1. Schwarzschild 半径 $r_s = 2GM/c^2$ と回転（Kerr）の効果
2. Hawking 温度・蒸発寿命の JavaScript 実装
3. 太陽質量から超大質量 BH までの構造を数値で確かめる

📐 **動くデモ**: [ブラックホール事象の地平面シミュレーター（NovaSolver）](https://novasolver.jp/tools/blackhole-event-horizon.html)

## 主要な式

回転しないブラックホールの地平面半径と、回転する Kerr ブラックホールの外側地平面 $r_+$：

$$
r_s = \frac{2GM}{c^2},\qquad r_+ = \frac{GM}{c^2}\bigl(1 + \sqrt{1 - (a/M)^2}\bigr)
$$

$a/M$ は 0（回転なし）から 1（極限 Kerr）までのスピンパラメータです。$a/M=0$ で $r_+ = r_s$、最大回転に近づくほど地平面は縮みます。

量子効果を取り入れると、ブラックホールは熱的な放射をして「蒸発」します（1974 年、Stephen Hawking）。その **Hawking 温度**と **蒸発寿命**は：

$$
T_{\text{Hawking}} = \frac{\hbar c^{3}}{8\pi G M k_{B}},\qquad t_{\text{evap}} = \frac{5120\,\pi\, G^{2} M^{3}}{\hbar c^{4}}
$$

温度は質量に反比例し、寿命は質量の 3 乗に比例します。さらに降着円盤に重要な **ISCO（最内縁安定円軌道）**と **光子球**：

$$
r_{\text{ISCO}}^{\text{Schw}} = \frac{6GM}{c^{2}} = 3r_s,\qquad r_{\text{photon}} = 1.5\,r_s
$$

## JavaScript で実装する

ツールが行う計算は、SI 単位の物理定数を入れた素直な式です：

```javascript
const G = 6.674e-11, c = 2.998e8;
const hbar = 1.0546e-34, k_B = 1.381e-23, M_sun = 1.989e30;

function blackhole(Msolar, aM = 0) {
  const M = Msolar * M_sun;
  const r_s = 2 * G * M / (c * c);                 // [m]
  const root = Math.sqrt(Math.max(0, 1 - aM * aM));
  const r_outer  = (1 + root) * r_s / 2;           // Kerr 外側地平面
  const r_photon = 1.5 * r_s;                      // 光子球
  const T_H  = (hbar * c ** 3) / (8 * Math.PI * G * M * k_B);   // [K]
  const life = 5120 * Math.PI * G * G * M ** 3 / (hbar * c ** 4); // [s]
  return {
    r_s_km: r_s / 1000,
    r_outer_km: r_outer / 1000,
    photon_km: r_photon / 1000,
    T_H,
    life_yr: life / (365.25 * 86400),
  };
}

const b = blackhole(10, 0);  // 10 太陽質量、回転なし
console.log(b.r_s_km.toFixed(2), b.T_H.toExponential(2), b.life_yr.toExponential(2));
// 29.54  6.17e-9  2.10e+70
```

10 太陽質量の非回転ブラックホールで $r_s \approx 29.5$ km、Hawking 温度は約 6.2 nK、蒸発寿命は約 $2\times10^{70}$ 年と求まります。

## 可視化：ブラックホールの構造

ツールは事象の地平面（黒）・光子球（紫）・ISCO（橙）・降着円盤を、質量とスピンに応じて描きます。

![ブラックホールの構造と r_s vs M の関係](/images/blackhole-event-horizon/charts-closeup.png)

Schwarzschild 半径は質量に正比例するため、log-log プロットでは一本の直線になります。一方、Hawking 温度は質量に反比例し、太陽質量級では宇宙背景放射（2.7 K）を遥かに下回ります。

## 質量スケールを数値で確かめる

代表的な天体について計算し、教科書値と突き合わせます：

| 対象 | 質量 | $r_s$ | Hawking 温度 |
|---|---|---|---|
| 地球 | $5.97\times10^{24}$ kg | 8.87 mm | — |
| 太陽 | $1\,M_\odot$ | 2.95 km | 62 nK |
| 恒星質量 BH | $10\,M_\odot$ | 29.5 km | 6.2 nK |
| Sgr A*（銀河中心） | $4.3\times10^6\,M_\odot$ | $1.27\times10^7$ km | $1.4\times10^{-14}$ K |
| M87*（EHT 撮像） | $6.5\times10^9\,M_\odot$ | 128 AU | — |

太陽を $r_s = 2.95$ km まで圧縮すればブラックホールになる、というのは典型的な教科書値と一致します。Hawking 温度 62 nK（太陽質量）も標準的な値です。

寿命の桁感も確認しておきます。太陽質量 BH の蒸発寿命は約 $2.1\times10^{67}$ 年で、宇宙年齢（$1.38\times10^{10}$ 年）の実に $10^{57}$ 倍。逆に「寿命 = 宇宙年齢」となる質量を逆算すると、約 $1.7\times10^{14}$ g（$1.7\times10^{11}$ kg）となり、これが「いま蒸発し終えるはずの原始ブラックホール」の質量スケールとされています。

回転の効果も確かめられます。$10\,M_\odot$ で $a/M=0.8$ にすると、$r_s$ は質量だけで決まるので 29.5 km のままですが、外側地平面 $r_+$ は 23.6 km に縮みます。スピンを上げるほど地平面が小さくなる、という Kerr 解の振る舞いがそのまま出ています。

## ツールで遊ぶ

NovaSolver のツールでは、質量とスピンを変えて構造をリアルタイムに観察できます：

![質量を変えると r_s と温度が変わる](/images/blackhole-event-horizon/slider-anim.gif)

試してほしい操作：

- **ブラックホール種別**セレクトで「恒星質量／中質量／超大質量」のプリセットをワンクリック切替
- **質量 $M$**（太陽質量単位）スライダーを動かし、$r_s$ が比例・温度が反比例で変わる様子を確認
- **Kerr スピン $a/M$**（0〜0.998）を上げて、外側地平面 $r_+$ が縮みエルゴ領域が現れるのを観察
- **観測者距離**を地平面に近づけて、重力赤方偏移・時間遅延の判定メッセージを確認
- **軌道半径 $r/r_s$** を ISCO 以下にして、安定軌道が存在しない領域を確認

## まとめ

- 事象の地平面の半径は $r_s = 2GM/c^2$、太陽で約 2.95 km、地球で約 8.87 mm
- 回転（Kerr）では $r_+ = (GM/c^2)(1+\sqrt{1-(a/M)^2})$ で、スピンを上げると地平面が縮む
- Hawking 温度 $T_H \propto 1/M$、蒸発寿命 $t_{\text{evap}} \propto M^3$。太陽質量で 62 nK・$2\times10^{67}$ 年
- 寿命が宇宙年齢に等しくなる原始 BH の質量は約 $1.7\times10^{11}$ kg

現実の星質量・超大質量ブラックホールは Hawking 温度が宇宙背景放射より遥かに低いため、蒸発より吸収が勝り、実質的に消えることはないと考えられています。それでも「温度がゼロでない」こと自体が量子重力への手がかりとして重要視されています。

📐 **[ブラックホール事象の地平面シミュレーター（NovaSolver）](https://novasolver.jp/tools/blackhole-event-horizon.html)** で、質量とスピンを動かして地平面の構造を見てみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。天体・重力分野では [ケプラー二体問題の軌道](https://novasolver.jp/tools/kepler-orbit.html)、[脱出速度と重力井戸](https://novasolver.jp/tools/escape-velocity.html)、[N 体重力シミュレーション](https://novasolver.jp/tools/n-body-gravity.html) なども揃えています。
