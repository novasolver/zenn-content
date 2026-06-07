---
title: "ブラキストクロン問題 — 最速で滑り降りる坂は「直線」ではない"
emoji: "🎢"
type: "tech"
topics: ["javascript", "物理シミュレーション", "数学", "可視化", "数値計算"]
published: false
---

![ブラキストクロン（最速降下線）— NovaSolver](/images/brachistochrone/cover.png)

## 「一番速い滑り台」の形は？

高さの違う2点 A・B を結ぶ滑り台を作るとき、ビーズが重力だけで A から B へ**最速で**到達する曲線はどんな形でしょうか。直感的には「最短距離＝直線」が速そうですが、答えは**直線ではありません**。1696 年にヨハン・ベルヌーイが出したこの**ブラキストクロン問題（最速降下線）** の答えは、**サイクロイド（円が転がるときに円周上の点が描く曲線）** でした。ニュートンは一晩で解いたと伝わります。

この記事では、なぜ直線が最速でないのかを数式で示し、JavaScript でサイクロイドと直線の「ビーズ競争」を再現します。

🎢 **動くデモ**: [最速降下曲線シミュレーター（NovaSolver）](https://novasolver.jp/tools/brachistochrone.html)

## なぜ直線より速いのか

ポイントは「序盤で急降下して早く加速する」ことです。サイクロイドは出だしでほぼ真下に落ちて速度を稼ぎ、その速度で水平距離を一気に詰めます。遠回りでも、速く動ける区間が長ければトータルで速くなる——これが最速降下線の核心です。

サイクロイドは媒介変数 $\theta$ で次のように表されます。

$$
x = a(\theta - \sin\theta),\qquad y = -a(1 - \cos\theta)
$$

始点 $A=(0,0)$ と終点 $B=(D, -H)$ を通る条件から、終端角 $\theta_f$ は次式を満たします。

$$
\frac{\theta_f - \sin\theta_f}{1 - \cos\theta_f} = \frac{D}{H},\qquad a = \frac{H}{1 - \cos\theta_f}
$$

そして降下時間は驚くほど簡潔です。

$$
T = \theta_f\sqrt{\frac{a}{g}}
$$

![サイクロイドと直線の経路、および降下時間の落差依存性](/images/brachistochrone/charts-closeup.png)

## 実際に時間を比べる

ツールの既定値（水平距離 $D=5\,\mathrm{m}$、垂直降下 $H=3\,\mathrm{m}$、$g=9.81$）で計算してみます。$D/H=1.667$ から二分法で $\theta_f=3.234\,\mathrm{rad}$、サイクロイド径 $a=1.503\,\mathrm{m}$。降下時間は

$$
T_{\text{cycloid}} = 3.234\times\sqrt{\frac{1.503}{9.81}} = 1.266\,\mathrm{s}
$$

一方、直線スロープ（斜面長 $L=\sqrt{D^2+H^2}=5.83\,\mathrm{m}$）は一様加速で

$$
T_{\text{line}} = \sqrt{\frac{2L^2}{gH}} = 1.520\,\mathrm{s}
$$

サイクロイドは直線より **0.254 秒（16.7%）速い**。なお終端速度はどちらの経路でもエネルギー保存から $v_{\text{end}}=\sqrt{2gH}=7.67\,\mathrm{m/s}$ で同じ——速いのは「途中の稼ぎ方」の差です。

## サイクロイドは「等時曲線」でもある

サイクロイドにはもう一つ驚きの性質があります。媒介変数 $\theta$ が**時間に比例して増加する**（$\theta = \sqrt{g/a}\,t$）のです。これは、サイクロイド上のどの高さから滑り出しても**最下点に到達する時間が同じ**という**等時性（tautochrone）** を意味します。ホイヘンスはこの性質を振り子時計に応用しようとしました。

## JavaScript 実装

終端角は二分法で解き、ビーズの位置は媒介変数から求めます。

```javascript
function solveThetaF(ratio) {          // (θ-sinθ)/(1-cosθ) = D/H を二分法で
  const f = th => (th - Math.sin(th)) / (1 - Math.cos(th)) - ratio;
  let lo = 0.001, hi = 2*Math.PI - 0.001;
  for (let i = 0; i < 80; i++) {
    const mid = 0.5*(lo + hi);
    if (f(mid) < 0) lo = mid; else hi = mid;
  }
  return 0.5*(lo + hi);
}
// 時刻 t のビーズ位置（θ は時間に比例＝等時性）
function cycloidAtTime(t) {
  const th = thetaF * Math.min(t / brachTime, 1);
  return { x: a*(th - Math.sin(th)), y: -a*(1 - Math.cos(th)) };
}
// 直線は一様加速: 進んだ割合 = (t/T)^2
```

![サイクロイドのビーズが直線より先にゴールする](/images/brachistochrone/slider-anim.gif)

## ツールで遊ぶ

[最速降下曲線シミュレーター](https://novasolver.jp/tools/brachistochrone.html)で試してほしい操作：

- **ビーズ競争アニメーション**で、サイクロイド（青）が直線（オレンジ）より先にゴールするのを見る
- **水平距離 D・垂直降下 H スライダー**を変え、**時間短縮率**がどう変化するか観察（落差が浅く横長なほど差が開く）
- **重力加速度 g スライダー**を月面（1.6）などにして降下時間の変化を見る
- **計算結果**で「最速降下時間」「直線スロープの時間」「サイクロイド角 θ_f」「サイクロイド径 a」を確認
- **降下時間 vs 落差 H のグラフ**で、サイクロイドが常に直線より下（速い）にあることを読み取る
- **終端運動エネルギー**が経路によらず同じ（エネルギー保存）であることを確認

## まとめ

- 最速降下線は直線ではなく**サイクロイド** $x=a(\theta-\sin\theta),\ y=-a(1-\cos\theta)$
- 序盤で急降下して加速を稼ぐため、遠回りでも直線より速い（既定値で 16.7% 短縮）
- 降下時間は $T=\theta_f\sqrt{a/g}$。終端速度は経路によらず $\sqrt{2gH}$
- サイクロイドは**等時曲線**でもある（$\theta\propto t$、どの高さからでも同時刻に最下点へ）

変分法（最小作用の原理）の歴史的出発点となったこの問題を、ビーズ競争で体感してみてください。

🎢 **[最速降下曲線シミュレーター（NovaSolver）](https://novasolver.jp/tools/brachistochrone.html)** で、「直線が最速ではない」ことを自分の目で確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。力学・数学系では [二重振り子](https://novasolver.jp/tools/double-pendulum.html)、[ケプラー軌道](https://novasolver.jp/tools/kepler-orbit.html)、[ニュートンのゆりかご](https://novasolver.jp/tools/newtons-cradle.html) なども揃えています。
