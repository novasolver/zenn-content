---
title: "三体問題はなぜ解けないのか — カオスと奇跡のfigure-8軌道"
emoji: "🪐"
type: "tech"
topics: ["javascript", "物理シミュレーション", "カオス", "天体力学", "数値計算"]
published: false
---

![三体問題のカオスとfigure-8 — NovaSolver](/images/three-body/cover.png)

## 三体問題とは

太陽と地球、2 つの天体なら軌道は楕円できれいに解けます（ケプラー）。ところが **天体を 3 つ**にした途端、一般には**解析的に解けなくなる**。これが三体問題です。

19 世紀末、ポアンカレは「三体問題には一般解（保存量で書ける閉じた式）が存在しない」ことを示し、初期条件のわずかな差が軌道を全く変える——**カオス**——の存在に最初に気づきました。現代の天体力学・宇宙機の軌道設計が数値積分に頼るのは、この「解けなさ」が根本にあるからです。

この記事では：

1. なぜ三体は解けず、どう数値積分するか
2. **シンプレクティック法（leapfrog）** がなぜ軌道計算に向くか
3. カオスの海に浮かぶ奇跡の安定解 **figure-8**

📐 **動くデモ**: [三体問題シミュレーター（NovaSolver）](https://novasolver.jp/tools/three-body.html)

## 運動方程式とソフトニング

各天体 $i$ は他の天体からの万有引力で加速します：

$$
\ddot{\mathbf{r}}_i = \sum_{j \neq i} G\, m_j \frac{\mathbf{r}_j - \mathbf{r}_i}{\lvert \mathbf{r}_j - \mathbf{r}_i \rvert^3}
$$

数値計算では、2 体が接近して $\lvert\mathbf{r}_j-\mathbf{r}_i\rvert \to 0$ になると力が発散します。これを防ぐため**ソフトニング** $\varepsilon$ を入れて分母を $(\,|\Delta\mathbf{r}|^2 + \varepsilon^2)^{3/2}$ にします（NovaSolver のツールは $\varepsilon=0.02,\ G=1$、等質量）。

```javascript
const G = 1, EPS = 0.02;
function accel(pos) {           // pos: [[x,y],...] 3体
  const a = [[0,0],[0,0],[0,0]];
  for (let i = 0; i < 3; i++)
    for (let j = 0; j < 3; j++) {
      if (i === j) continue;
      const dx = pos[j][0]-pos[i][0], dy = pos[j][1]-pos[i][1];
      const r3 = Math.pow(dx*dx + dy*dy + EPS*EPS, 1.5);
      a[i][0] += G * dx / r3;
      a[i][1] += G * dy / r3;
    }
  return a;
}
```

## なぜ RK4 でなく leapfrog なのか

前回までの記事（[ローレンツ](https://novasolver.jp/tools/lorenz-attractor.html)・[二重振り子](https://novasolver.jp/tools/double-pendulum.html)）では RK4 を使いました。ところが**長時間の軌道計算では RK4 は不向き**です。RK4 は 1 ステップの精度は高いものの、エネルギーが少しずつ一方向にずれていき（永年ドリフト）、何万周もすると軌道が膨らんだり縮んだりしてしまいます。

そこで天体力学では **シンプレクティック法**——位相空間の体積を保つ積分法——を使います。最も簡単なのが **leapfrog（速度ベルレ／KDK）** です：

```javascript
const DT = 0.0005;
function step(pos, vel) {
  let a = accel(pos);
  vel = add(vel, scale(a, DT/2));   // 速度を半歩
  pos = add(pos, scale(vel, DT));   // 位置を1歩
  a = accel(pos);
  vel = add(vel, scale(a, DT/2));   // 速度を残り半歩
  return [pos, vel];
}
```

たった 3 行の更新ですが、**全エネルギーがほぼ完全に保存**されます。figure-8 解（後述）を 1 周期積分したときのエネルギーを測ると：

| 量 | 値 |
|---|---|
| 初期全エネルギー $E_0$ | $-1.2867$ |
| 1 周期後のエネルギー変動幅 | $\mathbf{0.0000\%}$ |
| 角運動量 $L$ | $0$（保存） |

ドリフトが事実上ゼロ。これが RK4 との決定的な違いで、長期軌道の安定計算を可能にします。

## カオスの海

一般の初期条件から始めると、三体は予測不能に振り回されます。2 体が接近して 1 体が弾き飛ばされる（**スリングショット**）こともしばしば。初期位置を $10^{-3}$ ずらすだけで、数周期後にはまったく別の運命をたどります——リアプノフ指数が正、すなわちカオスです。

だからこそ「3 つの星が安定して回り続ける配置」はとても貴重です。

## 奇跡の figure-8

そのひとつが **figure-8（8 の字）コレオグラフィー**。**3 つの等質量の星が、たった 1 本の 8 の字曲線を等間隔で追いかけ続ける**という、信じがたい周期解です。

![figure-8 周期解：3つの質量が1本の8字を共有](/images/three-body/charts-closeup.png)

数値的には Moore が 1993 年に発見し、Chenciner と Montgomery が 2000 年に**その存在を厳密に証明**、さらに安定であることも示されました。初期条件は次のとおり（重心静止、$L=0$）：

```javascript
function figure8() {
  return {
    pos: [[-0.97000436, 0.24308753],
          [ 0.0,        0.0       ],
          [ 0.97000436,-0.24308753]],
    vel: [[ 0.46620369, 0.43236573],   // = -v2 / 2
          [-0.93240737,-0.86473146],
          [ 0.46620369, 0.43236573]],
  };
}
```

このツールの leapfrog で 1 周期（$T \approx 6.326$）積分すると、3 体は出発点に**誤差 0.005 で戻ってきます**。まさに閉じた周期軌道です。

![figure-8 コレオグラフィー](/images/three-body/slider-anim.gif)

## ツールで遊ぶ

[三体問題シミュレーター](https://novasolver.jp/tools/three-body.html)で試してほしい操作：

- **プリセット**「figure-8（周期解）」「安定三角形」「ランダム」「バイナリ+惑星」を切り替える
- **「ランダム」**を何度も押すと、ほとんどがすぐ崩壊（1 体が放出）する——安定解がいかに稀かを体感
- **再生/一時停止**と **速度（0.25×/1×/3×）**で、接近イベントをスローで観察
- **エネルギー表示**をオンにして、leapfrog が全エネルギーをほぼ一定に保つことを確認

## まとめ

- 三体問題は一般には解析的に解けず（ポアンカレ）、初期値鋭敏性＝カオスを示す
- 数値積分は**シンプレクティックな leapfrog** が定番。エネルギー永年ドリフトが無い（1 周期で 0.0000%）
- figure-8 は等質量 3 体が 1 本の 8 字を共有する稀な**安定**周期解（Chenciner–Montgomery 2000）
- ソフトニング $\varepsilon$ で近接特異点を回避するのが実装の勘所

「2 体は解ける、3 体は解けない」——この一線が、カオス理論と現代の軌道力学の出発点でした。

📐 **[三体問題シミュレーター（NovaSolver）](https://novasolver.jp/tools/three-body.html)** で、figure-8 の優雅さとランダム配置の脆さを見比べてみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。重力・カオス系では [N体重力シミュレーション](https://novasolver.jp/tools/n-body-gravity.html)、[ケプラー軌道](https://novasolver.jp/tools/kepler-orbit.html)、[ローレンツアトラクタ](https://novasolver.jp/tools/lorenz-attractor.html) なども揃えています。
