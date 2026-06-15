---
title: "玉軸受の接触応力 — Hertz 接触と「外輪の方が高い」理由"
emoji: "⚙️"
type: "tech"
topics: ["javascript", "機械工学", "物理シミュレーション", "可視化", "材料力学"]
published: true
---

![玉軸受の接触応力 — NovaSolver](/images/ball-bearing-hertz-stress/cover.png)

## 玉が転がるだけなのに、なぜ GPa の応力が出るのか

玉軸受は「玉が軌道を転がっているだけ」に見えますが、玉と軌道は**点で接触**しています。曲率の違う 2 つの曲面を押し付けると、接触領域はほんの数百ミクロン四方の小さな円になり、そこに玉 1 個あたり数 kN が集中します。結果、接触圧はあっという間に **GPa オーダー**——鋼の引張降伏応力をはるかに超える値——に達します。

この記事では、玉軸受の接触応力を支配する 3 つのポイントを、実際に手を動かせる形で見ていきます。

1. **Stribeck の荷重分布**——なぜ「1 玉あたり最大荷重」が単純平均の 5 倍になるのか
2. **Hertz 接触**による最大接触圧の式と、JavaScript での実装
3. **内輪 < 外輪**——同じ玉が接しているのに、なぜ外輪側の方が応力が高いのか

