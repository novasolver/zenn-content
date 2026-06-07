---
title: "マクスウェル・ボルツマン分布の3つの速さ — vp:⟨v⟩:vrms=1:1.13:1.22をJSで"
emoji: "🌡️"
type: "tech"
topics: ["javascript", "熱力学", "統計力学", "可視化", "数値計算"]
published: false
---

![マクスウェル・ボルツマン速度分布 — NovaSolver](/images/maxwell-boltzmann/cover.png)

## 気体分子は、みんな同じ速さでは飛んでいない

室温の空気でも、窒素分子は秒速 400〜500 m という猛スピードで飛び回っています。でも全部が同じ速さではありません。遅い分子も速い分子もいて、その分布を表すのが**マクスウェル・ボルツマン分布**です。面白いのは「最も多い速さ」「平均の速さ」「二乗平均平方根の速さ」が**すべて違う値**になること。

この記事では、3 つの代表的な速さを JavaScript で計算します。

🌡️ **動くデモ**: [マクスウェル・ボルツマン分布シミュレーター（NovaSolver）](https://novasolver.jp/tools/maxwell-boltzmann.html)

## 速さの分布と3つの代表値

質量 $m$ の分子が温度 $T$ で速さ $v$ を持つ確率密度は次式です。

$$
f(v) = 4\pi\left(\frac{m}{2\pi k_B T}\right)^{3/2} v^2 \exp\!\left(-\frac{mv^2}{2k_B T}\right)
$$

$v^2$ の項（低速で増加）と指数の項（高速で減少）の競争で、非対称な山型になります。代表的な 3 つの速さは

$$
v_p = \sqrt{\frac{2k_B T}{m}},\quad \langle v\rangle = \sqrt{\frac{8k_B T}{\pi m}},\quad v_{\text{rms}} = \sqrt{\frac{3k_B T}{m}}
$$

これらは常に $v_p : \langle v\rangle : v_{\text{rms}} = 1 : 1.128 : 1.225$ の比になります（最確速度が最小、rms が最大）。

窒素 N₂（$M=28\,\mathrm{g/mol}$）を $T=300\,\mathrm{K}$ で計算すると、**最確速度 $v_p = 422\,\mathrm{m/s}$、平均速さ $\langle v\rangle = 476\,\mathrm{m/s}$、rms 速度 $v_{\text{rms}} = 517\,\mathrm{m/s}$**。温度を 4 倍にすると速さは 2 倍（$v \propto \sqrt{T}$）、軽い水素 H₂ なら同じ 300 K でも $v_p = 1579\,\mathrm{m/s}$ と桁違いに速くなります。

![分布と3つの代表速度（左）と温度による広がり（右）](/images/maxwell-boltzmann/charts-closeup.png)

## JavaScript 実装

```javascript
const kB = 1.380649e-23, NA = 6.02214076e23;
function speeds(T, Mg) {                  // Mg: molar mass [g/mol]
  const m = Mg * 1e-3 / NA;              // 1 分子の質量 [kg]
  return {
    vp:   Math.sqrt(2 * kB * T / m),         // 最確速度
    vmean:Math.sqrt(8 * kB * T / (Math.PI * m)), // 平均速さ
    vrms: Math.sqrt(3 * kB * T / m),         // 二乗平均平方根速度
  };
}
function fMB(v, m, T) {                    // 確率密度
  const a = m / (2 * Math.PI * kB * T);
  return 4 * Math.PI * Math.pow(a, 1.5) * v*v * Math.exp(-m*v*v / (2*kB*T));
}
// speeds(300, 28) → vp=422, vmean=476, vrms=517 m/s
```

温度が上がると分布は**右へ広がり、ピークは低く**なります（全体の面積＝確率は 1 で一定なので）。これが「高温の気体ほど反応が速い」分子論的な理由です。

![温度を上げると分布が広がりピークが下がる](/images/maxwell-boltzmann/slider-anim.gif)

## ツールで遊ぶ

[マクスウェル・ボルツマン分布シミュレーター](https://novasolver.jp/tools/maxwell-boltzmann.html)で試してほしい操作：

- **温度 T スライダー**を上げ、分布が広がり「v_p・⟨v⟩・v_rms」が $\sqrt{T}$ で増えるのを確認
- **分子量 M スライダー**を H₂(2)・He(4)・O₂(32) などに変え、軽い分子ほど速いことを見る
- **観測速度 v スライダー**と**確率窓幅 Δv**で、特定速度域にいる分子の割合を確認
- **温度比較グラフ**（T/2・T・2T）で分布の広がり方を比較
- **3 本の破線**（v_p 青・⟨v⟩ 緑・v_rms 橙）の順序が常に保たれることを確認
- 「P(V > v) 累積確率」で、ある速さを超える分子の割合を読む

## まとめ

- 速さ分布は $f(v) = 4\pi(m/2\pi k_B T)^{3/2} v^2 e^{-mv^2/2k_B T}$
- 3 つの速さは常に $v_p:\langle v\rangle:v_{\text{rms}} = 1:1.128:1.225$
- N₂ 300 K で 422 / 476 / 517 m/s、温度の平方根に比例
- 軽い分子ほど速い（H₂ は N₂ の約 3.7 倍）

ミクロな分子の乱雑な運動が描く美しい分布を、温度や分子量を変えながら体感してみてください。

🌡️ **[マクスウェル・ボルツマン分布シミュレーター（NovaSolver）](https://novasolver.jp/tools/maxwell-boltzmann.html)** で、気体分子の速さを確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。熱・統計では [混合エントロピー](https://novasolver.jp/tools/entropy-mixing.html)、[ファンデルワールス気体](https://novasolver.jp/tools/van-der-waals-gas.html)、[シュテファン・ボルツマンの法則](https://novasolver.jp/tools/stefan-boltzmann.html) もどうぞ。
