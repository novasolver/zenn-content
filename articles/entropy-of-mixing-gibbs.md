---
title: "混合エントロピー ΔS=−nRΣx ln x をJavaScriptで — なぜ気体は勝手に混ざるのか"
emoji: "⚗️"
type: "tech"
topics: ["javascript", "熱力学", "統計力学", "可視化", "数値計算"]
published: true
---

![混合エントロピー — NovaSolver](/images/entropy-mixing/cover.png)

## 仕切りを外すと、気体は二度と分かれない

容器を仕切って左に赤い気体、右に青い気体を入れ、仕切りを抜く。すると 2 つの気体は自然に混ざり合い、放っておいても二度と元のように分かれません。エネルギーは何も変わっていないのに（理想気体の混合は発熱も吸熱もしない）、なぜ一方向にしか進まないのか――その答えが**混合エントロピー**です。

この記事では、混合エントロピーを JavaScript で計算し、「混ざるほどエントロピーが増える」ことを確かめます。

⚗️ **動くデモ**: [混合エントロピーシミュレーター（NovaSolver）](https://novasolver.jp/tools/entropy-mixing.html)

## 混合エントロピーの式

理想気体を混合したときのエントロピー増加は、モル分率 $x_i$ を使って次式で表されます。

$$
\Delta S_{\text{mix}} = -nR\sum_i x_i \ln x_i
$$

$n$ は全モル数、$R = 8.314\,\mathrm{J/(mol\,K)}$。$x_i < 1$ なので $\ln x_i < 0$、つまり $\Delta S_{\text{mix}} > 0$ で**必ず増加**します。等温・等圧で自発的に進む条件 $\Delta G < 0$ も、$\Delta G_{\text{mix}} = -T\Delta S_{\text{mix}} < 0$ から保証されます。

3 成分の既定値（$n=1$、$x_1=0.50$、$x_2=0.30$、$x_3=0.20$、$T=298\,\mathrm{K}$）で計算すると、$\Delta S_{\text{mix}} = 8.56\,\mathrm{J/K}$、$\Delta G_{\text{mix}} = -2.55\,\mathrm{kJ}$。最大値は等量混合（$x_i = 1/3$）のときの $\Delta S_{\max} = nR\ln 3 = 9.13\,\mathrm{J/K}$ で、既定の組成はその **93.7%** に達しています。

![二成分の混合エントロピー曲線（左, x=0.5で最大）と3成分の寄与（右）](/images/entropy-mixing/charts-closeup.png)

## JavaScript 実装

```javascript
const R = 8.314;  // J/(mol·K)
function entropyOfMixing(n, fractions, T) {
  let sum = 0;
  for (const x of fractions) {
    if (x > 0) sum += x * Math.log(x);   // 自然対数 ln
  }
  const dS = -n * R * sum;               // ΔS_mix [J/K]
  const dG = -T * dS / 1000;             // ΔG_mix [kJ]
  const dSmax = n * R * Math.log(fractions.length);  // 等量混合の最大値
  return { dS, dG, dSmax, ratio: dS / dSmax };
}
// 例: entropyOfMixing(1, [0.5, 0.3, 0.2], 298) → ΔS=8.56 J/K
```

二成分（$x, 1-x$）なら $\Delta S/R = -[x\ln x + (1-x)\ln(1-x)]$ で、$x=0.5$ のとき $nR\ln 2 = 5.76\,\mathrm{J/K}$ と最大になります。「半々が一番混ざっている」という直感と一致します。

> ギブズのパラドックス：もし左右が**同じ気体**なら、仕切りを抜いても状態は変わらずエントロピーは増えません（$\Delta S = 0$）。混合エントロピーが生じるのは**異なる種類**の粒子のときだけ、というのが量子的な区別不可能性の帰結です。

![仕切りを外すと2気体が混ざり、エントロピーが増大する](/images/entropy-mixing/slider-anim.gif)

## ツールで遊ぶ

[混合エントロピーシミュレーター](https://novasolver.jp/tools/entropy-mixing.html)で試してほしい操作：

- **モル分率 x₁, x₂ スライダー**を動かし、「ΔS_mix」がどう変わるか観察（$x_3 = 1-x_1-x_2$ は自動計算）
- 組成を**等量（1/3 ずつ）**に近づけ、「ΔS / ΔS_max」が 100% に近づくのを確認
- **温度 T スライダー**を変え、ΔS_mix は不変なのに **ΔG_mix だけが変わる**ことを確認（ΔG=−TΔS）
- **全モル数 n スライダー**で ΔS が比例して増えるのを見る
- **三角ダイヤグラム**で組成と等エントロピー線の位置関係を読む
- 一成分に極端に偏らせ、混合エントロピーが小さくなるのを確認

## まとめ

- 混合エントロピーは $\Delta S_{\text{mix}} = -nR\sum x_i \ln x_i$、常に正
- 自発混合は $\Delta G_{\text{mix}} = -T\Delta S_{\text{mix}} < 0$ から保証される
- 既定（3 成分）で ΔS=8.56 J/K、最大の 93.7%
- 等量混合で最大（3 成分なら $nR\ln 3 = 9.13$、2 成分なら $nR\ln 2 = 5.76$）

「なぜ自然は混ざる方向に進むのか」を、組成を変えながら体感してみてください。

⚗️ **[混合エントロピーシミュレーター（NovaSolver）](https://novasolver.jp/tools/entropy-mixing.html)** で、エントロピー増大の法則を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。熱・統計では [マクスウェル・ボルツマン分布](https://novasolver.jp/tools/maxwell-boltzmann.html)、[カルノーサイクル](https://novasolver.jp/tools/carnot-cycle.html)、[ファンデルワールス気体](https://novasolver.jp/tools/van-der-waals-gas.html) もどうぞ。
