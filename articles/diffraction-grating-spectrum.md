---
title: "回折格子 — d sinθ = mλ で光を虹に分け、波長を測る"
emoji: "🌈"
type: "tech"
topics: ["javascript", "光学", "波動", "可視化", "数値計算"]
published: false
---

![回折格子 — NovaSolver](/images/diffraction-grating/cover.png)

## CD の裏面が虹色に光る理由

CD や DVD の裏面を傾けると虹色に輝きます。これは細かく刻まれた溝が**回折格子**として働き、白色光を波長ごとに別の方向へ振り分けるためです。プリズムが屈折で光を分けるのに対し、回折格子は**干渉**で分ける——しかも波長分解能が高く、分光器（スペクトロメータ）の心臓部として星の組成分析から物質同定まで使われます。

この記事では回折格子の式を導き、JavaScript で干渉パターンと虹色分散を再現します。

🌈 **動くデモ**: [回折格子・干渉縞シミュレーター（NovaSolver）](https://novasolver.jp/tools/diffraction-grating.html)

## 回折格子の式

間隔 $d$ で並んだ多数のスリットに光が当たると、隣り合うスリットからの光の**行路差が波長の整数倍**になる方向で強め合います。入射角 $\theta_i$、回折角 $\theta_m$ として

$$
d(\sin\theta_m - \sin\theta_i) = m\lambda \qquad (m = 0, \pm1, \pm2, \dots)
$$

$m$ は**回折次数**。$m=0$ はまっすぐ（全波長同じ方向）、$|m|\ge1$ では波長ごとに角度が変わるため、白色光が虹に分かれます。ツールの既定値（$d=1.67\,\mu\mathrm{m}$、約 600 本/mm の格子、緑レーザー $\lambda=532\,\mathrm{nm}$、垂直入射）で計算すると

$$
\sin\theta_1 = \frac{1\times0.532}{1.67} = 0.319 \;\Rightarrow\; \theta_1 = 18.6°
$$

2 次は $39.6°$、3 次は $72.9°$。次数が上がるほど大きく曲がります。

![多スリット干渉パターン（左）と白色光の波長分散（右）](/images/diffraction-grating/charts-closeup.png)

## スリットが多いほど鋭く、よく分かれる

スリット数 $N$ が多いほど、強め合う方向のピークは**鋭く**なります。多スリット干渉の強度は

$$
I(\theta) = \left[\frac{\sin(N\delta)}{N\sin\delta}\right]^2,\qquad
\delta = \frac{\pi d(\sin\theta - \sin\theta_i)}{\lambda}
$$

で表され、$N$ が大きいほど主極大が細くなります（上図左の鋭いピーク）。この鋭さが波長分解能を決めます。**分解能** $R$ と分離できる最小波長差 $\delta\lambda$ は

$$
R = mN,\qquad \delta\lambda = \frac{\lambda}{R}
$$

既定値（$m=1$、$N=500$）では $R=500$、$\delta\lambda = 532/500 = 1.06\,\mathrm{nm}$。次数 $m$ を上げるかスリット数 $N$ を増やすほど、近い波長を見分けられます。

## 白色光が虹になる

回折角は波長に比例して変わるため、白色光（380〜780 nm）を当てると $m=1$ で扇状の**スペクトル**に分かれます（上図右）。屈折とは逆に、**波長の長い赤ほど大きく曲がる**のが回折の特徴です。これがプリズムの虹（紫が大きく曲がる）と回折格子の虹で色の並びが逆になる理由です。

## JavaScript 実装

格子の式と強度パターンはそのまま実装できます。

```javascript
const lamUM = lam / 1000;                          // nm -> um
const sinThm = m * lamUM / d + Math.sin(thi);      // 回折角の sin
if (Math.abs(sinThm) <= 1) {
  const thm = Math.asin(sinThm);                   // 回折角
  const R = Math.abs(m) * N;                        // 分解能 R = mN
  const dlam = lam / R;                             // 最小分離 δλ
}
// 多スリット干渉強度
const delta = Math.PI*d*1000*(Math.sin(th)-Math.sin(thi))/lam;
const I = Math.pow(Math.sin(N*delta)/(N*Math.sin(delta)), 2);
```

![波長を変えると回折ピークの位置が動く](/images/diffraction-grating/slider-anim.gif)

## ツールで遊ぶ

[回折格子・干渉縞シミュレーター](https://novasolver.jp/tools/diffraction-grating.html)で試してほしい操作：

- **波長 λ スライダー**を動かし、回折角が波長に応じて変わる（赤ほど大きく曲がる）のを見る
- **格子間隔 d スライダー**を小さく（本数を多く）すると、回折角が大きく開くことを確認
- **スリット総数 N スライダー**を増やし、干渉ピークが鋭くなり**分解能 R=mN** が上がるのを観察
- **回折次数 m スライダー**を変え、各次数の回折角と $R$ を比較
- **入射角 θi スライダー**を変えて、$d(\sin\theta_m-\sin\theta_i)=m\lambda$ の効果を見る
- **計算結果**（回折角・角度分散・分解能・最小分離 δλ）と**白色光の虹色分散アニメーション**を確認

## まとめ

- 回折格子の式 $d(\sin\theta_m-\sin\theta_i)=m\lambda$。次数 $m$ ごとに強め合う方向が決まる
- 既定値で 1 次回折角 18.6°、2 次 39.6°、3 次 72.9°
- スリット数 $N$ が多いほどピークが鋭く、**分解能 $R=mN$**、最小分離 $\delta\lambda=\lambda/R$
- 白色光は虹に分かれ、屈折と逆に**赤ほど大きく曲がる**

分光器・天文観測・レーザー波長計測の基礎となる回折格子を、波長や格子を変えながら体感してみてください。

🌈 **[回折格子・干渉縞シミュレーター（NovaSolver）](https://novasolver.jp/tools/diffraction-grating.html)** で、光を虹に分ける干渉の物理を見てみましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。光学・波動系では [スネルの法則](https://novasolver.jp/tools/snells-law.html)、[波の干渉](https://novasolver.jp/tools/wave-interference.html)、[薄肉レンズ光線追跡](https://novasolver.jp/tools/lens-ray-tracer.html) なども揃えています。
