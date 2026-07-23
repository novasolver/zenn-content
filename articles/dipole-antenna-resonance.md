---
title: "半波長ダイポールアンテナの共振 — L=VF·λ/2 と73Ωの正体"
emoji: "📡"
type: "tech"
topics: ["javascript", "物理", "電磁気", "無線", "アンテナ"]
published: true
---

![半波長ダイポールアンテナの共振 — NovaSolver](/images/dipole-antenna-resonance/cover.png)

## 半波長ダイポールとは

1本の導体を真ん中で割り、その切れ目に給電線をつなぐ。たったそれだけの構造が、無線工学で「基準アンテナ」と呼ばれる**半波長ダイポール**です。あらゆるアンテナの性能は「ダイポールと比べて何 dB 良いか」で語られる——つまり、業界共通のものさしになっています。

なぜ「半波長」なのか。導体の長さが波長の半分（$\lambda/2$）のとき、中央から入れた高周波電流が左右の腕を走って先端で反射し、戻ってきた波が位相をそろえて重なります。その結果、**強くて安定した電流の定在波**——中央で最大、両端でゼロ——が立ちます。これが「共振」です。

この記事では：

1. 共振素子長を決める $L = \text{VF}\cdot\lambda/2$ の意味
2. 放射抵抗 73Ω と給電点 SWR の関係
3. 電流定在波を 25 行の JavaScript で描く

