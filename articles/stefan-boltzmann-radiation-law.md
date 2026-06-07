---
title: "シュテファン・ボルツマンの法則 E=σT⁴ — 温度が2倍で放射は16倍になる理由"
emoji: "🔆"
type: "tech"
topics: ["javascript", "物理シミュレーション", "熱力学", "可視化", "数値計算"]
published: false
---

![シュテファン・ボルツマンの法則 — NovaSolver](/images/stefan-boltzmann/cover.png)

## 熱い物体はなぜ「光って」見えるのか

電気ストーブやろうそくの炎、溶けた鉄――温度が高い物体は赤く、さらに高温になると白く輝きます。あらゆる物体は温度に応じて電磁波（熱放射）を出しており、その総量を支配するのが**シュテファン・ボルツマンの法則** $E = \varepsilon\sigma T^4$ です。温度の **4 乗**に比例するため、温度がわずかに上がるだけで放射は爆発的に増えます。

この記事では、放射発散度とピーク波長を JavaScript で計算します。

🔆 **動くデモ**: [シュテファン・ボルツマンシミュレーター（NovaSolver）](https://novasolver.jp/tools/stefan-boltzmann.html)

## T⁴ の法則とウィーンの変位則

黒体（$\varepsilon=1$）が単位面積あたり放射する全パワーは次式です。

$$
E = \varepsilon\sigma T^4,\qquad \sigma = 5.67\times10^{-8}\,\mathrm{W/(m^2 K^4)}
$$

$\sigma$ はシュテファン・ボルツマン定数。さらに、放射が最も強くなる波長は**ウィーンの変位則**で決まります。

$$
\lambda_{\max} = \frac{2898}{T}\,[\mu\mathrm{m}]
$$

黒体（$T=1000\,\mathrm{K}$, $\varepsilon=1$, $A=1\,\mathrm{m^2}$）で計算すると、**放射発散度 $E = 56{,}704\,\mathrm{W/m^2} \approx 56.7\,\mathrm{kW/m^2}$**、ピーク波長 $\lambda_{\max} = 2.898\,\mathrm{\mu m}$（赤外）。温度を 2 倍の 2000 K にすると $E$ は $2^4 = 16$ 倍の約 907 kW/m² に跳ね上がり、ピーク波長は半分の 1.45 μm へ短くなります（より青い側へ）。これが「高温ほど明るく、色が変わる」正体です。

周囲温度 $T_{\text{env}}$ がある場合の正味放射は $Q_{\text{net}} = \varepsilon\sigma A(T^4 - T_{\text{env}}^4)$。1000 K の物体が 300 K の環境へ出す正味パワーは約 56.2 kW で、自分の放射がほとんどを占めます（環境からの戻りは小さい）。

![プランク曲線（左, 高温ほど短波長へ）と放射発散度 vs 温度（右, 対数）](/images/stefan-boltzmann/charts-closeup.png)

## JavaScript 実装

```javascript
const SIGMA = 5.670374419e-8;  // W/(m²·K⁴)
function radiation(T, eps, A, Tenv) {
  const E    = eps * SIGMA * Math.pow(T, 4);                  // 放射発散度 [W/m²]
  const Q    = E * A;                                         // 全放射パワー [W]
  const lamMax = 2898 / T;                                    // ウィーンの変位則 [μm]
  const Qnet = eps * SIGMA * A * (Math.pow(T,4) - Math.pow(Tenv,4)); // 正味交換 [W]
  return { E, Q, lamMax, Qnet };
}
// radiation(1000, 1.0, 1.0, 300) → E=56704 W/m², λ_max=2.898 μm
```

放射率 $\varepsilon$ は表面の性質で、黒体は 1.0、磨いたアルミは 0.05 程度、人肌は約 0.95。同じ温度でも $\varepsilon$ が小さい鏡面は放射が少なく、だから魔法瓶の内側は銀メッキされています。

![温度を上げるとプランク曲線が成長しピークが短波長へ移る](/images/stefan-boltzmann/slider-anim.gif)

## ツールで遊ぶ

[シュテファン・ボルツマンシミュレーター](https://novasolver.jp/tools/stefan-boltzmann.html)で試してほしい操作：

- **表面温度 T スライダー**を上げ、「放射発散度 E」が $T^4$ で急増するのを確認（対数グラフで直線的）
- **「黒体」「鏡面Al」「人肌」プリセット**で放射率 ε の違いによる放射量を比較
- **ピーク波長 λ_max** がウィーンの変位則で温度に反比例するのを見る
- **「正味交換」モード**に切り替え、環境温度 T_env を変えて $Q_{\text{net}}$ を確認
- **面積 A スライダー**で全放射パワー Q がスケールするのを見る
- **プランク曲線**で温度を上げるとピークが短波長（赤→青）へ移るのを観察

## まとめ

- 放射発散度は $E = \varepsilon\sigma T^4$、温度の 4 乗に比例
- 温度 2 倍で放射は 16 倍に増える
- ピーク波長は $\lambda_{\max} = 2898/T$（ウィーンの変位則）
- 黒体 1000 K で 56.7 kW/m²、ピーク 2.9 μm（赤外）

宇宙の温度測定から保温技術まで支えるこの法則を、温度や放射率を変えながら体感してみてください。

🔆 **[シュテファン・ボルツマンシミュレーター（NovaSolver）](https://novasolver.jp/tools/stefan-boltzmann.html)** で、熱放射の温度依存性を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。熱・放射では [黒体放射](https://novasolver.jp/tools/blackbody-radiation.html)、[マクスウェル・ボルツマン分布](https://novasolver.jp/tools/maxwell-boltzmann.html)、[熱拡散](https://novasolver.jp/tools/heat-diffusion.html) もどうぞ。
