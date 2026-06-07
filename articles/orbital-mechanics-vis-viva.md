---
title: "vis-viva方程式で軌道速度を解く — ケプラー方程式とニュートン法をJavaScriptで"
emoji: "🛰️"
type: "tech"
topics: ["javascript", "物理シミュレーション", "天体力学", "数値計算", "可視化"]
published: false
---

![軌道力学とvis-viva方程式 — NovaSolver](/images/orbital-mechanics/cover.png)

## 衛星は近地点で速く、遠地点で遅い

人工衛星は楕円軌道の上を、いつも同じ速さで回っているわけではありません。地球に最も近い**近地点**で最速、最も遠い**遠地点**で最遅になります。この速さを軌道の任意の点で与えるのが **vis-viva 方程式**です。さらに「今どこにいるか」を時間から求めるには、超越方程式である**ケプラー方程式**をニュートン法で解く必要があります。

この記事では、楕円軌道の速度と位置を JavaScript で計算します。

🛰️ **動くデモ**: [軌道力学シミュレーター（NovaSolver）](https://novasolver.jp/tools/orbital-mechanics.html)

## vis-viva 方程式とケプラーの第3法則

中心天体の重力パラメータを $\mu = GM$、軌道長半径を $a$ とすると、距離 $r$ における軌道速度は次式で与えられます。

$$
v = \sqrt{\mu\left(\frac{2}{r} - \frac{1}{a}\right)}
$$

周期はケプラーの第3法則そのものです。

$$
T = 2\pi\sqrt{\frac{a^3}{\mu}}
$$

地球は $\mu = 3.986\times10^{14}\,\mathrm{m^3/s^2}$。たとえば長半径 $a = 20000\,\mathrm{km}$、離心率 $e = 0.30$ の楕円軌道では、近地点距離 $r_p = a(1-e) = 14000\,\mathrm{km}$、遠地点距離 $r_a = a(1+e) = 26000\,\mathrm{km}$。vis-viva に代入すると近地点速度 **6.08 km/s**、遠地点速度 **3.28 km/s** と、近地点のほうが約 1.86 倍速いと分かります。

GPS 衛星（$a = 26560\,\mathrm{km}$）なら周期は $T = 11.97\,\mathrm{h}$、静止衛星（GEO, $a = 42164\,\mathrm{km}$）なら $T = 23.93\,\mathrm{h}$ ＝ ほぼ恒星日と一致し、地表から見て止まって見えるわけです。

![楕円軌道（左）と vis-viva による速度プロファイル（右）](/images/orbital-mechanics/charts-closeup.png)

## ケプラー方程式をニュートン法で解く

時刻に比例する平均近点角 $M$ から、実際の位置（離心近点角 $E$）を求めるには、次の超越方程式を解きます。

$$
M = E - e\sin E
$$

解析的には解けないので、ニュートン・ラフソン法で反復します。

```javascript
function solveKepler(M, e) {
  let E = M;                                  // 初期値は M
  for (let i = 0; i < 50; i++) {
    const dE = (M - E + e*Math.sin(E)) / (1 - e*Math.cos(E));
    E += dE;
    if (Math.abs(dE) < 1e-10) break;          // 収束したら終了
  }
  return E;
}
// 離心近点角 E から真近点角 ν（実際の方位）へ変換
function trueAnomaly(E, e) {
  return 2*Math.atan2(Math.sqrt(1+e)*Math.sin(E/2), Math.sqrt(1-e)*Math.cos(E/2));
}
// vis-viva と周期
const T  = 2*Math.PI*Math.sqrt(a*a*a / MU);
const vp = Math.sqrt(MU*(2/(a*(1-e)) - 1/a));   // 近地点速度
const va = Math.sqrt(MU*(2/(a*(1+e)) - 1/a));   // 遠地点速度
```

ニュートン法は二次収束するので、$e \le 0.7$ 程度なら数回の反復で機械精度に到達します。

![ケプラー運動：近地点で速く、遠地点で遅く動く衛星](/images/orbital-mechanics/slider-anim.gif)

## ツールで遊ぶ

[軌道力学シミュレーター](https://novasolver.jp/tools/orbital-mechanics.html)で試してほしい操作：

- **離心率 e スライダー**を上げ、軌道が円から細長い楕円へ変わり、近地点・遠地点速度の差が広がるのを見る
- **半長軸 a スライダー**を変え、「周期 T」が $a^{3/2}$ で伸びる（ケプラーの第3法則）ことを確認
- **「GEO」プリセット**で周期がほぼ 24 時間（静止軌道）になることを確認
- **「ISS」「GPS」「モルニヤ」プリセット**で実在軌道の周期・高度・速度を読む
- **計算結果**で「周期 T」「近地点／遠地点高度」「近地点／遠地点速度」「真近点角 ν」を確認

> 補足：既定値（$a = 8000\,\mathrm{km}$, $e = 0.30$）は近地点が地表より低くなる設定なので、現実の軌道を見るときは上のプリセットを使うのがおすすめです。

## まとめ

- 軌道速度は vis-viva $v = \sqrt{\mu(2/r - 1/a)}$ で任意の点で求まる
- 周期はケプラーの第3法則 $T = 2\pi\sqrt{a^3/\mu}$
- 時刻から位置を出すにはケプラー方程式 $M = E - e\sin E$ をニュートン法で解く
- GEO の周期はほぼ恒星日（23.93 h）＝静止軌道の正体

軌道設計の出発点となるこれらの式を、離心率や長半径を変えながら体感してみてください。

🛰️ **[軌道力学シミュレーター（NovaSolver）](https://novasolver.jp/tools/orbital-mechanics.html)** で、楕円軌道の速度と周期を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。天体力学では [ケプラー軌道](https://novasolver.jp/tools/kepler-orbit.html)、[ホーマン遷移軌道](https://novasolver.jp/tools/hohmann-transfer.html)、[N体重力](https://novasolver.jp/tools/n-body-gravity.html) もどうぞ。
