---
title: "放熱フィンの効率はなぜ100%にならない？ η=tanh(mL)/mL をJavaScriptで"
emoji: "🌡️"
type: "tech"
topics: ["javascript", "熱力学", "CAE", "数値計算", "可視化"]
published: true
---

![フィン（放熱板）の熱伝達 — NovaSolver](/images/fin-heat-transfer/cover.png)

## CPUクーラーの「ひだ」はなぜあの形なのか

CPU クーラーやバイクのエンジン、エアコンの室外機――冷やしたいものには必ず**フィン（放熱板）**がついています。表面積を増やして放熱を稼ぐ仕掛けですが、フィンを長くすればするほど効率よく冷えるわけではありません。先端に行くほど温度が下がり、放熱に貢献しなくなるからです。この「使えなさ具合」を表すのが**フィン効率**です。

この記事では、フィンの温度分布と効率を JavaScript で計算します。

🌡️ **動くデモ**: [フィン熱伝達シミュレーター（NovaSolver）](https://novasolver.jp/tools/fin-heat-transfer.html)

## フィンパラメータと効率

一様断面フィン（先端断熱）に沿った温度超過 $\theta = T - T_\infty$ は、フィンパラメータ $m$ を使って次式で表されます。

$$
\frac{\theta(x)}{\theta_b} = \frac{\cosh[m(L-x)]}{\cosh(mL)},\qquad m = \sqrt{\frac{hP}{kA}}
$$

$h$ は対流熱伝達率、$P$ は周長、$k$ は熱伝導率、$A$ は断面積。フィン効率（実際の放熱 ÷ 全体が根元温度だった場合の理想放熱）は無次元数 $mL$ だけで決まります。

$$
\eta = \frac{\tanh(mL)}{mL}
$$

アルミ製の既定フィン（$L=50\,\mathrm{mm}$, $t=3\,\mathrm{mm}$, $W=50\,\mathrm{mm}$, $k=200$, $h=25$）で計算すると、$m = 9.40\,\mathrm{m^{-1}}$、$mL = 0.470$、**フィン効率 $\eta = 93.2\%$**。先端温度は $T_{\text{tip}} = 74.4\,\mathrm{°C}$（根元 80°C、環境 25°C）で、根元からあまり下がっていません＝よく働いているフィンです。1 枚あたりの放熱は 6.79 W、フィンなし（根元面のみ）に比べ **32.9 倍**に増強されます。

熱伝導率を上げると効率が上がります：銅（$k=400$）で $\eta = 96.5\%$、鋼（$k=50$）では $\eta = 78.2\%$。熱を先端まで伝えられる材料ほど、フィン全体が放熱に使えるのです。

![材料別の温度分布（左）とフィン効率 η vs mL（右）](/images/fin-heat-transfer/charts-closeup.png)

## JavaScript 実装

```javascript
function fin(L, t, W, k, h, Tb, Tinf) {
  const P = 2 * (W + t);            // 周長 [m]
  const A = W * t;                  // 断面積 [m²]
  const m = Math.sqrt(h * P / (k * A));   // フィンパラメータ
  const mL = m * L;
  const eta = Math.tanh(mL) / mL;         // フィン効率
  const thetaB = Tb - Tinf;
  const As = P * L;                        // フィン表面積
  const Qsingle = eta * h * As * thetaB;   // 1枚の放熱量 [W]
  const Ttip = Tinf + thetaB / Math.cosh(mL);  // 先端温度
  return { m, mL, eta, Qsingle, Ttip };
}
// fin(0.05, 0.003, 0.05, 200, 25, 80, 25) → η=0.932, Ttip=74.4°C
```

$mL$ が大きい（長い・薄い・低伝導率・高対流）ほど効率は落ちます。$\eta = \tanh(mL)/mL$ は $mL \to 0$ で 1、大きくなると単調に 0 へ近づく。だから「長くすれば放熱量は増えるが、効率（材料あたりの貢献）は下がる」というトレードオフが生まれます。

![対流係数 h を変えるとフィンの温度分布と効率が変わる](/images/fin-heat-transfer/slider-anim.gif)

## ツールで遊ぶ

[フィン熱伝達シミュレーター](https://novasolver.jp/tools/fin-heat-transfer.html)で試してほしい操作：

- **フィン長さ L スライダー**を伸ばし、効率 η は下がるのに総放熱量は増える（先端温度が環境に近づく）のを確認
- **「アルミ」「銅」「鋼」プリセット**で熱伝導率 k による効率の違いを比較
- **対流係数 h スライダー**を上げ（強制空冷を模擬）、mL が増えて効率が落ちるのを見る
- **フィン枚数 N スライダー**でアレイ総放熱量がスケールするのを確認
- **温度分布グラフ**で根元から先端への温度低下を読む
- **伝熱増強比**で、フィンが平面に比べ何倍放熱するかを見る

> 補足：このシミュレーターの効率式は一様断面（矩形）フィンの先端断熱モデルに基づきます。形状セレクタは見た目を変えますが、効率計算は矩形フィンの式を用いています。

## まとめ

- フィン温度は $\theta(x)/\theta_b = \cosh[m(L-x)]/\cosh(mL)$
- フィン効率は $\eta = \tanh(mL)/mL$、無次元数 $mL$ だけで決まる
- アルミ既定で η=93.2%、放熱は平面の 32.9 倍
- 高伝導率ほど高効率（銅 96.5%、鋼 78.2%）

放熱設計の基礎を、長さ・材料・対流条件を変えながら体感してみてください。

🌡️ **[フィン熱伝達シミュレーター（NovaSolver）](https://novasolver.jp/tools/fin-heat-transfer.html)** で、放熱フィンの効率を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。熱・CAE では [熱拡散](https://novasolver.jp/tools/heat-diffusion.html)、[シュテファン・ボルツマンの法則](https://novasolver.jp/tools/stefan-boltzmann.html)、[レイリー・ベナール対流](https://novasolver.jp/tools/convection-cells.html) もどうぞ。
