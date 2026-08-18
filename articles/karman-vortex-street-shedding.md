---
title: "カルマン渦列 — fs = St·V/D とロックイン、橋を落とす流体振動"
emoji: "🌊"
type: "tech"
topics: ["javascript", "流体力学", "CFD", "可視化", "数値計算"]
published: true
---

![カルマン渦列 — NovaSolver](/images/karman-vortex/cover.png)

## 旗がはためき、橋が落ちる理由

川の橋脚の後ろにできる規則正しい渦の列、風で電線が「ヒューン」と鳴る音（エオルス音）、旗のはためき——これらはすべて同じ現象、**カルマン渦列（von Kármán vortex street）** が原因です。円柱のような鈍頭物体に流れが当たると、後流に上下交互の渦が周期的に剥がれていきます。

この周期的な力が構造物の固有振動数と一致すると、振幅が暴走的に増大する**ロックイン**が起き、最悪の場合は破壊に至ります。1940 年のタコマナローズ橋崩落はその象徴です。この記事では渦放出周波数の式 $f_s = \mathrm{St}\cdot V/D$ を軸に、危険な流速をどう見積もるかを解説します。

🌊 **動くデモ**: [カルマン渦 シミュレーター（NovaSolver）](https://novasolver.jp/tools/karman-vortex.html)

## 渦放出周波数とストローハル数

渦が剥がれる周波数 $f_s$ は、流速 $V$ と円柱直径 $D$ に対して次式で与えられます。

$$
f_s = \mathrm{St}\cdot\frac{V}{D}
$$

ここで **$\mathrm{St}$ はストローハル数**——渦放出の「リズム」を無次元化した量です。円柱では Reynolds 数が広い範囲（おおむね $\mathrm{Re}=300\sim2\times10^5$）で $\mathrm{St}\approx0.20$ にほぼ一定であり、これがカルマン渦の最大の特徴です。流速や直径が変わっても比例関係が崩れにくいため、設計時の予測が立てやすいのです。

ツールの既定値（$V=5\,\mathrm{m/s}$、$D=50\,\mathrm{mm}$、$\mathrm{St}=0.200$）で計算すると

$$
f_s = 0.200\times\frac{5}{0.05} = 20.0\,\mathrm{Hz}
$$

となります。流れの様子は Reynolds 数 $\mathrm{Re}=VD/\nu$ で決まり、空気（$\nu=1.5\times10^{-5}\,\mathrm{m^2/s}$）では

$$
\mathrm{Re} = \frac{5\times0.05}{1.5\times10^{-5}} \approx 1.67\times10^{4}
$$

と乱流域に入ります。なお渦放出が始まる臨界 Reynolds 数は本来 $\mathrm{Re}\approx47$ 付近（ベナール–カルマン不安定）で、そこから層流渦列・遷移を経て、本ツールが想定する乱流渦列の範囲に至ります。

![円柱後流の渦列と V-fs 線図（ロックイン帯）](/images/karman-vortex/charts-closeup.png)

左図のように、上側には反時計回り（赤）、下側には時計回り（青）の渦が交互に並びます。渦の間隔は波長 $\lambda=V/f_s$ に対応します。

## ロックイン：渦が構造に「引き込まれる」

通常の共振は「外力の周波数 = 固有振動数」で起きますが、カルマン渦では少し事情が違います。$f_s$ が構造物の固有振動数 $f_n$ に**近づく**と、渦の周期の方が $f_n$ に引き込まれて $f_s=f_n$ で同期してしまうのです。これが**ロックイン**で、判定条件はおおよそ

$$
0.85 < \frac{f_s}{f_n} < 1.15
$$

引き込まれた領域では振幅が急増します。ツール既定値では $f_s/f_n = 20/25 = 0.800$ でロックイン帯のすぐ外（判定「no」）。では危険な流速はどこか——青線（$f_s=\mathrm{St}V/D$）と緑線（$f_n$）の交点を与える**臨界流速**

$$
V_{cr} = \frac{f_n\,D}{\mathrm{St}} = \frac{25\times0.05}{0.20} = 6.25\,\mathrm{m/s}
$$

です。右図の橙点線がこの $V_{cr}=6.25\,\mathrm{m/s}$。$V$ をここまで上げると $f_s=25\,\mathrm{Hz}$、$f_s/f_n=1.00$ となり、黄色マーカーが赤いロックイン帯に入ります。設計では運転流速範囲がこの $V_{cr}$ を跨がないよう $f_n$ をずらすのが鉄則です。

## JavaScript での計算

計算ロジック自体は非常にシンプルで、CFD を解かずとも危険度評価ができます。

```javascript
const NU_AIR = 1.5e-5;                       // 空気 20°C
function evaluate(V, D_mm, St, fn) {
  const D  = D_mm * 1e-3;                     // mm -> m
  const fs = St * V / D;                      // 渦放出周波数
  const Re = V * D / NU_AIR;                  // Reynolds 数
  const ratio = fs / fn;                      // 周波数比
  const lockin = (ratio > 0.85 && ratio < 1.15) ? 'yes' : 'no';
  const Vcr = fn * D / St;                    // 臨界流速
  return { fs, Re, ratio, lockin, Vcr };
}
```

渦列の可視化部分は流速に応じて波長 $\lambda=V/f_s$ で渦を配置し、上下交互に時計回り／反時計回りの渦を流していくことで再現します。

![流速 V を上げると動作点が固有振動数に近づきロックインへ](/images/karman-vortex/slider-anim.gif)

## ツールで遊ぶ

[カルマン渦 シミュレーター](https://novasolver.jp/tools/karman-vortex.html)で試してほしい操作：

- **流速 V スライダー**を 5 → 6.25 m/s に上げ、$f_s/f_n$ が 0.80 → 1.00 になり**ロックイン判定が「yes」**に切り替わる瞬間を見る
- **「V をスイープ」ボタン**で流速を自動掃引し、黄色マーカーが緑の $f_n$ 線を横切る様子を観察
- **円柱直径 D スライダー**を変え、$f_s$ と Reynolds 数が同時に変わるのを確認
- **Strouhal 数 St スライダー**（0.18〜0.22）を動かし、同じ V・D でも $f_s$ がばらつく＝設計の不確かさを体感
- **固有振動数 fn スライダー**を変えて、臨界流速 $V_{cr}=f_n D/\mathrm{St}$ がどう移動するか見る
- **計算結果**（$f_s$、Reynolds 数、$f_s/f_n$、ロックイン）と **V-fs 線図**で危険域を読み取る

## まとめ

- カルマン渦の放出周波数は $f_s = \mathrm{St}\cdot V/D$。円柱では $\mathrm{St}\approx0.20$ が広い Re 範囲で一定
- 既定値で $f_s=20\,\mathrm{Hz}$、$\mathrm{Re}\approx1.67\times10^4$（渦放出の臨界は本来 $\mathrm{Re}\approx47$）
- **ロックイン**（$0.85<f_s/f_n<1.15$）で振幅が暴走。危険は臨界流速 $V_{cr}=f_n D/\mathrm{St}=6.25\,\mathrm{m/s}$ 付近
- 対策は $f_n$ をずらす・ヘリカルストレーキ・減衰付加など。橋・煙突・海洋ライザー・熱交換器伝熱管で必須の評価

CFD を回す前の「当たり」をつける流体振動の基礎を、スライダーで確かめてみてください。

🌊 **[カルマン渦 シミュレーター（NovaSolver）](https://novasolver.jp/tools/karman-vortex.html)** で、橋を落とす流速がどこにあるかを自分の目で見つけましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。流体・振動系では [渦形成シミュレーター](https://novasolver.jp/tools/vortex-formation.html)、[終端沈降速度](https://novasolver.jp/tools/settling-velocity.html)、[抗力係数](https://novasolver.jp/tools/drag-coefficient.html) なども揃えています。
