---
title: "レイノルズ数 — 流れが層流か乱流かを決める1つの無次元数"
emoji: "🌊"
type: "tech"
topics: ["javascript", "流体力学", "レイノルズ数", "可視化", "数値計算"]
published: false
---

![レイノルズ数と層流・乱流 — NovaSolver](/images/reynolds-number/cover.png)

## 蛇口の水が「すっと出る」か「ばしゃばしゃ暴れる」か

蛇口を細く開けると水は透明な棒のように整然と流れ（**層流**）、大きく開けると白く泡立って暴れます（**乱流**）。この切り替わりを支配するのが、流体力学で最も重要な無次元数——**レイノルズ数 $\mathrm{Re}$** です。たった1つの数で、流れの「性格」が決まります。

この記事ではレイノルズ数の意味を解説し、JavaScript で層流・乱流を判定し、なぜ無次元数が「相似則」として模型実験を可能にするのかを見ていきます。

🌊 **動くデモ**: [Reynolds数計算機・流れ場マップ（NovaSolver）](https://novasolver.jp/tools/reynolds-number.html)

## レイノルズ数とは「慣性力 ÷ 粘性力」

レイノルズ数は、流れを乱そうとする**慣性力**と、それを抑えてなめらかに保とうとする**粘性力**の比です。

$$
\mathrm{Re} = \frac{\rho U L}{\mu} = \frac{U L}{\nu}
$$

$\rho$ は密度、$U$ は流速、$L$ は代表長さ（管なら直径）、$\mu$ は粘度、$\nu=\mu/\rho$ は動粘度。$\mathrm{Re}$ が小さい＝粘性が優勢でなめらか（層流）、大きい＝慣性が優勢で乱れる（乱流）。

円管内流れの目安は次のとおりです。

- $\mathrm{Re} < 2300$：**層流**（整然と平行に流れる）
- $2300 \le \mathrm{Re} < 4000$：**遷移域**（不安定）
- $\mathrm{Re} \ge 4000$：**乱流**（渦が混ざり合う）

形状によって臨界値は変わり、平板上の境界層では $\mathrm{Re}\approx5\times10^5$、球まわりでは別の値になります。

![U×L の流れ場マップと、層流・乱流の流れの違い](/images/reynolds-number/charts-closeup.png)

## 実際に計算してみる

ツールの基準例（20°C の水、$\rho=998.2$、$\mu=1.002\times10^{-3}$、内径 $D=25\,\mathrm{mm}$、流速 $U=1\,\mathrm{m/s}$）で計算します。

$$
\mathrm{Re} = \frac{998.2\times1\times0.025}{1.002\times10^{-3}} \approx 24{,}900
$$

$\mathrm{Re}\approx2.5\times10^4$ で、しっかり乱流です。流速を 1.5 m/s に上げれば $\mathrm{Re}\approx37{,}400$、逆に 0.09 m/s 程度まで落とせば $\mathrm{Re}\approx2300$ の層流限界に達します。上図左の「流れ場マップ」は、流速 $U$ と代表長さ $L$ の組み合わせで層流（緑）・遷移・乱流（赤）のどこに入るかを一目で示します。

## 無次元数だから「模型実験」ができる

レイノルズ数の威力は、**無次元**であることにあります。実機と模型でレイノルズ数を一致させれば、流れのパターンが相似になります（**動的相似則**）。だから風洞で縮小模型の空力を測れるし、船の抵抗を水槽模型で評価できる。$\mathrm{Re}$ が同じなら、大きさや流速が違っても「同じ流れ」なのです。これが流体力学で無次元数が重視される理由です。

## JavaScript 実装

計算は1行、判定はしきい値で行います。

```javascript
function getRe() {
  const U = ...;   // 流速 [m/s]
  const L = ...;   // 代表長さ [m]
  const { rho, mu } = fluid;          // 流体物性
  const Re = rho * U * L / mu;        // = U*L/nu
  return Re;
}
function getRegime(Re) {              // 円管の場合
  if (Re < 2300) return '層流';
  if (Re < 4000) return '遷移域';
  return '乱流';
}
```

![流速を上げるとレイノルズ数が増え、層流から乱流へ移る](/images/reynolds-number/slider-anim.gif)

## ツールで遊ぶ

[Reynolds数計算機・流れ場マップ](https://novasolver.jp/tools/reynolds-number.html)で試してほしい操作：

- **流速 U スライダー**を上げ、**流れの状態**が「層流」→「遷移域」→「乱流」へ変わる Reynolds 数を確認
- **流体**を「水」「空気」「油」で切り替え、粘度の違いで同じ条件でも $\mathrm{Re}$ が大きく変わるのを見る（油は粘性大で層流になりやすい）
- **代表長さ L/D スライダー**を変え、太い管ほど乱流になりやすいことを観察
- **流れのタイプ**を「管内流」「平板」「球」で切り替え、臨界レイノルズ数が違うことを確認
- **流れ場マップ**で、自分の動作点が層流・乱流のどの領域に入るかを読み取る
- **計算結果**（Reynolds 数・流れの状態・動粘度・臨界速度）を確認

## まとめ

- レイノルズ数 $\mathrm{Re}=\rho UL/\mu$ は**慣性力と粘性力の比**。流れが層流か乱流かを決める
- 円管では層流 $\mathrm{Re}<2300$、遷移、乱流 $\mathrm{Re}\ge4000$（形状で臨界値は変わる）
- 水・D=25mm・U=1m/s で $\mathrm{Re}\approx24{,}900$（乱流）
- 無次元数なので**動的相似則**が成り立ち、模型実験で実機の流れを再現できる

CFD・配管設計・空力・伝熱のあらゆる場面で最初に確認するレイノルズ数を、流速や流体を変えながら体感してみてください。

🌊 **[Reynolds数計算機・流れ場マップ（NovaSolver）](https://novasolver.jp/tools/reynolds-number.html)** で、流れが乱れ始める境界を見つけましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。流体系では [パイプ流れ](https://novasolver.jp/tools/pipe-flow.html)、[カルマン渦](https://novasolver.jp/tools/karman-vortex.html)、[抗力係数](https://novasolver.jp/tools/drag-coefficient.html) なども揃えています。
