---
title: "2Dランダムウォークとブラウン運動 — MSDのべき乗則で拡散を見分ける"
emoji: "🎲"
type: "tech"
topics: ["javascript", "数学", "確率", "可視化", "統計"]
published: false
---

![2Dランダムウォークとブラウン運動 — NovaSolver](/images/random-walk-2d/cover.png)

## 酔歩がたどり着く「平均の距離」

水に浮かべた花粉の不規則な震え（ブラウン運動）、株価の変動、分子の拡散——いずれも**ランダムウォーク（酔歩）** でモデル化できます。一歩ごとにサイコロを振って進む向きを決めるだけ。それでも「平均してどれくらい原点から離れるか」には、$\sqrt{N}$ という美しい法則が現れます。

この記事ではランダムウォークの統計量 **平均二乗変位（MSD）** を導き、JavaScript で複数のウォーカーを歩かせ、MSD のべき乗則から拡散の「型」を見分けます。

🎲 **動くデモ**: [2Dランダムウォーク シミュレーター（NovaSolver）](https://novasolver.jp/tools/random-walk-2d.html)

## 平均二乗変位（MSD）と √N 則

各ステップで歩幅 $a$ だけランダムな向きに進むとき、$N$ 歩後の原点からの距離の2乗を平均した量が**平均二乗変位**

$$
\langle r^2(N)\rangle = \langle x^2 + y^2\rangle
$$

です。各ステップが独立なので、$N$ 歩後の MSD はステップ数に**比例**します。2 次元（$d=2$）の拡散係数 $D$ を使うと

$$
\langle r^2 \rangle = 2dD\,t = 4D\,t,\qquad D = \frac{a^2}{4}
$$

これを実測で確かめましょう。格子上を歩幅 $a=5$ で歩かせると、シミュレーションで $\langle r^2\rangle / t \approx 24.8 \approx a^2=25$ となり、$\langle r^2\rangle = a^2 t$（= $4Dt$）に一致します。重要なのは、**原点からの典型的な距離（RMS）は $\sqrt{\langle r^2\rangle}\propto\sqrt{N}$ でしか伸びない**こと。100 歩でも原点から平均 10 歩ぶんしか離れません。酔っぱらいが家になかなか帰れない理由です。

![6個のウォーカーの軌跡と、MSDのべき乗則](/images/random-walk-2d/charts-closeup.png)

## べき乗則で拡散の型を見分ける

MSD を $\langle r^2\rangle \propto t^{\,\gamma}$ と書いたときの**指数 $\gamma$**（両対数プロットの傾き）が、拡散の性質を分類します。

- $\gamma = 1$：**通常拡散**（ブラウン運動）。格子歩行・ガウス歩行はこれ
- $\gamma = 2$：**弾道的（ballistic）**。一方向のドリフトが効くと $\langle r^2\rangle\approx v^2 t^2$
- $1 < \gamma < 2$：**超拡散**。レヴィフライト（まれに大ジャンプ）など
- $\gamma < 1$：**劣拡散**。障害物の多い媒質など

上図右の両対数プロットでは、ドリフト無し（水色）が傾き **1.0**（$4Dt$ の基準線に重なる）、ドリフトを加えた歩行（オレンジ）が長時間で傾き **約 2.0** になり、確かに拡散から弾道へ移ることが読み取れます。

## JavaScript 実装

格子4方向の1ステップと MSD の集計はこう書けます。

```javascript
walkers.forEach(w => {
  const dir = Math.floor(Math.random() * 4);          // 上下左右
  const dx = [stepSize, -stepSize, 0, 0][dir] + driftX;
  const dy = [0, 0, stepSize, -stepSize][dir];
  w.x += dx; w.y += dy;                                // 一歩進む
});
// MSD = 原点からの距離の2乗の平均
const msd = walkers.reduce((s, w) =>
  s + (w.x - w.ox)**2 + (w.y - w.oy)**2, 0) / walkers.length;
```

歩行タイプを変えると `dx, dy` の決め方が変わります：ガウス連続（Box-Muller で正規乱数）、レヴィフライト（α安定分布でまれに大ジャンプ）など。境界条件（反射・周期・吸収）も選べます。

![原点から拡がるウォーカーの雲（RMS∝√t）](/images/random-walk-2d/slider-anim.gif)

## ツールで遊ぶ

[2Dランダムウォーク シミュレーター](https://novasolver.jp/tools/random-walk-2d.html)で試してほしい操作：

- **歩行タイプ**を「格子4方向」「格子8方向」「ガウス連続」「レヴィフライト」で切り替え、軌跡の質感の違いを見る
- **MSD グラフ（両対数）** で、**現在MSD と理論線がともに直線（傾き1）**＝通常拡散であることを確認
- **Xドリフトスライダー**を 0 から動かし、MSD の傾きが大きくなる（弾道的拡散へ）のを観察
- **レヴィ指数 α** を下げ、まれな大ジャンプで遠くまで飛ぶ超拡散的な軌跡を見る
- **ウォーカー数**を増やすと統計が安定し、MSD 曲線が滑らかになる
- **境界条件**を「反射」「周期」「吸収」で切り替え、壁の効果を比較
- **最大変位**の表示で、$\sqrt{N}$ より速く伸びる外れ値の振る舞いを追う

## まとめ

- ランダムウォークの MSD はステップ数に比例：$\langle r^2\rangle = 2dDt = 4Dt$（2次元、$D=a^2/4$）
- 典型距離は $\mathrm{RMS}\propto\sqrt{N}$。歩数を 4 倍にしても距離は 2 倍にしかならない
- MSD のべき指数で拡散型を判別：通常拡散（傾き1）／弾道的（傾き2）／超拡散（1〜2）
- 格子・ガウス・レヴィ・ドリフトを切り替えて、ブラウン運動から異常拡散まで体験できる

統計力学・金融工学・分子拡散の基礎となるランダムウォークを、軌跡と MSD グラフで体感してみてください。

🎲 **[2Dランダムウォーク シミュレーター（NovaSolver）](https://novasolver.jp/tools/random-walk-2d.html)** で、サイコロの足し算が描く拡散の法則を見つけましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。確率・数値系では [モンテカルロ円周率](https://novasolver.jp/tools/monte-carlo-pi.html)、[反応拡散](https://novasolver.jp/tools/reaction-diffusion.html)、[ライフゲーム](https://novasolver.jp/tools/game-of-life.html) なども揃えています。
