---
title: "ブラウザで動く FFT アナライザー — 信号を周波数領域で分解する仕組み"
emoji: "📊"
type: "tech"
topics: ["javascript", "数学", "信号処理", "可視化", "chartjs"]
published: true
---

![FFT アナライザー — NovaSolver](/images/fft-analyzer/cover.png)

## なぜ FFT を学ぶか

時間波形を見ているだけでは「この信号にどんな周波数成分が含まれているか」がわかりません。**FFT（高速フーリエ変換）** は、時間領域 → 周波数領域への変換を $O(N \log N)$ で計算できる定番アルゴリズムです。

実機では音声・振動・電流・脳波・経済時系列、ありとあらゆる「時間で変動するもの」に対して使われます。

この記事では：

1. 離散フーリエ変換（DFT）の数式を最小限おさらい
2. JavaScript で 50 行の FFT を実装
3. ピーク検出と周波数分解能の話

📊 **動くデモ**: [FFT アナライザー（NovaSolver）](https://novasolver.jp/tools/fft-analyzer.html)

## 離散フーリエ変換の数式

長さ $N$ のサンプル列 $x_0, x_1, \dots, x_{N-1}$ に対し、DFT は以下で定義されます：

$$
X_k = \sum_{n=0}^{N-1} x_n \, e^{-j 2\pi k n / N}, \quad k = 0, 1, \dots, N-1
$$

$X_k$ は周波数 $f_k = k \cdot f_s / N$（$f_s$: サンプリング周波数）における**複素振幅**です。

- $|X_k|$: その周波数のパワー
- $\angle X_k$: 位相

通常見たい「周波数スペクトル」は $|X_k|$（または $|X_k|^2$）を $f_k$ 軸でプロットしたものです。

## 50 行の FFT（Cooley-Tukey 再帰版）

```javascript
// 入力 x: 実数配列、長さは2のべき乗
// 戻り値: [{re, im}] の複素数配列
function fft(x) {
  const N = x.length;
  if (N === 1) return [{ re: x[0], im: 0 }];

  // 入力が複素数でない場合は実部のみで初期化
  const xC = x.map(v => (typeof v === 'number' ? { re: v, im: 0 } : v));
  return _fft(xC);
}

function _fft(x) {
  const N = x.length;
  if (N === 1) return x;
  const even = _fft(x.filter((_, i) => i % 2 === 0));
  const odd  = _fft(x.filter((_, i) => i % 2 === 1));
  const out = new Array(N);
  for (let k = 0; k < N / 2; k++) {
    const t = (-2 * Math.PI * k) / N;
    const wr = Math.cos(t), wi = Math.sin(t);
    const tr = wr * odd[k].re - wi * odd[k].im;
    const ti = wr * odd[k].im + wi * odd[k].re;
    out[k]         = { re: even[k].re + tr, im: even[k].im + ti };
    out[k + N/2]   = { re: even[k].re - tr, im: even[k].im - ti };
  }
  return out;
}

// 振幅スペクトル
function magnitudeSpectrum(x, fs) {
  const X = fft(x);
  const N = X.length;
  const half = N / 2;  // 実数信号なら N/2 まででOK
  const mag = [], freq = [];
  for (let k = 0; k <= half; k++) {
    mag.push(Math.sqrt(X[k].re ** 2 + X[k].im ** 2) / N * 2);
    freq.push(k * fs / N);
  }
  return { freq, mag };
}

// 例: 60Hz + 150Hz の合成波
const fs = 1024, N = 1024;
const t = Array.from({length: N}, (_, i) => i / fs);
const x = t.map(ti => Math.sin(2*Math.PI*60*ti) + 0.5*Math.sin(2*Math.PI*150*ti));
const { freq, mag } = magnitudeSpectrum(x, fs);
// freq[60] ≈ 60, mag[60] ≈ 1.0
// freq[150] ≈ 150, mag[150] ≈ 0.5
```

実用上は窓関数（Hanning / Hamming）を掛けるのが定番ですが、まずは素のままで十分動きます。

## NovaSolver の FFT アナライザーで触る

合成波（複数の正弦波の重ね合わせ）を入力すると、FFT が瞬時にピークを検出します：

![FFT アナライザーの時間波形とスペクトル](/images/fft-analyzer/charts-closeup.png)

時間波形（上、青）はランダムにしか見えない複雑な信号ですが、FFT を取ると **離散的なピーク** が周波数軸上に立ち上がります。元の周波数が綺麗に取り出せる、これが FFT の威力です。

## 周波数分解能とサンプリング定理

実用で気をつけたいのが 2 つ：

### 1. ナイキスト周波数
サンプリング周波数 $f_s$ で取得した信号からは、最大 $f_s / 2$ までの周波数しか復元できません。**入力信号の最大周波数 > $f_s / 2$ だとエイリアシング**で偽の周波数が現れます。

### 2. 周波数分解能
FFT の周波数分解能は：

$$
\Delta f = \frac{f_s}{N} = \frac{1}{T}
$$

$T$ は観測時間。**観測時間が短いと周波数を分離できない**ということ。たとえば 60Hz と 61Hz を分離したければ、観測時間が最低 1 秒必要です。

NovaSolver のツールで周波数 $f_1$ スライダーを動かすと、スペクトルのピークがリアルタイム移動するのが見えます：

![周波数スライダーを動かすとピークが移動](/images/fft-analyzer/slider-anim.gif)

「波形の形は変わってない（見た目同じ）のに、スペクトルだけが横滑りする」のが視覚的に強烈です。

## まとめ

- FFT は DFT を $O(N \log N)$ で計算する基本アルゴリズム
- 50 行の JavaScript で十分動くものが書ける
- 実用では **ナイキスト周波数** と **周波数分解能** が制約条件
- 触って学ぶには [NovaSolver の FFT アナライザー](https://novasolver.jp/tools/fft-analyzer.html) が便利

信号処理は「時間波形を見るな、スペクトルを見ろ」が鉄則。FFT はその出発点です。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。信号処理系では他にも [フーリエ級数](https://novasolver.jp/tools/fourier-series.html)、[フーリエ・エピサイクル](https://novasolver.jp/tools/fourier-epicycles.html) なども揃えています。
