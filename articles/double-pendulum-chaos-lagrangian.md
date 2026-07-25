---
title: "二重振り子はなぜカオスになるのか — ラグランジュ方程式とRK4で動かす"
emoji: "🌀"
type: "tech"
topics: ["javascript", "物理シミュレーション", "カオス", "数値計算", "可視化"]
published: true
---

![二重振り子のカオス — NovaSolver](/images/double-pendulum/cover.png)

## 二重振り子とは

振り子の先にもう一つ振り子をぶら下げただけ。たったそれだけの仕掛けが、**予測不能なカオス運動**を生みます。

単振り子はきれいな周期運動をしますが、2 本つなぐと話が一変します。上の振り子の揺れが下に伝わり、下の揺れが上にフィードバックする——この**非線形な連成**が、初期条件のごくわずかな差を爆発的に拡大させます。

この記事では：

1. ラグランジュ方程式で運動方程式を立てる
2. それを RK4 で数値積分する JavaScript 実装
3. 「初期角度 0.006° の差」が完全な乖離に至るまでを数値で確認

📐 **動くデモ**: [二重振り子（カオス）シミュレーター（NovaSolver）](https://novasolver.jp/tools/double-pendulum.html)

## ラグランジュ方程式で立式する

二重振り子は接続点の張力が複雑で、ニュートンの運動方程式（力のつり合い）で直接書くのは骨が折れます。そこで **ラグランジアン** $L = T - V$（運動エネルギー − 位置エネルギー）から導く解析力学の手法を使います。

一般化座標を 2 本の角度 $\theta_1, \theta_2$ にとると、オイラー・ラグランジュ方程式

$$
\frac{d}{dt}\frac{\partial L}{\partial \dot{\theta}_i} - \frac{\partial L}{\partial \theta_i} = 0
$$

から、角加速度について解いた式が得られます。質量を質点、棒を質量ゼロとしたときの標準形は次のとおりです（$\Delta = \theta_1 - \theta_2$、$M = m_1 + m_2$）：

$$
\ddot{\theta}_1 = \frac{-g(2m_1+m_2)\sin\theta_1 - m_2 g\sin(\theta_1-2\theta_2) - 2\sin\Delta\, m_2(\dot{\theta}_2^2 L_2 + \dot{\theta}_1^2 L_1\cos\Delta)}{L_1(2m_1 + m_2 - m_2\cos 2\Delta)}
$$

$$
\ddot{\theta}_2 = \frac{2\sin\Delta\left(\dot{\theta}_1^2 L_1 M + gM\cos\theta_1 + \dot{\theta}_2^2 L_2 m_2\cos\Delta\right)}{L_2(2m_1 + m_2 - m_2\cos 2\Delta)}
$$

ごつい式ですが、要は **角度・角速度の 4 変数 $(\theta_1, \dot\theta_1, \theta_2, \dot\theta_2)$ の 1 階連立 ODE** に落ちる、という点だけ押さえれば十分です。あとは数値積分するだけ。

## JavaScript で実装する

4 変数の状態ベクトル `s = [θ1, ω1, θ2, ω2]` に対して、右辺（時間微分）を返す関数を書きます：

```javascript
const G = 9.81;

function deriv(s, L1, L2, m1, m2) {
  const [a1, w1, a2, w2] = s;
  const da = a1 - a2;
  const sinDA = Math.sin(da), cosDA = Math.cos(da);
  const M = m1 + m2;
  const D = 2*m1 + m2 - m2*Math.cos(2*da);  // 共通分母

  const num1 = -G*(2*m1+m2)*Math.sin(a1) - m2*G*Math.sin(a1-2*a2)
             - 2*sinDA*m2*(w2*w2*L2 + w1*w1*L1*cosDA);
  const da1 = num1 / (L1*D);

  const num2 = 2*sinDA*(M*w1*w1*L1 + G*M*Math.cos(a1) + m2*w2*w2*L2*cosDA);
  const da2 = num2 / (L2*D);

  return [w1, da1, w2, da2];   // [θ1', ω1', θ2', ω2']
}
```

これを **RK4（ルンゲ・クッタ 4 次）** で 1 ステップ進めます。配列の各成分に同じ重み付き平均を適用するだけです：

```javascript
function rk4(s, dt, L1, L2, m1, m2) {
  const k1 = deriv(s, L1, L2, m1, m2);
  const k2 = deriv(s.map((v,i) => v + k1[i]*dt/2), L1, L2, m1, m2);
  const k3 = deriv(s.map((v,i) => v + k2[i]*dt/2), L1, L2, m1, m2);
  const k4 = deriv(s.map((v,i) => v + k3[i]*dt),   L1, L2, m1, m2);
  return s.map((v,i) => v + (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) * dt/6);
}
```

NovaSolver のツールはこれを $dt = 0.008$ 秒で 1 フレームあたり 4 ステップ回しています。

## エネルギー保存で精度を確かめる

カオス系のシミュレーションで怖いのは「軌道がデタラメなのか、数値誤差で壊れているのか区別がつかない」こと。そこで**全エネルギー（保存量）がどれだけ保たれるか**を精度のものさしにします。

減衰なしで両振り子を $120°$ から放すと、初期の全エネルギーは

$$
E_0 = T + V = 14.72\ \text{J}
$$

（$L_1=L_2=1\,\text{m},\ m_1=m_2=1\,\text{kg}$、位置エネルギーは支点基準）。これを RK4 で 30 秒積分しても：

| 時刻 | 全エネルギー $E$ |
|---|---|
| 0 s | 14.7150 J |
| 30 s | 14.7136 J |

ドリフトはわずか $-1.4\times10^{-3}$ J、相対誤差 **約 0.01%**。激しいカオス運動を 30 秒追ってもエネルギーがほぼ保存される——RK4 が信頼できる証拠です。オイラー法（1 次）だと同じ刻みでエネルギーが急増し、振り子が物理的にありえない速度まで加速してしまいます。

ツールでは運動エネルギー・ポテンシャル・全エネルギーがリアルタイム表示されるので、減衰スライダーを 0 にしたとき全エネルギーがほぼ一定に保たれることを目で確認できます。

## カオスを描く

二重振り子の下端 $(x_2, y_2)$ の軌跡を残像付きで描くと、二度と同じ線をなぞらない複雑な模様が現れます：

![二重振り子の軌跡](/images/double-pendulum/charts-closeup.png)

角度から座標への変換は単純です：

```javascript
const x1 = L1 * Math.sin(a1),  y1 = -L1 * Math.cos(a1);
const x2 = x1 + L2 * Math.sin(a2),  y2 = y1 - L2 * Math.cos(a2);
```

## 0.006° の差が世界を変える

カオスの核心は **初期値鋭敏性**。NovaSolver のツールの「2 軌道比較」ボタンは、青い振り子と、初期角度を $10^{-4}$ ラジアン（**約 0.006°**）だけずらした赤い振り子を同時に走らせます。

両者の角度差 $|\Delta\theta|$ を追うと：

| 時刻 | 角度差 $\lvert\Delta\theta\rvert$ |
|---|---|
| 1 s | $1.2\times10^{-4}$ rad |
| 4 s | $8.8\times10^{-3}$ rad |
| 8 s | $0.55$ rad（約 31°） |
| 12 s | $7.2$ rad（完全に別物） |

最初は肉眼で見分けられないほど重なっていた 2 本が、**10 秒ほどで完全に別の運動**になります。これがバタフライ効果。初期条件をどれだけ精密に測っても、わずかな誤差が指数関数的に拡大するため、長期予測は原理的に不可能です。

![2軌道比較：青と赤が見る間に乖離する](/images/double-pendulum/slider-anim.gif)

## ツールで遊ぶ

[二重振り子シミュレーター](https://novasolver.jp/tools/double-pendulum.html)で試してほしい操作：

- **「2 軌道比較」ボタン**で青と赤の乖離を観察——カオスを一目で体感できる
- **プリセット**「🌀カオス」「⬆️規則的」「⚖️対称」を切り替える（規則的は小角度＋減衰あり）
- **初期角度 θ₁・θ₂** を小さく（〜20°）すると準規則的、大きく（>60°）するとカオス域に入る（バッジが切り替わる）
- **質量 m₂** を増やすと下の振り子が暴れやすくなる
- **減衰スライダー**で空気抵抗を加え、エネルギーが散逸して静止に向かう様子を見る

## まとめ

- 二重振り子はラグランジアン $L=T-V$ から角加速度の連立 ODE を導いて解く
- 状態 $(\theta_1,\omega_1,\theta_2,\omega_2)$ を RK4 + $dt=0.008$ で積分すれば 30 行ほどで実装できる
- 全エネルギーの保存（30 秒で誤差 0.01%）が数値精度のものさしになる
- 初期角度 $0.006°$ の差が約 10 秒で完全な乖離に——カオスの初期値鋭敏性

ロボットアームの多関節制御や柔軟構造物の非線形振動も、根っこは同じ連成ダイナミクス。二重振り子はその直感を養う最小のモデルです。

📐 **[二重振り子（カオス）シミュレーター（NovaSolver）](https://novasolver.jp/tools/double-pendulum.html)** で、「2 軌道比較」を押してカオスを体感してみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。カオス・非線形系では [ローレンツアトラクタ](https://novasolver.jp/tools/lorenz-attractor.html)、[三体問題](https://novasolver.jp/tools/three-body.html)、[磁気振り子](https://novasolver.jp/tools/magnetic-pendulum.html) なども揃えています。
