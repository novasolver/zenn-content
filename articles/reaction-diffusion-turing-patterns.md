---
title: "反応拡散でチューリングパターンを作る — Gray-Scottモデル入門"
emoji: "🐆"
type: "tech"
topics: ["javascript", "数学", "可視化", "アルゴリズム", "物理シミュレーション"]
published: false
---

![反応拡散とチューリングパターン — NovaSolver](/images/reaction-diffusion/cover.png)

## チューリングパターンとは

ヒョウの斑点、シマウマの縞、熱帯魚の模様、サンゴの形——生き物の表面に現れる規則的な模様は、**2 種類の物質が「反応」しながら「拡散」する**だけで自然に生まれます。1952 年、アラン・チューリングが計算機科学者になる前に予言したこの現象を、**反応拡散系**といいます。

最も有名なモデルが **Gray-Scott モデル**。2 つの化学物質 $U$ と $V$ の濃度が、次の偏微分方程式で時間発展します：

$$
\frac{\partial u}{\partial t} = D_u \nabla^2 u - uv^2 + F(1-u)
$$
$$
\frac{\partial v}{\partial t} = D_v \nabla^2 v + uv^2 - (F+k)v
$$

この記事では：

1. 各項の意味（拡散・反応・供給・消滅）
2. JavaScript（グリッド＋ラプラシアン）での実装
3. パラメータ $F, k$ で斑点・縞・迷路が切り替わる仕組み

📐 **動くデモ**: [反応拡散シミュレーター（NovaSolver）](https://novasolver.jp/tools/reaction-diffusion.html)

## 4つの項を読む

各方程式の右辺は 3 つの働きの足し算です：

- $D\nabla^2$ … **拡散**（濃いところから薄いところへ広がる）
- $-uv^2,\ +uv^2$ … **反応**（$U$ が $V$ に変わる自己触媒反応。$V$ が $V$ を増やす）
- $+F(1-u)$ … **供給**（$U$ を外から補充、率 $F$）
- $-(F+k)v$ … **消滅**（$V$ が率 $k$ で取り除かれる）

ポイントは **2 つの拡散係数の差**です。$U$ が $V$ より速く拡散する（このデモは $D_u=0.30,\ D_v=0.075$ で **$U$ が 4 倍速い**）ことで、「局所的に $V$ が増え、まわりには広がらない」という不均一さが安定化し、**静止した模様**が生まれます。これがチューリングの言う **拡散誘起不安定（diffusion-driven instability）** です。均一に混ざろうとする拡散が、逆に模様を作るのが逆説的で面白いところ。

## ラプラシアンで実装する

格子上で濃度を持ち、各セルの**ラプラシアン**（周囲との差）を計算して更新します。周期境界なら端が反対側につながります：

```javascript
// 9点ラプラシアン（中心 -1、隣 0.2、斜め 0.05）
function lap(A, x, y, N) {
  const at = (i,j) => A[((i+N)%N)*N + ((j+N)%N)];
  return 0.2*(at(x-1,y)+at(x+1,y)+at(x,y-1)+at(x,y+1))
       + 0.05*(at(x-1,y-1)+at(x-1,y+1)+at(x+1,y-1)+at(x+1,y+1))
       - at(x,y);
}

function step(u, v, Du, Dv, F, k, N) {
  const nu = new Float32Array(N*N), nv = new Float32Array(N*N);
  for (let x = 0; x < N; x++)
    for (let y = 0; y < N; y++) {
      const i = x*N + y;
      const uvv = u[i]*v[i]*v[i];
      nu[i] = u[i] + (Du*lap(u,x,y,N) - uvv + F*(1 - u[i]));
      nv[i] = v[i] + (Dv*lap(v,x,y,N) + uvv - (F + k)*v[i]);
    }
  return [nu, nv];
}
```

初期状態は「$u=1,\ v=0$ の海に、$v$ の種をいくつか撒く」だけ。あとは反応拡散が勝手に模様を育てます。

![Gray-Scott が育てる珊瑚状のチューリングパターン](/images/reaction-diffusion/charts-closeup.png)

## F と k で模様が変わる

同じ方程式でも、供給率 $F$ と消滅率 $k$ の組み合わせで、現れる模様ががらりと変わります：

| パターン | 特徴 |
|---|---|
| 斑点（spots） | 孤立した点が分裂・増殖（細胞分裂のよう） |
| 縞（stripes） | 指紋のような平行な筋 |
| 泡（bubbles） | 穴あき・泡状 |
| 珊瑚・迷路（coral） | 枝分かれする迷路状ネットワーク |

このデモ（$F=0.0545,\ k=0.062$）では、種から枝が伸びて迷路状に画面を埋めていきます（最終的に約 40% を $V$ が占有）：

![種から模様が育っていく様子](/images/reaction-diffusion/slider-anim.gif)

$(F, k)$ をほんの少し動かすだけで斑点 ⇄ 縞 ⇄ 迷路と相転移するのが、このモデルの醍醐味です。

## ツールで遊ぶ

[反応拡散シミュレーター](https://novasolver.jp/tools/reaction-diffusion.html)で試してほしい操作：

- **プリセット**「斑点」「縞」「泡」「珊瑚」をワンクリックで切り替え
- **F（フィード率）と k（消滅率）スライダー**を少しずつ動かし、模様の相転移を探す
- **Du / Dv スライダー**で拡散係数の比を変え、$D_u > D_v$ が崩れると模様が消えるのを確認
- **速度スライダー**でパターン形成のスピードを上げ下げ
- **リセット**で種を撒き直し、毎回違う模様の育ち方を観察

## まとめ

- 反応拡散は「拡散＋自己触媒反応＋供給／消滅」で記述される（Gray-Scott）
- $U$ が $V$ より速く拡散する（比 ≈4）ことで静止模様が安定化＝拡散誘起不安定
- 格子上でラプラシアンを計算するだけで実装でき、種を撒けば自己組織化する
- 供給率 $F$・消滅率 $k$ で斑点・縞・泡・珊瑚へ相転移する

「混ぜると均一になる」はずの拡散が、反応と組むと模様を生む——生命の形づくりに通じる自己組織化の入口です。

📐 **[反応拡散シミュレーター（NovaSolver）](https://novasolver.jp/tools/reaction-diffusion.html)** で、$F$ と $k$ を動かして自分だけの模様を育ててみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。自己組織化・パターン系では [ロジスティック写像の分岐図](https://novasolver.jp/tools/bifurcation-diagram.html)、[マンデルブロ集合](https://novasolver.jp/tools/mandelbrot.html)、[Boids 群れ](https://novasolver.jp/tools/boids-flocking.html) なども揃えています。
