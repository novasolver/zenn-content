---
title: "放物運動 — 射程が最大になる角度はなぜ45°なのか"
emoji: "🎯"
type: "tech"
topics: ["javascript", "物理シミュレーション", "力学", "可視化", "数値計算"]
published: false
---

![放物運動と射程 — NovaSolver](/images/projectile-motion/cover.png)

## ボールを一番遠くへ投げる角度

ボールを投げる、砲弾を撃つ、ホースで水を飛ばす——重力だけを受けて飛ぶ物体は**放物線**を描きます。では「最も遠くへ飛ばす発射角」は何度でしょうか。答えは**45°**。なぜ 45° なのか、月や火星ではどう変わるのかを、放物運動の式とともに見ていきます。

🎯 **動くデモ**: [放物運動シミュレーター（NovaSolver）](https://novasolver.jp/tools/projectile-motion.html)

## 放物運動の式

水平・鉛直に分解すると、水平方向は等速、鉛直方向は等加速度（重力）です。発射高度 $h_0=0$ なら

$$
x(t) = v_0\cos\theta\cdot t,\qquad
y(t) = v_0\sin\theta\cdot t - \tfrac12 g t^2
$$

着地時間 $T = 2v_0\sin\theta/g$、最高点 $H = v_0^2\sin^2\theta/(2g)$、そして**射程**は

$$
R = \frac{v_0^2\sin(2\theta)}{g}
$$

$\sin(2\theta)$ は $2\theta = 90°$、つまり **$\theta = 45°$ で最大**になります。これが「45°が最も飛ぶ」の正体です。ツールの既定値（$v_0=30\,\mathrm{m/s}$、$\theta=45°$、$g=9.81$）で計算すると $R=91.7\,\mathrm{m}$、$H=22.9\,\mathrm{m}$、$T=4.32\,\mathrm{s}$ になります。

![発射角ごとの弾道と、射程が45°で最大になる様子](/images/projectile-motion/charts-closeup.png)

## 余角は同じ距離に落ちる

$\sin(2\theta)$ の性質から、**互いに余角（足して90°）になる2つの角度は同じ射程**になります。たとえば 30° と 60°、15° と 75° は同じ距離に着弾します（上図で 30° と 60° の弾道が同じ地点に落ちているのが見えます）。違うのは弾道の高さと滞空時間——60° は高く打ち上がって長く飛び、30° は低く速く飛びます。

## 重力が変われば射程も変わる

射程は重力 $g$ に反比例します。月（$g=1.62$）では同じ初速で

$$
R_{\text{moon}} = \frac{30^2\times\sin90°}{1.62} = 555.6\,\mathrm{m}
$$

と地球の約 6 倍飛びます。火星（$g=3.72$）なら約 242 m。低重力ほど物体は遠くまで飛ぶのです。

## JavaScript 実装

理想弾道は解析式そのまま、空気抵抗を入れる場合は数値積分します。ツールは速度に比例する抗力モデルを微小時間ステップで解きます。

```javascript
function computeTrajectory(p) {
  const { v0, theta, h0, g, cd } = p;
  const dt = 0.005; const pts = [];
  let x = 0, y = h0, vx = v0*Math.cos(theta), vy = v0*Math.sin(theta);
  while (y >= 0) {
    pts.push({ x, y, vx, vy });
    const v = Math.hypot(vx, vy);
    vx += (-cd * v * vx) * dt;          // 空気抵抗（速度に依存）
    vy += (-g - cd * v * vy) * dt;      // 重力 + 抵抗
    x += vx * dt; y += vy * dt;
  }
  return pts;
}
```

空気抵抗を入れると最適角は 45° より小さく（典型的に 30〜40°）なり、弾道は前のめりに歪みます。

![発射角を変えると射程が変わり、45°で最大になる](/images/projectile-motion/slider-anim.gif)

## ツールで遊ぶ

[放物運動シミュレーター](https://novasolver.jp/tools/projectile-motion.html)で試してほしい操作：

- **発射角 θ スライダー**を動かし、**飛距離 R** が 45° で最大になることを確認
- **30° と 60°**（余角）で射程が同じになることを試す
- **プリセット**「地球」「月」「火星」を切り替え、重力で射程が変わるのを見る（月で約6倍）
- **空気抵抗 ON/OFF** を切り替え、最適角が 45° より小さくなり弾道が歪むことを観察
- **初速度 v₀ スライダー**を上げ、射程が $v_0^2$ で増える（速度2倍で射程4倍）ことを確認
- **発射高度 h スライダー**を上げると、最適角が 45° より小さくなることを見る
- **計算結果**（飛距離・最高点・飛行時間・着地速度）を読み取る

## まとめ

- 射程は $R = v_0^2\sin(2\theta)/g$。$\sin(2\theta)$ が最大の **θ=45°**（高度 0・抵抗なし）で最遠
- 余角（30°と60°など）は同じ射程。高さと滞空時間だけが異なる
- 射程は $v_0^2$ に比例、$g$ に反比例（月で約6倍）
- 空気抵抗を入れると最適角は小さくなり弾道が前傾する

弾道学・スポーツ・宇宙物理の基礎となる放物運動を、角度と重力を変えながら体感してみてください。

🎯 **[放物運動シミュレーター（NovaSolver）](https://novasolver.jp/tools/projectile-motion.html)** で、一番遠くへ飛ばす角度を自分の手で見つけましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。力学系では [1次元衝突](https://novasolver.jp/tools/collision-1d.html)、[ケプラー軌道](https://novasolver.jp/tools/kepler-orbit.html)、[ニュートンのゆりかご](https://novasolver.jp/tools/newtons-cradle.html) なども揃えています。
