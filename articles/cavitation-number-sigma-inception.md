---
title: "キャビテーション数 σ — 流れが「常温で沸く」瀬戸際を測る無次元数"
emoji: "🫧"
type: "tech"
topics: ["javascript", "物理", "流体力学", "可視化", "シミュレーション"]
published: false
---

![キャビテーション数 σ — NovaSolver](/images/cavitation-number/cover.png)

## キャビテーション数とは

やかんの水は温度を上げると沸きますが、液体は**圧力を下げても沸きます**。流れの中で物体のまわりを水が速く回ると、その部分の圧力がぐっと下がり、蒸気圧まで達すると常温の水でもそこで蒸発して泡（空洞）ができます。これがキャビテーションです。

その「泡のできやすさ」を測る無次元数が **キャビテーション数 $\sigma$** です。

$$
\sigma = \frac{p - p_v}{\tfrac12 \rho V^2}
$$

分子 $(p - p_v)$ は「いまの局所静圧が蒸気圧からどれだけ余裕があるか」、分母 $\tfrac12\rho V^2$ は「流れの動圧」。つまり $\sigma$ は **圧力の余裕を流れの勢いで割った値**です。$\sigma$ が大きければ余裕たっぷりで安全、小さいと泡ができる瀬戸際にあります。

この記事では、$\sigma$ が流速に対してどう変化するか、初生キャビテーション数 $\sigma_i$ による判定の仕組み、そして実機設計での留意点を扱います。

