---
title: "梁のたわみと曲げモーメント — δ∝L⁴ が効く Euler-Bernoulli 梁理論"
emoji: "🏗️"
type: "tech"
topics: ["javascript", "構造力学", "CAE", "数値計算", "可視化"]
published: false
---

![梁のたわみと曲げモーメント — NovaSolver](/images/beam-deflection/cover.png)

## 棚板はなぜ真ん中が垂れるのか

本棚の棚板が中央で垂れ下がる、橋桁が荷重でたわむ、片持ちの庇が先端で下がる——これらはすべて**梁のたわみ**です。構造設計で最初に学ぶ **Euler-Bernoulli 梁理論**は、荷重とたわみ・応力の関係を簡潔な式で結びつけます。そして設計者が肝に銘じる教訓のひとつが「**たわみは長さの4乗で効く**」こと。長さを2倍にすると、たわみは16倍にもなります。

🏗️ **動くデモ**: [梁のたわみ・応力解析シミュレーター（NovaSolver）](https://novasolver.jp/tools/beam-deflection.html)

## 支配方程式とたわみ公式

梁のたわみ $w(x)$ は、曲げ剛性 $EI$（ヤング率 × 断面二次モーメント）と分布荷重 $q$ を結ぶ4階の微分方程式で決まります。

$$
EI\,\frac{d^4w}{dx^4} = q(x)
$$

これを境界条件で解くと、代表的なケースの最大たわみは次のようになります。

- **単純支持梁＋等分布荷重**：$\displaystyle\delta_{\max} = \frac{5qL^4}{384EI}$（中央）
- **単純支持梁＋中央集中荷重**：$\displaystyle\delta_{\max} = \frac{PL^3}{48EI}$（中央）
- **片持ち梁＋先端集中荷重**：$\displaystyle\delta_{\max} = \frac{PL^3}{3EI}$（先端）

いずれも $EI$ に反比例（剛いほどたわまない）、そして長さ $L$ の **3〜4乗**に比例します。

## 実際に計算してみる

ツールの既定値（$E=200\,\mathrm{GPa}$ の鋼、$I=1\times10^{-6}\,\mathrm{m^4}$、$L=2\,\mathrm{m}$、$q=10\,\mathrm{kN/m}$）で単純支持＋等分布荷重を計算します。曲げ剛性 $EI = 200\times10^9\times10^{-6}=2\times10^5\,\mathrm{N\cdot m^2}$ から

$$
\delta_{\max} = \frac{5\times10000\times2^4}{384\times2\times10^5} = 0.01042\,\mathrm{m} = 10.42\,\mathrm{mm}
$$

最大曲げモーメントは中央で

$$
M_{\max} = \frac{qL^2}{8} = \frac{10000\times2^2}{8} = 5000\,\mathrm{N\cdot m} = 5.0\,\mathrm{kN\cdot m}
$$

![たわみ曲線（誇張表示）と放物線状の曲げモーメント図](/images/beam-deflection/charts-closeup.png)

上図のように、等分布荷重による曲げモーメントは中央が最大の**放物線**を描きます。最大応力はこの $M_{\max}$ から $\sigma_{\max} = M_{\max}c/I$（$c$ は中立軸から縁までの距離）で求まり、許容応力と比較して断面を決めます。

## 「長さの4乗」が設計を支配する

$\delta\propto L^4$（等分布）という関係は強烈です。スパンを 2 倍にすると、同じ断面・同じ単位荷重ならたわみは $2^4=16$ 倍。逆に、たわみを抑えたいなら $EI$（断面を大きく・材料を剛く）を増やすか、スパンを短くするのが効果的です。床のたわみ規制（例：$L/300$ 以下）が厳しいのは、この強い長さ依存性のためです。

## JavaScript 実装

各支持・荷重条件のたわみ公式を場所 $x$ ごとに評価し、たわみ曲線・モーメント図・せん断力図を描きます。

```javascript
// 単純支持梁 + 等分布荷重 q
const EI = E * I;                                   // 曲げ剛性
const w = q*x*(L*L*L - 2*L*x*x + x*x*x)/(24*EI);    // たわみ w(x)
const M = q*x*(L - x)/2;                            // 曲げモーメント M(x)
const V = q*(L/2 - x);                              // せん断力 V(x)
// 片持ち梁 + 先端荷重 P なら w = P*x^2*(3L - x)/(6EI) など条件別
```

![荷重を増やすとたわみが比例して大きくなる](/images/beam-deflection/slider-anim.gif)

## ツールで遊ぶ

[梁のたわみ・応力解析シミュレーター](https://novasolver.jp/tools/beam-deflection.html)で試してほしい操作：

- **梁タイプ**を「単純支持＋等分布」「単純支持＋集中」「片持ち＋等分布」「片持ち＋集中」で切り替え、たわみの形の違いを見る
- **梁の長さ L スライダー**を 1m → 2m に伸ばし、**最大たわみ**が $L^4$（または $L^3$）で急増することを確認
- **ヤング率 E・断面二次モーメント I スライダー**を上げ、$EI$（曲げ剛性）が増えるとたわみが反比例で減ることを観察
- **荷重 q/P スライダー**を上げ、たわみ・モーメントが比例で増えるのを見る
- **たわみ曲線・曲げモーメント図・せん断力図**を見比べ、$M$ が最大の位置と $\delta$ が最大の位置の関係を確認
- **計算結果**（最大たわみ・最大モーメント・最大せん断力・曲げ剛性 EI）を読む

## まとめ

- Euler-Bernoulli 梁：$EI\,w'''' = q$。たわみは曲げ剛性 $EI$ に反比例
- 単純支持＋等分布で $\delta_{\max}=5qL^4/384EI$、中央集中で $PL^3/48EI$、片持ち先端で $PL^3/3EI$
- 既定値で $\delta_{\max}=10.42\,\mathrm{mm}$、$M_{\max}=qL^2/8=5\,\mathrm{kN\cdot m}$
- **たわみは長さの3〜4乗で効く**。スパン2倍でたわみ最大16倍

橋・建築・機械の構造設計（Ansys・Abaqus などの CAE）の出発点となる梁理論を、条件を変えながら体感してみてください。

🏗️ **[梁のたわみ・応力解析シミュレーター（NovaSolver）](https://novasolver.jp/tools/beam-deflection.html)** で、たわみと曲げモーメントの関係を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。構造解析系では [オイラー座屈](https://novasolver.jp/tools/euler-buckling.html)、[モール円](https://novasolver.jp/tools/mohr-circle.html)、[トラス解析](https://novasolver.jp/tools/truss-analysis.html) なども揃えています。
