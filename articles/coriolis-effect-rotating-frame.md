---
title: "コリオリの力はなぜ「見かけの力」なのか — 慣性系と回転系をJavaScriptで比べる"
emoji: "🌀"
type: "tech"
topics: ["javascript", "物理シミュレーション", "力学", "可視化", "数値計算"]
published: false
---

![コリオリの力と回転系 — NovaSolver](/images/coriolis-effect/cover.png)

## まっすぐ進んだはずなのに、なぜ曲がる

台風が渦を巻き、北半球の低気圧が反時計回りに回る原因が**コリオリの力**です。けれどコリオリの力は重力や摩擦のような「本物の力」ではありません。**回転する座標系から世界を眺めたときにだけ現れる、見かけの力**です。慣性系（静止した観測者）から見れば、物体はまっすぐ等速で進んでいるだけ。それを回転する観測者が見ると、軌道が曲がって見えるのです。

この記事では、慣性系と回転系の軌道を JavaScript で並べて描き、コリオリ偏向の正体を確かめます。

🌀 **動くデモ**: [コリオリの力シミュレーター（NovaSolver）](https://novasolver.jp/tools/coriolis-effect.html)

## 回転系に現れる見かけの力

角速度 $\vec{\Omega}$ で回転する座標系では、実際の加速度に加えて 2 つの見かけの加速度が現れます。

$$
\vec{a}_{\text{app}} = \vec{a}_{\text{real}} - 2\vec{\Omega}\times\vec{v} - \vec{\Omega}\times(\vec{\Omega}\times\vec{r})
$$

第2項が**コリオリ加速度** $\vec{a}_{\text{Cor}} = -2\vec{\Omega}\times\vec{v}$、第3項が**遠心加速度**です。2 次元の回転（$\vec\Omega$ が面に垂直）では外積はスカラー倍に簡約され、コリオリ加速度は常に速度に直交します。だから速度の大きさは変えず、進行方向だけを曲げます。

北半球（$\Omega > 0$）では進行方向の**右**へ、南半球では**左**へ偏向します。

![慣性系の直線（左）と、回転系での曲がった軌跡（右）](/images/coriolis-effect/charts-closeup.png)

## JavaScript 実装：慣性系で解いて回転系へ変換

最もすっきりした実装は「慣性系で等速直線運動を解き、座標を回転変換して回転系の軌跡を得る」方法です。これは数学的に、回転系でコリオリ＋遠心力を積分したものと完全に一致します。

```javascript
// 慣性系：力が無いのでまっすぐ進む
ix += ivx * dt;
iy += ivy * dt;
// 回転系の位置 = 慣性系の位置を -Ωt だけ回す
frameAngle += omega * dt;
const c = Math.cos(-sign * frameAngle), s = Math.sin(-sign * frameAngle);
const rx = ix * c - iy * s;
const ry = ix * s + iy * c;
// 表示用コリオリ加速度 a_Cor = -2Ω × v（速度に直交）
const corX =  2 * omega * sign * vy_r;
const corY = -2 * omega * sign * vx_r;
```

回転角は時間に比例して $\Delta\theta = \Omega\,t$ だけ進みます。たとえば $\Omega = 1\,\mathrm{rad/s}$ で 2 秒後には、慣性系の直線に対して回転系の軌跡は **114.6° 回転**して見えます（$= \Omega t$ をラジアンから度に直した値）。北半球では時計回り（右偏向）、南半球では反時計回り（左偏向）と、符号だけが反転します。

![回転系で見た粒子の曲がった軌跡（北半球）](/images/coriolis-effect/slider-anim.gif)

## ツールで遊ぶ

[コリオリの力シミュレーター](https://novasolver.jp/tools/coriolis-effect.html)で試してほしい操作：

- **慣性系（左）と回転系（右）の分割表示**で、同じ運動が「直線」と「曲線」に見える違いを比較
- **角速度 Ω スライダー**を上げ、偏向（曲がり）が強くなるのを見る
- **半球選択**を北→南に切り替え、偏向の向きが右↔左で逆転するのを確認
- **「北半球の台風」「南半球の台風」プリセット**で渦の回転方向の違いを再現
- **計算結果**で「コリオリ加速度」「偏向角」「経過時間」を読む
- **力ベクトル表示**で、コリオリ力が常に速度に直交していることを確認

## まとめ

- コリオリの力は回転系でのみ現れる見かけの力 $\vec{a}_{\text{Cor}} = -2\vec{\Omega}\times\vec{v}$
- 速度に直交するため、速さは変えず進行方向だけを曲げる
- 北半球は右、南半球は左へ偏向（符号が反転するだけ）
- 慣性系で直線運動を解き座標回転すれば、回転系の曲線軌道が得られる

「力が無いのに曲がる」不思議を、慣性系と回転系を見比べて納得してみてください。

🌀 **[コリオリの力シミュレーター（NovaSolver）](https://novasolver.jp/tools/coriolis-effect.html)** で、見かけの力の正体を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。回転・力学系では [フーコーの振り子](https://novasolver.jp/tools/foucault-pendulum.html)、[ジャイロスコープ](https://novasolver.jp/tools/gyroscope.html)、[単振り子](https://novasolver.jp/tools/simple-pendulum.html) もどうぞ。
