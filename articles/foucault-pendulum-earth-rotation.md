---
title: "フーコーの振り子で地球の自転を測る — 歳差はΩ sin(緯度)、東京で約41.7時間/回転"
emoji: "🌍"
type: "tech"
topics: ["javascript", "物理シミュレーション", "力学", "可視化", "数値計算"]
published: true
---

![フーコーの振り子と地球自転 — NovaSolver](/images/foucault-pendulum/cover.png)

## 振り子だけで「地球は回っている」と証明する

1851 年、レオン・フーコーは長さ 67 m の巨大な振り子をパリのパンテオンに吊るしました。振り子はただ往復するだけ――なのに、その**振動面が時間とともにゆっくり回転**していきました。外から力を加えていないのに振動面が回るのは、振り子の下で**地球そのものが自転している**から。星を見るまでもなく、屋内の振り子だけで地球の自転を可視化した歴史的実験です。

この記事では、振動面の歳差速度を緯度の関数として JavaScript で計算します。

🌍 **動くデモ**: [フーコーの振り子シミュレーター（NovaSolver）](https://novasolver.jp/tools/foucault-pendulum.html)

## 歳差は緯度の正弦に比例する

振り子の振動面は、地球の自転角速度 $\Omega_\oplus$ のうち**鉛直成分だけ**を感じて歳差します。緯度 $\varphi$ における歳差角速度は次式です。

$$
\Omega_{\text{pre}} = \Omega_\oplus \sin|\varphi|,\qquad
\Omega_\oplus = \frac{2\pi}{86164.1\,\mathrm{s}} \approx 7.292\times10^{-5}\,\mathrm{rad/s}
$$

ここで分母の 86164.1 秒は**恒星日**（地球が星に対して 1 回転する時間）です。1 回転にかかる時間は $T_{\text{pre}} = 2\pi/\Omega_{\text{pre}}$。

東京（$\varphi = 35^\circ$）で計算すると、歳差角速度は **8.63°/時**、1 回転に **41.73 時間**かかります。緯度を上げるほど速くなり、**北極（$\varphi=90^\circ$）では 23.93 時間** ＝ ちょうど恒星日。逆に**赤道（$\varphi=0^\circ$）では $\sin 0 = 0$ なので歳差せず、振動面は回りません**。

振り子そのものの周期は重力に支配される別物で、$T_{\text{osc}} = 2\pi\sqrt{L/g}$。長さ 20 m なら 8.97 秒です。

![振動面の歳差（左, 北半球で時計回り）と緯度別の歳差角の時間変化（右）](/images/foucault-pendulum/charts-closeup.png)

## JavaScript 実装

歳差は解析式そのままで計算できます。

```javascript
const SIDEREAL_DAY = 86164.1;                 // 恒星日 [s]
const OMEGA_EARTH = 2 * Math.PI / SIDEREAL_DAY; // 7.292e-5 rad/s

function precession(latDeg, L, g, tHours) {
  const Tosc = 2 * Math.PI * Math.sqrt(L / g);          // 振り子の周期 [s]
  const omega = OMEGA_EARTH * Math.sin(Math.abs(latDeg) * Math.PI / 180);
  const Tpre = omega > 0 ? (2 * Math.PI / omega) : Infinity;  // 1回転 [s]
  const degPerHour = omega * 180 / Math.PI * 3600;       // 歳差速度 [°/h]
  const dTheta = degPerHour * tHours;                    // 経過時間での歳差角 [°]
  return { Tosc, Tpre, degPerHour, dTheta };
}
// 例: 東京 lat=35, L=20, g=9.81, t=6h → degPerHour≈8.63, Tpre≈41.73h
```

北半球では振動面は上から見て**時計回り**に、南半球では**反時計回り**に回ります（符号が反転）。6 時間後の歳差角は東京で **51.8°** になります。

![上から見た振動面が時計回りに歳差していく様子（北半球）](/images/foucault-pendulum/slider-anim.gif)

## ツールで遊ぶ

[フーコーの振り子シミュレーター](https://novasolver.jp/tools/foucault-pendulum.html)で試してほしい操作：

- **緯度 φ スライダー**を変え、「歳差角速度」と「一回転に要する時間」がどう変わるか観察
- 緯度を **0°（赤道）**にして歳差が止まる（「∞ (赤道)」表示）のを確認
- 緯度を **±90°（極）**にして 1 回転が恒星日（約 23.93 時間）になるのを確認
- **「時間をスイープ」ボタン**で経過時間を進め、振動面（コンパス図）が回るのを見る
- **緯度比較グラフ**で、赤道・中緯度・極の歳差角 $\Delta\theta(t)$ の傾きの違いを読む
- **振り子長さ L スライダー**を変え、振動周期 $T_{\text{osc}} = 2\pi\sqrt{L/g}$ が歳差とは独立であることを確認

## まとめ

- フーコーの振り子は屋内で地球の自転を可視化する実験
- 歳差角速度は $\Omega_{\text{pre}} = \Omega_\oplus \sin|\varphi|$（緯度の正弦に比例）
- 東京（35°）で 1 回転 41.73 時間、極で恒星日、赤道では回らない
- 振り子の周期 $T_{\text{osc}} = 2\pi\sqrt{L/g}$ は歳差とは独立

緯度を変えて、歳差が「止まる赤道」から「最速の極」まで連続的に変わる様子を体感してみてください。

🌍 **[フーコーの振り子シミュレーター（NovaSolver）](https://novasolver.jp/tools/foucault-pendulum.html)** で、振り子に映る地球の自転を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。回転・力学系では [コリオリの力](https://novasolver.jp/tools/coriolis-effect.html)、[ジャイロスコープ](https://novasolver.jp/tools/gyroscope.html)、[単振り子](https://novasolver.jp/tools/simple-pendulum.html) もどうぞ。
