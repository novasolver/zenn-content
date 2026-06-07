---
title: "量子トンネル効果：壁を越えられないはずの粒子がすり抜ける — T≈e^(-2κd)をJSで"
emoji: "⚛️"
type: "tech"
topics: ["javascript", "量子力学", "物理シミュレーション", "可視化", "数値計算"]
published: false
---

![量子トンネル効果 — NovaSolver](/images/quantum-tunneling/cover.png)

## エネルギーが足りないのに、壁を通り抜ける

古典物理では、坂を登る運動エネルギーが足りなければ、ボールは坂を越えられません。ところが量子の世界では、エネルギー $E$ が障壁の高さ $V_0$ より低くても、粒子は一定の確率で**障壁をすり抜けます**。これが**量子トンネル効果**。太陽の核融合、走査トンネル顕微鏡（STM）、フラッシュメモリ、放射性崩壊――すべてこの効果に支えられています。

この記事では、矩形障壁の透過確率を JavaScript で計算します。

⚛️ **動くデモ**: [量子トンネル効果シミュレーター（NovaSolver）](https://novasolver.jp/tools/quantum-tunneling.html)

## 透過確率と減衰定数

障壁内（$E < V_0$）では波動関数が振動せず、指数的に減衰します。その減衰率が**減衰定数** $\kappa$ です。

$$
\kappa = \frac{\sqrt{2m(V_0 - E)}}{\hbar},\qquad T \approx e^{-2\kappa d}
$$

（$T$ は透過確率、$d$ は障壁の幅。これは WKB 近似。）厳密には矩形障壁で

$$
T = \frac{1}{1 + \dfrac{V_0^2}{4E(V_0-E)}\sinh^2(\kappa d)}
$$

が成り立ちます。重要なのは、**$T$ が障壁の幅 $d$ に対して指数的に減少する**こと。少しの幅の違いが、透過確率を桁違いに変えます。

電子（$V_0 = 5\,\mathrm{eV}$、$E = 3\,\mathrm{eV}$、$d = 1\,\mathrm{nm}$）で計算すると、$\kappa = 7.24\,\mathrm{nm^{-1}}$、**WKB 透過確率 $T \approx 5.1\times10^{-7}$**（厳密式では約 $2\times10^{-6}$）。障壁を半分の $0.5\,\mathrm{nm}$ に薄くすると $T \approx 7.2\times10^{-4}$ と**約 1400 倍**に跳ね上がります。STM がnm スケールの距離変化を電流で読み取れるのは、この鋭い指数依存のおかげです。逆に重い陽子（電子の 1836 倍の質量）では $T \approx 10^{-270}$ と、事実上トンネルしません。

![障壁と波動関数（左, 染み出して透過）と透過確率 T vs 幅（右）](/images/quantum-tunneling/charts-closeup.png)

## JavaScript 実装

```javascript
const me = 9.109e-31, eV = 1.602e-19, hbar = 1.055e-34, nm = 1e-9;
function tunnel(V0_eV, E_eV, d_nm, m_rel) {
  const dE = (V0_eV - E_eV) * eV;
  if (dE <= 0) return { T: 1 };                    // E≥V0 は古典的に通過
  const m = m_rel * me;
  const kappa = Math.sqrt(2 * m * dE) / hbar;      // 減衰定数 [1/m]
  const T = Math.exp(-2 * kappa * d_nm * nm);      // WKB 透過確率
  return { kappa_nm: kappa * nm, T, R: 1 - T };
}
// tunnel(5, 3, 1.0, 1) → κ≈7.24/nm, T≈5.1e-7
```

障壁の中で波動関数の振幅が $e^{-\kappa x}$ で減衰し、向こう側に小さく漏れ出した分が透過波になります。「壁の向こうに染み出す」というイメージが、量子トンネルの本質です。

![障壁の幅を変えると透過確率が指数的に変わる](/images/quantum-tunneling/slider-anim.gif)

## ツールで遊ぶ

[量子トンネル効果シミュレーター](https://novasolver.jp/tools/quantum-tunneling.html)で試してほしい操作：

- **障壁の幅 d スライダー**を変え、透過確率 T が指数的に変化するのを確認（薄いほど通る）
- **障壁の高さ V₀・粒子エネルギー E スライダー**で $\kappa = \sqrt{2m(V_0-E)}/\hbar$ の依存を見る
- **「電子」「陽子」「α粒子」プリセット**で質量による透過確率の桁違いの差を比較
- **波動関数図**で入射波・障壁内の減衰・透過波を観察
- **「T vs 障壁幅」「T vs エネルギー」グラフ**（対数）で指数依存を読む
- d を 0.5 nm にして T が約 1000 倍に増えるのを確認

## まとめ

- 量子トンネルは $E < V_0$ でも有限の透過確率を持つ現象
- 減衰定数 $\kappa = \sqrt{2m(V_0-E)}/\hbar$、透過確率 $T \approx e^{-2\kappa d}$
- 電子・1nm 障壁で $T \approx 5\times10^{-7}$、幅半減で約 1400 倍
- 重い粒子ほど $\kappa$ が大きく、トンネルしにくい

ミクロな世界の不思議を、障壁の高さ・幅・粒子の質量を変えながら体感してみてください。

⚛️ **[量子トンネル効果シミュレーター（NovaSolver）](https://novasolver.jp/tools/quantum-tunneling.html)** で、壁をすり抜ける確率を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。物理では [黒体放射](https://novasolver.jp/tools/blackbody-radiation.html)、[マクスウェル・ボルツマン分布](https://novasolver.jp/tools/maxwell-boltzmann.html)、[二重スリット干渉](https://novasolver.jp/tools/wave-interference.html) もどうぞ。