📐 **動くデモ**: [半波長ダイポールアンテナ シミュレーター（NovaSolver）](https://novasolver.jp/tools/dipole-antenna-resonance.html)

## 共振素子長を計算する

まず自由空間の波長は光速 $c$ と周波数 $f$ から決まります：

$$
\lambda = \frac{c}{f}
$$

理想的にはアンテナ全長を $\lambda/2$ にしたいところですが、実際にはそのまま切ると目標より低い周波数で共振してしまいます。原因は**端効果**です。導体の先端では電界が外側へ少しはみ出すため、アンテナは物理長より少し長い導体のようにふるまうのです。

そこで $\lambda/2$ より少し短く切ります。その短縮率が**速度係数 VF**で、共振素子長（全長）は次式になります：

$$
L = \text{VF}\cdot\frac{\lambda}{2}
$$

VF は細い導体で約 0.97、太い導体で 0.95 程度が目安です。たとえばアマチュア無線の 144MHz・VF=0.95 で計算すると：

$$
\lambda = \frac{3\times10^8}{144\times10^6} = 2.083\,\text{m},\quad
L = 0.95\times\frac{2.083}{2} = 0.990\,\text{m}
$$

全長 0.990m、片側エレメントはその半分の 0.495m です。VF を掛けなければ $\lambda/2 = 1.096\text{m}$ になり、約 11cm も長すぎることになります。

## 放射抵抗73Ωと給電点SWR

共振すると、アンテナの入力インピーダンスはやっかいなリアクタンス分が消えて、ほぼ**純抵抗**になります。その値が**放射抵抗**で、理想的な半波長ダイポールでは約 73Ω。これは損失ではなく、ちゃんと電波として空間へ放射された電力を表す抵抗です。

問題は、よく使う同軸ケーブルが 50Ω であること。少しズレているので、送った電力の一部が給電点で反射します。この不整合の度合いが**定在波比 SWR** で、純抵抗どうしなら次のように書けます：

$$
\text{SWR} = \frac{\max(R_r,\,Z_0)}{\min(R_r,\,Z_0)}
$$

給電線ごとに計算すると、こうなります：

| 給電線 $Z_0$ | SWR | 整合 |
|---|---|---|
| 50Ω 同軸 | $73/50 = 1.46$ | 実用範囲（1.5以下） |
| 75Ω 同軸 | $73/75 = 1.03$ | ほぼ完璧 |
| 300Ω フィーダ | $300/73 = 4.11$ | 不整合が大きい |

SWR は 1 に近いほど反射が少なく効率的です。50Ω 同軸で 1.46 は実用上問題ない範囲、75Ω なら 1.03 とほぼ理想です。

## 電流定在波を描く

共振時の電流分布は、両端でゼロ・中央で最大の**半周期の正弦波**で近似できます。素子上の規格化位置 $x\in[0,1]$ に対して：

$$
I(x) = \sin(\pi x)
$$

これを Canvas に時間振動させて描くと、25 行ほどで定在波アニメーションになります：

```javascript
const C = 3e8;                 // 光速 m/s
function dipole(fMHz, vf) {
  const lambda = C / (fMHz * 1e6);
  const L = vf * lambda / 2;    // 共振全長 L = VF·λ/2
  return { lambda, L, element: L / 2 };
}
function swr(z0) {              // 放射抵抗 73Ω に対する SWR
  const Rr = 73;
  return Math.max(Rr, z0) / Math.min(Rr, z0);
}

const d = dipole(144, 0.95);
console.log(d.lambda.toFixed(3), d.L.toFixed(3), d.element.toFixed(3));
// 2.083 0.990 0.495
console.log(swr(50).toFixed(2), swr(75).toFixed(2));
// 1.46 1.03

let t = 0;
function frame(ctx, W, H) {     // 電流定在波 I(x)=sin(πx)·sin(ωt)
  ctx.clearRect(0, 0, W, H);
  const osc = Math.sin(t), pad = 40, cy = H / 2;
  ctx.beginPath();
  for (let i = 0; i <= 100; i++) {
    const x = i / 100;                       // 0..1（左端→給電点→右端）
    const px = pad + x * (W - 2 * pad);
    const py = cy - Math.sin(Math.PI * x) * 60 * osc;
    i ? ctx.lineTo(px, py) : ctx.moveTo(px, py);
  }
  ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = 2.5; ctx.stroke();
  t += 0.06;
  requestAnimationFrame(() => frame(ctx, W, H));
}
```

下のグラフ左は $L = \text{VF}\cdot\lambda/2$ が周波数に反比例する様子、右が $I(x)=\sin(\pi x)$ の定在波です。VF を変えても曲線はほぼ重なり、端効果による短縮はわずか数 % であることが読み取れます：

![共振素子長と電流定在波](/images/dipole-antenna-resonance/charts-closeup.png)

## ツールで遊ぶ

NovaSolver のシミュレーターでは、周波数スライダーを動かすと共振素子長が伸び縮みし、ダイポール構造の上を電流定在波が脈打ちます：

![周波数を動かすと共振素子長が変わる](/images/dipole-antenna-resonance/slider-anim.gif)

試してほしい操作：

- **周波数 f スライダー**（1〜3000MHz）を動かして、波長・共振全長・1エレメント長が即座に変わるのを見る
- **速度係数 VF スライダー**（0.90〜0.99）で端効果による短縮量を調整
- **素子の直径 d** を変えて太い導体のふるまいを確認
- **給電線インピーダンス**を 50/75/300Ω で切り替え、給電点 SWR の判定（良好/高め）が変わるのを見る
- 「ダイポール構造と電流定在波」アニメーションで、中央最大・両端ゼロの定在波とドーナツ状放射パターンを観察

## まとめ

- 半波長ダイポールの共振全長は $L = \text{VF}\cdot\lambda/2$、$\lambda=c/f$
- 144MHz・VF=0.95 で全長 0.990m、片側 0.495m（端効果で $\lambda/2$ より約 11cm 短い）
- 共振時の入力は純抵抗 73Ω、利得は 2.15dBi が理論値
- 50Ω 同軸なら SWR=1.46、75Ω なら 1.03 とほぼ整合
- 電流定在波は $I(x)=\sin(\pi x)$、25 行の JavaScript で描ける

「電線を真ん中で割っただけ」のシンプルさが、無線工学共通のものさしになっている——それが半波長ダイポールの面白さです。なお放射抵抗 73Ω や利得 2.15dBi は自由空間に孤立した理想ダイポールの値で、実際は地面や周辺金属の影響を受ける点には注意してください。

📐 **[半波長ダイポールアンテナ シミュレーター（NovaSolver）](https://novasolver.jp/tools/dipole-antenna-resonance.html)** で、周波数を変えて共振素子長と定在波の変化を見てみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。無線・電磁気では [アンテナアレイ](https://novasolver.jp/tools/antenna-array.html)、[フリスの伝達公式](https://novasolver.jp/tools/antenna-friis-equation.html)、[RLC共振回路](https://novasolver.jp/tools/rlc-resonance.html) なども揃えています。
