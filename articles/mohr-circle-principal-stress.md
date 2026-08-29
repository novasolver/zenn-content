---
title: "モールの応力円 — 主応力と最大せん断応力を「円」で読む"
emoji: "⭕"
type: "tech"
topics: ["javascript", "構造力学", "材料力学", "可視化", "数値計算"]
published: true
---

![モールの応力円と主応力 — NovaSolver](/images/mohr-circle/cover.png)

## 同じ応力状態でも、見る向きで値が変わる

材料のある点に働く応力 $\sigma_x,\ \sigma_y,\ \tau_{xy}$ は、**面の向きを変えると別の値**になります。45° 傾けた面では垂直応力もせん断応力も違う。では「最も大きい垂直応力（主応力）」や「最も大きいせん断応力」はいくつで、どの向きの面に現れるのか——これを一目で読み取れる図が、19 世紀の技師 Otto Mohr が考案した**モールの応力円**です。

破壊や降伏は主応力・最大せん断応力で起きるため、強度設計では必ず登場します。この記事では応力変換の式を導き、JavaScript でモール円を描いて主応力を求めます。

⭕ **動くデモ**: [モールの応力円ツール（NovaSolver）](https://novasolver.jp/tools/mohr-circle.html)

## 応力変換と主応力

面を角度 $\theta$ 回転させたときの垂直応力・せん断応力は、

$$
\sigma(\theta) = \frac{\sigma_x+\sigma_y}{2} + \frac{\sigma_x-\sigma_y}{2}\cos2\theta + \tau_{xy}\sin2\theta
$$

$$
\tau(\theta) = -\frac{\sigma_x-\sigma_y}{2}\sin2\theta + \tau_{xy}\cos2\theta
$$

この $(\sigma,\tau)$ を平面にプロットすると、$\theta$ を変えるにつれて点は**円**を描きます。これがモール円です。円の中心と半径は

$$
C = \frac{\sigma_x+\sigma_y}{2},\qquad
R = \sqrt{\left(\frac{\sigma_x-\sigma_y}{2}\right)^2 + \tau_{xy}^2}
$$

主応力（せん断が 0 になる向きの垂直応力）と最大せん断応力は、円の幾何から即座に読めます。

$$
\sigma_{1,2} = C \pm R,\qquad \tau_{\max} = R,\qquad \tan2\theta_p = \frac{2\tau_{xy}}{\sigma_x-\sigma_y}
$$

## 実際に読んでみる

ツールの既定値（$\sigma_x=80$、$\sigma_y=-40$、$\tau_{xy}=60\,\mathrm{MPa}$）で計算します。中心 $C=20$、半径

$$
R = \sqrt{\left(\frac{80-(-40)}{2}\right)^2 + 60^2} = \sqrt{60^2+60^2} = 84.85\,\mathrm{MPa}
$$

したがって主応力 $\sigma_1 = 104.85$、$\sigma_2 = -64.85\,\mathrm{MPa}$、最大せん断応力 $\tau_{\max}=84.85\,\mathrm{MPa}$、主応力方向 $\theta_p = 22.5°$。

![モール円（左）と、面を回したときの応力変化（右）](/images/mohr-circle/charts-closeup.png)

左図のモール円で、点 A $(\sigma_x,\tau_{xy})$ と点 B $(\sigma_y,-\tau_{xy})$ は円の**直径の両端**にあります。円が σ 軸と交わる2点が主応力 $\sigma_1,\sigma_2$、円の最上点が最大せん断応力 $\tau_{\max}$。右図は面の回転角に対する $\sigma,\tau$ の変化で、$\theta_p=22.5°$ で**せん断がゼロ**＝主応力面になることがわかります。

## モール円の幾何が教えること

モール円からは重要な事実が読み取れます。

- **最大せん断応力の面は、主応力面から 45° 傾いた向き**（円上で $\tau_{\max}$ は主応力点から 90°、実空間では 45°）に現れる
- $\tau_{\max} = (\sigma_1-\sigma_2)/2$。主応力の差が大きいほどせん断も大きい
- 静水圧状態（$\sigma_x=\sigma_y$、$\tau_{xy}=0$）では円が点に縮み、どの向きでもせん断ゼロ

延性材料はせん断で降伏する（トレスカ／ミーゼス基準）ため、$\tau_{\max}$ が設計の鍵になります。

## JavaScript 実装

主応力の計算はわずか数行です。

```javascript
const C = (sx + sy) / 2;
const R = Math.sqrt(Math.pow((sx - sy)/2, 2) + txy*txy);
const s1 = C + R, s2 = C - R;           // 主応力
const tmax = R;                          // 最大せん断応力
const theta_p = 0.5 * Math.atan2(2*txy, sx - sy) * 180/Math.PI;  // 主応力角
// 円: 中心(C,0)、半径R を σ-τ 平面に描画
```

![面を回すと応力点が円周上を2θ動く](/images/mohr-circle/slider-anim.gif)

## ツールで遊ぶ

[モールの応力円ツール](https://novasolver.jp/tools/mohr-circle.html)で試してほしい操作：

- **σx・σy・τxy スライダー**を動かし、モール円の中心と半径が変わる様子を見る
- **計算結果**で「主応力 σ₁・σ₂」「最大せん断 τmax」「主応力角 θp」を読む
- **τxy を 0** にすると、$\sigma_x,\sigma_y$ がそのまま主応力になる（円が σ 軸上に乗る）ことを確認
- **σx = σy** かつ **τxy = 0** で円が点に縮む（どの向きもせん断ゼロ）静水圧状態を試す
- **「応力状態アニメーション」**をオンにして、面の回転に伴い応力点が円周上を回る（実空間 θ に対し円上は 2θ）のを観察
- **「主応力面を表示」**で主応力の向きを可視化

## まとめ

- 面の向きを変えると応力は変わり、$(\sigma,\tau)$ は**モール円**を描く
- 円の中心 $C=(\sigma_x+\sigma_y)/2$、半径 $R=\sqrt{((\sigma_x-\sigma_y)/2)^2+\tau_{xy}^2}$
- 主応力 $\sigma_{1,2}=C\pm R$、最大せん断 $\tau_{\max}=R$、主応力角 $\tan2\theta_p=2\tau_{xy}/(\sigma_x-\sigma_y)$
- 既定値で $\sigma_1=104.85$、$\sigma_2=-64.85$、$\tau_{\max}=84.85\,\mathrm{MPa}$、$\theta_p=22.5°$。最大せん断は主応力面から 45°

材料の降伏・破壊判定の基礎となるモール円を、応力を変えながら読み解いてみてください。

⭕ **[モールの応力円ツール（NovaSolver）](https://novasolver.jp/tools/mohr-circle.html)** で、主応力と最大せん断を円から読み取りましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。材料・構造系では [梁のたわみ](https://novasolver.jp/tools/beam-deflection.html)、[オイラー座屈](https://novasolver.jp/tools/euler-buckling.html)、[応力ひずみ線図](https://novasolver.jp/tools/stress-strain.html) なども揃えています。
