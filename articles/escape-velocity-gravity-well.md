---
title: "脱出速度を支配する√(2GM/R) — 地球11.2、太陽617、中性子星では光速の6割"
emoji: "🌍"
type: "tech"
topics: ["javascript", "物理シミュレーション", "天体力学", "力学", "可視化"]
published: false
---

![脱出速度と重力井戸 — NovaSolver](/images/escape-velocity/cover.png)

## どれだけの速さで打ち出せば、二度と落ちてこないか

ボールを上に投げれば落ちてきます。でも十分に速く投げれば、重力を振り切って無限遠まで飛んでいきます。その境目の速さが**脱出速度** $v_e$。地球なら 11.2 km/s ＝ マッハ 33 という途方もない速さです。脱出速度は天体の質量 $M$ と半径 $R$ だけで決まり、たった一つの式 $v_e = \sqrt{2GM/R}$ に支配されています。

この記事では、各天体の脱出速度を JavaScript で計算し、極限としてブラックホールまで追いかけます。

🌍 **動くデモ**: [脱出速度シミュレーター（NovaSolver）](https://novasolver.jp/tools/escape-velocity.html)

## エネルギー保存から導く脱出速度

無限遠で速度ゼロになるギリギリの条件は、運動エネルギーと重力位置エネルギーの和がゼロになることです。

$$
\frac{1}{2}mv_e^2 - \frac{GMm}{R} = 0 \;\Longrightarrow\; v_e = \sqrt{\frac{2GM}{R}}
$$

円軌道を保つだけの**第一宇宙速度（軌道速度）** $v_o = \sqrt{GM/R} = v_e/\sqrt{2}$ とは $\sqrt{2}$ 倍の関係。地球なら $v_o = 7.91\,\mathrm{km/s}$ です。

$G = 6.674\times10^{-11}$ として各天体を計算すると：

| 天体 | 質量(地球比) | 半径(地球比) | 脱出速度 $v_e$ |
|---|---|---|---|
| 月 | 0.0123 | 0.273 | 2.38 km/s |
| 火星 | 0.107 | 0.532 | 5.02 km/s |
| 地球 | 1 | 1 | 11.19 km/s |
| 木星 | 317.8 | 11.21 | 59.6 km/s |
| 太陽 | 333000 | 109.2 | 617.7 km/s |

質量が大きいほど速く、半径が大きいほど遅くなる――この綱引きが脱出速度を決めます。

![天体ごとの脱出速度（対数軸）](/images/escape-velocity/charts-closeup.png)

## JavaScript 実装とブラックホールの極限

```javascript
const G = 6.674e-11, c = 2.998e8;          // 重力定数・光速
function escapeVelocity(M, R) {
  return Math.sqrt(2 * G * M / R);          // m/s
}
const vo = escapeVelocity(M, R) / Math.SQRT2;       // 第一宇宙速度
const rs = 2 * G * M / (c * c);             // シュバルツシルト半径
const overLight = escapeVelocity(M, R) >= c;        // 光速を超えるか？
```

天体を圧縮して半径を縮めると、脱出速度はどこまでも上がります。中性子星（質量 1.4 太陽質量、半径 10 km）では $v_e \approx 1.93\times10^5\,\mathrm{km/s}$、つまり**光速の約 64%**。さらに圧縮して $v_e$ が光速 $c$ に達すると、光すら脱出できない――それがブラックホールです。このときの半径が**シュバルツシルト半径** $r_s = 2GM/c^2$。$v_e = c$ を $v_e = \sqrt{2GM/R}$ に入れれば、$R = 2GM/c^2 = r_s$ がそのまま出てきます。

![脱出速度未満は落下、以上は無限遠へ脱出する打ち上げ](/images/escape-velocity/slider-anim.gif)

## ツールで遊ぶ

[脱出速度シミュレーター](https://novasolver.jp/tools/escape-velocity.html)で試してほしい操作：

- **質量スライダー・半径スライダー**（対数スケール）を動かし、$v_e = \sqrt{2GM/R}$ の依存性を確認
- **「🌍 地球」「☀️ 太陽」「⭐ 中性子星」などのプリセット**で実天体の脱出速度を比較
- **「脱出速度」「軌道速度（第一宇宙速度）」**の値が常に $\sqrt2$ 倍の関係にあることを確認
- **「光速比 $v_e/c$」**が中性子星で 0.6 を超えるのを見る
- 半径を極端に縮めて $v_e \ge c$ にし、**ブラックホール警告**と**シュバルツシルト半径**の表示を出す

## まとめ

- 脱出速度は $v_e = \sqrt{2GM/R}$、天体の質量と半径だけで決まる
- 第一宇宙速度は $v_o = v_e/\sqrt2$（地球で 7.91 km/s）
- 中性子星では光速の約 64%、$v_e = c$ でブラックホール
- シュバルツシルト半径 $r_s = 2GM/c^2$ は脱出速度の式から自然に導ける

身近な「投げ上げ」から相対論の入口まで地続きの $v_e$ を、スライダーで体感してみてください。

🌍 **[脱出速度シミュレーター（NovaSolver）](https://novasolver.jp/tools/escape-velocity.html)** で、重力井戸の深さを確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。天体力学では [軌道力学（vis-viva）](https://novasolver.jp/tools/orbital-mechanics.html)、[ホーマン遷移](https://novasolver.jp/tools/hohmann-transfer.html)、[ケプラー軌道](https://novasolver.jp/tools/kepler-orbit.html) もどうぞ。
