---
title: "ビュフォンの針で円周率πを求める — 針を投げるだけでπ=2LN/(dm)をJSで"
emoji: "📐"
type: "tech"
topics: ["javascript", "確率", "モンテカルロ", "数学", "可視化"]
published: false
---

![ビュフォンの針と円周率 — NovaSolver](/images/buffon-needle/cover.png)

## 床に針を落とすだけで円周率が出る不思議

等間隔の平行線を引いた床に針をランダムに落とす。針が線をまたぐ確率を数えるだけで、なぜか**円周率 π** が現れます。1733 年にビュフォンが見つけたこの問題は、確率を使って定数を求める**モンテカルロ法**の最も古く美しい例です。コンピュータも三角関数表もない時代に、π が「幾何学的な偶然」から立ち上がるのは驚きです。

この記事では、ビュフォンの針を JavaScript でシミュレーションし、π を推定します。

📐 **動くデモ**: [ビュフォンの針シミュレーター（NovaSolver）](https://novasolver.jp/tools/buffon-needle.html)

## なぜ針が円周率を教えるのか

線間隔 $d$、針の長さ $\ell$（$\ell \le d$）とします。針の中心から最寄り線までの距離 $y$ と、針が線となす角 $\theta$ を一様分布とすると、針が線と交差する条件は

$$
y \le \frac{\ell}{2}\sin\theta
$$

これを積分すると、交差確率は

$$
P = \frac{2\ell}{\pi d}
$$

ここに π が現れます。$N$ 本投げて $m$ 本が交差したら $m/N \approx P$ なので、π を逆算できます。

$$
\hat\pi = \frac{2\ell N}{d\,m}
$$

既定値 $\ell=5\,\mathrm{mm}$、$d=10\,\mathrm{mm}$（$\ell/d = 0.5$）では理論交差確率 $P = 2\times5/(\pi\times10) = 0.3183$。乱数シード 42 で $N=5000$ 本投げると交差 $m=1542$ 本、$m/N = 0.3084$、**π 推定値 $\hat\pi = 3.2425$**（誤差 3.21%）。さらに $N=100000$ 本まで増やすと $\hat\pi = 3.1475$（誤差 0.19%）へと精度が上がります。誤差は $1/\sqrt N$ で減るので、桁を増やすには本数を 100 倍にする必要があります。

![針の落下（赤=交差/青=非交差, 左）とNに対するπ推定の収束（右）](/images/buffon-needle/charts-closeup.png)

## JavaScript 実装

再現性のため、決定論的な線形合同法（LCG）で乱数を生成します。

```javascript
function makeLCG(seed) {                    // Numerical Recipes パラメータ
  let state = (seed >>> 0) || 1;
  return () => { state = (state*1664525 + 1013904223) >>> 0; return state / 4294967296; };
}
function simulate(N, L, d, seed) {
  const rand = makeLCG(seed);
  let m = 0;
  for (let i = 0; i < N; i++) {
    const y = rand() * (d / 2);            // 中心-最寄り線の距離 [0, d/2]
    const theta = rand() * Math.PI / 2;    // 角度 [0, π/2]
    if (y <= (L / 2) * Math.sin(theta)) m++;  // 交差判定
  }
  return m;
}
const m = simulate(5000, 5, 10, 42);
const piHat = (2 * 5 * 5000) / (10 * m);   // ≈ 3.2425
```

針が長すぎる（$\ell > d$）と一本が複数線をまたぎ得るので、この単純な式は成り立ちません（シミュレーターは警告を出します）。

![Nを増やすとπ推定値が真のπへ収束していく](/images/buffon-needle/slider-anim.gif)

## ツールで遊ぶ

[ビュフォンの針シミュレーター](https://novasolver.jp/tools/buffon-needle.html)で試してほしい操作：

- **針の本数 N スライダー**を増やし、「推定 π」が真の π に近づき「相対誤差」が下がるのを確認
- **針の長さ ℓ・線間隔 d スライダー**を変え、交差確率（推定確率 m/N）が $2\ell/\pi d$ に従うのを見る
- **乱数 seed スライダー**を変え、同じ条件でも結果がばらつく（モンテカルロの統計誤差）のを確認
- ℓ > d にして警告が出る（式が成り立たない領域）のを見る
- **キャンバス**で赤（交差）と青（非交差）の針を観察
- N を 10 倍にして誤差が約 1/√10 ≈ 1/3.16 に減るのを確かめる

## まとめ

- ビュフォンの針は確率から π を求めるモンテカルロ法の古典
- 交差確率は $P = 2\ell/(\pi d)$、π 推定は $\hat\pi = 2\ell N/(dm)$
- 既定（ℓ=5, d=10, seed=42, N=5000）で $\hat\pi = 3.2425$、N=10万で 3.1475
- 誤差は $1/\sqrt N$ で減る（精度 1 桁に本数 100 倍）

確率と幾何が交わる美しい問題を、本数や針の長さを変えながら体感してみてください。

📐 **[ビュフォンの針シミュレーター（NovaSolver）](https://novasolver.jp/tools/buffon-needle.html)** で、針が描く円周率を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。確率・モンテカルロでは [モンテカルロ法でπ推定](https://novasolver.jp/tools/monte-carlo-pi.html)、[正規分布](https://novasolver.jp/tools/normal-distribution.html)、[2次元ランダムウォーク](https://novasolver.jp/tools/random-walk-2d.html) もどうぞ。
