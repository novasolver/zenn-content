---
title: "ブレイトンサイクルの熱効率は圧力比だけで決まる — ガスタービンの基礎をJavaScriptで"
emoji: "✈️"
type: "tech"
topics: ["javascript", "熱力学", "CAE", "可視化", "数値計算"]
published: false
---

![ブレイトンサイクル（ガスタービン） — NovaSolver](/images/brayton-cycle/cover.png)

## ジェットエンジンと発電用タービンの心臓

ジェットエンジンやガスタービン発電所の動作を理想化したのが**ブレイトンサイクル**です。圧縮機で空気を圧縮し、燃焼室で加熱し、タービンで膨張させて仕事を取り出す――この連続フローの熱効率は、なんと**圧力比 $r_p$ と比熱比 $\gamma$ だけ**で決まります。オットーサイクルが圧縮比で決まるのと美しく対応しています。

この記事では、ブレイトンサイクルの効率と T-s 線図上の状態点を JavaScript で計算します。

✈️ **動くデモ**: [ブレイトンサイクルシミュレーター（NovaSolver）](https://novasolver.jp/tools/brayton-cycle.html)

## 4つの行程と熱効率

ブレイトンサイクルは ①断熱圧縮 ②定圧加熱 ③断熱膨張 ④定圧排熱 の 4 行程。理想気体の熱効率は次式です。

$$
\eta = 1 - \frac{1}{r_p^{(\gamma-1)/\gamma}},\qquad
\frac{T_2}{T_1} = \frac{T_3}{T_4} = r_p^{(\gamma-1)/\gamma}
$$

ここで $r_p = P_2/P_1$ は圧力比。指数が $(\gamma-1)/\gamma$ になる点がオットー（指数 $\gamma-1$）との違いです。

既定値 $r_p=12$、$\gamma=1.4$、$T_1=290\,\mathrm{K}$、$T_3=1500\,\mathrm{K}$ で計算すると、$r_p^{(\gamma-1)/\gamma} = 12^{0.2857} = 2.034$、**熱効率 $\eta = 50.8\%$**、圧縮機出口温度 $T_2 = 589.8\,\mathrm{K}$、タービン出口温度 $T_4 = 737.5\,\mathrm{K}$、正味仕事 $w_{net} = 465\,\mathrm{kJ/kg}$ になります。

圧力比を $r_p = 6 \to 20 \to 30$ と上げると効率は $40.1\% \to 57.5\% \to 62.2\%$ と向上します。ただし圧力比を上げすぎると正味仕事がやせ細る（圧縮機が食う仕事が増える）ため、実機にはタービン入口温度 $T_3$ との兼ね合いで最適圧力比が存在します。

![ブレイトンサイクルのT-s線図（左）と圧力比に対する効率（右）](/images/brayton-cycle/charts-closeup.png)

## JavaScript 実装

```javascript
const CP = 1.005;  // 空気の定圧比熱 [kJ/(kg·K)]
function brayton(rp, gamma, T1, T3) {
  const ex = (gamma - 1) / gamma;
  const rpex = Math.pow(rp, ex);   // rp^((γ-1)/γ)
  const T2 = T1 * rpex;            // 圧縮機出口
  const T4 = T3 / rpex;            // タービン出口
  const eta = 1 - 1 / rpex;       // 熱効率（rp,γ のみ）
  const qin = CP * (T3 - T2);      // 燃焼室の投入熱
  const wnet = qin * eta;          // 正味仕事
  return { eta, T2, T4, qin, wnet };
}
```

T-s 線図では、断熱（等エントロピー）の 1→2 と 3→4 が垂直線、定圧の 2→3 と 4→1 が等圧線（曲線）として現れ、囲む面積が正味仕事に対応します。

![T-s線図上を一周する状態点](/images/brayton-cycle/slider-anim.gif)

## ツールで遊ぶ

[ブレイトンサイクルシミュレーター](https://novasolver.jp/tools/brayton-cycle.html)で試してほしい操作：

- **圧力比 r_p スライダー**を上げ、「熱効率 η」が向上するのを確認
- **タービン入口温度 T₃ スライダー**を上げ、効率は変わらないのに**正味仕事**が増えるのを見る（効率は r_p,γ のみで決まる）
- **吸気温度 T₁ スライダー**で状態点温度のスケールを確認
- **比熱比 γ スライダー**で効率の依存性を見る
- **「圧力比をスイープ」ボタン**で効率カーブ上を動く点を観察
- **T-s 線図**で断熱（垂直）と定圧（曲線）の 4 行程を読む

## まとめ

- ブレイトンの熱効率は $\eta = 1 - 1/r_p^{(\gamma-1)/\gamma}$、圧力比と比熱比だけで決まる
- 既定値（r_p=12）で η=50.8%、正味仕事 465 kJ/kg
- 圧力比を上げると効率は向上（ただし正味仕事とのトレードオフ）
- 指数 $(\gamma-1)/\gamma$ がオットー（$\gamma-1$）との違い

ジェットエンジンの基礎を、圧力比とタービン入口温度を動かしながら体感してみてください。

✈️ **[ブレイトンサイクルシミュレーター（NovaSolver）](https://novasolver.jp/tools/brayton-cycle.html)** で、圧力比と効率の関係を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。熱力学では [オットーサイクル](https://novasolver.jp/tools/otto-cycle.html)、[ランキンサイクル](https://novasolver.jp/tools/rankine-cycle.html)、[カルノーサイクル](https://novasolver.jp/tools/carnot-cycle.html) もどうぞ。
