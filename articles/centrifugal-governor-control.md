---
title: "遠心調速機（ガバナー）の物理 — 回転数でフライボールが開く角度を計算する"
emoji: "🎛️"
type: "tech"
topics: ["javascript", "制御工学", "力学", "可視化", "数値計算"]
published: true
---

![遠心調速機（ガバナー） — NovaSolver](/images/centrifugal-governor/cover.png)

## 蒸気機関の速度を自動で一定に保つ仕掛け

ワットの蒸気機関を実用にした立役者が**遠心調速機（フライボール・ガバナー）**です。回転が速くなると遠心力で 2 個の鉄球が外へ開き、スリーブを押し上げて蒸気バルブを絞る――回転が速すぎれば自動で減速、遅すぎれば加速する**負のフィードバック制御**を、電子回路なしの純機械式で実現します。マクスウェルがこの安定性を解析したことが制御理論の出発点になりました。

この記事では、回転数に対するアーム角とボール半径を JavaScript で計算します。

🎛️ **動くデモ**: [遠心調速機シミュレーター（NovaSolver）](https://novasolver.jp/tools/centrifugal-governor.html)

## 円錐振り子としての釣り合い

回転するフライボールは、遠心力・重力・アーム張力が釣り合う円錐振り子です。アーム角 $\theta$（鉛直からの開き）は、ガバナー高さ $h$ を介して次式で決まります。

$$
h = \frac{m+M}{m}\cdot\frac{g}{\omega^2},\qquad \cos\theta = \frac{h}{L},\qquad \omega = \frac{2\pi n}{60}
$$

ここで $m$ はボール質量、$M$ はスリーブ荷重、$L$ はアーム長。ボールの回転半径は $r = L\sin\theta$、遠心力は $F_c = m\omega^2 r$ です。

既定値 $m=1.5\,\mathrm{kg}$、$M=4.0\,\mathrm{kg}$、$L=0.20\,\mathrm{m}$、$n=200\,\mathrm{rpm}$ で計算すると、$\omega = 20.94\,\mathrm{rad/s}$、$h = 82.0\,\mathrm{mm}$、**アーム角 $\theta = 65.8^\circ$**、回転半径 $r = 182.4\,\mathrm{mm}$、遠心力 $F_c = 120.0\,\mathrm{N}$ になります。

重要なのは**動作開始回転数**。$h = L$ となる $\omega_{\min} = \sqrt{\frac{m+M}{m}\cdot\frac{g}{L}}$ 以下ではボールが垂れ下がったまま（$\theta = 0$）。既定値では **128 rpm** を超えて初めてボールが開き始めます。

![アーム角（左）とボール回転半径（右）の回転数依存性](/images/centrifugal-governor/charts-closeup.png)

## JavaScript 実装

```javascript
function governorState(m, M, L, rpm) {
  const g = 9.81, omega = 2 * Math.PI * rpm / 60;
  const h = ((m + M) / m) * (g / (omega * omega));  // ガバナー高さ
  const theta = h >= L ? 0 : Math.acos(h / L);       // h≥L ならボールは垂れ下がり
  const r = L * Math.sin(theta);                     // 回転半径
  const Fc = m * omega * omega * r;                  // 遠心力
  return { omega, h, theta, r, Fc };
}
// 動作開始回転数（h=L のとき）
const omegaMin = Math.sqrt(((m + M) / m) * (9.81 / L));
const rpmLiftoff = omegaMin * 60 / (2 * Math.PI);    // 既定で 128 rpm
```

スリーブ荷重 $M$ を増やすと動作開始回転数が上がり、同じ回転数でもボールが開きにくくなります。これが「設定速度」の調整つまみに相当します。

![回転数を上げるとフライボールが開いていく様子](/images/centrifugal-governor/slider-anim.gif)

## ツールで遊ぶ

[遠心調速機シミュレーター](https://novasolver.jp/tools/centrifugal-governor.html)で試してほしい操作：

- **回転数スライダー**を上げ、「アーム角 θ」と「ボール回転半径」が増えるのを見る
- **回転数を動作開始値（既定 128 rpm）以下**にして、ボールが垂れ下がる（θ=0）のを確認
- **スリーブ荷重 M スライダー**を増やし、動作開始回転数が上がる（設定速度が変わる）のを観察
- **アーム長 L・ボール質量 m スライダー**で釣り合い角の変化を確認
- **アーム角／半径グラフ**で回転数に対する応答カーブを読む
- **アニメーション**でスリーブとバルブが連動する様子を見る

## まとめ

- ガバナーは円錐振り子の釣り合いで回転数を機械的に検出
- アーム角は $\cos\theta = h/L$、$h = \frac{m+M}{m}\frac{g}{\omega^2}$ で決まる
- 既定値（200 rpm）で θ=65.8°、半径 182 mm、遠心力 120 N
- 動作開始回転数 $\omega_{\min}$ 以下ではボールは開かない（既定 128 rpm）

純機械式フィードバック制御の名作を、パラメータを変えながら体感してみてください。

🎛️ **[遠心調速機シミュレーター（NovaSolver）](https://novasolver.jp/tools/centrifugal-governor.html)** で、回転と遠心力の釣り合いを確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。制御・力学系では [PID制御](https://novasolver.jp/tools/pid.html)、[ジャイロスコープ](https://novasolver.jp/tools/gyroscope.html)、[単振り子](https://novasolver.jp/tools/simple-pendulum.html) もどうぞ。
