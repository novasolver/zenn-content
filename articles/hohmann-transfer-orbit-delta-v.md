---
title: "ホーマン遷移軌道のΔvをJavaScriptで計算する — LEOからGEOまで何km/s？"
emoji: "🚀"
type: "tech"
topics: ["javascript", "物理シミュレーション", "天体力学", "数値計算", "可視化"]
published: true
---

![ホーマン遷移軌道 — NovaSolver](/images/hohmann-transfer/cover.png)

## 低軌道から静止軌道へ、最も燃料が少ない乗り換え

人工衛星を低い円軌道（LEO）から高い円軌道（GEO）へ移すとき、エンジンを噴かし続ける必要はありません。**2 回だけ加速・減速**して、その間を楕円軌道で「滑空」するのが、燃料効率の良い **ホーマン遷移**です。必要な速度変化 $\Delta v$ は、ロケットの燃料（＝ペイロード）を決める最重要量です。

この記事では、ホーマン遷移の $\Delta v$ と遷移時間を JavaScript で計算します。

🚀 **動くデモ**: [ホーマン遷移シミュレーター（NovaSolver）](https://novasolver.jp/tools/hohmann-transfer.html)

## 2回の噴射と遷移楕円

半径 $r_1$ の円軌道から半径 $r_2$ の円軌道へ移るとき、両者に接する楕円（半長軸 $a = (r_1+r_2)/2$）を経由します。出発時の加速 $\Delta v_1$ と到着時の加速 $\Delta v_2$ は次式です。

$$
\Delta v_1 = \sqrt{\frac{\mu}{r_1}}\left(\sqrt{\frac{2 r_2}{r_1+r_2}} - 1\right),\qquad
\Delta v_2 = \sqrt{\frac{\mu}{r_2}}\left(1 - \sqrt{\frac{2 r_1}{r_1+r_2}}\right)
$$

遷移時間は遷移楕円の半周期です。

$$
t_{\mathrm{tx}} = \pi\sqrt{\frac{a^3}{\mu}}
$$

地球（$\mu = 398600\,\mathrm{km^3/s^2}$, $R = 6378\,\mathrm{km}$）で、LEO（高度 400 km）から GEO（高度 35800 km）へ向かう既定シナリオを計算すると、$\Delta v_1 = 2.398\,\mathrm{km/s}$、$\Delta v_2 = 1.456\,\mathrm{km/s}$、**合計 $\Delta v = 3.854\,\mathrm{km/s}$**。遷移時間は **5.29 時間**になります。実際の静止衛星打ち上げで語られる「約 3.9 km/s」とぴたり一致します。

![遷移軌道の幾何（左）と、半径比に対する無次元Δv（右）](/images/hohmann-transfer/charts-closeup.png)

## JavaScript 実装

公式をそのまま実装します。式は小さい方の半径を $r_1$ として扱うと安全です。

```javascript
function computeHohmann(r1, r2, mu) {
  const rs = Math.min(r1, r2), rl = Math.max(r1, r2);
  const v1c = Math.sqrt(mu / rs);                          // 出発円軌道の速度
  const v2c = Math.sqrt(mu / rl);                          // 目的円軌道の速度
  const dv1 = v1c * (Math.sqrt(2*rl/(rs+rl)) - 1);         // 第1噴射（加速）
  const dv2 = v2c * (1 - Math.sqrt(2*rs/(rs+rl)));         // 第2噴射（加速）
  const a_tx = (rs + rl) / 2;                              // 遷移楕円の半長軸
  const t_tx = Math.PI * Math.sqrt(a_tx*a_tx*a_tx / mu);   // 半周期＝遷移時間
  return { dv1, dv2, dv_total: dv1 + dv2, t_tx };
}
```

## 高く上げるほど損？ Δvが最大になる半径比

面白いのは、**遠くへ行くほど $\Delta v$ が増え続けるわけではない**点です。無次元化した合計 $\Delta v / \sqrt{\mu/r_1}$ を半径比 $R = r_2/r_1$ の関数として見ると、$R \approx 15.58$ で最大値 **0.536** に達し、それより遠い軌道では逆にわずかに減ります（無限遠で再び減少）。これがホーマンより双楕円遷移が有利になる領域の目印です。LEO→GEO は $R \approx 6.2$ で、まだ右肩上がりの途中にあります。

![遷移楕円に沿って内側から外側の軌道へ乗り換える宇宙機](/images/hohmann-transfer/slider-anim.gif)

## ツールで遊ぶ

[ホーマン遷移シミュレーター](https://novasolver.jp/tools/hohmann-transfer.html)で試してほしい操作：

- **出発高度 h1・目的高度 h2 スライダー**を変え、「Δv1」「Δv2」「合計 Δv」がどう動くか観察
- **「h2 をスイープ」ボタン**で目的高度を自動で上げ、効率曲線上を現在位置マーカーが動くのを見る
- **中心天体 GM スライダー**を月や火星相当に変え、必要 Δv が変わることを確認
- **効率曲線**で、半径比 $R \approx 15.6$ のピーク（白丸）と現在の半径比（黄丸）の位置関係を読む
- **遷移時間 t_tx** が半長軸の $a^{3/2}$ で伸びることを確認

## まとめ

- ホーマン遷移は 2 回の噴射で円軌道間を乗り換える最小燃料に近い方法
- LEO（400 km）→GEO（35800 km）は合計 $\Delta v = 3.85\,\mathrm{km/s}$、遷移時間 5.29 時間
- 無次元 $\Delta v$ は半径比 $R \approx 15.58$ で最大（0.536）
- $t_{\mathrm{tx}} = \pi\sqrt{a^3/\mu}$ で遷移時間が決まる

ミッション設計の第一歩となる $\Delta v$ 計算を、出発・目的高度を変えながら体感してみてください。

🚀 **[ホーマン遷移シミュレーター（NovaSolver）](https://novasolver.jp/tools/hohmann-transfer.html)** で、軌道乗り換えのコストを確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。天体力学では [軌道力学（vis-viva）](https://novasolver.jp/tools/orbital-mechanics.html)、[ケプラー軌道](https://novasolver.jp/tools/kepler-orbit.html)、[脱出速度](https://novasolver.jp/tools/escape-velocity.html) もどうぞ。