📐 **動くデモ**: [キャビテーション数シミュレーター（NovaSolver）](https://novasolver.jp/tools/cavitation-number.html)

## 流速の 2 乗で効く

分母の動圧 $q = \tfrac12\rho V^2$ は流速 $V$ の 2 乗で増えるため、$\sigma$ は $1/V^2$ で急減します。流速を 2 倍にすると動圧は 4 倍、$\sigma$ は約 1/4 になります。

$$
q = \tfrac12 \rho V^2, \qquad \Delta p = p - p_v
$$

高速の流れほど物体表面の圧力が下がりやすく、キャビテーションを起こしやすいのはこのためです。プロペラを高回転で回したり、バルブを絞って流速を上げたりすると危険域に入ります。

## 初生キャビテーション数 σ_i による判定

「いくつ以下だとアウトか」の境目が **初生キャビテーション数 $\sigma_i$** です。翼・バルブ・ポンプ羽根車・船舶プロペラなど、形状ごとに固有の値を持ちます。運転中の $\sigma$ が $\sigma_i$ まで下がると気泡が発生し始め、それを下回ると本格的に発生します。

$$
\sigma \le \sigma_i \;\Rightarrow\; \text{キャビテーション発生}
$$

## JavaScript で書くと

ツールの計算ロジックはシンプルです（圧力は kPa 入力、動圧は Pa で計算）。

```javascript
function compute(pLocal, pVapor, rho, vel, sigInc) {
  const qDyn = 0.5 * rho * vel * vel;              // 動圧 [Pa]
  const dPmargin = pLocal - pVapor;                // 圧力余裕 [kPa]
  const sigma = qDyn > 0
    ? (pLocal * 1000 - pVapor * 1000) / qDyn        // 無次元
    : Infinity;
  const ratio = sigma / sigInc;

  let judge;
  if (sigma > 1.2 * sigInc)      judge = "安全（発生せず）";
  else if (sigma >= sigInc)      judge = "初生近傍（注意）";
  else                            judge = "キャビテーション発生";

  return { qDyn, dPmargin, sigma, ratio, judge };
}
```

デフォルト値 $p = 101.3\ \mathrm{kPa},\ p_v = 2.34\ \mathrm{kPa},\ \rho = 998\ \mathrm{kg/m^3},\ V = 12\ \mathrm{m/s},\ \sigma_i = 1.0$ を入れると：

- 動圧 $q = \tfrac12 \times 998 \times 12^2 = 71.86\ \mathrm{kPa}$
- 圧力余裕 $\Delta p = 101.3 - 2.34 = 98.96\ \mathrm{kPa}$
- $\sigma = 98960 / 71856 = 1.377$、$\sigma/\sigma_i = 1.38$ → **安全（発生せず）**

## σ vs 流速 — 急降下するカーブ

$\sigma$ を流速の関数として描くと、$1/V^2$ の急降下が見えます。

![キャビテーション数と流速・静圧の関係](/images/cavitation-number/charts-closeup.png)

低速側では $\sigma$ が大きく安全ですが、流速が上がると急にカーブが落ち、$\sigma_i$ のライン（赤破線）を割ったところでキャビテーションが始まります。デフォルト条件で流速だけを倍にすると：

| 流速 $V$ [m/s] | 動圧 $q$ [kPa] | $\sigma$ | 判定（$\sigma_i = 1.0$） |
|---|---|---|---|
| 6 | 17.96 | 5.510 | 安全 |
| 12 | 71.86 | 1.377 | 安全 |
| 18 | 161.7 | 0.612 | 発生 |
| 24 | 287.4 | 0.344 | 発生 |

$V=12$ から $V=24$ へ倍にすると、$\sigma$ は $1.377 \to 0.344$ とちょうど 1/4 になり、$\sigma_i = 1.0$ を割って発生域に入ります。

## ツールで遊ぶ

NovaSolver のツールでは、5 つのスライダーと翼まわりの気泡雲アニメーションで $\sigma$ を体感できます。

![流速を上げると気泡雲が発生する](/images/cavitation-number/slider-anim.gif)

試してほしい操作：

- **流速 $V$ スライダー**を上げて「キャビテーション数 σ」カードが急減し、「キャビテーション判定」が安全 → 注意 → 発生に切り替わる様子を観察
- **流体の蒸気圧 $p_v$** を上げる（高温水を模擬）と圧力余裕が縮み、$\sigma$ が下がることを確認（水は 20°C で約 2.34 kPa、80°C で約 47.4 kPa）
- **初生キャビテーション数 $\sigma_i$** を変えて、同じ運転点でも判定（verdict メッセージ）が変わることを見る
- **「σ vs 流速」「σ vs 局所静圧」グラフ**で、現在の運転点（オレンジ点）と $\sigma_i$ ライン（赤破線）の位置関係を確認

翼の負圧面に気泡雲が湧き、下流で崩壊する様子がキャンバスに描かれます。

## まとめ

- キャビテーション数 $\sigma = (p - p_v)/(\tfrac12\rho V^2)$ は「圧力余裕 ÷ 動圧」の無次元数
- 動圧が $V^2$ で効くため、$\sigma$ は $1/V^2$ で急減する
- $\sigma \le \sigma_i$ でキャビテーション発生。デフォルト条件では $\sigma = 1.377$（安全）
- 流速を 12→24 m/s に倍にすると $\sigma$ は 1/4（1.377→0.344）になり発生域へ

実機設計では基準点の取り方と運転温度（$p_v$ は温度に強く依存）に注意が必要です。$\sigma_i$ 自体も表面粗さや溶存気体で変動する不確かな値のため、運転 $\sigma$ を $\sigma_i$ の 1.2〜2 倍程度に保つ余裕を持たせるのが一般的です。遠心ポンプ（NPSH）・水力タービン・船舶プロペラ・制御弁の壊食対策で広く使われる考え方です。

📐 **[キャビテーション数シミュレーター（NovaSolver）](https://novasolver.jp/tools/cavitation-number.html)** で、流速を上げて気泡雲が湧く瞬間を見てみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。流体・水力機械まわりでは [ベルヌーイの定理・管路流れ](https://novasolver.jp/tools/bernoulli-flow.html)、[管内流れ](https://novasolver.jp/tools/pipe-flow.html)、[クェット流れ](https://novasolver.jp/tools/couette-flow.html) なども揃えています。
