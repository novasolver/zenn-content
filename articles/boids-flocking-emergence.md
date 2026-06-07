---
title: "Boids — たった3つのルールから群れが「創発」する仕組み"
emoji: "🐦"
type: "tech"
topics: ["javascript", "アルゴリズム", "可視化", "シミュレーション", "創発"]
published: false
---

![Boids 群れの創発 — NovaSolver](/images/boids-flocking/cover.png)

## 中央司令塔のいない群れ

ムクドリの大群が空で渦を巻き、イワシの群れが一斉に身をひるがえす——あの複雑な集団運動には、実は**リーダーも全体設計図もありません**。各個体は近くの仲間だけを見て、たった3つの単純なルールに従っているだけ。それでも全体としては有機的なうねりが生まれます。

1986年に Craig Reynolds が考案した **Boids**（bird-oid object）は、この「局所ルールから大域的秩序が立ち上がる」=**創発（emergence）** の代表例です。この記事では3ルールを定義し、JavaScript で実装し、群れの「秩序の度合い」を数値で測ります。

🐦 **動くデモ**: [ボイドシミュレーター（NovaSolver）](https://novasolver.jp/tools/boids-flocking.html)

## 3つのルール

各ボイドは視野半径 $r$ 内にいる仲間に対して、次の3つの操舵力を計算します。

- **分離（Separation）**：近づきすぎた仲間から離れる（衝突回避）
- **整列（Alignment）**：仲間の平均速度に自分の向きを合わせる
- **結合（Cohesion）**：仲間の重心（平均位置）に向かう

数式で書くと、視野内の仲間集合を $N_i$、近接集合を $N_i^{\text{sep}}$ として

$$
\mathbf{F}_s = -\!\!\sum_{j\in N_i^{\text{sep}}}\frac{\mathbf{r}_{ij}}{|\mathbf{r}_{ij}|^2},\quad
\mathbf{F}_a = \langle\mathbf{v}_j\rangle - \mathbf{v}_i,\quad
\mathbf{F}_c = \langle\mathbf{x}_j\rangle - \mathbf{x}_i
$$

最終的な加速度は3つの重み付き和です。

$$
\mathbf{a}_i = w_s\mathbf{F}_s + w_a\mathbf{F}_a + w_c\mathbf{F}_c
$$

このたった3項の綱引きで、魚群から鳥群、整然とした隊列まで、あらゆる集団行動が再現されます。重み $w_s, w_a, w_c$ を変えるだけで全く違う「生き物」になるのが面白いところです。

## JavaScript 実装

近傍探索は素朴な $O(n^2)$ の総当たりで十分動きます（$n=100$ なら 1 フレームあたり $100\times99=9{,}900$ 回の距離判定）。1つのボイドの更新はこうです。

```javascript
for (let j = 0; j < boids.length; j++) {
  if (i === j) continue;
  const dx = o.x - b.x, dy = o.y - b.y, d2 = dx*dx + dy*dy;
  if (d2 > range2) continue;            // 視野外は無視
  if (d2 < sepRange2 && d2 > 0) {        // 分離（近接のみ）
    const d = Math.sqrt(d2);
    sx -= dx/d*(sepRange/d); sy -= dy/d*(sepRange/d);
  }
  ax += o.vx; ay += o.vy;                // 整列（速度を集計）
  cx += o.x;  cy += o.y;  nc++;          // 結合（位置を集計）
}
// 重み付き合成 → 力をクランプ → 速度を maxSpeed でクランプ
fx = sx*sepW + (ax/nc - b.vx)*aliW*0.1 + (cx/nc - b.x)*cohW*0.002;
```

仕上げに操舵力を上限 `maxForce` で、速度を `maxSpeed` でクランプし、画面端を出たら反対側から再登場させます（**トーラス空間**）。これだけで群れが動き出します。

## 「秩序の度合い」を数値で測る

創発を定量化するには、群れがどれだけ同じ方向を向いているかを表す**整列度（order parameter）**

$$
\varphi = \frac{\left|\sum_i \mathbf{v}_i\right|}{\sum_i |\mathbf{v}_i|}
$$

が便利です。全員がバラバラなら $\varphi\to0$、完全に同方向なら $\varphi\to1$。ツールの4つのプリセットを同条件（600 ステップ）で回して実測すると、明確な差が出ます。

![整列度はルールの重み配分で決まる（実測値）](/images/boids-flocking/charts-closeup.png)

| プリセット | 整列度 $\varphi$ | クラスター数 |
|---|---|---|
| 💥 混沌（整列・結合ほぼ0） | **0.48** | 20 |
| 標準 | 0.86 | 3 |
| 🐦 鳥の群れ（整列強め） | **0.91** | 2 |
| 🎯 密集隊形（結合・整列大） | 0.73 | 1 |

「混沌」は整列・結合の重みをほぼ 0 にしたもので、$\varphi=0.48$ とバラバラ、群れは 20 個の小集団に割れます。一方「鳥の群れ」は整列を強めると $\varphi=0.91$ まで揃い、ほぼ1つの群れ（クラスター数2）になります。**同じ3ルールでも、重みの配分だけでここまで秩序が変わる**——これが創発の核心です。

## ツールで遊ぶ

[ボイドシミュレーター](https://novasolver.jp/tools/boids-flocking.html)で試してほしい操作：

- **分離の重み**を 0 にして、個体同士がぶつかり始める（衝突回避が消える）のを見る
- **整列の重み**を大きくして、群れが軍隊のように一方向へピシッと揃うのを観察
- **結合の重み**を上げて密集塊に、下げて拡散させる
- **視野半径**を小さくすると群れが分裂、大きくすると1つの大群にまとまる（**クラスター数**の表示で確認）
- **プリセット**「🐟 魚の群れ」「🐦 鳥の群れ」「💥 混沌」「🎯 密集隊形」を切り替えて挙動を比較
- **キャンバスをクリック**で天敵を置くと群れが逃げ散り、**右クリック（長押し）**で引力源を置くと吸い寄せられる
- **表示オプション**で「視野圏」「速度ベクトル」「軌跡」をオンにして内部状態を可視化
- **平均速度・クラスター数**の表示で、群れの状態を数値で追う

![ランダムな初期状態から秩序が立ち上がる（整列度 φ の上昇）](/images/boids-flocking/slider-anim.gif)

## まとめ

- Boids は**分離・整列・結合**の3ルールだけで群れを生む。中央制御も全体計画も不要
- 加速度は3項の重み付き和 $\mathbf{a}=w_s\mathbf{F}_s+w_a\mathbf{F}_a+w_c\mathbf{F}_c$。重み配分で挙動が一変する
- 局所情報だけから大域的秩序が生まれる＝**創発**。整列度 $\varphi$ で定量化できる（混沌 0.48 → 鳥群 0.91 と実測）
- 素朴な $O(n^2)$ 実装でも数百個体までは軽快に動く

群衆シミュレーション、ゲームの集団AI、粒子法 CFD の基礎にもつながる「単純ルールの創発」を、スライダーひとつで体感してみてください。

🐦 **[ボイドシミュレーター（NovaSolver）](https://novasolver.jp/tools/boids-flocking.html)** で、3つの重みを動かして自分だけの群れを作ってみましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。創発・アルゴリズム系では [反応拡散（チューリングパターン）](https://novasolver.jp/tools/reaction-diffusion.html)、[ライフゲーム](https://novasolver.jp/tools/game-of-life.html)、[フーリエ・エピサイクル](https://novasolver.jp/tools/fourier-epicycles.html) なども揃えています。
