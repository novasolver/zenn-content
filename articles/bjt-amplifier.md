---
title: "BJTアンプCE/CB/CC — 3構成の電圧利得とボード線図を小信号モデルで読む"
emoji: "📻"
type: "tech"
topics: ["javascript", "電子回路", "アナログ", "可視化", "電子工学"]
published: false
---

![BJTアンプの交流小信号解析 — NovaSolver](/images/bjt-amplifier/cover.png)

## BJTアンプの3つの「つなぎ方」

トランジスタ（BJT）1石でも、信号の入り口と出口をどの端子にするかで、性格のまったく違う増幅回路が3種類できあがります。

- **コモンエミッタ（CE）**: ベース入力・コレクタ出力。大きな電圧利得を持つが位相が反転する
- **コモンベース（CB）**: エミッタ入力・コレクタ出力。入力インピーダンスが低く高周波に強い
- **コモンコレクタ（CC / エミッタフォロワ）**: ベース入力・エミッタ出力。利得はほぼ1だがバッファとして優秀

この記事では、BJTの**小信号等価モデル**から3構成の電圧利得・入出力インピーダンス・周波数特性（ボード線図）を導き、数値で確かめていきます。式はすべて NovaSolver のシミュレーターが内部で使っているものと同じで、載せている数値も Python で実測したものです。

