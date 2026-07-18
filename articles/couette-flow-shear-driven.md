---
title: "クェット流れ — 板を引きずる流れが直線プロファイルを作る理由"
emoji: "🛢️"
type: "tech"
topics: ["javascript", "物理", "流体力学", "可視化", "シミュレーション"]
published: true
---

![クェット流れ — NovaSolver](/images/couette-flow/cover.png)

## クェット流れとは

配管を流れる水は圧力差で「押し出される」流れですが、軸受の油膜やレオメーター内の流体は、片方の壁が動いて流体を「引きずる」流れです。後者を **クェット流れ（Couette flow）** と呼びます。

2 枚の平行平板（隙間 $h$）で粘性流体を挟み、上板を速度 $U$ で動かし下板を静止させます。圧力勾配がゼロなら、速度は底（$u=0$）から天井（$u=U$）まで**きれいな直線**でつながります。

$$
u(y) = U\,\frac{y}{h}
$$

ポアズイユ流れ（円管内）が放物線になるのと対照的です。この記事では、なぜ直線になるのか、圧力勾配を加えると何が起きるのか、そして「逆流」がどう現れるのかを数値で確かめます。

📐 **動くデモ**: [クェット流れ シミュレーター（NovaSolver）](https://novasolver.jp/tools/couette-flow.html)

## なぜ直線なのか

純粋クェット流れでは、流体に圧力勾配も体積力もかからないため、ナビエ・ストークス方程式の運動量バランスは極めて単純な形に帰着します。

$$
\mu\,\frac{d^2 u}{dy^2} = 0
$$

二階微分がゼロ → せん断速度 $du/dy$ が定数 → 速度は $y$ の一次関数。境界条件 $u(0)=0,\ u(h)=U$ で解けば $u(y) = U\,y/h$ が得られます。物理的には、上板から下板へ粘性で一様にせん断応力が伝わり、流体の各層が「トランプのデッキを横にずらす」ように一定勾配で滑ります。

圧力勾配 $dp/dx$ を加えると右辺に定数が乗り、放物線成分が重ね合わさります。一般解は次のとおりです。

$$
u(y) = U\,\frac{y}{h} - \frac{1}{2\mu}\,\frac{dp}{dx}\,y(h-y)
$$

壁面せん断応力（ニュートン粘性則 $\tau = \mu\,du/dy$）と単位幅流量、平均流速はそれぞれ次式です。

$$
\tau_{\mathrm{top}} = \frac{\mu U}{h} - \frac{h}{2}\frac{dp}{dx},\quad
Q' = \frac{Uh}{2} - \frac{h^3}{12\mu}\frac{dp}{dx},\quad
Re = \frac{\rho U h}{\mu}
$$

## JavaScript で書くと

ツールの計算ロジックは解析解そのものです（流体は水、$\rho = 1000\ \mathrm{kg/m^3}$）。

```javascript
const RHO = 1000;

// 速度プロファイル（y は 0..h、単位 SI）
function profileU(y, U, h, mu, dpdx) {
  return U * (y / h) - (1 / (2 * mu)) * dpdx * y * (h - y);
}

function computePhysics(U, h, mu, dpdx) {
  const tauTop = mu * U / h - (h / 2) * dpdx;
  const tauBot = mu * U / h + (h / 2) * dpdx;
  const tauMean = (Math.abs(tauTop) + Math.abs(tauBot)) / 2;
  const Qp   = U * h / 2 - (h ** 3 / (12 * mu)) * dpdx; // 単位幅流量 m²/s
  const Vavg = Qp / h;
  const Re   = RHO * U * h / mu;
  return { tauMean, Qp, Vavg, Re };
}
```

デフォルト値 $U = 1\ \mathrm{m/s},\ h = 2\ \mathrm{mm},\ \mu = 0.001\ \mathrm{Pa\cdot s},\ dp/dx = 0$（水）では：

- $\tau = \mu U/h = 0.001 \times 1 / 0.002 = 0.5\ \mathrm{Pa}$
- $Q' = Uh/2 = 1.0\times10^{-3}\ \mathrm{m^2/s}$、$V_{\mathrm{avg}} = U/2 = 0.5\ \mathrm{m/s}$
- $Re = \rho U h/\mu = 2000$

## 速度プロファイルと逆流

圧力勾配を変えると、直線が曲がり、ついには「逆流」が現れます。

![クェット＋ポアズイユの合成プロファイル](/images/couette-flow/charts-closeup.png)

$dp/dx > 0$（上板の動きに逆らう方向）にすると、ポアズイユ成分が上板駆動と反対向きに流体を押します。下板付近では速度が負（逆流）になります。逆流が始まる境界は、$y=0$ 近傍の速度勾配が負になる条件、すなわち

$$
\frac{dp}{dx} > \frac{2\mu U}{h^2}
$$

から求まります。デフォルト値では $2\mu U/h^2 = 2\times0.001\times1/(0.002)^2 = 500\ \mathrm{Pa/m}$。実際にスライダー最大の $dp/dx = 2000\ \mathrm{Pa/m}$ では、プロファイル最小値が $u_{\min} \approx -0.56\ \mathrm{m/s}$ となり、はっきりとした逆流域が下板付近にできます。

| $dp/dx$ [Pa/m] | 状態 | $u_{\min}$ [m/s] |
|---|---|---|
| 0 | 純粋クェット（直線） | 0.00 |
| 500 | 逆流開始の境界 | 約 0.00 |
| 1000 | 弱い逆流 | 約 −0.13 |
| 2000 | 明確な逆流 | 約 −0.56 |

これは軸受や歯車のすき間で実際に起きる現象で、潤滑膜内の油が部分的に逆向きに流れる「逆流ポケット」に対応します。

## せん断応力が効く現実のスケール

デフォルトの $\tau = 0.5\ \mathrm{Pa}$ は小さい値ですが、隙間 $h$ を潤滑膜の典型値 $0.02\ \mathrm{mm}$ に縮めると、

$$
\tau = \frac{\mu U}{h} = \frac{0.001 \times 1}{2\times10^{-5}} = 50\ \mathrm{Pa}
$$

と 100 倍に跳ね上がります。軸受の摩擦損失や油膜温度上昇は、まさにこの $\tau$ から発熱量 $W = \tau \cdot U \cdot (\text{面積})$ として見積もられます。スマホの精密モーターから自動車のクランクシャフトまで、油膜のある回転機械はこのクェット流れの式に支配されています。

## ツールで遊ぶ

NovaSolver のツールでは、4 つのスライダーと自動スイープでプロファイルの変形を体感できます。

![dp/dx をスイープすると逆流が現れる](/images/couette-flow/slider-anim.gif)

試してほしい操作：

- **「$dp/dx$ をスイープ」ボタン**で圧力勾配を $-2000 \to +2000\ \mathrm{Pa/m}$ まで自動スイープし、直線 → 放物線で膨らむ → 逆流発生（赤色表示）の遷移を観察
- **上板速度 $U$ / 隙間 $h$** を変えて「平均壁面せん断応力」カードが $\mu U/h$ どおりに動くことを確認
- **粘性係数 $\mu$** を油の値（0.01〜0.1 Pa·s）に上げて「Reynolds 数」カードが下がり、確実な層流域に入る様子を見る
- **「正規化プロファイル $u/U$ vs $y/h$」グラフ**で、合成プロファイル（青実線）と純粋クェット直線（灰破線）のずれを比較

## まとめ

- 純粋クェット流れは $\mu\,d^2u/dy^2 = 0$ から $u(y) = U\,y/h$ という直線になる
- 圧力勾配を加えると放物線成分が重なり $u(y) = U\,y/h - (1/2\mu)(dp/dx)\,y(h-y)$
- $dp/dx > 2\mu U/h^2$ で下板付近に逆流が現れる（デフォルトでは 500 Pa/m）
- デフォルト条件（水・$U=1$・$h=2\,\mathrm{mm}$）で $\tau = 0.5\ \mathrm{Pa},\ Re = 2000$

平行平板せん断駆動流は円管とは臨界 Re が異なり、実験では $Re \approx 360$〜$1500$ あたりから乱流に遷移するとされます。本ツールは層流の解析解を表示するため、$Re$ が高い場合は実流れとの乖離に注意してください。潤滑工学（レイノルズ方程式）・レオメーター・マイクロ流体の基礎となる流れです。

📐 **[クェット流れ シミュレーター（NovaSolver）](https://novasolver.jp/tools/couette-flow.html)** で、圧力勾配を動かして逆流が生まれる瞬間を見てみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。流体・粘性まわりでは [管内流れ](https://novasolver.jp/tools/pipe-flow.html)、[ベルヌーイの定理・管路流れ](https://novasolver.jp/tools/bernoulli-flow.html)、[血流・血管力学](https://novasolver.jp/tools/blood-flow.html) なども揃えています。
