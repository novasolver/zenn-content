---
title: "PID 制御のチューニング法 4つ — Z-N / Cohen-Coon / IMC / SIMC をステップ応答で比較する"
emoji: "🎛️"
type: "tech"
topics: ["javascript", "数学", "制御工学", "可視化", "chartjs"]
published: false
---

![PID 調整法比較ツール — NovaSolver](/images/pid-tuning/cover.png)

## なぜ PID チューニングは難しいのか

PID 制御は単純な式 $u(t) = K_p e(t) + K_i \int e \, dt + K_d \frac{de}{dt}$ で表せますが、現場で困るのは **「$K_p, K_i, K_d$ をいくつに設定するか」** という一点に尽きます。

経験的にはトライ&エラーですが、**プロセスを一次遅れ + むだ時間（FOPDT）** にモデル化できれば、いくつかの **解析的チューニング法** が使えます。代表的なのが：

| 手法 | 設計思想 | 得意な場面 |
|---|---|---|
| Ziegler-Nichols (Z-N) | 4 分の 1 減衰応答を狙う | サーボ系・追従重視 |
| Cohen-Coon | 統計的経験則 | 1次遅れ系の代表値として |
| IMC（Internal Model Control） | 内部モデルで $\lambda$ を陽に指定 | 振動を抑えたい |
| SIMC（Skogestad IMC） | IMC を 1パラメータで近似 | 最もシンプル、安全側 |

この記事では：

1. FOPDT モデルから 4 手法のゲインを求める数式を整理
2. ステップ応答で実際に違いを見る
3. JavaScript 50 行でゲイン計算 + シミュレーションを実装

📐 **動くデモ**: [PID 調整法比較ツール（NovaSolver）](https://novasolver.jp/tools/pid-tuning.html)

## FOPDT モデル

プロセス（制御対象）を以下のように近似します：

$$
G_p(s) = \frac{K}{\tau s + 1} e^{-\theta s}
$$

- $K$: プロセスゲイン
- $\tau$: 時定数
- $\theta$: むだ時間

この 3 パラメータがあれば、解析的にゲインが出ます。

## 4 手法の計算式

| 手法 | $K_p$ | $T_i$（積分時間） | $T_d$（微分時間） |
|---|---|---|---|
| Z-N | $\dfrac{1.2 \tau}{K \theta}$ | $2\theta$ | $0.5\theta$ |
| Cohen-Coon | $\dfrac{1}{K}\left(\dfrac{\tau}{\theta}\right)\left(\dfrac{4}{3} + \dfrac{\theta}{4\tau}\right)$ | $\theta \dfrac{32 + 6\theta/\tau}{13 + 8\theta/\tau}$ | $\dfrac{4\theta}{11 + 2\theta/\tau}$ |
| IMC | $\dfrac{\tau}{K(\lambda + \theta)}$ | $\tau$ | $0$（PI 制御として） |
| SIMC | $\dfrac{\tau}{K(\lambda + \theta)}$ | $\min(\tau, 4(\lambda+\theta))$ | $0$ |

IMC と SIMC は **$\lambda$（クローズドループ時定数の目標値）** を設計者が指定する点が特徴。$\lambda = \theta$ にすると速い応答、$\lambda = 5\theta$ なら振動を強く抑制。

## JavaScript で実装

```javascript
function tuningGains(K, tau, theta, lambda) {
  const tt = theta / tau;
  return {
    'Z-N': {
      Kp: 1.2 * tau / (K * theta),
      Ti: 2 * theta,
      Td: 0.5 * theta,
    },
    'Cohen-Coon': {
      Kp: (tau / (K * theta)) * (4/3 + tt / 4),
      Ti: theta * (32 + 6 * tt) / (13 + 8 * tt),
      Td: 4 * theta / (11 + 2 * tt),
    },
    'IMC': {
      Kp: tau / (K * (lambda + theta)),
      Ti: tau,
      Td: 0,
    },
    'SIMC': {
      Kp: tau / (K * (lambda + theta)),
      Ti: Math.min(tau, 4 * (lambda + theta)),
      Td: 0,
    },
  };
}

// 例: K=1, τ=10, θ=2, λ=5
console.table(tuningGains(1, 10, 2, 5));
```

`console.table` で並べると、Z-N が一番ゲイン大、SIMC が一番穏やか、という関係が一目でわかります。

## ステップ応答の比較

NovaSolver のツールでは、4 手法のステップ応答が同じグラフに重ねて表示されます：

![4手法のステップ応答比較](/images/pid-tuning/charts-closeup.png)

特徴をざっと読み取ると：

- **Z-N**：立ち上がりは最速、ただし **オーバーシュート 20% 超え**
- **Cohen-Coon**：Z-N に近い挙動だがやや穏やか
- **IMC**：オーバーシュートほぼゼロ、整定までも安定
- **SIMC**：最も保守的、整定は遅いが絶対に振動しない

「速さ」と「安定」のトレードオフが、グラフから直感的に読み取れます。

## 評価指標

ツールでは各手法を 4 つの指標で定量評価します：

![オーバーシュート・整定時間などの定量指標](/images/pid-tuning/stats.png)

- **IAE**（Integral of Absolute Error）: $\int |e(t)| dt$ — 全体的な追従誤差
- **オーバーシュート [%]**：行き過ぎ量
- **整定時間 [s]**：±5% 以内に収まる時間
- **ピーク値**：応答の最大値

実機では「オーバーシュート < 10%、整定時間 < 30 秒」のような数値目標があるはずなので、**目標を満たす手法を選ぶ**だけです。

## $\lambda$ を動かして体感する

IMC/SIMC の真価は **$\lambda$ を自由に動かせる**ところにあります。NovaSolver のツールで $\lambda$ スライダーを動かすと、リアルタイムに応答が変化します：

![λ スライダーでクローズドループ時定数を変える](/images/pid-tuning/slider-anim.gif)

- $\lambda$ 小 → 速いが攻めた応答
- $\lambda$ 大 → 遅いが安全な応答

実機で発振しそうなときは、まず $\lambda$ を大きくして安全側に振るのが定石です。

## まとめ

- PID チューニングは「FOPDT モデル化 → 解析的式でゲイン計算」が出発点
- 4 手法は **トレードオフが違う**：Z-N（速い）⇔ SIMC（安全）
- 実機では **指標目標を満たす一番速い手法** を選ぶ
- IMC/SIMC は $\lambda$ で挙動を調整できる柔軟性が利点

理論を知ったら、あとは触って体に染み込ませるのが早い。

📐 **[PID 調整法比較ツール（NovaSolver）](https://novasolver.jp/tools/pid-tuning.html)** で、プロセスパラメータと $\lambda$ を動かしてみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。制御系のラインナップは [シミュレーター一覧 → 制御工学](https://novasolver.jp/tools/) からどうぞ。
