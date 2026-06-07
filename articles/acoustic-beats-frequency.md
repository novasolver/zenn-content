---
title: "うなり（音のビート）の正体 — なぜ440Hzと444Hzで毎秒4回ワンワン鳴るのか"
emoji: "🔊"
type: "tech"
topics: ["javascript", "物理シミュレーション", "波動", "音響", "可視化"]
published: false
---

![うなり（音のビート） — NovaSolver](/images/acoustic-beats/cover.png)

## ギターの調弦で聞こえる「ワンワン」の物理

ギターやピアノを調律するとき、2 つの音の高さが少しずれていると「ワンワンワン…」と音量が周期的に揺れます。これが**うなり（ビート）**。2 つの音を完全に合わせると、このうなりが止まります。耳だけで超精密な周波数合わせができるのは、うなりが**わずかな周波数差を増幅して聞かせてくれる**から。

この記事では、うなり周波数と包絡線（エンベロープ）を JavaScript で計算します。

🔊 **動くデモ**: [うなりシミュレーター（NovaSolver）](https://novasolver.jp/tools/acoustic-beats.html)

## 重ね合わせとうなり周波数

近い周波数 $f_1, f_2$ の 2 音を足すと、和積の公式により次のように書き換えられます（等振幅の場合）。

$$
\cos(2\pi f_1 t) + \cos(2\pi f_2 t) = 2\cos\!\left(2\pi \frac{f_1-f_2}{2}t\right)\cos\!\left(2\pi \frac{f_1+f_2}{2}t\right)
$$

右辺は「平均周波数 $f_{\text{avg}} = (f_1+f_2)/2$ で速く振動する波」が「ゆっくり変化する包絡線」で振幅変調された形です。一般振幅では包絡線は

$$
\text{env}(t) = \sqrt{A_1^2 + A_2^2 + 2A_1A_2\cos(2\pi(f_1-f_2)t)}
$$

ここがポイント：包絡線の $\cos$ は $(f_1-f_2)$ で振動しますが、私たちが「音量の脈動」として聞くのは包絡線の**絶対値の山**なので、1 周期に 2 回の山＝**うなり周波数は $f_{\text{beat}} = |f_1 - f_2|$** になります。

既定値 $f_1 = 440\,\mathrm{Hz}$、$f_2 = 444\,\mathrm{Hz}$ では、**うなり周波数 $= 4\,\mathrm{Hz}$**（毎秒 4 回ワンワン鳴る）、うなり周期 $= 250\,\mathrm{ms}$、平均周波数 442 Hz。等振幅なので合成振幅は最大 $A_1+A_2 = 1.0$、最小 $|A_1-A_2| = 0$（完全に打ち消す瞬間がある）です。

![合成波形と包絡線（左）と周波数スペクトルの2本のスパイク（右）](/images/acoustic-beats/charts-closeup.png)

## JavaScript 実装

```javascript
function beats(f1, f2, A1, A2) {
  const fBeat = Math.abs(f1 - f2);       // うなり周波数 = |f1 - f2|
  const fAvg  = (f1 + f2) / 2;           // 平均（搬送）周波数
  const Tbeat = fBeat > 0 ? 1000 / fBeat : Infinity;  // うなり周期 [ms]
  const Amax = A1 + A2, Amin = Math.abs(A1 - A2);
  return { fBeat, fAvg, Tbeat, Amax, Amin };
}
// 合成波と包絡線
const y   = A1*Math.cos(2*Math.PI*f1*t) + A2*Math.cos(2*Math.PI*f2*t);
const env = Math.sqrt(A1*A1 + A2*A2 + 2*A1*A2*Math.cos(2*Math.PI*(f1-f2)*t));
// beats(440, 444, 0.5, 0.5) → fBeat=4Hz, Tbeat=250ms
```

周波数差を広げるほどうなりは速くなり、やがて「ワンワン」が個別に聞き取れなくなって 2 音として分離します。逆に差をゼロに近づけるとうなりは限りなく遅くなり、完全一致で止まります。

![周波数差を変えるとうなりの速さが変わる](/images/acoustic-beats/slider-anim.gif)

## ツールで遊ぶ

[うなりシミュレーター](https://novasolver.jp/tools/acoustic-beats.html)で試してほしい操作：

- **周波数 f₂ スライダー**を f₁ に近づけ、「うなり周波数」が小さくなり「うなり周期」が伸びるのを確認
- f₁ = f₂ にして、うなりが消える（周期が ∞）のを見る
- **振幅 A₁・A₂ スライダー**を変え、最小振幅 $|A_1-A_2|$ が 0 でなくなる（打ち消しが不完全になる）のを観察
- **「f₂ をスイープ」ボタン**でうなりが速くなっていく様子を見る
- **合成波形**の橙破線（包絡線）が周波数差で脈打つのを読む
- **周波数スペクトル**で 2 本のスパイクの間隔が $|f_1-f_2|$ であることを確認

## まとめ

- うなりは近い 2 音の重ね合わせで生じる振幅変調
- うなり周波数は $f_{\text{beat}} = |f_1 - f_2|$（既定で 4 Hz、周期 250 ms）
- 包絡線は $\sqrt{A_1^2+A_2^2+2A_1A_2\cos(2\pi(f_1-f_2)t)}$
- 搬送波は平均周波数 $(f_1+f_2)/2$ で振動

楽器の調律から無線の検波まで使われるうなりを、周波数差を変えながら体感してみてください。

🔊 **[うなりシミュレーター（NovaSolver）](https://novasolver.jp/tools/acoustic-beats.html)** で、2 音の重ね合わせを確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。波動・音響では [気柱の共鳴](https://novasolver.jp/tools/acoustic-resonance.html)、[ドップラー効果](https://novasolver.jp/tools/doppler-effect.html)、[弦の共振](https://novasolver.jp/tools/string-resonance.html) もどうぞ。