📐 **動くデモ**: [玉軸受の接触応力シミュレーター（NovaSolver）](https://novasolver.jp/tools/ball-bearing-hertz-stress.html)

## Stribeck の荷重分布

半径方向の荷重 $F_\text{total}$ は、全玉が均等に分担するわけではありません。すきまや弾性変形のために、**下半周の限られた玉だけ**が荷重を受け持ち、しかも分担は不均等です。Stribeck の解析によれば、内部すきまを考慮した実務式として、最も荷重を受ける 1 玉の荷重は次のように見積もられます（$\alpha$ は接触角、深溝玉軸受では $\alpha = 0$）：

$$
F_\text{max} = \frac{5\,F_\text{total}}{Z\,\cos\alpha}
$$

ここがこのモデルの肝です。玉数 $Z = 8$、全荷重 $F_\text{total} = 10\ \text{kN}$ の場合、**単純平均**なら $10000/8 = 1250\ \text{N/玉}$ ですが、最大荷重を受ける玉は

$$
F_\text{max} = \frac{5 \times 10000}{8} = 6250\ \text{N} = 6.25\ \text{kN}
$$

と、単純平均の 5 倍に達します。応力計算ではこの**最大荷重を受ける 1 玉**を使うのが正しい設計手順です。「玉数で均等割りした荷重で設計する」のはよくある誤りで、危険側（応力を過小評価する側）に外れます。

## Hertz 接触の最大接触圧

接触する 2 曲面の幾何は、**等価曲率半径** $R_{eq}$ に集約されます。玉半径を $r_b = D_b/2$、内輪・外輪の軌道半径を $R_i = (D_p - D_b)/2$、$R_o = (D_p + D_b)/2$ とすると：

$$
\frac{1}{R_{eq,i}} = \frac{1}{r_b} - \frac{1}{R_i},
\qquad
\frac{1}{R_{eq,o}} = \frac{1}{r_b} + \frac{1}{R_o}
$$

内輪は玉に対して**凹面**（軌道のくぼみに玉が乗る）なので符号がマイナス、外輪は**凸面**なのでプラスになります。この符号の差が、後で効いてきます。

球-平面型ヘルツ接触の最大接触圧と接触半径は、等価弾性率 $E^*$ を使って次式で書けます：

$$
p_\text{max} = \frac{1}{\pi}\left(\frac{6\,F_\text{max}\,{E^*}^2}{R_{eq}^{\,2}}\right)^{1/3},
\qquad
a = \left(\frac{3\,F_\text{max}\,R_{eq}}{4\,E^*}\right)^{1/3}
$$

軸受鋼同士（$E = 200\ \text{GPa},\ \nu = 0.3$）の組み合わせで $E^* = 115.4\ \text{GPa}$ です。注目すべきは $p_\text{max} \propto F_\text{max}^{1/3}$ という**弱い荷重依存性**。荷重が 8 倍になっても応力は 2 倍にしかなりません。

## JavaScript で 25 行の実装

ツールが内部で回しているのと同じ計算を、そのまま書き起こせます：

```javascript
const ESTAR = 115.4e9; // Pa（軸受鋼同士の等価弾性率）

function hertz(Fmax, Req) {
  // p_max = (1/pi) * (6 F E*^2 / Req^2)^(1/3)
  return Math.cbrt(6 * Fmax * ESTAR * ESTAR / (Req * Req)) / Math.PI;
}

function ballBearing(F_kN, Db_mm, Z, Dp_mm) {
  const F = F_kN * 1000, Db = Db_mm / 1000, Dp = Dp_mm / 1000;
  const rb = Db / 2;            // 玉半径
  const Ri = (Dp - Db) / 2;     // 内輪軌道半径
  const Ro = (Dp + Db) / 2;     // 外輪軌道半径
  const Fmax = 5 * F / Z;       // Stribeck の1玉最大荷重（α=0）
  const ReqI = rb * Ri / (Ri - rb); // 内輪：凹面（1/rb - 1/Ri）
  const ReqO = rb * Ro / (Ro + rb); // 外輪：凸面（1/rb + 1/Ro）
  return {
    Fmax,
    pmaxI: hertz(Fmax, ReqI),
    pmaxO: hertz(Fmax, ReqO),
  };
}

const r = ballBearing(10, 12, 8, 50);
console.log((r.Fmax / 1e3).toFixed(2), "kN");          // 6.25 kN
console.log((r.pmaxI / 1e9).toFixed(2), "GPa");        // 5.94 GPa（内輪）
console.log((r.pmaxO / 1e9).toFixed(2), "GPa");        // 8.61 GPa（外輪）
```

既定値（$F = 10\ \text{kN}$, $D_b = 12\ \text{mm}$, $Z = 8$, $D_p = 50\ \text{mm}$）で、内輪 **5.94 GPa**、外輪 **8.61 GPa** が得られます。等価曲率半径はそれぞれ $R_{eq,i} \approx 8.77\ \text{mm}$、$R_{eq,o} \approx 5.03\ \text{mm}$、接触半径 $a \approx 0.71\ \text{mm}$ です。

## 内輪より外輪の応力が高い理由

![内輪・外輪の接触応力と玉数依存性](/images/ball-bearing-hertz-stress/charts-closeup.png)

左の棒グラフを見てください。同じ玉・同じ荷重なのに、外輪側（8.61 GPa）が内輪側（5.94 GPa）の **約 1.45 倍**になっています。理由は等価曲率半径です：

$$
\frac{R_{eq,o}}{R_{eq,i}} = \frac{5.03}{8.77} \approx 0.57
$$

外輪は凸面接触で $R_{eq}$ が**小さく**なり、接触面積が狭くなって応力が集中します。一方、内輪は凹面接触で $R_{eq}$ が**大きく**なり、面積が広がって応力が下がります。$p_\text{max} \propto R_{eq}^{-2/3}$ なので、$0.57^{-2/3} \approx 1.45$ と、棒グラフの比とぴたり一致します。

実機の軸受寿命を決める「クリティカルな接触」は、応力の高い**外輪側**になることが多い——この基本特性が、本ツールの一番の見どころです。

## 玉数を増やしても応力はあまり下がらない

右のグラフは、玉数 $Z$ を 5〜20 に振ったときの応力です。$Z$ を増やせば 1 玉荷重 $F_\text{max} = 5F/Z$ は反比例で下がりますが、応力は荷重の 1/3 乗でしか効きません：

$$
p_\text{max} \propto F_\text{max}^{1/3} \propto Z^{-1/3}
$$

実際、$Z = 8 \to 16$ と倍にしても、内輪応力は $5.94\ \text{GPa} \to 4.71\ \text{GPa}$、つまり $2^{-1/3} \approx 0.794$ 倍——**20% 程度しか下がりません**。応力を本気で下げたいなら、玉数より玉径 $D_b$ を大きくする方が効きます（$D_b$ は 1 玉荷重には影響せず、接触面積を直接広げるため）。

> 注意：このモデルは「球と円筒軌道」の球-平面近似で、実機の溝適合度（溝半径 ÷ 玉半径、通常 0.52〜0.54）を考慮していません。実機では接触が楕円になり、応力は本モデル値の 60〜80% 程度に収まることが多い、つまり**安全側（厳しめ）の見積もり**です。設計初期のトレンド把握には十分ですが、最終評価は L10 寿命計算と組み合わせてください。

## ツールで遊ぶ

NovaSolver のツールでは、**$F_\text{total}$ スライダー**を動かすと、軸受断面の最大荷重玉（黄色）と内輪・外輪の接触応力がリアルタイムに変化します：

![全荷重を動かすと内外輪の応力が変わる](/images/ball-bearing-hertz-stress/slider-anim.gif)

試してほしい操作：

- **軸受全荷重 $F_\text{total}$**（0.5〜100 kN）を動かし、応力が $F^{1/3}$ でゆっくり増えるのを体感する
- **玉数 $Z$**（5〜20）を増やしても応力が急には下がらないことを確認する
- **玉直径 $D_b$**（3〜50 mm）を増やすと、外輪応力が大きく下がる
- **ピッチ円直径 $D_p$**（10〜200 mm）を増やすと、内輪応力は上がり外輪応力は下がる（両者のバランス設計）
- 4 枚の **stat-card**（$F_\text{max}$ / 内輪 $p_{max,i}$ / 外輪 $p_{max,o}$ / 接触半径 $a$）と断面図で、設計領域を探す

## まとめ

- 半径荷重は全玉で均等割りされず、Stribeck 式 $F_\text{max} = 5F_\text{total}/(Z\cos\alpha)$ で最大荷重玉に集中する（単純平均の 5 倍）
- Hertz 接触で $p_\text{max} = \frac{1}{\pi}(6 F_\text{max} {E^*}^2 / R_{eq}^2)^{1/3}$、既定値で内輪 5.94 GPa・外輪 8.61 GPa
- 凸面接触の外輪は $R_{eq}$ が小さく、内輪の約 1.45 倍の応力——寿命を決めるのは外輪側
- 応力は $F^{1/3}$・$Z^{-1/3}$ と弱く効くだけ。玉径 $D_b$ を増やす方が効果的

軸受鋼が HV 700 前後まで焼入れされているのは、この GPa オーダーの接触応力に耐えるためです。式は 4 本、JavaScript は 25 行——機械要素の設計感覚を、手元で確かめてみてください。

📐 **[玉軸受の接触応力シミュレーター（NovaSolver）](https://novasolver.jp/tools/ball-bearing-hertz-stress.html)** で、$D_b$ や $D_p$ を動かして応力が許容範囲に収まる設計領域を探してみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。接触・軸受まわりでは [Hertz 接触応力](https://novasolver.jp/tools/hertz-contact.html)、[転がり軸受寿命計算（L10）](https://novasolver.jp/tools/rolling-bearing.html)、[転がり接触疲労・ピッティング強度](https://novasolver.jp/tools/rolling-contact-fatigue.html) なども揃えています。
