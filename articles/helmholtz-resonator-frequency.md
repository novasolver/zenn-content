---
title: "ビンを吹くとなぜ「ボー」と鳴る？ ヘルムホルツ共鳴をJavaScriptで計算する"
emoji: "🍶"
type: "tech"
topics: ["javascript", "物理シミュレーション", "波動", "音響", "可視化"]
published: true
---

![ヘルムホルツ共鳴器 — NovaSolver](/images/helmholtz-resonator/cover.png)

## 空のビンの口を吹くと鳴る、あの音の正体

空のビンの口に息を吹きかけると「ボー」と低い音が鳴ります。これが**ヘルムホルツ共鳴**。気柱の共鳴（定在波）とは違い、首の部分の空気が「おもり」、容器内の空気が「バネ」として働く**バネ-質量系の振動**です。スピーカーのバスレフポート、ギターの胴、自動車の消音器まで、低音の制御に幅広く使われています。

この記事では、ヘルムホルツ共鳴周波数を JavaScript で計算します。

🍶 **動くデモ**: [ヘルムホルツ共鳴器シミュレーター（NovaSolver）](https://novasolver.jp/tools/helmholtz-resonator.html)

## バネ-質量系としての共鳴

首の断面積 $A$、容積 $V$、実効首長 $L_{\text{eff}}$ とすると、共鳴周波数は

$$
f_H = \frac{c}{2\pi}\sqrt{\frac{A}{V\,L_{\text{eff}}}},\qquad A = \pi r_n^2
$$

ここで首の端では空気が外側にも少しはみ出すため、**端補正**を加えた実効長を使います。

$$
L_{\text{eff}} = L + 1.7\,r_n
$$

直感的には、首の空気（質量 $\propto L_{\text{eff}}$）が容器内の空気（バネ定数 $\propto 1/V$）の上で振動する系です。だから**容器が大きいほど（$V$ 大）低い音**になります（$f_H \propto 1/\sqrt{V}$）。

既定値（$V=1\,\mathrm{L}$、首径 $20\,\mathrm{mm}$、首長 $50\,\mathrm{mm}$、$c=343\,\mathrm{m/s}$）で計算すると、実効首長 $L_{\text{eff}} = 67\,\mathrm{mm}$、**共鳴周波数 $f_H = 118\,\mathrm{Hz}$**（波長 2.9 m）。容積を半分の $0.5\,\mathrm{L}$ にすると $f_H = 167\,\mathrm{Hz}$ へ上がります（$\sqrt 2$ 倍）。飲みかけのビンほど音が高くなる経験と一致します。

![共鳴器の構造（左, バネ-質量系）と容積に対する周波数（右）](/images/helmholtz-resonator/charts-closeup.png)

## JavaScript 実装

```javascript
function helmholtz(V_liters, neckDiam_mm, neckLen_mm, c = 343) {
  const V = V_liters * 1e-3;                 // L → m³
  const rn = (neckDiam_mm / 2) / 1000;       // mm → m（半径）
  const A = Math.PI * rn * rn;               // 首の断面積 [m²]
  const Leff = neckLen_mm / 1000 + 1.7 * rn; // 端補正込みの実効首長
  const f = (c / (2 * Math.PI)) * Math.sqrt(A / (V * Leff));
  return { f, Leff, wavelength: c / f };
}
// helmholtz(1.0, 20, 50) → f ≈ 118 Hz
```

気柱共鳴と違い、ヘルムホルツ共鳴は**1 つの低い基本周波数**だけを強く持ちます。波長（2.9 m）が容器サイズよりずっと大きい「集中定数系」近似が成り立つのがポイントです。

![容積を変えると共鳴周波数が 1/√V で変化する](/images/helmholtz-resonator/slider-anim.gif)

## ツールで遊ぶ

[ヘルムホルツ共鳴器シミュレーター](https://novasolver.jp/tools/helmholtz-resonator.html)で試してほしい操作：

- **キャビティ体積 V スライダー**を変え、$f_H \propto 1/\sqrt{V}$（大きいほど低音）を確認
- **ネック直径 d_n スライダー**を変え、断面積 $A$ が増えると周波数が上がるのを見る
- **ネック長 L スライダー**を変え、首が長いほど低音になるのを確認
- **「実効ネック長 L_eff」**で端補正（+1.7r）の効果を読む
- **「共鳴波長 λ・周期 T」**で波長が容器より大きい集中定数系であることを確認
- **f vs V グラフ（対数）**で 1/√V の傾きを観察

## まとめ

- ヘルムホルツ共鳴は首の空気（質量）＋容器の空気（バネ）の振動
- 共鳴周波数は $f_H = (c/2\pi)\sqrt{A/(V L_{\text{eff}})}$
- 端補正 $L_{\text{eff}} = L + 1.7r$ を加える
- 既定で 118 Hz、容積が大きいほど低音（$f \propto 1/\sqrt V$）

身近な「ビンの音」から音響設計まで使われる原理を、容積や首の寸法を変えながら体感してみてください。

🍶 **[ヘルムホルツ共鳴器シミュレーター（NovaSolver）](https://novasolver.jp/tools/helmholtz-resonator.html)** で、バネ-質量系の共鳴を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。波動・音響では [気柱の共鳴](https://novasolver.jp/tools/acoustic-resonance.html)、[うなり](https://novasolver.jp/tools/acoustic-beats.html)、[弦の共振](https://novasolver.jp/tools/string-resonance.html) もどうぞ。
