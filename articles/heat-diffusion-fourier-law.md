---
title: "2D熱拡散シミュレーション — フーリエの熱方程式とFTCS陽解法の安定条件"
emoji: "🔥"
type: "tech"
topics: ["javascript", "熱力学", "CAE", "数値計算", "可視化"]
published: true
---

![2D熱拡散とフーリエの法則 — NovaSolver](/images/heat-diffusion/cover.png)

## 熱はどう「広がる」のか

熱いコーヒーが冷め、CPU のヒートシンクが熱を逃がし、地中の温度が季節でゆっくり変化する——熱の伝わり方（熱伝導）は、**フーリエの熱方程式**という1本の偏微分方程式で記述できます。そしてこれを計算機で解く最も素直な方法が、**FTCS（前進時間・中心空間）陽解法**です。

この記事では熱方程式を離散化し、JavaScript で 2D の温度場を時間発展させ、陽解法に必ずついてまわる**数値安定条件**まで踏み込みます。

🔥 **動くデモ**: [2D熱拡散シミュレーター（NovaSolver）](https://novasolver.jp/tools/heat-diffusion.html)

## フーリエの熱方程式

温度 $T(x,y,t)$ の時間変化は、温度の空間的な「曲がり具合」（ラプラシアン）に比例します。

$$
\frac{\partial T}{\partial t} = \alpha\left(\frac{\partial^2 T}{\partial x^2} + \frac{\partial^2 T}{\partial y^2}\right)
$$

$\alpha$ は**熱拡散率**で、材料の性質（熱伝導率 $\lambda$、密度 $\rho$、比熱 $c_p$）から決まります。

$$
\alpha = \frac{\lambda}{\rho c_p}
$$

$\alpha$ が大きいほど熱が速く広がります。金属は大きく（銅 $\approx116\times10^{-6}\,\mathrm{m^2/s}$）、断熱材は小さい（木材 $\approx0.13\times10^{-6}$）。ツールでは相対値で銅 11.6、アルミ 8.4、鋼材 1.2、ガラス 0.34、木材 0.13 として比較できます。

## FTCS 陽解法で離散化する

格子上で2階微分を中心差分に置き換えると、次の時刻の温度が「今の自分と上下左右の平均的なずれ」で書けます。

$$
T_{i,j}^{\,n+1} = T_{i,j}^{\,n} + \frac{\alpha\,\Delta t}{\Delta x^2}\left(T_{i+1,j}^{\,n} + T_{i-1,j}^{\,n} + T_{i,j+1}^{\,n} + T_{i,j-1}^{\,n} - 4T_{i,j}^{\,n}\right)
$$

各セルが周囲との温度差をならしていく、という直感そのままの式です。ツールは $100\times100$ 格子、$\Delta t=0.02$、$\Delta x=1$ で計算します。

![中央熱源の温度場と、時間とともに拡がる断面温度](/images/heat-diffusion/charts-closeup.png)

左図は中央に 100°C の熱源を置いたときの温度場、右図は中央を横切る断面温度の時間変化です。初期の鋭いピークが、時間とともになだらかに拡がっていくのが拡散の本質です。

## 陽解法の落とし穴：安定条件

FTCS は実装が簡単ですが、**時間刻みを大きくしすぎると発散します**。2次元では次の安定条件を満たす必要があります。

$$
\frac{\alpha\,\Delta t}{\Delta x^2} \le \frac{1}{4}
$$

この無次元数を $a$ と呼ぶと、ツールの設定（$\Delta t=0.02$、$\Delta x=1$）では各材料で

| 材料 | $\alpha$（相対） | $a=\alpha\Delta t/\Delta x^2$ | 判定 |
|---|---|---|---|
| 木材 | 0.13 | 0.003 | 安定 |
| ガラス | 0.34 | 0.007 | 安定 |
| 鋼材 | 1.2 | 0.024 | 安定 |
| アルミ | 8.4 | 0.168 | 安定 |
| 銅 | 11.6 | **0.232** | 安定（上限0.25に接近） |

最も熱拡散率の大きい銅でも $a=0.232<0.25$ ぎりぎりで安定するよう設計されています。もし $a>0.25$ になると温度が振動・発散して物理的に無意味な結果になります——陽解法を使うときに最も注意すべき点です。

## JavaScript 実装

ラプラシアンを足し込むだけのループで実装できます。

```javascript
const a = alpha * dt / (dx * dx);           // 安定条件: a <= 0.25
for (let i = 1; i < N-1; i++) {
  for (let j = 1; j < N-1; j++) {
    const idx = i*N + j;
    if (sources[idx] === 1) { T2[idx] = 100; continue; }  // 熱源は固定
    T2[idx] = T[idx] + a * (
      T[(i+1)*N+j] + T[(i-1)*N+j] +
      T[i*N+j+1]   + T[i*N+j-1]   - 4*T[idx]
    );
  }
}
```

境界条件は**断熱（Neumann, $\partial T/\partial n=0$）** か **恒温 0°C（Dirichlet）** を選べます。Dirichlet で両端を固定すると、定常状態では温度分布が**線形**（$T(x)=ax+b$）に落ち着きます——これはフーリエの法則の基本的な帰結です。

![中央熱源から熱が拡散していく様子（FTCS）](/images/heat-diffusion/slider-anim.gif)

## ツールで遊ぶ

[2D熱拡散シミュレーター](https://novasolver.jp/tools/heat-diffusion.html)で試してほしい操作：

- **キャンバスをクリック／ドラッグ**で熱源（100°C）や冷却（0°C）を描き、熱が広がる様子を見る
- **材料プリセット**「銅」「アルミ」「鋼材」「ガラス」「木材」を切り替え、拡散の速さの違いを比較
- **境界条件**を「断熱」「恒温 0°C」で切り替え、端での熱の振る舞いを観察
- **プリセット**「中央熱源」「温度勾配」「複数熱源」で典型的なシナリオを再現
- **温度勾配**プリセット＋恒温境界で、定常状態が**線形分布**になることを確認
- **計算結果**（最高温度・最低温度・平均温度・シム時間）と**プローブのグラフ**で温度履歴を追う
- **速度スライダー**やステップ送りで拡散の速さを調整

## まとめ

- 熱伝導は**フーリエの熱方程式** $\partial T/\partial t=\alpha\nabla^2T$。$\alpha=\lambda/(\rho c_p)$ が拡散の速さを決める
- **FTCS 陽解法**で素直に解けるが、安定条件 $\alpha\Delta t/\Delta x^2\le1/4$ を破ると発散する
- ツールは銅でも $a=0.232$ と上限ぎりぎりで安定するよう設計
- Dirichlet 境界の定常状態は線形温度分布

CAE の熱解析（Ansys・Abaqus）の出発点となる熱方程式と陽解法を、自分で熱を描きながら体感してみてください。

🔥 **[2D熱拡散シミュレーター（NovaSolver）](https://novasolver.jp/tools/heat-diffusion.html)** で、材料と境界条件を変えて熱の広がりを観察しましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。CAE・数値計算系では [反応拡散](https://novasolver.jp/tools/reaction-diffusion.html)、[パイプ流れ](https://novasolver.jp/tools/pipe-flow.html)、[カルマン渦](https://novasolver.jp/tools/karman-vortex.html) なども揃えています。
