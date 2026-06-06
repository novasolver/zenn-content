---
title: "二次遅れ系のステップ応答 — 減衰係数 ζ で過渡応答はこう決まる"
emoji: "🌀"
type: "tech"
topics: ["javascript", "数学", "制御工学", "可視化", "chartjs"]
published: false
---

![二次遅れ系のステップ応答 — NovaSolver](/images/control-step/cover.png)

## なぜ二次遅れ系か

実機の制御対象は、ほとんどが **二次遅れ系またはその近似** で表せます：

$$
G(s) = \frac{K \omega_n^2}{s^2 + 2\zeta \omega_n s + \omega_n^2}
$$

- $K$: 定常ゲイン（最終値）
- $\omega_n$: 固有角周波数（応答の速さ）
- $\zeta$: **減衰係数**（オーバーシュート量を決める）

サーボモータ、車のサスペンション、RLC 共振回路、地震応答、ロボットアームの先端剛性——どれもこの形に落ちます。

**$\zeta$ という1つの数字で過渡応答の質感がほぼ決まる**、これが二次遅れ系の威力です。

📐 **動くデモ**: [ステップ応答シミュレーター（NovaSolver）](https://novasolver.jp/tools/control-step.html)

## ζ による 4つのモード

ステップ入力 $r(t) = 1$ を加えたときの応答 $y(t)$ は $\zeta$ によって質的に変わります：

| 領域 | 名前 | 特徴 |
|---|---|---|
| $\zeta = 0$ | 無減衰 | 永久に振動（不安定ではないが減衰しない） |
| $0 < \zeta < 1$ | **不足減衰** | オーバーシュートあり、減衰振動 |
| $\zeta = 1$ | 臨界減衰 | オーバーシュート無し、最速の整定 |
| $\zeta > 1$ | 過減衰 | オーバーシュート無し、ゆっくり整定 |

実用上の **目安は $\zeta = 0.7$**（約 5% オーバーシュート）。サーボ系設計の経験則です。

## 不足減衰系の解析解

$0 < \zeta < 1$ の場合、ステップ応答は閉じた形で書けます：

$$
y(t) = K \left[ 1 - \frac{e^{-\zeta \omega_n t}}{\sqrt{1-\zeta^2}} \sin\left(\omega_d t + \phi\right) \right]
$$

ただし：

$$
\omega_d = \omega_n \sqrt{1-\zeta^2}, \quad \phi = \arctan\frac{\sqrt{1-\zeta^2}}{\zeta}
$$

$\omega_d$ は **減衰固有周波数**。実機での振動の周波数はこれで観測されます（$\omega_n$ ではない、ここが盲点になりがち）。

## オーバーシュート量と整定時間の公式

不足減衰系の **最大オーバーシュート** は：

$$
\text{OS} = e^{-\pi \zeta / \sqrt{1-\zeta^2}} \times 100 \, [\%]
$$

| $\zeta$ | OS [%] |
|---|---|
| 0.3 | 37 |
| 0.5 | 16 |
| 0.7 | 4.6 |
| 0.9 | 0.15 |

**2% 整定時間** はざっくり：

$$
t_s \approx \frac{4}{\zeta \omega_n}
$$

$\omega_n$ を上げれば速くなる、$\zeta$ を上げればオーバーシュートが減る、という関係です。

## 50 行で実装

ステップ応答は **状態空間モデルを陽 Euler で数値積分** すれば書けます：

```javascript
function stepResponse(K, omegaN, zeta, T = 10, dt = 0.001) {
  // x1 = y, x2 = dy/dt
  // dx1/dt = x2
  // dx2/dt = -ωn² x1 - 2ζωn x2 + K ωn² (入力 r=1)
  const omn2 = omegaN * omegaN;
  const c2zomn = 2 * zeta * omegaN;
  let x1 = 0, x2 = 0;
  const t = [], y = [];
  for (let ti = 0; ti < T; ti += dt) {
    t.push(ti);
    y.push(x1);
    const dx1 = x2;
    const dx2 = -omn2 * x1 - c2zomn * x2 + K * omn2;
    x1 += dx1 * dt;
    x2 += dx2 * dt;
  }
  return { t, y };
}

// 例: K=1, ωn=3, ζ=0.5
const { t, y } = stepResponse(1, 3, 0.5);
console.log('最大値:', Math.max(...y).toFixed(3));  // ≈ 1.16（OS ≈ 16%）
```

陽 Euler は数値誤差が乗りやすいので、本気で精度を求めるなら 4 次 Runge-Kutta を使います。

## ζ を動かしてみる

NovaSolver のツールで $\zeta$ スライダーを動かすと、4 つのモードを連続的に体感できます：

![ζ スライダーで過渡応答が連続変化](/images/control-step/slider-anim.gif)

$\zeta = 0.2$ → 派手なオーバーシュート → $\zeta = 0.7$ → 設計目安 → $\zeta = 1.0$ → 臨界 → $\zeta = 2.0$ → ゆっくり収束。

「振動を抑えたい」「速く整定させたい」「設計余裕を取りたい」という現場の要求が、すべてこの 1 つのパラメータで議論できます。

## ステップ応答指標

ツールでは過渡応答の主要指標を自動計算します：

![オーバーシュート・立ち上がり時間・整定時間の数値表示](/images/control-step/stats.png)

実機の制御系設計では、これらの数値目標を満たすゲインを逆算するのが定石です（PID 設計、IMC など）。

## 実用上のチェックポイント

1. **モーター駆動系**: 機械系の $\omega_n$ と電気時定数が分離できない場合、3次以上で考える必要あり
2. **アンチワインドアップ**: 不足減衰系で大入力を入れると、積分項が暴走しがち
3. **離散時間化**: サンプリング周期が遅いと連続時間設計と挙動が変わる（$\omega_n T_s < 0.3$ を目安）

## まとめ

- 二次遅れ系は $K, \omega_n, \zeta$ の 3 パラメータで決まる定番モデル
- 過渡応答の質は **$\zeta$ がほぼ全部を決める**
- 設計目安は $\zeta = 0.7$、OS ≈ 5%
- 整定時間は $t_s \approx 4/(\zeta \omega_n)$

「制御を学ぶ最初の 1 ヶ月で身につけるべき」と言える基礎中の基礎です。

📐 **[ステップ応答シミュレーター（NovaSolver）](https://novasolver.jp/tools/control-step.html)** で、$\zeta$ をスライダーで動かして体感してください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。制御系では [PID チューニング比較](https://novasolver.jp/tools/pid-tuning.html)、[Bode 線図ジェネレーター](https://novasolver.jp/tools/bode-plot.html) もあります。