📐 **動くデモ**: [BJTアンプ交流特性 解析シミュレーター（NovaSolver）](https://novasolver.jp/tools/bjt-amplifier.html)

## まず3つの小信号パラメータ

交流（小信号）解析の出発点は、直流動作点（バイアス点）で決まる3つのパラメータです。

$$
g_m = \frac{I_C}{V_T},\quad r_\pi = \frac{\beta}{g_m},\quad r_o = \frac{V_A}{I_C}
$$

- $g_m$（相互コンダクタンス）: ベース電圧の変化がコレクタ電流をどれだけ動かすか。利得の源泉
- $r_\pi$: ベース–エミッタ間の小信号抵抗。入力インピーダンスに効く
- $r_o$: コレクタ側の出力抵抗。アーリー電圧 $V_A$ から決まる

ここで $V_T$ は熱電圧で、室温では約 $26\,\mathrm{mV}$ です。標準的な動作点 $I_C = 1\,\mathrm{mA},\ \beta = 100,\ V_A = 100\,\mathrm{V}$ を代入すると：

$$
g_m = \frac{1\,\mathrm{mA}}{26\,\mathrm{mV}} = 38.5\,\mathrm{mA/V},\quad
r_\pi = \frac{100}{38.5\,\mathrm{mA/V}} = 2.6\,\mathrm{k\Omega},\quad
r_o = \frac{100\,\mathrm{V}}{1\,\mathrm{mA}} = 100\,\mathrm{k\Omega}
$$

注目すべきは $g_m = I_C/V_T$ という比例関係です。**コレクタ電流を増やすほど $g_m$ が大きくなり、利得が上がる**——後で数値で見ます。

## 3構成の利得とインピーダンス

小信号モデルから各構成の式は次のように整理できます（$R_C\|R_L$ は並列合成）。

| 構成 | 電圧利得 $A_v$ | 入力 $Z_{in}$ | 出力 $Z_{out}$ |
|---|---|---|---|
| CE | $-g_m(R_C\|R_L\|r_o)$ | $R_B\|r_\pi$ | $R_C\|r_o$ |
| CB | $+g_m(R_C\|R_L\|r_o)$ | $1/g_m$ | $R_C\|r_o$ |
| CC | $\dfrac{g_m(R_E\|R_L)}{1+g_m(R_E\|R_L)}\approx +1$ | $R_B\|\beta R_E$ | $\approx 1/g_m$ |

CE の利得に付くマイナス符号が「位相反転」です。CB は同じ大きさでも符号が正（非反転）。CC は利得が1未満ですが、入力インピーダンスが高く出力インピーダンスが $1/g_m$ と低い——これが「バッファ」として効く理由です。

標準パラメータ（$R_C=3.3\,\mathrm{k\Omega},\ R_L=10\,\mathrm{k\Omega},\ R_E=1\,\mathrm{k\Omega},\ R_B=20\,\mathrm{k\Omega}$、エミッタバイパスあり）で Python に計算させると：

| 構成 | $A_v$ | $A_v$ [dB] | $Z_{in}$ | $Z_{out}$ |
|---|---|---|---|---|
| CE | $-93.1$ | $39.4$ | $2.30\,\mathrm{k\Omega}$ | $3.20\,\mathrm{k\Omega}$ |
| CB | $+93.1$ | $39.4$ | $26\,\Omega$ | $3.20\,\mathrm{k\Omega}$ |
| CC | $+0.97$ | $-0.2$ | $16.5\,\mathrm{k\Omega}$ | $25\,\Omega$ |

CE と CB が同じ $39.4\,\mathrm{dB}$ の利得を出すのに、CB の入力インピーダンスは $1/g_m = 26\,\Omega$ しかありません。一方 CC は利得こそ約1ですが、$Z_{in}=16.5\,\mathrm{k\Omega}$／$Z_{out}=25\,\Omega$ という極端なインピーダンス変換をこなします。

## 25行で書く小信号ソルバー

3構成の交流特性は、ブラウザでもこれだけのコードで計算できます。NovaSolver のツールと同じロジックです：

```javascript
const VT = 0.026; // 熱電圧 26mV

function calcAC(p) {
  const { ic, beta, rc, rl, re, rb, va, config, bypass } = p;
  const gm  = ic / VT;          // 相互コンダクタンス
  const rpi = beta / gm;        // ベース-エミッタ間抵抗
  const ro  = va / ic;          // アーリー効果の出力抵抗
  const reEff = bypass ? 0 : re; // バイパスONでREは交流的に短絡
  let av, zin, zout;
  if (config === "CE") {
    const rcP = 1 / (1/rc + 1/rl + 1/ro);     // RC || RL || ro
    av   = -gm * rcP / (1 + gm * reEff);       // 位相反転(マイナス)
    zin  = 1 / (1/rb + 1/(rpi + (1 + beta) * reEff));
    zout = 1 / (1/rc + 1/ro);
  } else if (config === "CB") {
    const rcP = 1 / (1/rc + 1/rl + 1/ro);
    av = gm * rcP;  zin = 1 / (gm + 1/rpi);  zout = 1 / (1/rc + 1/ro);
  } else { // CC (エミッタフォロワ)
    const reP = 1 / (1/re + 1/rl);
    av = gm * reP / (1 + gm * reP);            // ほぼ +1
    zin = 1 / (1/rb + 1/(rpi + (1 + beta) * reP));
    zout = 1 / (1/re + gm + 1/rpi);            // ≈ 1/gm と小さい
  }
  return { gm, av, av_db: 20 * Math.log10(Math.abs(av)), zin, zout };
}
```

並列抵抗をコンダクタンス（$1/R$）の和で扱うのがポイントです。`config` を切り替えるだけで CE/CB/CC を同じ枠組みで比較できます。

## コレクタ電流を上げると利得が伸びる

$g_m = I_C/V_T$ なので、CE 利得 $A_v = -g_m(R_C\|R_L\|r_o)$ はコレクタ電流とともに大きくなります。実際に $I_C$ を振ってみると：

| $I_C$ | $g_m$ | $A_v$ [dB] |
|---|---|---|
| $0.5\,\mathrm{mA}$ | $19\,\mathrm{mA/V}$ | $33.5$ |
| $1\,\mathrm{mA}$ | $38\,\mathrm{mA/V}$ | $39.4$ |
| $2\,\mathrm{mA}$ | $77\,\mathrm{mA/V}$ | $45.2$ |
| $5\,\mathrm{mA}$ | $192\,\mathrm{mA/V}$ | $52.6$ |
| $10\,\mathrm{mA}$ | $385\,\mathrm{mA/V}$ | $57.7$ |

![CE/CB/CCのボード線図とIC-利得の関係](/images/bjt-amplifier/charts-closeup.png)

左がボード線図、右が $I_C$ と CE 利得の関係です。電流を10倍（$1\to10\,\mathrm{mA}$）にすると $g_m$ も10倍になり、利得は約 $18\,\mathrm{dB}$ 上昇します。ただし $r_o = V_A/I_C$ は逆に小さくなるので、$R_C\|R_L\|r_o$ の頭打ちにより利得の伸びは対数的に鈍ります。実回路では電流を上げるほど発熱・消費電力が増えるため、闇雲に大電流にすればよいわけではない点に注意してください。

## ボード線図の読み方

横軸を対数の周波数にとり、利得 $|A_v|$ [dB] をプロットしたのがボード線図です。中域は平坦で、低域と高域でそれぞれ利得が落ちます。

- **低域カットオフ $f_L$**: 結合・バイパスコンデンサのインピーダンスが効いてくる帯域。$f_L \approx 1/(2\pi C Z_{in})$ で、$Z_{in}$ が小さいほど高くなる
- **高域カットオフ $f_H$**: トランジスタの寄生容量 $C_\pi,\ C_\mu$ で利得が落ち始める帯域

上のボード線図で CE と CB は同じ中域利得（$39.4\,\mathrm{dB}$）ですが、CB は $Z_{in}=26\,\Omega$ と低いため $f_L$ が高め（約 $618\,\mathrm{Hz}$）に出ます。実務上 CB が「高周波向き」と言われるのは、ミラー効果の影響が小さく高域側に余裕があるためです。CC は中域利得が $0\,\mathrm{dB}$ 付近の平坦な線になり、増幅はしないが広帯域でフラット——という性格がそのまま現れます。

> 補足: このツールの $f_L,\ f_H$ は結合容量 $C=10\,\mathrm{\mu F}$、$f_T=500\,\mathrm{MHz}$ といった代表値を仮定した**一次近似**です。実際のカットオフは部品定数や寄生成分で動くため、傾向をつかむ目安として読んでください。

## ツールで遊ぶ

NovaSolver のツールでは、スライダーを動かすと3構成のボード線図がリアルタイムに描き変わります：

![ICを動かすとCEのボード線図が持ち上がる](/images/bjt-amplifier/slider-anim.gif)

試してほしい操作：

- **構成セレクト**で CE / CB / CC を切り替え、利得の符号（位相反転）とインピーダンスの違いを比較
- **コレクタ電流 $I_C$ スライダー**を上げて、$g_m=I_C/V_T$ に従い CE 利得が持ち上がるのを確認
- **REバイパス トグル**を ON/OFF。OFF だと $A_v=-g_m R_C/(1+g_m R_E)$ となり利得が大きく下がる（電流帰還）
- **$\beta$・$R_C$・$R_L$・$V_A$** を動かして、利得とボード線図の連動を観察
- ボード線図上で **CE / CB / CC の3本がオーバーレイ**表示されるので、3構成を一目で比べられる

計算結果カードには利得 $A_v$ [dB]、$Z_{in}$、$Z_{out}$、$f_L$、$f_H$、利得帯域幅積 GBW が並びます。

## まとめ

- BJTアンプは入出力端子の取り方で CE / CB / CC の3構成に分かれる
- 出発点は $g_m=I_C/V_T,\ r_\pi=\beta/g_m,\ r_o=V_A/I_C$ の3パラメータ
- CE は高利得・位相反転、CB は低 $Z_{in}$・高周波向き、CC は利得約1だがバッファに最適
- $g_m \propto I_C$ なので $I_C$ を上げると利得が伸びる（ただし発熱とのトレードオフ）
- ボード線図で低域 $f_L$・高域 $f_H$ のカットオフと中域利得の関係が読める

「1石のトランジスタでも、つなぎ方ひとつで増幅器にもバッファにもなる」——その違いを式と数値で体感できるのがこのテーマの面白さです。

📐 **[BJTアンプ交流特性 解析シミュレーター（NovaSolver）](https://novasolver.jp/tools/bjt-amplifier.html)** で、構成と $I_C$ を切り替えてボード線図の変化を見てみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。電子回路では [トランジスタ増幅回路計算機](https://novasolver.jp/tools/transistor-amp.html)、[BJT直流バイアス設計](https://novasolver.jp/tools/transistor-bias.html)、[オペアンプ基本回路](https://novasolver.jp/tools/opamp-circuit.html) なども揃えています。
