---
title: "ドップラー効果 — 救急車のサイレンが変わる理由とマッハ円錐"
emoji: "🚑"
type: "tech"
topics: ["javascript", "物理シミュレーション", "波動", "可視化", "数値計算"]
published: false
---

![ドップラー効果 — NovaSolver](/images/doppler-effect/cover.png)

## 通り過ぎる救急車の「ピーポー」が下がる

救急車が近づくときサイレンは高く、通り過ぎると急に低く聞こえる——誰もが体験する**ドップラー効果**です。音源そのものの周波数は変わっていないのに、なぜ聞こえる高さが変わるのか。答えは「波面の間隔（波長）が、音源や観測者の運動で詰まったり伸びたりするから」です。

この記事ではドップラーの式を導き、JavaScript で波面アニメーションを再現し、音速を超えたときに生まれる**マッハ円錐（衝撃波）**まで見ていきます。

🚑 **動くデモ**: [ドップラー効果シミュレーター（NovaSolver）](https://novasolver.jp/tools/doppler-effect.html)

## ドップラーの式

音速を $v$、音源の周波数を $f_0$、音源の速度を $v_s$、観測者の速度を $v_o$ とすると、観測される周波数は

$$
f_{\text{obs}} = f_0\,\frac{v \pm v_o}{v \mp v_s}
$$

複号は「近づくとき上の符号」。近づく音源では分母が小さくなり $f_{\text{obs}}$ が上がる、遠ざかると分母が大きくなって下がる、という仕組みです。

ツールの「Ma=0.5（近づく）」プリセット（$f_0=440\,\mathrm{Hz}$、$v_s=170\,\mathrm{m/s}$、$v=340\,\mathrm{m/s}$）で計算すると

$$
f_{\text{near}} = 440\times\frac{340}{340-170} = 880\,\mathrm{Hz},\qquad
f_{\text{far}} = 440\times\frac{340}{340+170} = 293.3\,\mathrm{Hz}
$$

近づくとき **2 倍（1 オクターブ上）**、遠ざかると約 0.67 倍。これほど極端なのは音源が音速の半分（$\mathrm{Ma}=0.5$）も出しているからですが、身近な例でも効果は明確です。たとえば $f_0=800\,\mathrm{Hz}$ のサイレンが $20\,\mathrm{m/s}$（72 km/h）で近づくと $850\,\mathrm{Hz}$、遠ざかると $755.6\,\mathrm{Hz}$ で、約 100 Hz の差が生まれます。

![移動する音源の波面と、観測周波数の速度依存性](/images/doppler-effect/charts-closeup.png)

左図のように、音源が動くと**前方の波面が詰まり（波長が短く＝高音）、後方が伸びます（波長が長く＝低音）**。右図は周波数比 $f/f_0$ を音源マッハ数で見たもので、近づく側は $v_s\to v$ で発散することがわかります。

## 音速を超えると：マッハ円錐

音源が音速に達する（$\mathrm{Ma}=1$）と、前方の波面がすべて重なり**衝撃波**を作ります。音速を超える（$\mathrm{Ma}>1$）と、波面の包絡線が円錐になり、これが**マッハ円錐**です。円錐の半頂角 $\theta$ は

$$
\sin\theta = \frac{1}{\mathrm{Ma}} = \frac{v}{v_s}
$$

で決まります。たとえば戦闘機が $\mathrm{Ma}=1.2$ で飛ぶと $\theta = \arcsin(1/1.2) \approx 56.4°$、$\mathrm{Ma}=2$ では $\theta=30°$ と、速いほど円錐が鋭く尖ります。地上で聞こえる「ソニックブーム」はこの衝撃波が通過する音です。

## JavaScript 実装

観測周波数の計算自体は一行です。

```javascript
function calcFreq(vs, vo, v, f0) {
  if (v - vs <= 0) return Infinity;     // 音速到達で発散
  return f0 * (v + vo) / (v - vs);
}
// 近づく: calcFreq(vs, vo, ...), 遠ざかる: calcFreq(-vs, -vo, ...)
```

波面アニメーションは、一定間隔で円（波面）を放出し、各波面を「放出された位置」を中心に音速で広げます。音源が動くので、放出位置がずれて前方の円が詰まります。

```javascript
// 時刻 t における波面 k: 中心 x_k = vs*t_k、半径 r = v*(t - t_k)
waves.forEach(w => { const r = V_SOUND * (t - w.t0); drawCircle(w.x0, r); });
```

![音源が動くと前方の波面が詰まる（ドップラー）](/images/doppler-effect/slider-anim.gif)

## ツールで遊ぶ

[ドップラー効果シミュレーター](https://novasolver.jp/tools/doppler-effect.html)で試してほしい操作：

- **音源の速度 vs スライダー**を上げ、**波面アニメ**タブで前方の波面が詰まっていくのを見る
- **計算結果**の「観測周波数（近づく時）／（遠ざかる時）」と「周波数変化率」を読む
- **プリセット**「Ma=0.5（近づく）」「Ma=1（音速）」「Ma=1.5（超音速）」を切り替える
- **マッハ円錐**タブで、$\mathrm{Ma}>1$ にしたとき衝撃波の円錐角 $\theta=\arcsin(1/\mathrm{Ma})$ が変わるのを観察
- **周波数-速度グラフ**タブで、近づく／遠ざかる曲線が $v_s\to v$ で発散する様子を見る
- **観測者の速度 vo スライダー**や**「観測者が近づく」プリセット**で、観測者側が動く場合との違いを比較
- **音速 v スライダー**を変え、媒質（空気・水中など）による違いを試す

## まとめ

- ドップラー効果は $f_{\text{obs}}=f_0(v\pm v_o)/(v\mp v_s)$。波面の詰まり・伸びが音の高さを変える
- $\mathrm{Ma}=0.5$ で近づく音源は周波数 2 倍、遠ざかると約 0.67 倍
- $v_s\to v$ で発散し、$\mathrm{Ma}\ge1$ で衝撃波・**マッハ円錐**（$\sin\theta=1/\mathrm{Ma}$）が生じる
- レーダー・超音波血流計・天文の赤方偏移まで、応用は波動全般に広がる

身近な現象から超音速の衝撃波まで地続きの物理を、スライダーで体感してみてください。

🚑 **[ドップラー効果シミュレーター（NovaSolver）](https://novasolver.jp/tools/doppler-effect.html)** で、サイレンの高さが変わる瞬間を波面で見てみましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。波動系では [波の干渉](https://novasolver.jp/tools/wave-interference.html)、[弦の共振](https://novasolver.jp/tools/string-resonance.html)、[カルマン渦](https://novasolver.jp/tools/karman-vortex.html) なども揃えています。
