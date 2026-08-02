---
title: "ブラウザだけで動く1Dシステムシミュレータを自作した — 熱回路網と管路網を1つのNewtonソルバーで解く"
emoji: "🔧"
type: "tech"
topics: ["javascript", "数値計算", "シミュレーション", "物理", "CAE"]
published: true
---

![NovaSolver 1D 熱回路網シミュレータ](/images/novasolver-1d-browser-simulator/cover.png)

## なぜブラウザで1Dシミュレータなのか

熱回路網や管路網を回路図のように組んで解く「1Dシステムシミュレーション」の世界には、AMESim や Simscape という強力な商用ツールがあります。ただしライセンスは高価で、無料帯にはぽっかり空白がある。学生や、3D CFD/FEA に進む前の**システムレベルの当たり付け**をしたいエンジニアが気軽に触れるものが、意外と見当たりません。

もうひとつの現実として、企業の管理された PC では exe のインストール自体が申請の壁に阻まれることが多い。ブラウザで開くだけなら、この壁を越えられます。

そこで、**インストール不要・サインアップ不要・計算はすべて手元のブラウザ内**（モデルが外に出ない）という 1D シミュレータを作りました。現状は熱回路網と管路網（配管網）の 2 ドメイン、定常＋熱の過渡解析まで。回路図エディタで部品をドラッグ＆ドロップして配線すると、編集のたびに再計算されます（「実行」ボタンはありません）。

