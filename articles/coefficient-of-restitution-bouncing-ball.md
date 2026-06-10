---
title: "跳ねるボールが必ず止まる理由 — 反発係数と無限級数の収束"
emoji: "🏀"
type: "tech"
topics: ["javascript", "物理", "数学", "数値計算", "可視化"]
published: false
---

![跳ねるボールが必ず止まる理由 — NovaSolver](/images/coefficient-of-restitution/cover.png)

## 反発係数とは

ボールを床に落とすと、一度ごとに少しずつ跳ね高さが減り、やがて止まります。この減り方を決めるたった一つの数が **反発係数（coefficient of restitution）** $e$ です。Newton が定義した無次元量で、衝突直後と直前の相対速度の比として書けます：

$$
e = \frac{v_{\text{after}}}{v_{\text{before}}}
$$

$e=1$ なら速度が減らない完全弾性衝突、$e=0$ なら跳ね返らない完全非弾性衝突。現実の物体は $0 < e < 1$ の間にあります。

この記事では：

1. 跳ね高さが $e^{2n}$ で減る理由
2. 無限に跳ねるのに「全跳ね時間」が有限になる仕組み
3. 数式どおりの値を出す JavaScript 実装と数値検証

🏀 **動くデモ**: [反発係数シミュレーター（NovaSolver）](https://novasolver.jp/tools/coefficient-of-restitution.html)

## なぜ高さは $e^{2n}$ で減るのか

高さ $h$ から落とすと、着地直前の速度はエネルギー保存から決まります：

$$
v_0 = \sqrt{2gh}
$$

衝突で速度は $e$ 倍になるので、1回跳ねた後の上昇速度は $v_1 = e\,v_0$。ところが **高さは速度の2乗に比例** します（$h = v^2/(2g)$）。したがって跳ね高さは1回ごとに $e^2$ 倍、$n$ 回後には：

$$
h_n = h\,e^{2n}, \qquad v_n = v_0\,e^{n}
$$

指数が $2n$ になるのは、この「速度 → エネルギー → 高さ」の二乗連鎖のためです。エネルギーで見ても、1回の衝突で運動エネルギーは $e^2$ 倍だけ残り、$(1-e^2)$ の割合が熱・音・変形に消えます。$e=0.8$ なら毎回 36% を失う計算です。

## 無限に跳ねるのに時間は有限

ここが反発係数の面白いところです。$n$ 回目の跳ねにかかる往復時間 $t_n = (2v_0 e^n)/g$ は、公比 $e$ の等比数列をなします。$e<1$ なら無限和が収束し、全跳ね時間 $T$ と全鉛直移動距離 $D$ は有限値になります：

$$
T = \frac{2v_0}{g}\cdot\frac{1+e}{1-e}, \qquad D = h\cdot\frac{1+e^2}{1-e^2}
$$

跳ねる回数は数学的には無限なのに、それが終わる時刻は有限——古典力学版の **ゼノンのパラドックス** です。

## 20行で書く実装

公式をそのまま関数にできます：

```javascript
const vImpact = (g, h) => Math.sqrt(2 * g * h);
const bounceHeight = (h, e, n) => h * Math.pow(e, 2 * n);

function totalTime(g, h, e) {
  if (e >= 1) return Infinity;          // 完全弾性は収束しない
  const v0 = vImpact(g, h);
  return (2 * v0 / g) * (1 + e) / (1 - e);
}

function totalDistance(h, e) {
  if (e >= 1) return Infinity;
  return h * (1 + e * e) / (1 - e * e);
}

// h=2 m, e=0.8, g=9.81, n=5
const h = 2, e = 0.8, g = 9.81, n = 5;
console.log(vImpact(g, h).toFixed(2));        // 6.26 m/s
console.log(bounceHeight(h, e, n).toFixed(3)); // 0.215 m
console.log(totalTime(g, h, e).toFixed(2));   // 11.49 s
console.log(totalDistance(h, e).toFixed(2));  // 9.11 m
```

Python で照合しても同じ値（$v_0=6.2642$、$h_5=0.2147$、$T=11.4939$、$D=9.1111$）になり、ツールの「計算結果」表示とも一致します。$e=1$ のときは $1-e$ が0になり $T,D$ が発散する——これも公式どおりの挙動です。

## 幾何級数の減衰を見る

ツールでは、跳ねる軌跡と $h_n = h\,e^{2n}$ の減衰曲線を並べて描きます：

![反発係数ごとの跳ね高さ減衰](/images/coefficient-of-restitution/charts-closeup.png)

$e$ の違いがどれほど効くかは、$n=5$ での跳ね高さを比べると一目瞭然です（$h=2\ \mathrm{m}$）：

| 反発係数 $e$ | 例 | 5回後の高さ $h_5$ | 全跳ね時間 $T$ |
|---|---|---|---|
| 0.55 | 野球ボール（木製バット） | 0.005 m | 4.40 s |
| 0.80 | 弾性ゴム球 | 0.215 m | 11.49 s |
| 0.92 | スーパーボール | 0.869 m | 30.65 s |
| 0.99 | （ほぼ弾性） | 1.642 m | 254 s |

$e=0.55$ では5回でほぼ静止するのに、$e=0.92$ では5回跳ねてもまだ0.87 m 残ります。$e$ を1へ近づけると $T$ が急激に伸びるのも、$\frac{1+e}{1-e}$ の分母が0に近づくためです。

## ツールで遊ぶ

NovaSolver のツールでは、4つのスライダーと「$n$ をスイープ」アニメーションで減衰を体感できます：

![n をスイープすると跳ねが減衰する](/images/coefficient-of-restitution/slider-anim.gif)

試してほしい操作：

- **反発係数 $e$ スライダー**（0〜0.99）を動かし、「着地時速度」「$n$ 回後跳ね高さ」「全跳ね時間 $T$」「全鉛直移動距離 $D$」の4つの計算結果が変わるのを見る
- **初期高さ $h$**（0.1〜10 m）を変えても、$e$ による高さ比は変わらないことを確認（$h$ は $v_0$ と総時間にしか効かない）
- **重力加速度 $g$** を変えて、月や火星のような環境を試す
- **「$n$ をスイープ」ボタン** で跳ね回数を1〜30まで往復させ、幾何級数の減衰を観察

## まとめ

- 反発係数 $e$ は速度比で定義され、跳ね高さは $h_n = h\,e^{2n}$ と幾何級数で減る
- 1回の衝突でエネルギーは $e^2$ 倍だけ残り、$(1-e^2)$ が失われる
- $e<1$ なら全跳ね時間 $T = \frac{2v_0}{g}\frac{1+e}{1-e}$ と全距離 $D = h\frac{1+e^2}{1-e^2}$ は有限に収束する
- 公式はそのまま数行の JavaScript になり、$h=2,e=0.8$ で $T=11.49\ \mathrm{s}$ と検証できる

反発係数はスポーツ用具の規格（テニス・ゴルフ・野球の公認球）や、自動車のクラッシャブルゾーン設計など、衝突を扱う場面で広く使われる基本量です。$e$ を動かして、跳ねが「いつ止まるか」を確かめてみてください。

🏀 **[反発係数シミュレーター（NovaSolver）](https://novasolver.jp/tools/coefficient-of-restitution.html)** で、$e$ と $n$ を変えて減衰の速さを体感できます。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。衝突・運動量では [1次元衝突](https://novasolver.jp/tools/collision-1d.html)、[運動量保存則・衝突](https://novasolver.jp/tools/momentum-conservation.html)、[ニュートンのゆりかご](https://novasolver.jp/tools/newtons-cradle.html) なども揃えています。
