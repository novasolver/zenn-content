---
title: "超音波ドップラー血流計測 — エイリアシングはなぜ起きるのか"
emoji: "🩺"
type: "tech"
topics: ["javascript", "信号処理", "医療", "可視化", "物理シミュレーション"]
published: false
---

![超音波ドップラー血流計測 — NovaSolver](/images/ultrasound-doppler-flow/cover.png)

## 超音波ドップラー法とは

病院のエコー検査で聞こえる「シャー、シャー」という音は、超音波が血液中の赤血球に当たって跳ね返るときの**周波数のズレ**を音に変えたものです。動く物体が反射波の周波数を変える——救急車のサイレンが近づくと高く聞こえるのと同じ**ドップラー効果**です。

この周波数のズレ（ドップラー偏移）$f_d$ から血流速度を逆算するのが超音波ドップラー血流計測で、頸動脈・心臓・胎児循環の評価に日常的に使われます。式は高校物理レベルですが、**パルス方式（PW ドップラー）では「エイリアシング」という厄介な現象**が付きまといます。この記事では：

1. ドップラー偏移と速度逆算の式、角度誤差がなぜ効くか
2. Nyquist 限界とエイリアシングを数値で確かめる
3. 30 行ほどの JavaScript で計算ロジックを再現する

🩺 **動くデモ**: [超音波ドップラー血流計測シミュレーター（NovaSolver）](https://novasolver.jp/tools/ultrasound-doppler-flow.html)

## ドップラー偏移の式

送信した超音波の周波数を $f_0$、血流速度を $v$、ビームと血流のなす角を $\theta$、組織中の音速を $c$ とすると、戻ってくる波の周波数のズレ $f_d$ は次式で与えられます：

$$
f_d = \frac{2 f_0 v \cos\theta}{c}
$$

係数 2 は往復でドップラー効果が二重に効くため。軟部組織の音速は $c \approx 1540\ \mathrm{m/s}$ が標準値です。逆に装置は測った $f_d$ から速度を逆算します：

$$
v = \frac{f_d\, c}{2 f_0 \cos\theta}
$$

ここに $1/\cos\theta$ が掛かるのが落とし穴です。$\theta = 90^\circ$（垂直）では $\cos\theta = 0$ でドップラー効果は理論上ゼロ、$\theta = 0^\circ$（平行）が最も高感度になります。

| 記号 | 意味 | 代表値 |
|---|---|---|
| $f_0$ | 送信超音波周波数 | 5〜10 MHz |
| $v$ | 血流速度 | 頸動脈 ≈ 100 cm/s |
| $\theta$ | ビーム-血流角 | 45〜60° |
| $c$ | 軟部組織の音速 | 1540 m/s |

## 角度誤差がなぜ効くか

$v \propto 1/\cos\theta$ なので、角度 $\theta$ の小さな測定誤差が速度に増幅されて伝わります。$\theta$ を $1^\circ$ 取り違えたときの相対速度誤差は、$\lvert\tan\theta\rvert$ に比例します：

$$
\frac{\Delta v}{v} \approx \lvert\tan\theta\rvert\cdot\Delta\theta
$$

$\Delta\theta = 1^\circ = \pi/180\ \mathrm{rad}$ を代入して計算すると：

| $\theta$ | $\tan\theta$ | 1° あたりの速度誤差 |
|---|---|---|
| 30° | 0.577 | 約 1.0 %/° |
| 60° | 1.732 | 約 3.0 %/° |
| 70° | 2.747 | 約 4.8 %/° |
| 80° | 5.671 | 約 9.9 %/° |

$\theta = 80^\circ$ では $1^\circ$ のズレが約 $10\%$ もの速度誤差になります。臨床で $\theta \le 60^\circ$ が推奨されるのはこのためです。

## Nyquist 限界とエイリアシング

ここからが本題です。PW（Pulsed-Wave）ドップラーは連続波ではなく、「ピッ、ピッ」と一定周期で間欠的にパルスを送ります。その繰り返し周波数が **PRF（Pulse Repetition Frequency）**で、これは波形を一定間隔でサンプリングしているのと同じ。つまり**標本化定理**が効きます。

標本化定理から、PRF で測れる最大周波数は **Nyquist 周波数 = PRF/2** まで。ドップラー偏移 $f_d$ がこれを超えると、波形が折り返して**反対方向の流れに見えてしまう**——これがエイリアシングです：

$$
\text{エイリアシング発生条件:}\quad f_d > \frac{\mathrm{PRF}}{2}
$$

ツールの初期設定（$f_0 = 5\ \mathrm{MHz}$、$v = 100\ \mathrm{cm/s}$、$\theta = 60^\circ$、$\mathrm{PRF} = 5\ \mathrm{kHz}$）で確かめてみましょう。$v = 100\ \mathrm{cm/s} = 1.0\ \mathrm{m/s}$ に注意して：

$$
f_d = \frac{2 \times 5{\times}10^{6} \times 1.0 \times \cos 60^\circ}{1540} \approx 3247\ \mathrm{Hz} = 3.25\ \mathrm{kHz}
$$

一方 Nyquist は $\mathrm{PRF}/2 = 2.5\ \mathrm{kHz}$。$3.25 > 2.5$ なので**エイリアシングが発生**します。スペクトル波形は Nyquist のラインを越えた瞬間に下端へ折り返り、まるで逆流のように描かれます。

![スペクトル波形のエイリアシングと Nyquist 速度曲線](/images/ultrasound-doppler-flow/charts-closeup.png)

速度に換算した上限が **Nyquist 速度**です：

$$
v_{\text{Nyquist}} = \frac{c\cdot\mathrm{PRF}}{4 f_0 \cos\theta}
$$

同じ条件で代入すると $v_{\text{Nyquist}} \approx 77\ \mathrm{cm/s}$。測りたい血流 $100\ \mathrm{cm/s}$ が上限を超えており、やはり折り返します。右図の青点（$\theta = 60^\circ$）がオレンジ破線（流速 $100\ \mathrm{cm/s}$）より下にある＝測れていない、という関係です。

## PRF を上げれば解決……ではない

「Nyquist が低いなら PRF を上げればいい」——その通りですが、深さとのトレードオフがあります。1 パルスが組織を往復して戻るまで次のパルスは送れないため、測れる最大深度は PRF で決まります：

$$
d_{\max} = \frac{c}{2\,\mathrm{PRF}}
$$

$\mathrm{PRF} = 5\ \mathrm{kHz}$ なら $d_{\max} = 1540/(2\times5000) = 0.154\ \mathrm{m} = 15.4\ \mathrm{cm}$。$\mathrm{PRF} = 10\ \mathrm{kHz}$ では $7.7\ \mathrm{cm}$ と半分です。先ほどのエイリアシングを消すには $\mathrm{PRF}$ を約 $6.5\ \mathrm{kHz}$ 以上（Nyquist が $f_d = 3.25\ \mathrm{kHz}$ を上回る）にすればよいのですが、その分だけ深部が見えなくなります。

深い血管は低 PRF を使わざるを得ず Nyquist が低くなるため、高速血流でエイリアシングが起きやすい。これが PW の根本的な制約で、回避策は概ね (1) 低周波プローブで $f_d$ を下げる、(2) 角度を浅くする、(3) ベースラインシフト、(4) CW（連続波）ドップラーに切り替える、の順で検討されます。CW は速度上限がない代わりに距離分解能を失います。

## JavaScript で計算ロジックを再現

ツールの中核は次の関数です。入力から $f_d$・Nyquist・$v_{\text{Nyquist}}$・$d_{\max}$・角度誤差感度・エイリアシング判定をまとめて求めます：

```javascript
const C = 1540; // 軟部組織の音速 [m/s]

function doppler(f0_MHz, v_cmps, thetaDeg, prfHz) {
  const f0 = f0_MHz * 1e6;          // Hz
  const v = v_cmps / 100;           // m/s に変換（ここが落とし穴）
  const cos = Math.cos(thetaDeg * Math.PI / 180);

  // ドップラー偏移と Nyquist 限界
  const fd = 2 * f0 * v * cos / C;  // Hz
  const nyquist = prfHz / 2;        // Hz
  const aliasing = fd > nyquist;

  // Nyquist 速度（θ=90° のゼロ割を回避）
  const absCos = Math.max(Math.abs(cos), 1e-6);
  const vNyq = C * nyquist / (2 * f0 * absCos) * 100; // cm/s

  // 最大撮像深度と角度誤差感度（1°あたりの%）
  const dMax = C / (2 * prfHz) * 100;                 // cm
  const angErr = Math.abs(Math.tan(thetaDeg*Math.PI/180)) * (Math.PI/180) * 100;

  return { fd, nyquist, aliasing, vNyq, dMax, angErr };
}

const r = doppler(5, 100, 60, 5000);
console.log(r.fd.toFixed(0), r.nyquist, r.aliasing, r.vNyq.toFixed(0));
// 3247 2500 true 77
```

$v$ を `cm/s` から `m/s` へ直す `/100` を忘れると、$f_d$ が 100 倍ズレる典型的なバグになります（後述）。実行結果の `3247 2500 true 77` は、本文で手計算した値と一致します。

## ツールで遊ぶ

NovaSolver のツールでは、スライダーを動かすと**エイリアシングが出たり消えたりする様子**をその場で体感できます：

![PRF を上げるとエイリアシングが解消する](/images/ultrasound-doppler-flow/slider-anim.gif)

試してほしい操作：

- **PRF スライダー**を上げていくと、折り返していたスペクトルが Nyquist 限界を超えて伸び、ある点で「あり → なし」に切り替わる
- **ビーム角 θ** を 60° の前後で動かし、角度誤差感度（%/°）が急増する様子を見る
- **超音波周波数 $f_0$** を下げると $f_d$ 自体が下がり、深部でもエイリアシングを避けやすくなる
- **血管種類プリセット**（頸動脈／MCA／大腿動脈／心臓）を切り替えると、拍動指数 PI の代表値が変わる
- 計算結果カードで **ドップラー周波数・Nyquist 速度・最大撮像深度・角度誤差感度・エイリアシング判定**を同時に確認

## まとめ

- ドップラー偏移は $f_d = 2 f_0 v\cos\theta/c$、速度逆算には $1/\cos\theta$ が掛かるため $\theta \le 60^\circ$ が推奨
- PW ドップラーは PRF でサンプリングするため、$f_d > \mathrm{PRF}/2$ でエイリアシング（折り返し）が起きる
- 初期設定では $f_d = 3.25\ \mathrm{kHz} > \mathrm{Nyquist}\ 2.5\ \mathrm{kHz}$ で実際に折り返す（$v_{\text{Nyquist}} \approx 77\ \mathrm{cm/s} < 100\ \mathrm{cm/s}$）
- PRF を上げれば Nyquist は上がるが $d_{\max} = c/(2\,\mathrm{PRF})$ で深度が下がるトレードオフがある

「単純なドップラーの式」と「標本化定理」が組み合わさると、現場のエコー画像に直結する制約が立ち現れる——その感覚を 30 行のコードとスライダーで掴めるのが、このツールの面白いところです。

🩺 **[超音波ドップラー血流計測シミュレーター（NovaSolver）](https://novasolver.jp/tools/ultrasound-doppler-flow.html)** で、PRF とビーム角を動かしてエイリアシングの境目を探してみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。波動・信号処理の関連では [ドップラー効果](https://novasolver.jp/tools/doppler-effect.html)、[フーリエ級数の可視化](https://novasolver.jp/tools/fourier-series.html)、[FFT スペクトル解析](https://novasolver.jp/tools/fft-analyzer.html) なども揃えています。
