---
title: "弦の共振と定在波 — fn=(n/2L)√(T/μ) と「弾く位置で音色が変わる」理由"
emoji: "🎻"
type: "tech"
topics: ["javascript", "物理シミュレーション", "波動", "可視化", "数値計算"]
published: false
---

![弦の共振と定在波 — NovaSolver](/images/string-resonance/cover.png)

## ギターの弦が「ドレミ」を出す仕組み

ギターやバイオリンの弦は、張力と太さと長さだけで音の高さが決まります。さらに、同じ弦でも**弾く位置を変えると音色（倍音の混ざり方）が変わる**——これは弦に立つ**定在波**と倍音系列の物理で完全に説明できます。

この記事では固有周波数の式 $f_n=(n/2L)\sqrt{T/\mu}$ を導き、JavaScript で弦の振動をモード分解で再現し、「弾く位置で消える倍音」を数値とスペクトルで確かめます。

🎻 **動くデモ**: [弦の共振・定在波シミュレーター（NovaSolver）](https://novasolver.jp/tools/string-resonance.html)

## 固有周波数と波速

両端を固定した長さ $L$ の弦には、両端が節（動かない点）になる定在波だけが立てます。許される波長は $\lambda_n = 2L/n$（$n=1,2,3,\dots$）。弦を伝わる波の速さ $v$ は張力 $T$ と線密度 $\mu$（単位長さあたりの質量）で決まります。

$$
v = \sqrt{\frac{T}{\mu}}
$$

周波数 $f=v/\lambda$ から、固有周波数（倍音系列）は

$$
f_n = \frac{n}{2L}\sqrt{\frac{T}{\mu}},\qquad n=1,2,3,\dots
$$

$n=1$ が**基本音**、$n=2,3,\dots$ が**倍音**で、整数比 $1:2:3:\dots$ で並びます。ツールの既定値（$T=60\,\mathrm{N}$、$\mu=1.0\,\mathrm{g/m}=10^{-3}\,\mathrm{kg/m}$、$L=1.0\,\mathrm{m}$）で計算すると

$$
v = \sqrt{\frac{60}{10^{-3}}} = 244.9\,\mathrm{m/s},\qquad
f_1 = \frac{1}{2}\times244.9 = 122.5\,\mathrm{Hz}
$$

倍音は $122.5,\ 245,\ 367,\ 490,\dots\,\mathrm{Hz}$。実際のギターの A 弦（$L=0.65\,\mathrm{m}$、$T=73\,\mathrm{N}$、$\mu=0.85\,\mathrm{g/m}$）なら $f_1\approx225\,\mathrm{Hz}$ と、実機に近い値になります。

![弦の固有モードと、弾く位置による倍音スペクトルの違い](/images/string-resonance/charts-closeup.png)

## 弾く位置で音色が変わる理由

弦を一点でつまんで離す（撥弦）と、その三角形の初期形状を**フーリエ級数**に分解した分だけ各モードが励起されます。位置 $p$（弦長比）で弾いたときのモード $n$ の振幅は

$$
A_n \propto \frac{1}{n^2}\sin\!\left(n\pi p\right)
$$

ここに鍵があります。$\sin(n\pi p)=0$ になる倍音は**まったく鳴りません**。なぜなら、弾いた点がそのモードの「節」にあたると、そのモードは励起できないからです。

- **中央（$p=1/2$）を弾く**：偶数倍音 $n=2,4,6,\dots$ がすべて節 → **奇数倍音だけ**が鳴る（柔らかい音）
- **$1/3$ 点を弾く**：$n=3,6,9,\dots$ が消える
- **$1/4$ 点を弾く**：$n=4,8,\dots$ が消える

上図右のスペクトルがまさにこれで、中央弾き（水色）は奇数のみ、$1/3$ 弾き（オレンジ）は $n=3$ が欠落しています。ギターで「ブリッジ寄りを弾くと硬い音、中央寄りだと丸い音」になるのは、この倍音構成の違いです。

## JavaScript 実装（モード分解）

弦の変位はモードの重ね合わせで書けます。各モードは固有周波数で振動し、減衰がかかります。

```javascript
function f1(){ return (1/(2*L))*Math.sqrt(T/mu); }   // 基本周波数
function fn(n){ return n * f1(); }                   // n次倍音
function omega(n){ return 2*Math.PI*fn(n); }

function getStringY(x, t){                            // 時刻 t の弦の形
  const xf = x / canvasWidth * L;
  let y = 0;
  for (let n = 1; n <= N_MODES; n++){
    const decay = Math.exp(-damp * omega(n) * t);     // 高次ほど速く減衰
    y += amplitudes[n-1] * decay
         * Math.sin(n*Math.PI*xf/L)                    // 空間モード
         * Math.cos(omega(n)*t);                       // 時間振動
  }
  return y;
}
```

高次倍音ほど速く減衰する（$\propto e^{-\zeta\omega_n t}$）ので、弾いた直後は華やかでも、すぐに基本音中心の落ち着いた音に変わります。

![中央を弾いた弦の振動（奇数倍音の重ね合わせ）](/images/string-resonance/slider-anim.gif)

## ツールで遊ぶ

[弦の共振・定在波シミュレーター](https://novasolver.jp/tools/string-resonance.html)で試してほしい操作：

- **張力 T スライダー**を上げると音が高く（$f_1\propto\sqrt{T}$）、**線密度 μ** を上げると低くなる（$f_1\propto1/\sqrt{\mu}$）のを**計算結果の f₁**で確認
- **弦長 L スライダー**を半分にすると $f_1$ が 2 倍に（フレットを押さえる＝弦長短縮）
- **プリセット**「中央」「1/3点」「1/4点」で弾く位置を変え、**スペクトル表示**で消える倍音を観察
- **モードフィルタ**（n=1〜7）で特定の倍音だけを取り出して定在波の形を見る
- **「ノード」表示**で各モードの節・腹の位置を確認
- **「分解」表示**で、振動が複数モードの重ね合わせであることを可視化
- **「音を聴く」**で実際の倍音構成を耳で確かめる（減衰スライダーで余韻も調整）

## まとめ

- 弦の固有周波数は $f_n=(n/2L)\sqrt{T/\mu}$。波速 $v=\sqrt{T/\mu}$、倍音は整数比 $1:2:3:\dots$
- 既定値で $v=244.9\,\mathrm{m/s}$、$f_1=122.5\,\mathrm{Hz}$
- 弾く位置 $p$ が節になる倍音（$\sin(n\pi p)=0$）は鳴らない＝**弾く位置で音色が決まる**
- 高次倍音ほど速く減衰し、音は時間とともにまろやかになる

楽器の物理、構造物の固有振動、弦理論の出発点にもなる「定在波」を、スライダーと音で体感してみてください。

🎻 **[弦の共振・定在波シミュレーター（NovaSolver）](https://novasolver.jp/tools/string-resonance.html)** で、弾く位置と音色の関係を自分の耳で確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。波動系では [波の干渉](https://novasolver.jp/tools/wave-interference.html)、[ドップラー効果](https://novasolver.jp/tools/doppler-effect.html)、[フーリエ変換](https://novasolver.jp/tools/fourier-transform.html) なども揃えています。
