---
title: "RLC共振回路 — f₀=1/(2π√LC) とQ値、ラジオが1局だけ選べる理由"
emoji: "📻"
type: "tech"
topics: ["javascript", "電気回路", "信号処理", "可視化", "数値計算"]
published: false
---

![RLC共振回路とQ値 — NovaSolver](/images/rlc-resonance/cover.png)

## ラジオのダイヤルは何を「合わせて」いるのか

ラジオのチューニングは、無数に飛び交う電波の中からたった1つの放送局の周波数を選び出す操作です。これを可能にするのが、抵抗 R・コイル L・コンデンサ C からなる **RLC 共振回路**。特定の周波数だけに強く応答する「共振」という性質が、選局を実現します。

この記事では共振周波数と、共振の「鋭さ」を表す **Q 値**を導き、JavaScript で周波数特性を計算します。

📻 **動くデモ**: [RLC回路共振シミュレーター（NovaSolver）](https://novasolver.jp/tools/rlc-resonance.html)

## 共振周波数

直列 RLC 回路のインピーダンスは、コイルのリアクタンス $X_L=\omega L$ とコンデンサのリアクタンス $X_C=1/(\omega C)$ を使って

$$
|Z| = \sqrt{R^2 + (X_L - X_C)^2}
$$

$X_L$ は周波数とともに増え、$X_C$ は減るので、ある周波数で両者が打ち消し合い $|Z|$ が最小（$=R$）になります。これが**共振**で、その周波数は

$$
f_0 = \frac{1}{2\pi\sqrt{LC}}
$$

直列回路では共振時にインピーダンスが最小＝電流が最大になります（上図左で $|Z|$ が谷、$|I|$ が山）。$L$ や $C$ を変えると $f_0$ が移動し、これがラジオの選局そのものです。

![直列RLCの周波数特性（左）と、Rによる共振の鋭さの違い（右）](/images/rlc-resonance/charts-closeup.png)

## Q値：共振の「鋭さ」と選択性

共振がどれだけ鋭いかを表すのが **Q 値（品質係数）** です。直列回路では

$$
Q = \frac{\omega_0 L}{R} = \frac{1}{R}\sqrt{\frac{L}{C}}
$$

そして共振の幅（**帯域幅**）は

$$
\mathrm{BW} = \frac{f_0}{Q}
$$

**$Q$ が高いほど共振が鋭く、帯域幅が狭い**＝近い周波数を鋭く選り分けられます。上図右のように、抵抗 $R$ を小さくすると $Q$ が上がり、ピークが鋭く尖ります（$R=5\,\Omega$ で $Q=20$、$R=30\,\Omega$ で $Q=3$）。

ラジオの選局には高い $Q$ が不可欠です。ツールの「AM ラジオ」プリセット（$R=5\,\Omega$、$L=270\,\mu\mathrm{H}$、$C=100\,\mathrm{pF}$）では $f_0\approx969\,\mathrm{kHz}$（AM 放送帯）、$Q\approx329$ という鋭い共振になり、隣の局を排除して1局だけを拾えます。

## JavaScript 実装

共振周波数・Q値・周波数特性は素直に書けます。

```javascript
function getF0() { return 1 / (2*Math.PI*Math.sqrt(L*C)); }   // 共振周波数
function getZ(f) {                                            // インピーダンス（直列）
  const w = 2*Math.PI*f, XL = w*L, XC = 1/(w*C);
  return Math.sqrt(R*R + (XL - XC)**2);
}
function getQ() { return 2*Math.PI*getF0()*L / R; }           // Q = ω₀L/R
function getBW() { return getF0() / getQ(); }                 // 帯域幅
// 電流 I = V / |Z|（直列は共振で最大）
```

![Rを下げると共振が鋭くなり帯域幅が狭まる](/images/rlc-resonance/slider-anim.gif)

## ツールで遊ぶ

[RLC回路共振シミュレーター](https://novasolver.jp/tools/rlc-resonance.html)で試してほしい操作：

- **インダクタンス L・キャパシタンス C スライダー**を変え、**共振周波数 f₀** が $1/\sqrt{LC}$ で移動するのを見る
- **抵抗 R スライダー**を下げ、**Q 値**が上がり共振ピークが鋭く・帯域幅が狭くなることを確認
- **プリセット**「AM ラジオ」「音声フィルター」「電力補正」で実用回路の特性を比較
- **計算結果**の「共振周波数」「Q 値」「帯域幅」「共振時 |Z|」を読む
- **直列／並列**を切り替え、直列は共振で電流最大、並列は逆（インピーダンス最大）になることを観察
- **フェーザー図**で、共振時に $V_L$ と $V_C$ が打ち消し合う様子を見る

## まとめ

- RLC 共振周波数は $f_0=1/(2\pi\sqrt{LC})$。$X_L=X_C$ で直列はインピーダンス最小・電流最大
- **Q 値** $Q=\omega_0L/R$ が共振の鋭さ＝選択性を決める。帯域幅 $\mathrm{BW}=f_0/Q$
- $R$ が小さいほど高 $Q$・狭帯域。ラジオの選局には高 $Q$ が必須（AM 帯で $Q\approx329$）
- $L,C$ で $f_0$ を合わせるのがチューニングそのもの

ラジオ・フィルタ・発振器・無線通信の基礎となる RLC 共振を、素子値を変えながら体感してみてください。

📻 **[RLC回路共振シミュレーター（NovaSolver）](https://novasolver.jp/tools/rlc-resonance.html)** で、1つの周波数だけを選び出す共振の鋭さを確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。回路・信号系では [RC/RL回路](https://novasolver.jp/tools/rc-rl-circuit.html)、[ボード線図](https://novasolver.jp/tools/bode-plot.html)、[フーリエ変換](https://novasolver.jp/tools/fourier-transform.html) なども揃えています。
