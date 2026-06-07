---
title: "ファンデルワールス状態方程式で実在気体を解く — 臨界点と圧縮率因子をJavaScriptで"
emoji: "💨"
type: "tech"
topics: ["javascript", "熱力学", "物理シミュレーション", "可視化", "数値計算"]
published: false
---

![ファンデルワールス実在気体 — NovaSolver](/images/van-der-waals-gas/cover.png)

## 理想気体では説明できない「気体が液体になる」現象

理想気体の法則 $PV = nRT$ は便利ですが、高圧・低温では破綻します。なにより、理想気体は**決して液体になりません**。現実の気体が冷やすと液化するのは、分子に「大きさ（排除体積）」と「引力」があるから。この 2 つを $PV=nRT$ に加えたのが**ファンデルワールス状態方程式**です。

この記事では、ファンデルワールス方程式をニュートン法で解き、臨界点と圧縮率因子を JavaScript で計算します。

💨 **動くデモ**: [ファンデルワールス気体シミュレーター（NovaSolver）](https://novasolver.jp/tools/van-der-waals-gas.html)

## 2つの補正と臨界点

ファンデルワールス方程式は、圧力に引力補正 $a/V_m^2$、体積に排除体積補正 $b$ を加えます。

$$
\left(P + \frac{a}{V_m^2}\right)(V_m - b) = RT
$$

この式の P-V 等温線は、ある温度を境に形が変わります。その境界が**臨界点**で、$\partial P/\partial V = \partial^2 P/\partial V^2 = 0$ から次のように $a, b$ だけで決まります。

$$
T_c = \frac{8a}{27Rb},\qquad P_c = \frac{a}{27b^2},\qquad V_c = 3b
$$

窒素 N₂（$a=1.35\,\mathrm{L^2 atm/mol^2}$, $b=0.039\,\mathrm{L/mol}$）で計算すると、$T_c = 125\,\mathrm{K}$、$P_c = 32.9\,\mathrm{atm}$。これは実測の窒素の臨界値（126 K, 33.5 atm）とよく一致します。$T < T_c$ では等温線が S 字の「ループ」を描き、これが気液共存（液化）に対応します。

既定条件（$T=300\,\mathrm{K}$, $P=50\,\mathrm{atm}$）でモル体積を解くと $V_m = 0.480\,\mathrm{L/mol}$、**圧縮率因子 $Z = PV_m/RT = 0.974$**。$Z < 1$ は理想気体（$Z=1$）より縮んでいる＝**分子間引力が支配的**であることを意味します。

![P-V等温線（左, 臨界点と亜臨界ループ）と圧縮率因子Z-P（右）](/images/van-der-waals-gas/charts-closeup.png)

## JavaScript 実装（ニュートン法）

体積について 3 次式になるので、ニュートン法で数値的に解きます。

```javascript
const R = 0.08206;  // L·atm/(mol·K)
function solveVm(P, T, a, b) {
  let V = R * T / P;                         // 理想気体を初期値に
  for (let i = 0; i < 60; i++) {
    const f  = (P + a/(V*V)) * (V - b) - R*T;        // 残差
    const fp = (P + a/(V*V)) - (2*a/(V*V*V))*(V - b); // 導関数
    const dV = f / fp;
    V -= dV;
    if (Math.abs(dV) < 1e-10) break;
  }
  return V;
}
const Z  = P * solveVm(P,T,a,b) / (R * T);   // 圧縮率因子
const Tc = 8*a / (27*R*b), Pc = a / (27*b*b), Vc = 3*b;  // 臨界点
```

圧力を上げていくと、低温では $Z$ がいったん 1 より小さくなり（引力）、さらに高圧では 1 を超えます（斥力＝排除体積が効く）。この $Z$ の振る舞いが、実在気体が理想からどうずれるかの指標です。

![温度を変えると等温線が変化（Tc以下で不安定ループ）](/images/van-der-waals-gas/slider-anim.gif)

## ツールで遊ぶ

[ファンデルワールス気体シミュレーター](https://novasolver.jp/tools/van-der-waals-gas.html)で試してほしい操作：

- **温度 T スライダー**を $T_c$ 以下に下げ、P-V 等温線が S 字ループ（気液共存の兆候）になるのを見る
- **引力定数 a スライダー**を上げ、$T_c$ と $P_c$ が上がる（液化しやすくなる）のを確認
- **排除体積 b スライダー**を変え、臨界体積 $V_c = 3b$ が動くのを見る
- **圧力 P スライダー**で「圧縮率因子 Z」が 1 からどれだけずれるか観察
- **Z-P 曲線**で低温時に Z が 1 を下回り（引力支配）、高圧で 1 を超える（斥力支配）のを読む
- a=0, b=0 に近づけて理想気体（Z=1）に戻ることを確認

## まとめ

- ファンデルワールス式は引力 $a/V^2$ と排除体積 $b$ で実在気体を表す
- 臨界点は $T_c = 8a/27Rb$、$P_c = a/27b^2$、$V_c = 3b$（N₂ で 125 K, 32.9 atm）
- モル体積はニュートン法で数値的に解ける
- 圧縮率因子 $Z = PV/RT$ が理想からのずれを示す（既定で 0.974＝引力支配）

理想気体の限界と液化の入口を、温度や分子定数を変えながら体感してみてください。

💨 **[ファンデルワールス気体シミュレーター（NovaSolver）](https://novasolver.jp/tools/van-der-waals-gas.html)** で、実在気体の振る舞いを確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。熱・統計では [マクスウェル・ボルツマン分布](https://novasolver.jp/tools/maxwell-boltzmann.html)、[混合エントロピー](https://novasolver.jp/tools/entropy-mixing.html)、[カルノーサイクル](https://novasolver.jp/tools/carnot-cycle.html) もどうぞ。