📐 **動くもの**: [熱回路網シミュレータ](https://novasolver.jp/1d/thermal-network.html) / [管路網シミュレータ](https://novasolver.jp/1d/fluid-network.html)（ソースは [GitHub](https://github.com/novasolver/physics-simulators/tree/main/1d) で MIT 公開）

先に断っておくと、これは商用ツールの代替ではなく、**見積り・教育グレードの v0.2** です。この記事では、その中身——「なぜ熱と流体が同じソルバーで解けるのか」という設計判断と、非線形（放射の $T^4$、Darcy–Weisbach）の扱い、そして正直にハマった話を書きます。

## 核心の設計判断：熱・流体・電気は同じ数学

熱回路網・管路網・電気回路は、見た目は違っても数学的には同じ構造をしています。

- **節点の保存則**: 各節点で流入と流出が釣り合う（熱流 [W]、体積流量 [m³/s]、電流 [A]）
- **枝の構成則**: 各枝でポテンシャル差が流れを決める（$q = \Delta T/R$、$Q = f^{-1}(\Delta p)$、$I = \Delta V/R$）

つまり節点ごとに残差

$$
F_i = \sum_{\text{枝}} (\text{節点 } i \text{ から流出する流れ}) = 0
$$

を立てて、Newton 法で解けばよい。構成則が非線形でも枠組みは変わりません。

この観察から、アーキテクチャは自然に決まりました。**ソルバーは 1 つ（ドメイン非依存の純粋関数群）、ドメインは部品ライブラリの追加で増やす**。ファイル構成はこうです。

| ファイル | 役割 |
|---|---|
| `solver.js` | 数値コア。残差＋ヤコビアン定式化の Newton 法、部分ピボット付き密 LU、後退 Euler。DOM 依存なし |
| `lib-thermal.js` | 熱部品：熱抵抗 R、対流 hA、放射 εσA（非線形）、熱容量 C、発熱源 P、固定温度 |
| `lib-fluid.js` | 流体部品：直管（Darcy–Weisbach）、局所損失 ζ、ポンプ、流量源、固定圧力 |

ソルバーと部品ライブラリの間の契約は 1 行で書けます。

```js
// ctx = { J, F, T, Tprev, dt, transient }
// F[i] += net flow OUT of node i;  J[i][j] += dF[i]/dT[j]
```

各部品は `stamp(ctx, el)` という関数を持ち、自分の残差寄与を `F` に、その微分を `J` に**押印（stamp）**します。SPICE 系回路シミュレータでおなじみのやり方です。たとえば熱抵抗や対流のような線形コンダクタンス $q = G(T_a - T_b)$ の stamp は、`lib-thermal.js` ではこう書かれています。

```js
/* two-node conductance helper: q = G*(Ta - Tb) */
function stampConductance(ctx, a, b, G) {
  var Ta = ctx.T[a], Tb = ctx.T[b], q = G * (Ta - Tb);
  ctx.F[a] += q; ctx.F[b] -= q;
  ctx.J[a][a] += G; ctx.J[a][b] -= G;
  ctx.J[b][a] -= G; ctx.J[b][b] += G;
}
```

ソルバー側は部品が何者かをいっさい知りません。全部品の stamp を呼んで行列を組み立て、Newton 反復を回すだけです。`solver.js` の中核はこの 30 行弱です。

```js
function newton(sys, T0, Tprev, dt, opt) {
  opt = opt || {};
  var tol = opt.tol || 1e-8, maxIt = opt.maxIter || 60, n = sys.n;
  var T = Float64Array.from(T0), it, i;
  for (it = 0; it < maxIt; it++) {
    var a = assemble(sys, T, Tprev, dt);
    var dec = luDecompose(a.J, n);
    if (!dec) {
      return { ok: false, reason: "singular",
               T: T, iterations: it };
    }
    var rhs = new Float64Array(n);
    for (i = 0; i < n; i++) rhs[i] = -a.F[i];
    var dT = luSolve(dec, rhs, n);
    var norm = 0, scale = 0;
    for (i = 0; i < n; i++) {
      var ad = Math.abs(dT[i]);
      if (ad > norm) norm = ad;
      var at = Math.abs(T[i]);
      if (at > scale) scale = at;
    }
    // damping keeps radiation-dominated systems from overshooting
    var relax = norm > 100 ? 100 / norm : 1;
    for (i = 0; i < n; i++) T[i] += relax * dT[i];
    if (norm <= tol * Math.max(1, scale)) {
      return { ok: true, T: T, iterations: it + 1, residual: norm };
    }
  }
  return { ok: false, reason: "no-convergence", T: T, iterations: maxIt };
}
```

線形の LU は自前の密行列＋部分ピボット（数百節点までなら十分）、固定温度・固定圧力の Dirichlet 条件は組み立て後の**行置換**（$J_{ii}=1$、$F_i = T_i - T_{\text{fix}}$）で課します。過渡解析は後退 Euler で、熱容量が stamp 時に $C(T_i - T_i^{\text{prev}})/\Delta t$ を残差へ足すだけ。無条件安定なので、ミリ秒オーダーの電子部品と時間オーダーの筐体熱容量が混在するスティフな系でも大きな $\Delta t$ で回せます。

## 非線形はどう扱うか

### 放射の T⁴ — ヤコビアンに微分を書くだけ

放射は $q = \varepsilon\sigma A(T_a^4 - T_b^4)$（$T$ はケルビン）という強い非線形ですが、stamp 契約の上では特別扱い不要です。微分 $\partial q/\partial T_a = 4\varepsilon\sigma A T_a^3$ をヤコビアンに書けば、Newton 法が他の部品と一緒に解いてくれます。

```js
/* q = eps*sigma*A*(Ta^4 - Tb^4) with T in kelvin; dq/dTa = 4 eps sigma A Ta^3 */
stamp: function (ctx, el) {
  var a = el.nodes[0], b = el.nodes[1];
  var c = num(el.p.eps, 0.85) * SIGMA * Math.max(num(el.p.A, 0.01), 1e-9);
  var Ta = ctx.T[a] + K0, Tb = ctx.T[b] + K0;
  var q = c * (Ta * Ta * Ta * Ta - Tb * Tb * Tb * Tb);
  var da = 4 * c * Ta * Ta * Ta, db = -4 * c * Tb * Tb * Tb;
  ctx.F[a] += q; ctx.F[b] -= q;
  ctx.J[a][a] += da; ctx.J[a][b] += db;
  ctx.J[b][a] -= da; ctx.J[b][b] -= db;
}
```

先ほどの `newton` にあったステップ制限（1 反復あたり最大 100 単位）は、主にこの放射のためです。$T^4$ は初期推定から遠いと接線が暴れ、無減衰の Newton は容易にオーバーシュートします。

### 流体の Darcy–Weisbach — stamp の中に局所 Newton を入れ子にする

管路のほうは一段厄介です。直管の圧力損失は Darcy–Weisbach 式

$$
\Delta p = f\,\frac{L}{D}\,\frac{\rho}{2}\,v\lvert v\rvert
$$

で、摩擦係数 $f$ 自体が Reynolds 数（つまり流量）に依存します。層流なら Hagen–Poiseuille で線形、乱流なら Swamee–Jain の陽公式。つまり $\Delta p(Q)$ は素直に書けるのに、大域ソルバーが必要とするのは逆向きの $Q(\Delta p)$ です。

そこで、**stamp の内側で局所 Newton を回して $\Delta p(Q) = \Delta p_{\text{target}}$ を逆算**し、その点での接線コンダクタンス $G = dQ/d(\Delta p)$ を大域ヤコビアンに渡す構造にしました。

```js
/* two-node resistive stamp shared by PIPE and KV */
function stampResistive(ctx, el, dpFn, m) {
  var a = el.nodes[0], b = el.nodes[1];
  var dpPa = (ctx.T[a] - ctx.T[b]) * KPA;
  var Q = solveQ(dpFn, m, dpPa, el._Q);
  el._Q = Q;                                    // warm start for the next iteration
  var h = Math.max(1e-14, Math.abs(Q) * 1e-7);
  var dpdQ = (dpFn(Q + h, m) - dpFn(Q - h, m)) / (2 * h);
  var G = KPA / Math.max(dpdQ, 1e-9);           // dQ/dx, x in kPa
  ctx.F[a] += Q; ctx.F[b] -= Q;
  ctx.J[a][a] += G; ctx.J[a][b] -= G;
  ctx.J[b][a] -= G; ctx.J[b][b] += G;
}
```

`solveQ` はステップをクランプしたガード付き Newton で、前回の大域反復の解 `el._Q` をウォームスタートに使うため、実際は数回で収束します。$\Delta p(Q)$ が滑らかで狭義単調である限りこの入れ子は安定に動きます——そして「滑らかで単調」を守ること自体が、次のハマりポイントでした。

## ハマった話（2 件）

### (a) Pa で解いたら収束が死んだ → 未知数を kPa に

最初、圧力を SI 素直に Pa で解いていました。すると典型的な管路（数十〜数百 kPa）で Newton がまったく収束しない。原因は先ほどの**ステップ制限**です。熱の世界では「1 反復 100 単位（= 100 ℃）まで」は妥当な減衰ですが、Pa の世界では 100 Pa ずつしか進めないことを意味します。目標が 300,000 Pa なら 3000 反復——上限 60 反復では絶望的です。

対策はソルバーをいじるのではなく、**未知数のスケールを物理に合わせる**こと。節点未知数を kPa にしたら、典型圧力は数十〜数百の範囲に収まり、数回の減衰ステップで届くようになりました。`lib-fluid.js` の冒頭コメントにその決定が残っています。

```js
/* Unknown per node: pressure in kPa. (The solver caps Newton steps at 100 units per
 * iteration — with Pa that damping would cripple convergence; kPa keeps typical
 * pressures within a few damped steps.) */
```

「ソルバーの内部定数を触る前に、問題を無次元化・スケーリングせよ」という数値計算の教科書的教訓を、身をもって確認した形です。

### (b) 層流/乱流の生スイッチで解が消える → 遷移帯を線形ブレンド

層流式と乱流式を Re = 2300 で単純に切り替えると、$\Delta p(Q)$ が**その点で不連続**になります（層流側と乱流側の値が一致しないため、曲線にジャンプができる）。すると、目標の $\Delta p$ がちょうどそのギャップの中に落ちた場合、**$\Delta p(Q) = \Delta p_{\text{target}}$ を満たす $Q$ が存在しない**。局所 Newton はジャンプの両側を行き来して振動し、大域反復ごと巻き添えで発散します。

対策は Re 2300–3500 の遷移帯で両式を線形ブレンドして、$\Delta p(Q)$ を連続かつ単調に保つこと。

```js
function pipeDp(Q, m) {
  var A = Math.PI * m.D * m.D / 4;
  var v = Q / A;
  var av = Math.abs(v);
  var lam = 32 * m.mu * m.L * v / (m.D * m.D);
  var Re = m.rho * av * m.D / m.mu;
  if (Re < 2300) return lam;
  var sj = 0.25 / Math.pow(Math.log10(m.rough / (3.7 * m.D) + 5.74 / Math.pow(Re, 0.9)), 2);
  var turb = sj * (m.L / m.D) * (m.rho / 2) * v * av;
  if (Re >= 3500) return turb;
  var w = (Re - 2300) / 1200;
  return (1 - w) * lam + w * turb;
}
```

物理的にも遷移域の摩擦係数は不確かな領域なので、数値の都合で入れた補間が物理の不定性とだいたい重なってくれる、という割り切りです。同様に、弁などの局所損失 $\Delta p = \zeta\frac{\rho}{2}v\lvert v\rvert$ も $v\lvert v\rvert \to v\sqrt{v^2+\epsilon^2}$ と正則化して、$\Delta p = 0$ 近傍で微分が消えないようにしています。

## 検証の思想：開くたびに答え合わせする

無料のソルバーが仕事で使われない最大の理由は、機能不足ではなく**信用できないから**だと思っています。中身が見えず、誰も答え合わせをしていない計算機に、根拠が必要な数字を任せられるわけがない。

だからこのプロジェクトでは、**解析解と突き合わせる検証ケースを、ユーザーがページを開くたびに実行して全ケース表示**する設計にしました。熱は 6 ケース（直列/並列抵抗、対流境界、集中熱容量の過渡指数則、エネルギー保存、放射平衡）、流体は 4 ケース（Hagen–Poiseuille、直列、並列分流、乱流分岐の質量保存）。たとえば放射平衡のケースは、非線形方程式 $P = \varepsilon\sigma A(T^4 - T_\infty^4)$ の閉形式解

$$
T = \left(\frac{P}{\varepsilon\sigma A} + T_\infty^4\right)^{1/4}
$$

とソルバー出力を比較します。同じスイートが Node でそのまま走るので、1 コマンドが CI にもなります。

```
$ node js/verify.js
PASS series-R  ...
PASS radiation  got=82.251209 exact=82.251209 rel=6.91e-16
ALL PASS (6)

$ node js/verify-fluid.js
ALL PASS (4)
```

定常の相対誤差は最悪でも 1e-15 程度（丸め誤差レベル）、過渡は後退 Euler の理論通り $O(\Delta t)$。「このツールがどこまで合っていて、どこからは合わないか」を数字で開示するのが、無料ツールにできる最低限の誠実さだと考えています。

## まとめと今後

- 熱・流体（・電気）の回路網は「節点の保存則＋枝の構成則」という同じ数学 → **ドメイン非依存の Newton ソルバー 1 つ＋ドメイン別部品ライブラリ**で構成できる
- stamp 契約（`F[i]` に流出、`J[i][j]` に微分）に従えば、放射の $T^4$ のような非線形も微分を書くだけで乗る
- 陽に逆変換できない構成則（Darcy–Weisbach）は、**stamp 内の局所 Newton で逆算＋接線コンダクタンスを大域ヤコビアンへ**
- ハマりどころは数値のスケーリング（Pa → kPa）と構成則の連続性（層流/乱流ブレンド）。どちらも「ソルバーではなく問題の側を整える」のが正解だった
- 検証は解析解との突き合わせを**ページを開くたび全表示**。`node` 一発で CI にもなる

繰り返しになりますが、現状は集中定数（1D）の定常＋熱過渡のみを解く見積り・教育グレードの v0.2 で、部品内部の温度分布や流れ場は出ません。今後は、ポンプの Q–H 性能曲線、熱と流体の連成（冷却ループ：流量が熱伝達を決め、温度が粘度を変える）、電気ドメイン、大規模モデル向けの疎行列ソルバーあたりを予定しています。

同じ構造の系がひとつのソルバーに乗っていく過程は、作っていて素直に楽しいものでした。回路図を組むとその場で解が出る感覚は、ぜひ実物で試してみてください。

📐 **[熱回路網シミュレータ](https://novasolver.jp/1d/thermal-network.html) / [管路網シミュレータ](https://novasolver.jp/1d/fluid-network.html)**（ソース: [GitHub — physics-simulators/1d](https://github.com/novasolver/physics-simulators/tree/main/1d)）
