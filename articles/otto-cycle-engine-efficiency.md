---
title: "オットーサイクルの熱効率は圧縮比だけで決まる — η=1−1/r^(γ−1)をJavaScriptで"
emoji: "🚗"
type: "tech"
topics: ["javascript", "熱力学", "CAE", "可視化", "数値計算"]
published: false
---

![オットーサイクル（ガソリン機関） — NovaSolver](/images/otto-cycle/cover.png)

## ガソリンエンジンの効率を決める、たった一つの数

自動車のガソリンエンジンを理想化したのが**オットーサイクル**です。驚くべきことに、その理論熱効率は燃料の量にも温度にもよらず、**圧縮比 $r$ と比熱比 $\gamma$ だけ**で決まります。「圧縮比を上げると効率が上がる」とよく言われる根拠が、この一本の式に凝縮されています。

この記事では、オットーサイクルの効率と P-V 線図上の状態点を JavaScript で計算します。

🚗 **動くデモ**: [オットーサイクルシミュレーター（NovaSolver）](https://novasolver.jp/tools/otto-cycle.html)

## 4つの行程と熱効率

オットーサイクルは 4 つの行程からなります：①断熱圧縮 ②定積加熱（燃焼） ③断熱膨張 ④定積排熱。理想気体（空気標準サイクル）の熱効率は次式です。

$$
\eta = 1 - \frac{1}{r^{\gamma-1}}
$$

ここで $r = V_1/V_2$ は圧縮比、$\gamma$ は比熱比（空気で約 1.4）。状態点の温度は

$$
T_2 = T_1\,r^{\gamma-1},\qquad T_3 = T_2 + \frac{Q_{in}}{c_v},\qquad c_v = \frac{R}{\gamma-1}
$$

既定値 $r=9$、$\gamma=1.4$、$T_1=300\,\mathrm{K}$、$Q_{in}=1500\,\mathrm{kJ/kg}$ で計算すると、$r^{\gamma-1} = 9^{0.4} = 2.408$、**熱効率 $\eta = 58.5\%$**、$T_2 = 722.5\,\mathrm{K}$、燃焼後温度 $T_3 = 2813\,\mathrm{K}$、正味仕事 $w_{net} = \eta Q_{in} = 877\,\mathrm{kJ/kg}$ になります。

圧縮比を $r=6 \to 12 \to 16$ と上げると効率は $51.2\% \to 63.0\% \to 67.0\%$ と単調に向上します。ただし実機では圧縮比を上げすぎるとノッキング（異常燃焼）が起きるため、ガソリン機関の圧縮比は 10 前後に制限されます。

![オットーサイクルのP-V線図（左）と圧縮比に対する効率（右）](/images/otto-cycle/charts-closeup.png)

## JavaScript 実装

```javascript
const R = 0.287;  // 空気の気体定数 [kJ/(kg·K)]
function otto(r, gamma, T1, Qin) {
  const cv = R / (gamma - 1);
  const rgm1 = Math.pow(r, gamma - 1);   // r^(γ-1)
  const T2 = T1 * rgm1;                   // 断熱圧縮後
  const T3 = T2 + Qin / cv;              // 定積加熱後
  const T4 = T3 / rgm1;                  // 断熱膨張後
  const eta = 1 - 1 / rgm1;             // 熱効率（r,γ のみで決まる）
  const wnet = eta * Qin;               // 正味仕事
  return { eta, T2, T3, T4, wnet };
}
// P-V 状態点（P1=1, v1=1 で正規化）
const v2 = 1 / r, P2 = Math.pow(r, gamma);          // 断熱圧縮 PV^γ=const
const P3 = P2 * (T3 / T2);                          // 定積加熱 P/T=const
const P4 = P3 * Math.pow(v2 / 1, gamma);            // 断熱膨張
```

P-V 線図で 4 つの状態点が囲む面積が、1 サイクルの正味仕事に対応します。

![P-V線図上を一周する状態点。囲む面積が正味仕事](/images/otto-cycle/slider-anim.gif)

## ツールで遊ぶ

[オットーサイクルシミュレーター](https://novasolver.jp/tools/otto-cycle.html)で試してほしい操作：

- **圧縮比 r スライダー**を上げ、「熱効率 η」が単調に増えるのを確認
- **比熱比 γ スライダー**を変え、効率が γ にも依存することを見る
- **加熱量 Q_in スライダー**を変え、効率は変わらないのに**燃焼後温度 T₃ と正味仕事**が動くことを確認（効率は r,γ のみで決まる）
- **吸入温度 T₁ スライダー**で状態点の温度がスケールする様子を見る
- **「圧縮比をスイープ」ボタン**で効率カーブ上を動く点を観察
- **P-V 線図**で 4 行程と囲む面積（仕事）を読む

## まとめ

- オットーサイクルの熱効率は $\eta = 1 - 1/r^{\gamma-1}$、圧縮比と比熱比だけで決まる
- 既定値（r=9）で η=58.5%、燃焼後温度 2813 K、正味仕事 877 kJ/kg
- 圧縮比を上げると効率は単調向上（ただし実機はノッキングで制限）
- 加熱量を変えても効率は不変（温度と仕事だけが変わる）

ガソリンエンジンの心臓部を、圧縮比を動かしながら体感してみてください。

🚗 **[オットーサイクルシミュレーター（NovaSolver）](https://novasolver.jp/tools/otto-cycle.html)** で、圧縮比と効率の関係を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。熱力学では [カルノーサイクル](https://novasolver.jp/tools/carnot-cycle.html)、[ディーゼルサイクル](https://novasolver.jp/tools/diesel-cycle.html)、[ブレイトンサイクル](https://novasolver.jp/tools/brayton-cycle.html) もどうぞ。
