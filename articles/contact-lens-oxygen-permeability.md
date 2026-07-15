---
title: "コンタクトレンズの酸素透過率 Dk/t — 角膜が「呼吸」できる設計を数式で見る"
emoji: "👁️"
type: "tech"
topics: ["javascript", "物理シミュレーション", "可視化", "医療", "拡散"]
published: true
---

![コンタクトレンズの酸素透過率 Dk/t — NovaSolver](/images/contact-lens-oxygen-permeability/cover.png)

## 角膜は血管を持たず、大気から直接「呼吸」している

体の組織のほとんどは血液で酸素を受け取ります。ところが**角膜には血管がありません**。透明性を保つためで、その代わり酸素は大気（酸素分圧 約 155 mmHg、濃度 21%）から涙液層を介して、**拡散だけ**で角膜に届きます。

ここにコンタクトレンズを乗せると、酸素はまずレンズ材料を通り抜けなければなりません。レンズがどれだけ酸素を通すかを表すのが、本記事の主役 **Dk/t（酸素透過率, oxygen transmissibility）** です。

この記事では：

1. 酸素透過係数 $D_k$ と透過率 $D_k/t$ の違い
2. Holden-Mertz の臨床基準（24 / 87 / 125）が何を意味するか
3. 拡散モデルから等価酸素濃度 EOP を求める ~25 行の JavaScript
4. 標準的なシリコーンハイドロゲルレンズを数値で検証する

