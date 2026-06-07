---
title: "弾性振り子と2:1パラメトリック共振 — バネと振れが「エネルギーを交換」する"
emoji: "🌀"
type: "tech"
topics: ["javascript", "物理シミュレーション", "非線形", "可視化", "数値計算"]
published: false
---

![弾性振り子とパラメトリック共振 — NovaSolver](/images/spring-pendulum/cover.png)

## バネにおもりを吊るして、横に少しだけ揺らすと

普通の振り子（伸びない糸）は単純な周期運動をしますが、**バネにおもりを吊るした「弾性振り子（swinging spring）」** は、まったく違う顔を見せます。上下のバネ運動（バウンド）と左右の振り子運動（スイング）が**非線形に連成**し、条件が揃うと**エネルギーが2つのモードを行き来する**——上下に弾んでいたはずが、いつの間にか大きく横に振れ、また弾みに戻る。この自発的な「エネルギーの授受」が、**2:1 自動パラメトリック共振**です。

この記事では弾性振り子の運動方程式を立て、RK4 で数値積分し、エネルギーがバネ↔振れで交換する様子を再現します。

🌀 **動くデモ**: [弾性振り子シミュレーター（NovaSolver）](https://novasolver.jp/tools/spring-pendulum.html)

## 連成した運動方程式

バネの長さ $r$ と鉛直からの角度 $\theta$ を一般化座標にとり、ラグランジアン $L = \frac12 m(\dot r^2 + r^2\dot\theta^2) + mgr\cos\theta - \frac12 k(r-L_0)^2$ から運動方程式を導くと、次の連成した非線形方程式が得られます。

$$
\ddot{r} = r\dot\theta^2 + g\cos\theta - \frac{k}{m}(r - L_0)
$$

$$
\ddot\theta = \frac{-g\sin\theta - 2\dot r\dot\theta}{r}
$$

第1式は動径（バネ）方向：遠心力 $r\dot\theta^2$、重力の動径成分 $g\cos\theta$、バネの復元力。第2式は角度方向で、**コリオリ項 $-2\dot r\dot\theta/r$** がバネ運動と振り子運動を結びつけます。この項が連成、ひいてはエネルギー交換の源です。

## 2つの固有振動数と共振条件

小振幅では2つのモードが分離します。**バネ（上下）の振動数**と**振り子（振れ）の振動数**は

$$
\omega_{\text{spring}} = \sqrt{\frac{k}{m}},\qquad
\omega_{\text{swing}} = \sqrt{\frac{g}{r_{\text{eq}}}}
$$

ここで $r_{\text{eq}} = L_0 + mg/k$ は重力で伸び切った平衡長です（振り子の実効長は自然長 $L_0$ ではなくこの $r_{\text{eq}}$）。そして、**バネ振動数が振り子振動数のちょうど2倍**のとき——

$$
\omega_{\text{spring}} = 2\,\omega_{\text{swing}}
$$

——上下に1往復する間に振り子が半周期動く、という位相関係が成立し、バネ運動が振り子運動を**パラメトリックに励起**します。これが 2:1 共振です。

![おもりの軌跡（蝶ネクタイ型）と、バネ⇄振れのエネルギー授受](/images/spring-pendulum/charts-closeup.png)

## エネルギーは行ったり来たりする

2:1 共振に合わせたパラメータ（$m=0.5$、$L_0=0.5$、$k\approx28$ で $r_{\text{eq}}\approx0.675$、$\omega_{\text{spring}}/\omega_{\text{swing}}\approx2.0$）で、わずかな初期角（3°）を与えて上下に弾ませると、上図右のように**バネのエネルギー（オレンジ）が減るときに振り子のエネルギー（水色）が増え**、また戻る——緩やかな「うなり」のようなエネルギー授受が現れます。総エネルギー（破線）は一定に保たれ、RK4 積分での誤差は実質 0%。左図のおもりの軌跡は、エネルギーが両モードを巡るために生まれる**蝶ネクタイ型**の美しいパターンになります。

## JavaScript 実装（RK4）

非線形連成系なので、4次のルンゲ・クッタで精度よく積分します。

```javascript
function deriv(s) {
  const { r, dr, theta, dtheta } = s;
  const rs = Math.max(r, 0.01);
  const ddr = rs*dtheta*dtheta + g*Math.cos(theta) - (k/m)*(rs - L0);
  const ddtheta = (-g*Math.sin(theta) - 2*dr*dtheta) / rs;   // コリオリ項が連成
  return { dr, ddr, dtheta, ddtheta };
}
// RK4 で1ステップ進める（dt = 0.001）
// 全エネルギー E = ½m(ṙ² + r²θ̇²) − mgr·cosθ + ½k(r−L0)²
```

![弾性振り子の運動：上下のバウンドが横の振れに変わる](/images/spring-pendulum/slider-anim.gif)

## ツールで遊ぶ

[弾性振り子シミュレーター](https://novasolver.jp/tools/spring-pendulum.html)で試してほしい操作：

- **バネ定数 k スライダー**を調整し、共振表示の **$\omega_{\text{spring}}$ と $\omega_{\text{pendulum}}$ の比が 2 に近づく**ように合わせると、エネルギー授受が顕著になる
- 共振に合わせた状態で**初期角 θ₀ を小さく**（数度）して上下に弾ませ、振れが自発的に育つのを観察
- **計算結果**の「全エネルギー E」が運動を通じて**保存**されることを確認
- **プリセット**「共振」「カオス」「単振り子」を切り替えて挙動を比較（k を非常に大きくすると伸びない単振り子に近づく）
- **質量 m・自然長 L₀ スライダー**で2つの固有振動数を動かし、共振条件から外すとエネルギー授受が止まることを見る
- おもりの**軌跡**が描く複雑なリサジュー模様を眺める

## まとめ

- 弾性振り子はバネ（上下）と振り子（振れ）が**コリオリ項 $-2\dot r\dot\theta/r$ で連成**した非線形系
- 固有振動数は $\omega_{\text{spring}}=\sqrt{k/m}$、$\omega_{\text{swing}}=\sqrt{g/r_{\text{eq}}}$（実効長は平衡長 $r_{\text{eq}}=L_0+mg/k$）
- $\omega_{\text{spring}}=2\,\omega_{\text{swing}}$ の **2:1 共振**で、エネルギーがバネ↔振れを周期的に行き来する
- 総エネルギーは保存（RK4 で誤差ほぼ 0）。軌跡は蝶ネクタイ型のリサジュー模様に

非線形力学・パラメトリック励振・カオスの入り口となる弾性振り子を、共振条件を合わせながら体感してみてください。

🌀 **[弾性振り子シミュレーター（NovaSolver）](https://novasolver.jp/tools/spring-pendulum.html)** で、上下の弾みが横揺れに化ける2:1共振を見つけてみましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。非線形・力学系では [二重振り子](https://novasolver.jp/tools/double-pendulum.html)、[位相空間ポートレート](https://novasolver.jp/tools/phase-space-portrait.html)、[磁気振り子](https://novasolver.jp/tools/magnetic-pendulum.html) なども揃えています。
