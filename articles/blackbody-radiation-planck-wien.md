---
title: "黒体放射 — プランク分布・ウィーン変位則・Stefan-Boltzmann則"
emoji: "🔥"
type: "tech"
topics: ["javascript", "物理シミュレーション", "熱力学", "量子", "可視化"]
published: false
---

![黒体放射とプランク分布 — NovaSolver](/images/blackbody-radiation/cover.png)

## 熱い物体はなぜ「赤→白→青」と色が変わるのか

鉄を熱すると、暗い赤からオレンジ、黄色、そして白く輝きます。星の色も、赤い星は低温、青白い星は高温。温度だけで物体が放つ光の色が決まる——この**黒体放射**の法則は、19 世紀末の物理学最大の難問でした。古典論では説明できず、1900 年にプランクが「エネルギーは飛び飛びの値しかとれない」と仮定して初めて解決——これが**量子論の誕生**です。

この記事ではプランクの放射法則と、そこから導かれるウィーン変位則・Stefan-Boltzmann 則を、JavaScript のスペクトル計算とともに見ていきます。

🔥 **動くデモ**: [黒体放射・プランク分布シミュレーター（NovaSolver）](https://novasolver.jp/tools/blackbody-radiation.html)

## プランクの放射法則

温度 $T$ の黒体が波長 $\lambda$ で放つ分光放射輝度は、プランクの法則で与えられます。

$$
B_\lambda(T) = \frac{2hc^2}{\lambda^5}\cdot\frac{1}{e^{hc/\lambda kT} - 1}
$$

$h$ はプランク定数、$c$ は光速、$k$ はボルツマン定数。鍵は分母の指数関数で、これが短波長側で発散を抑え、古典論の「紫外破綻（UV catastrophe）」を解消します。プランクはこの式を導くためにエネルギーの量子化 $E=h\nu$ を持ち込みました。

このスペクトルから、2 つの重要な法則が導けます。

## ウィーンの変位則：ピーク波長は温度に反比例

スペクトルがピークになる波長 $\lambda_{\max}$ は温度に反比例します。

$$
\lambda_{\max} T = 2.898\times10^{-3}\,\mathrm{m\cdot K}
$$

温度が高いほどピークが短波長（青）側へ移動する——これが「赤→白→青」の正体です。代表的な温度で計算すると：

| 物体 | 温度 | ピーク波長 | 領域 |
|---|---|---|---|
| 人体 | 310 K | 9348 nm | 遠赤外 |
| 白熱電球 | 2700 K | 1073 nm | 近赤外 |
| 太陽 | 5778 K | **502 nm** | 可視光（緑） |
| 青色星 | 10000 K | 290 nm | 紫外 |

**太陽のピークがちょうど可視光の真ん中**に来ているのは偶然ではなく、私たちの目がその光に適応して進化したためです。白熱電球がピーク 1073 nm（赤外）で、可視光に出るエネルギーがわずかなのは、白熱灯が非効率（大半が熱）な理由でもあります。

![温度ごとのプランク分布（左）と、ウィーン変位則（右）](/images/blackbody-radiation/charts-closeup.png)

## Stefan-Boltzmann 則：総放射は温度の4乗

スペクトル全体を積分した**総放射エネルギー**は、温度の **4乗**に比例します。

$$
P = \sigma T^4,\qquad \sigma = 5.67\times10^{-8}\,\mathrm{W/m^2K^4}
$$

太陽（5778 K）なら $P=\sigma T^4 \approx 6.3\times10^7\,\mathrm{W/m^2}$（63 MW/m²）。温度を 2 倍にすると放射は **16 倍**——だから高温の星は桁違いに明るく、わずかな温度上昇が放熱に大きく効きます。

## JavaScript 実装

プランク関数とその応用法則はそのまま実装できます。

```javascript
const h = 6.626e-34, c = 3e8, k = 1.381e-23, sigma = 5.67e-8;
function planck(lam_nm, T) {
  const lam = lam_nm * 1e-9;
  const exp = Math.exp(h*c / (lam*k*T));
  return (2*h*c*c / Math.pow(lam, 5)) / (exp - 1);   // 分光放射輝度
}
function wienPeak(T) { return 2.898e-3 / T * 1e9; }   // ピーク波長 [nm]
function stefanTotal(T) { return sigma * Math.pow(T, 4); }  // 総放射 [W/m²]
```

![温度を上げると分布が明るく短波長側へ移る](/images/blackbody-radiation/slider-anim.gif)

## ツールで遊ぶ

[黒体放射・プランク分布シミュレーター](https://novasolver.jp/tools/blackbody-radiation.html)で試してほしい操作：

- **温度 T スライダー**を上げ、スペクトルが**明るく・短波長側へ**移る（ウィーン変位則）のを見る
- **プリセット**「人体」「白熱灯」「太陽」「青色星」「X線源」を切り替え、ピーク波長の違いを比較
- **「曲線を追加」**で複数温度のスペクトルを重ねて表示（最大5本）
- **計算結果**の「ピーク波長」「全放射」を読み、温度を2倍にすると全放射が16倍（$T^4$）になることを確認
- **可視帯ハイライト**をオンにして、太陽のピークが可視光に入る一方、白熱灯は赤外に偏ることを観察
- **log/linear 切替**でスペクトルの形を見比べる

## まとめ

- 黒体放射は**プランクの法則** $B_\lambda=\frac{2hc^2}{\lambda^5}\frac{1}{e^{hc/\lambda kT}-1}$ で記述（量子論の出発点）
- **ウィーン変位則** $\lambda_{\max}T=2.898\times10^{-3}$：温度が高いほどピークは短波長（青）へ
- 太陽のピーク 502 nm は可視光の真ん中。白熱灯は赤外に偏り非効率
- **Stefan-Boltzmann 則** $P=\sigma T^4$：総放射は温度の4乗（温度2倍で16倍）

熱放射・天体物理・放射温度計・地球の放射収支の基礎となる黒体放射を、温度を変えながら体感してみてください。

🔥 **[黒体放射・プランク分布シミュレーター（NovaSolver）](https://novasolver.jp/tools/blackbody-radiation.html)** で、温度が決める光の色を見てみましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。熱・量子系では [2D熱拡散](https://novasolver.jp/tools/heat-diffusion.html)、[カルノーサイクル](https://novasolver.jp/tools/carnot-cycle.html)、[光電効果](https://novasolver.jp/tools/photoelectric-effect.html) なども揃えています。
