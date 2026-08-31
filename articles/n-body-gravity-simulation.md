---
title: "N体重力シミュレーションの作り方 — O(N²)・軟化長・シンプレクティック積分"
emoji: "✨"
type: "tech"
topics: ["javascript", "物理シミュレーション", "天体力学", "数値計算", "可視化"]
published: true
---

![N体重力シミュレーション — NovaSolver](/images/n-body-gravity/cover.png)

## N体問題とは

星・惑星・塵——重力で引き合う物体がたくさんあると、それぞれが他のすべてから引力を受けて動きます。2 体なら楕円軌道、3 体ですでにカオス。**N 体**になると、銀河の渦も星団の蒸発も、この同じ単純な法則の積み重ねから生まれます。

この記事では、ブラウザで動く N 体シミュレータを支える 3 つの実装技術を解説します：

1. **O(N²)** の全ペア力計算
2. **軟化長（softening）** で $1/r^2$ の発散を抑える
3. **シンプレクティック積分（velocity-Verlet）** でエネルギーを保つ

📐 **動くデモ**: [N体重力シミュレーター（NovaSolver）](https://novasolver.jp/tools/n-body-gravity.html)

## O(N²)：全ペアの力を足す

物体 $i$ が受ける加速度は、他のすべての物体 $j$ からの万有引力の和です：

$$
\ddot{\mathbf{r}}_i = \sum_{j \neq i} G\, m_j \frac{\mathbf{r}_j - \mathbf{r}_i}{\lvert \mathbf{r}_j - \mathbf{r}_i \rvert^{3}}
$$

各ステップで**すべてのペア**を見るので、計算量は $N(N-1)/2$、つまり **$O(N^2)$**。$N$ を 2 倍にすると計算は約 4 倍です。今回のデモ（中心星＋6 天体、$N=7$）なら 1 ステップ **21 ペア**ですが、$N=1000$ なら約 50 万ペア——大規模になると Barnes–Hut 木（$O(N\log N)$）などの近似が必要になります。

```javascript
const G = 1, EPS = 8;            // EPS = 軟化長（後述）
function accel(pos, mass) {
  const n = mass.length;
  const a = pos.map(() => [0, 0]);
  for (let i = 0; i < n; i++)
    for (let j = 0; j < n; j++) {
      if (i === j) continue;
      const dx = pos[j][0]-pos[i][0], dy = pos[j][1]-pos[i][1];
      const r2 = dx*dx + dy*dy + EPS*EPS;     // 軟化
      const inv = mass[j] / (r2 * Math.sqrt(r2));  // 1/r^3 相当
      a[i][0] += G*dx*inv;  a[i][1] += G*dy*inv;
    }
  return a;
}
```

## 軟化長：1/r² の罠を避ける

万有引力は $1/r^2$。2 つの物体が接近して $r \to 0$ になると力が**無限大**に発散し、数値計算が一発で壊れます（おもりが光速で吹き飛ぶ）。

これを防ぐのが**軟化長 $\varepsilon$** で、分母を $r^2 + \varepsilon^2$ に置き換えます。こうすると $r=0$ でも加速度が有限にとどまり（このツールは $\varepsilon=8$ ピクセル）、近接遭遇でシミュレーションが破綻しません。代償として、ごく近距離の重力は本物よりやや弱くなります。星団や銀河の N 体計算でも標準的に使われるテクニックです。

## velocity-Verlet：エネルギーを保つ積分

軌道を何百周も追うと、普通の RK4 では**エネルギーが少しずつ一方向にずれ**（永年ドリフト）、軌道が膨らんだり縮んだりします。天体計算では**シンプレクティック法**——位相空間の体積を保つ積分——を使うのが鉄則で、最も手軽なのが **velocity-Verlet** です：

```javascript
function step(pos, vel, mass, dt) {
  let a = accel(pos, mass);
  vel = add(vel, scale(a, dt/2));   // 速度を半歩
  pos = add(pos, scale(vel, dt));   // 位置を1歩
  a = accel(pos, mass);             // 新しい位置で再計算
  vel = add(vel, scale(a, dt/2));   // 速度を残り半歩
  return [pos, vel];
}
```

このデモを velocity-Verlet で長時間積分しても、**全エネルギーの変動はわずか 0.017%**。エネルギーが上下に揺れるだけで一方向に流れないのがシンプレクティック法の効能で、軌道が崩れずに保たれます。

![中心星のまわりの安定した軌道トレイル](/images/n-body-gravity/charts-closeup.png)

## 創発する構造

単純な引力の足し算からでも、豊かな振る舞いが生まれます：

- 軽い天体は重い中心星のまわりを**ケプラー的な楕円**で回る
- 天体どうしの摂動で軌道がゆっくり**歳差**する
- 三体以上の近接遭遇で 1 体が高速で**放出**される（スリングショット）
- 多数になると、全体が一定の比率に落ち着く（**ビリアル定理** $2\langle T\rangle + \langle V\rangle = 0$）

![時間とともに軌道が発展する様子](/images/n-body-gravity/slider-anim.gif)

## ツールで遊ぶ

[N体重力シミュレーター](https://novasolver.jp/tools/n-body-gravity.html)で試してほしい操作：

- **プリセット**を選んで太陽系風・連星系などを読み込む
- **キャンバスをクリックで天体を配置／ドラッグで初速度を付けて配置**
- **天体タイプ**（星・惑星・小惑星）と**質量**スライダーで重さを変える
- **重力定数 G・時間刻み dt** を変え、dt を上げ過ぎると軌道が崩れる（積分誤差）のを体感
- **軌道トレイル・速度ベクトル・力ベクトル**の表示を切り替え、**全エネルギー**の値が保たれるか観察

## まとめ

- N 体重力は全ペアの引力和（$O(N^2)$、$N=7$ なら 21 ペア／ステップ）
- $1/r^2$ の発散は**軟化長 $\varepsilon$**（分母 $r^2+\varepsilon^2$）で回避する
- 長期軌道は **velocity-Verlet（シンプレクティック）** でエネルギーを保つ（ドリフト 0.017%）
- 単純な法則から楕円・歳差・放出・ビリアル平衡が創発する

「全ペアの足し算＋エネルギーを保つ積分」——これが宇宙論シミュレーションまで地続きの、N 体計算の骨格です。

📐 **[N体重力シミュレーター（NovaSolver）](https://novasolver.jp/tools/n-body-gravity.html)** で、自分で天体を放り込んで重力ダンスを作ってみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。重力・天体系では [三体問題](https://novasolver.jp/tools/three-body.html)、[ケプラー軌道](https://novasolver.jp/tools/kepler-orbit.html)、[磁気振り子](https://novasolver.jp/tools/magnetic-pendulum.html) なども揃えています。
