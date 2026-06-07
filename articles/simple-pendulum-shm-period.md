---
title: "単振り子の周期はなぜ振幅で変わる？ 線形近似とRK4で確かめる単振動"
emoji: "🟤"
type: "tech"
topics: ["javascript", "物理シミュレーション", "力学", "可視化", "数値計算"]
published: false
---

![単振り子と単振動 — NovaSolver](/images/simple-pendulum/cover.png)

## 「振り子の周期は振幅によらない」は本当か

理科で習う単振り子の周期 $T = 2\pi\sqrt{L/g}$ には、振れ幅 $\theta_0$ が出てきません。だから「周期は振幅によらず一定（等時性）」と覚えます。でもこれは**微小振幅の近似**にすぎません。大きく振ると、周期は確実に伸びます。

この記事では線形近似の公式を出発点に、非線形の運動方程式を JavaScript の RK4 で数値積分し、「周期がどれだけ伸びるか」を実際に計算して確かめます。

🟤 **動くデモ**: [単振り子シミュレーター（NovaSolver）](https://novasolver.jp/tools/simple-pendulum.html)

## 運動方程式と線形近似

振り子の角度 $\theta$ に対する運動方程式は、減衰 $\gamma$ を含めると次の通りです。

$$
\ddot{\theta} + \frac{g}{L}\sin\theta + \gamma\,\dot{\theta} = 0
$$

微小振幅では $\sin\theta \approx \theta$ と近似でき、単振動になります。このときの周期が有名な線形近似式です。

$$
T_0 = 2\pi\sqrt{\frac{L}{g}}
$$

$L = 1\,\mathrm{m}$、$g = 9.81\,\mathrm{m/s^2}$ なら $T_0 = 2.006\,\mathrm{s}$。月面（$g = 1.62$）では $T_0 = 4.937\,\mathrm{s}$ と、ゆっくり揺れます。

## 振幅が大きいと周期はどれだけ伸びるか

$\sin\theta \approx \theta$ の近似を外すと、厳密な周期は第1種完全楕円積分 $K$ で表せます。

$$
T = 4\sqrt{\frac{L}{g}}\,K\!\left(\sin^2\frac{\theta_0}{2}\right)
$$

ツールの既定（$L=1$, $g=9.81$）で計算すると、$\theta_0 = 30^\circ$ では $T = 2.041\,\mathrm{s}$ と線形値より **+1.7%**。「大振幅」プリセットの $\theta_0 = 120^\circ$ では $T = 2.754\,\mathrm{s}$ と、なんと **+37%** も伸びます。等時性が成り立つのは小振幅だけ、というわけです。

![初期角度に対する周期比 T/T₀（楕円積分）と振り子の模式図](/images/simple-pendulum/charts-closeup.png)

## JavaScript 実装（RK4）

非線形方程式を 4 次のルンゲ・クッタ法で積分します。状態は $[\theta, \omega]$ の 2 成分です。

```javascript
function derivatives([th, om], g, L, gamma) {
  return [om, -(g / L) * Math.sin(th) - gamma * om];  // [dθ/dt, dω/dt]
}
function rk4(s, dt, g, L, gamma) {
  const k1 = derivatives(s, g, L, gamma);
  const s2 = s.map((v, i) => v + dt/2 * k1[i]);
  const k2 = derivatives(s2, g, L, gamma);
  const s3 = s.map((v, i) => v + dt/2 * k2[i]);
  const k3 = derivatives(s3, g, L, gamma);
  const s4 = s.map((v, i) => v + dt * k3[i]);
  const k4 = derivatives(s4, g, L, gamma);
  return s.map((v, i) => v + dt/6 * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]));
}
// 全エネルギー（無減衰なら保存）：E = ½L²ω² + gL(1 - cosθ)
const E = 0.5*L*L*om*om + g*L*(1 - Math.cos(th));
```

この RK4 で求めた周期は、上の楕円積分の厳密値と小数第3位まで一致します（$\theta_0=120^\circ$ で 2.754 s）。数値解と解析解が合うことは、実装が正しい何よりの証拠です。

![小振幅（青）と大振幅（橙）の振り子。大振幅ほど周期が長い](/images/simple-pendulum/slider-anim.gif)

## ツールで遊ぶ

[単振り子シミュレーター](https://novasolver.jp/tools/simple-pendulum.html)で試してほしい操作：

- **初期角度 θ₀ スライダー**を 30° → 120° と上げ、「周期 T（線形近似）」表示はそのままでも実際の揺れがゆっくりになるのを体感
- **長さ L スライダー**を変え、$T \propto \sqrt{L}$（4 倍にすると周期は 2 倍）を確認
- **「月（g=1.62）」プリセット**で重力が弱いと周期が伸びることを確認
- **減衰係数 γ スライダー**を上げ、振幅が指数的に減衰する様子を見る
- **「位相空間」タブ**で $\theta$–$\omega$ 平面の軌道（無減衰なら閉曲線、減衰ありなら内向きの渦）を観察
- **「全エネルギー（比）」**が無減衰時に 1.0 付近で保たれることを確認

## まとめ

- 線形近似 $T_0 = 2\pi\sqrt{L/g}$ は微小振幅でのみ成立
- 厳密な周期は楕円積分 $T = 4\sqrt{L/g}\,K(\sin^2(\theta_0/2))$
- $\theta_0=30^\circ$ で +1.7%、$120^\circ$ で +37% も周期が伸びる
- RK4 数値解は楕円積分の厳密値と一致し、実装の正しさを裏づける

「振幅によらない」は便利な近似ですが、大きく振ればきちんと破れます。スライダーを動かして、近似が崩れる瞬間を確かめてみてください。

🟤 **[単振り子シミュレーター（NovaSolver）](https://novasolver.jp/tools/simple-pendulum.html)** で、振幅と周期の関係を体感しましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。関連して [二重振り子](https://novasolver.jp/tools/double-pendulum.html)、[バネ振り子](https://novasolver.jp/tools/spring-pendulum.html)、[位相空間ポートレート](https://novasolver.jp/tools/phase-space-portrait.html) もどうぞ。
