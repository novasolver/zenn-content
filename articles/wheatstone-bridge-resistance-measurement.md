---
title: "ホイートストンブリッジで微小抵抗変化を測る — 平衡条件R1R4=R2R3をJavaScriptで"
emoji: "⚖️"
type: "tech"
topics: ["javascript", "電気回路", "計測", "可視化", "数値計算"]
published: false
---

![ホイートストンブリッジ — NovaSolver](/images/wheatstone-bridge/cover.png)

## ひずみゲージや温度センサーの心臓部

体重計、圧力センサー、温度計――これらの内部では、わずかな抵抗変化を高精度に電圧へ変換する**ホイートストンブリッジ**が働いています。4 つの抵抗をダイヤモンド型に組み、対角の電圧差を読むだけ。**平衡状態では出力がぴたり 0** になるので、その 0 点からのわずかなズレを増幅すれば、ppm レベルの抵抗変化も検出できます。

この記事では、ブリッジの出力電圧と平衡条件を JavaScript で計算します。

⚖️ **動くデモ**: [ホイートストンブリッジシミュレーター（NovaSolver）](https://novasolver.jp/tools/wheatstone-bridge.html)

## 出力電圧と平衡条件

ブリッジは 2 つの分圧回路の差を取ります。励起電圧 $V_{in}$ に対する出力は

$$
V_{out} = V_{in}\left(\frac{R_2}{R_1+R_2} - \frac{R_4}{R_3+R_4}\right)
= V_{in}\,\frac{R_2 R_3 - R_1 R_4}{(R_1+R_2)(R_3+R_4)}
$$

分子が 0 になる条件が**平衡条件**で、未知抵抗を高精度に求める基礎です。

$$
R_1 R_4 = R_2 R_3 \;\Longleftrightarrow\; R_4 = \frac{R_2 R_3}{R_1}
$$

既定値（$R_1 = R_2 = R_3 = 1000\,\Omega$、$R_4 = 1010\,\Omega$、$V_{in} = 5\,\mathrm{V}$）はひずみゲージに約 1% の変化を与えた状態。計算すると **出力電圧 $V_{out} = -12.44\,\mathrm{mV}$**、感度 $-2.49\,\mathrm{mV/V}$。平衡値は $R_4 = R_2 R_3/R_1 = 1000\,\Omega$ なので、$R_4$ を 1000 Ω に戻すと **$V_{out} = 0$** になります。この 0 点を基準に微小変化を測るのがブリッジの真骨頂です。

![ブリッジ回路（左, R4=1010Ωで不平衡）と R4 に対する出力電圧（右）](/images/wheatstone-bridge/charts-closeup.png)

## JavaScript 実装

```javascript
const Vin = 5.0;
function bridge(R1, R2, R3, R4) {
  const d1 = R2 / (R1 + R2);              // 分圧比（左）
  const d2 = R4 / (R3 + R4);              // 分圧比（右）
  const Vout = Vin * (d1 - d2);           // 出力電圧 [V]
  const R4balance = R2 * R3 / R1;         // 平衡となる R4
  return {
    Vout_mV: Vout * 1000,
    sensitivity_mVperV: (Vout / Vin) * 1000,
    R4balance,
    deltaR4: R4 - R4balance,
  };
}
// bridge(1000, 1000, 1000, 1010) → Vout=-12.44mV, balance R4=1000Ω, ΔR4=+10Ω
```

ひずみゲージでは、ゲージ率 $G_F$ とひずみ $\varepsilon$ に対して $\Delta R/R = G_F\varepsilon$。1 ゲージ構成なら出力は $V_{out}/V_{in} \approx (G_F/4)\varepsilon$ となり、ブリッジがひずみを電圧へ線形変換するセンサーになります。

![R4 を変えると出力電圧が平衡点（0）を横切る](/images/wheatstone-bridge/slider-anim.gif)

## ツールで遊ぶ

[ホイートストンブリッジシミュレーター](https://novasolver.jp/tools/wheatstone-bridge.html)で試してほしい操作：

- **抵抗 R1〜R4 スライダー**を変え、出力電圧 $V_{out}$ がどう動くか観察
- **「R4を平衡値に」ボタン**で $R_4 = R_2 R_3/R_1$ にし、出力が 0（平衡）になるのを確認
- **「不平衡量 ΔR4」**で平衡点からのズレを読む
- R4 を平衡値からわずかに動かし、微小変化が mV の出力に増幅されるのを見る
- **回路図**でブリッジが平衡（緑）か不平衡（赤）かを確認
- **Vout vs R4 グラフ**で出力が平衡点で 0 を横切る直線的な応答を読む

## まとめ

- ブリッジ出力は $V_{out} = V_{in}(R_2/(R_1+R_2) - R_4/(R_3+R_4))$
- 平衡条件は $R_1 R_4 = R_2 R_3$、このとき出力 0
- 既定（R4=1010Ω）で $V_{out} = -12.44\,\mathrm{mV}$、平衡 R4=1000Ω
- 0 点基準で微小抵抗変化を高精度に検出できる

センサー計測の基礎回路を、抵抗値を変えながら体感してみてください。

⚖️ **[ホイートストンブリッジシミュレーター（NovaSolver）](https://novasolver.jp/tools/wheatstone-bridge.html)** で、平衡条件と微小変化の検出を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。電気回路では [RLC共振回路](https://novasolver.jp/tools/rlc-resonance.html)、[ハイパスフィルタ](https://novasolver.jp/tools/high-pass-filter.html)、[RC/RL回路](https://novasolver.jp/tools/rc-rl-circuit.html) もどうぞ。