👁️ **動くデモ**: [コンタクトレンズ酸素透過率シミュレーター（NovaSolver）](https://novasolver.jp/tools/contact-lens-oxygen-permeability.html)

## Dk と Dk/t は別物

混同しやすいので最初に整理します。

| 記号 | 名前 | 意味 |
|---|---|---|
| $D_k$ | 酸素透過係数 | **材料そのもの**の酸素の通しやすさ |
| $t$ | 中心肉厚 | レンズ中央の厚さ（mm） |
| $D_k/t$ | 酸素透過率 | **そのレンズ**が実際に通す量 |

$D_k$ は拡散係数 $D$ と溶解度 $k$ の積で、単位は $10^{-11}\,(\mathrm{cm^2/s})\cdot(\mathrm{mL\,O_2}/\mathrm{mL\cdot mmHg})$（通称 barrer）です。同じ材料でも、レンズを薄くすれば角膜に届く酸素は増えます。だから角膜健康を直接決めるのは、$D_k$ を肉厚で割った

$$
\frac{D_k}{t}
$$

のほう。フィックの拡散則で、定常状態の酸素フラックスが膜厚に反比例することの素直な帰結です。

## カオスではなく、臨床で決まった「合格ライン」

$D_k/t$ がいくつあれば角膜が低酸素にならないか——これは理論だけでなく**臨床研究**で境界値が決まっています。

- **Holden & Mertz (1984)**：起きている間だけの装用（デイリーウェア）で $D_k/t > 24$、寝ている間も付けたまま（連続装用）で $D_k/t > 87$ を最低ライン
- **Harvitt & Bonanno (1999)**：就寝時の角膜浮腫（むくみ）を生理的限界の 4% 以下に抑えるには $D_k/t > 125$ が望ましい、と酸素分圧の数値モデルで提示

オルソケラトロジー（夜間に角膜を矯正するハードレンズ）は閉瞼下での装用が前提なので、125 以上を狙うのが安全側です。本ツールはこの 24 / 87 / 125 の 3 本のラインを棒グラフで描き、選んだ装用モードに対する適否を自動判定します。

![Dk vs 含水率と、装用モード別の Dk/t 要求ライン](/images/contact-lens-oxygen-permeability/charts-closeup.png)

## 拡散モデルから EOP を求める

角膜表面に届く酸素を「もし大気にさらした場合と同じになる酸素濃度」に換算したものを **EOP（Equivalent Oxygen Percentage, 等価酸素濃度）** と呼びます。$D_k/t$ が大きいほど EOP は大気の 21% に漸近し、低いほど 0 に近づく——この飽和曲線を指数関数で近似します。

$$
\mathrm{EOP} \approx 21\%\cdot\left[1 - e^{-\,(D_k/t)\,/\,30}\right]
$$

同様に、装用時の推定角膜浮腫も $D_k/t$ が上がるほど指数的に消えていくモデルにします。これを素直に JavaScript にすると ~25 行です：

```javascript
// 材料プリセット（Dk_max と含水依存性）
const matProps = {
  "silicone-hydrogel": { Dk_max: 175, waterFactor: 0.5 },
  "hema":              { Dk_max: 25,  waterFactor: 0.85 },
  "rigid-gas":         { Dk_max: 100, waterFactor: 0 },
};

function evaluate(mat, t, WC, mode) {
  const m = matProps[mat];
  // シリコーンハイドロゲル: 含水率が下がっても Dk は大きく落ちない
  let Dk = (mat === "silicone-hydrogel")
    ? m.Dk_max * (1 - m.waterFactor * (1 - WC / 100))
    : m.Dk_max;
  const Dk_t = (Dk / t) * 0.1;            // ISO 形式 (×10^-9) へ換算
  const EOP = Math.min(21, 21 * (1 - Math.exp(-Dk_t / 30)));
  const swell = Math.max(0,
      4 * Math.exp(-Dk_t / 30) - (mode === "extended" ? 0 : 1));
  return {
    Dk: Dk.toFixed(0), Dk_t: Dk_t.toFixed(0),
    EOP: EOP.toFixed(1), swell: swell.toFixed(1),
    daily: Dk_t > 24, ext: Dk_t > 87, noSwell: Dk_t > 125,
  };
}

console.log(evaluate("silicone-hydrogel", 0.10, 38, "daily"));
// { Dk: '121', Dk_t: '121', EOP: '20.6', swell: '0.0',
//   daily: true, ext: true, noSwell: false }
```

## 標準的なレンズを数値で検証する

代表的なシリコーンハイドロゲル（$D_{k,\max}=175$、含水率 38%）を中心肉厚 0.10 mm で作ると、含水率補正を入れた酸素透過係数は

$$
D_k = 175\cdot\left[1 - 0.5\cdot\left(1 - \tfrac{38}{100}\right)\right] = 120.75
$$

となり、透過率は $D_k/t \approx 121$。EOP は 20.6% で大気の 21% にほぼ届きます。装用モード別に見ると：

| 装用モード | 基準 $D_k/t$ | このレンズ（121） |
|---|---|---|
| デイリー (8h) | $> 24$ | ✅ 余裕で合格 |
| 連続装用 (24h+) | $> 87$ | ✅ 合格 |
| オルソK・無浮腫 | $> 125$ | ❌ あと一歩 |

つまり「日中の使い捨てとしては申し分ないが、夜通し付けて浮腫ゼロを狙うにはわずかに足りない」という設計点です。ここで肉厚を 0.07 mm まで薄くすると $D_k/t \approx 173$ に跳ね上がり、125 の壁も越えます。**肉厚は透過率に反比例で効く**ことが数値で実感できます。

> 補足：$D_k/t$ はあくまで角膜健康の**必要条件**で、十分条件ではありません。実際の浮腫は瞬きによる涙液交換やドライアイ、装用時間でも変わります。

## ツールで遊ぶ

NovaSolver のシミュレーターでは、材料・肉厚・含水率・装用モードを動かすと、Dk/t と EOP、Holden-Mertz 基準への適合、推定浮腫がリアルタイムで更新されます。角膜断面のアニメーションでは、酸素分子が大気→レンズ→涙液層→角膜へ拡散する様子と、現在の Dk/t に応じた浮腫レベルが色で表示されます。

![肉厚スライダーを動かすと Dk/t と浮腫が変化する](/images/contact-lens-oxygen-permeability/slider-anim.gif)

試してほしい操作：

- **材料セレクト**で「シリコーンハイドロゲル」「HEMA ハイドロゲル」「ハードGP」「ハイブリッド」を切り替え、Dk の出方の違いを見る
- **中心肉厚 t スライダー**を 0.10 → 0.07 mm に薄くして、Dk/t が 125 の壁を越える瞬間を探す
- **装用モードセレクト**を「デイリー / 連続装用 / オルソK 夜間」で切り替え、判定（verdict）がどう変わるか見る
- **含水率 WC スライダー**で材料ごとの含水依存性を比較する
- **「装用モード別 Dk/t 要求」棒グラフ**で、自分の設計点が 24 / 87 / 125 のどこに立っているか確認する

## まとめ

- 角膜は血管を持たず、酸素は大気から拡散だけで届く。レンズの通しやすさが $D_k/t$
- $D_k$ は材料の係数、$D_k/t$ は肉厚で割った実効値。**薄いほど有利**（反比例）
- 臨床基準は Holden-Mertz の $D_k/t > 24$（デイリー）/ $> 87$（連続装用）、Harvitt-Bonanno の $> 125$（無浮腫）
- 標準的な Si-Hy（Dk 121, t=0.10mm）は $D_k/t \approx 121$、EOP 20.6%。デイリー・連続装用は合格、無浮腫の 125 はわずかに未達

「材料を薄く・高 Dk に」というレンズ設計のセオリーが、フィックの拡散則と臨床基準だけで定量的に説明できる——それがこのテーマの面白さです。

👁️ **[コンタクトレンズ酸素透過率シミュレーター（NovaSolver）](https://novasolver.jp/tools/contact-lens-oxygen-permeability.html)** で、肉厚を動かして Dk/t が基準ラインを越える瞬間を見てみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。拡散・輸送現象では [熱拡散シミュレーター](https://novasolver.jp/tools/heat-diffusion.html)、[フィンの熱伝達](https://novasolver.jp/tools/fin-heat-transfer.html)、[レイノルズ数](https://novasolver.jp/tools/reynolds-number.html) なども揃えています。
