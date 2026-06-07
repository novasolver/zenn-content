---
title: "パイプ流れの圧力損失 — レイノルズ数・層流乱流遷移・Moodyチャート"
emoji: "🚰"
type: "tech"
topics: ["javascript", "流体力学", "レイノルズ数", "可視化", "数値計算"]
published: false
---

![パイプ流れと層流乱流遷移 — NovaSolver](/images/pipe-flow/cover.png)

## ポンプの選定は「圧力損失」から始まる

水道、空調の冷温水、油圧、化学プラントの配管——あらゆる流体輸送で、エンジニアがまず計算するのが**管内の圧力損失** $\Delta P$ です。これが分からないとポンプの動力も配管径も決められません。そして $\Delta P$ を支配するのが、流れが**層流か乱流か**を決める無次元数、**レイノルズ数**です。

この記事では、配管設計の心臓部である Darcy-Weisbach 式・Colebrook-White 式・Moody チャートを、実際の数値とともに解説します。

🚰 **動くデモ**: [パイプ流れ圧力損失計算機（NovaSolver）](https://novasolver.jp/tools/pipe-flow.html)

## レイノルズ数と層流乱流遷移

レイノルズ数は「慣性力 ÷ 粘性力」の比です。

$$
\mathrm{Re} = \frac{\rho U D}{\mu} = \frac{U D}{\nu}
$$

$\rho$ は密度、$U$ は平均流速、$D$ は管内径、$\mu$ は粘度。円管内流れでは経験的に

- $\mathrm{Re} < 2300$：**層流**（整然と層状に流れる）
- $2300 \le \mathrm{Re} < 4000$：**遷移域**（不安定）
- $\mathrm{Re} \ge 4000$：**乱流**（渦が混ざり合う）

と区分されます。この遷移は流れの「質」を一変させます。層流の速度分布は放物線、乱流では中央が平らに均された「fuller」なプロファイルになります。

![Moody チャートと層流・乱流の速度プロファイル](/images/pipe-flow/charts-closeup.png)

## 摩擦係数と Darcy-Weisbach 式

圧力損失は **Darcy-Weisbach 式**で計算します。

$$
\Delta P = f\,\frac{L}{D}\,\frac{\rho U^2}{2}
$$

$L$ は管長、$f$ は **Darcy 摩擦係数**。この $f$ をどう決めるかが要点で、流れの領域で式が変わります。

**層流**では理論的にきれいな式が成り立ちます。

$$
f = \frac{64}{\mathrm{Re}}
$$

**乱流**では管壁の相対粗さ $\varepsilon/D$ も効いてきて、陰関数の **Colebrook-White 式**を反復で解きます。

$$
\frac{1}{\sqrt{f}} = -2\log_{10}\!\left(\frac{\varepsilon/D}{3.7} + \frac{2.51}{\mathrm{Re}\sqrt{f}}\right)
$$

これを $\mathrm{Re}$ と $\varepsilon/D$ の組ごとにプロットしたのが、上図左の **Moody チャート**です。配管設計者がポンプ動力・圧力損失・流量の関係を読み取る、最も基本的な図です。

## 実際に計算してみる

ツールの既定値（$D=50\,\mathrm{mm}$、$L=10\,\mathrm{m}$、流量 $Q=0.01\,\mathrm{m^3/s}$、水 20°C、鋼管 $\varepsilon=0.046\,\mathrm{mm}$）で追ってみます。まず断面積 $A=\pi D^2/4 = 1.963\times10^{-3}\,\mathrm{m^2}$ から平均流速

$$
U = \frac{Q}{A} = \frac{0.01}{1.963\times10^{-3}} = 5.09\,\mathrm{m/s}
$$

レイノルズ数は（水 $\rho=998.2$、$\mu=1.002\times10^{-3}$）

$$
\mathrm{Re} = \frac{998.2 \times 5.09 \times 0.05}{1.002\times10^{-3}} \approx 2.54\times10^{5}
$$

完全に乱流です。$\varepsilon/D = 0.046/50 \approx 9.2\times10^{-4}$ で Colebrook を解くと $f\approx0.0204$。したがって

$$
\Delta P = 0.0204\times\frac{10}{0.05}\times\frac{998.2\times5.09^2}{2} \approx 5.29\times10^{4}\,\mathrm{Pa} = 0.529\,\mathrm{bar}
$$

10 m の鋼管で約 0.53 気圧もの損失。流速を下げるか管径を上げないとポンプ動力が嵩むことが、数値からはっきり見えます（$\Delta P \propto U^2$ なので流速の影響は絶大です）。

## JavaScript 実装（Colebrook の反復解）

陰関数の Colebrook 式は固定点反復で解けます。初期値 $f=0.02$ から数回で収束します。

```javascript
function colebrookTurb(Re, epsD) {
  let f = 0.02;
  for (let i = 0; i < 40; i++) {
    const rhs = -2 * Math.log10(epsD/3.7 + 2.51/(Re*Math.sqrt(f)));
    f = 1 / (rhs*rhs);
  }
  return f;
}
function frictionFactor(Re, epsD) {
  if (Re < 2300) return 64 / Re;                       // 層流
  if (Re < 4000) {                                     // 遷移は線形補間
    const fl = 64/2300, ft = colebrookTurb(4000, epsD);
    return fl + (ft - fl) * (Re - 2300) / 1700;
  }
  return colebrookTurb(Re, epsD);                      // 乱流
}
```

![レイノルズ数を上げると動作点が乱流へ移り、速度分布が平らになる](/images/pipe-flow/slider-anim.gif)

## ツールで遊ぶ

[パイプ流れ圧力損失計算機](https://novasolver.jp/tools/pipe-flow.html)で試してほしい操作：

- **流量 Q（または速度 U）スライダー**を上げ、Moody チャート上の**赤い動作点が層流→遷移→乱流**へ移るのを追う
- **管径 D スライダー**を変え、$\mathrm{Re}$ と $\Delta P$ がどう動くか確認（細い管ほど損失大）
- **粗さ ε（材料）**を「なめらかガラス/PE」「鋼管」「鋳鉄管」「コンクリート管」で切り替え、乱流域での $f$ の差を見る
- **流体**を「水」「空気」「カスタム」で切り替え、粘度・密度の影響を比較
- **流量 Q / 速度 U の入力切替**トグルで、好きな方から入力する
- **計算結果**（Reynolds 数、摩擦係数 $f$、$\Delta P$ を Pa と bar で）と **ΔP vs Q 曲線**、**速度プロファイル断面アニメーション**で流れの様子を確認

## まとめ

- 圧力損失は **Darcy-Weisbach 式** $\Delta P = f(L/D)(\rho U^2/2)$。流速の2乗で効くのが効率設計の急所
- 流れの領域はレイノルズ数で決まる：層流 $\mathrm{Re}<2300$、遷移、乱流 $\mathrm{Re}\ge4000$
- 摩擦係数は層流 $f=64/\mathrm{Re}$、乱流は **Colebrook-White 式**を反復で解く。**Moody チャート**で一覧できる
- 既定値で $\mathrm{Re}\approx2.5\times10^5$、$f\approx0.020$、$\Delta P\approx0.53\,\mathrm{bar}$（10 m 鋼管）

CFD を回す前の手計算・概算に、配管エンジニアの基本ツールを使ってみてください。

🚰 **[パイプ流れ圧力損失計算機（NovaSolver）](https://novasolver.jp/tools/pipe-flow.html)** で、あなたの配管の圧力損失とレイノルズ数を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。流体系では [カルマン渦](https://novasolver.jp/tools/karman-vortex.html)、[終端沈降速度](https://novasolver.jp/tools/settling-velocity.html)、[乱流境界層](https://novasolver.jp/tools/boundary-layer-turbulent.html) なども揃えています。
