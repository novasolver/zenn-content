---
title: "パーセプトロンが境界線を学習する仕組み — 誤分類で重みを直す更新則をJSで"
emoji: "🧠"
type: "tech"
topics: ["javascript", "機械学習", "アルゴリズム", "可視化", "数学"]
published: false
---

![パーセプトロン（線形分類器） — NovaSolver](/images/perceptron/cover.png)

## ニューラルネットの原点 — 1958年生まれの学習機械

ディープラーニングの最小単位は、1958 年にローゼンブラットが考案した**パーセプトロン**です。入力に重みを掛けて足し、しきい値で 2 クラスに分ける――たったこれだけ。しかも「間違えたら、その分だけ重みを直す」という単純な規則で、データを分ける境界線を**自分で学習**します。線形分離可能なデータなら必ず収束することが証明されています（パーセプトロン収束定理）。

この記事では、パーセプトロンの学習則を JavaScript で実装します。

🧠 **動くデモ**: [パーセプトロンシミュレーター（NovaSolver）](https://novasolver.jp/tools/perceptron.html)

## 出力と学習則

入力 $\boldsymbol x = (x_1, x_2)$ に対し、重み $\boldsymbol w$ とバイアス $b$ で符号を取って分類します。

$$
y = \operatorname{sign}(w_1 x_1 + w_2 x_2 + b)
$$

教師ラベル $t$ と出力 $y$ が食い違ったとき（誤分類）だけ、学習率 $\eta$ で重みを補正します。

$$
w_i \leftarrow w_i + \eta\,(t - y)\,x_i,\qquad b \leftarrow b + \eta\,(t - y)
$$

正解なら $t-y=0$ で更新せず、間違えたら正解方向へ少し動く――この繰り返しだけで境界線 $w_1 x_1 + w_2 x_2 + b = 0$ が正しい位置に向かいます。

シミュレーターのデータは $(3,3)$ と $(-3,-3)$ を中心とする 2 つのガウス分布（各 10 点、標準偏差 0.8）で、真の境界 $x_1+x_2=0$ で**線形分離可能**です。学習率 $\eta=0.1$ で学習させると、境界線が回転しながらデータを分け、最終的に**分類精度 100%** に到達します。初期値が良ければ 1 エポックで、悪ければ数エポックで収束します。

![学習前の境界（左）と学習後に100%分類できた境界（右）](/images/perceptron/charts-closeup.png)

## JavaScript 実装

```javascript
const sgn = v => (v >= 0 ? 1 : -1);
function train(data, eta, maxEpoch, w1, w2, b) {
  for (let ep = 1; ep <= maxEpoch; ep++) {
    let errors = 0;
    for (const p of data) {
      const y = sgn(w1*p.x1 + w2*p.x2 + b);
      if (y !== p.t) {                       // 誤分類のときだけ更新
        const delta = p.t - y;               // = ±2
        w1 += eta * delta * p.x1;
        w2 += eta * delta * p.x2;
        b  += eta * delta;
        errors++;
      }
    }
    if (errors === 0) return { w1, w2, b, convergedAt: ep };  // 全問正解で収束
  }
  return { w1, w2, b, converged: false };
}
```

学習率 $\eta$ は更新の歩幅です。大きすぎると境界が暴れ、小さすぎると収束が遅くなります。なお単層パーセプトロンは**線形分離可能な問題しか解けません**（XOR は解けない）。この限界を多層化と非線形活性化で乗り越えたのが、現代のニューラルネットワークです。

![誤分類を直しながら境界線が正しい位置へ回転していく](/images/perceptron/slider-anim.gif)

## ツールで遊ぶ

[パーセプトロンシミュレーター](https://novasolver.jp/tools/perceptron.html)で試してほしい操作：

- **学習率 η スライダー**を変え、収束の速さ・安定性の違いを見る
- **w₁ 初期値・b 初期値 スライダー**を悪い値（例：w₁=−2）にして、収束に要するエポック数が増えるのを確認
- **エポック数 スライダー**で学習の打ち切りを変える
- **「最終分類精度」「学習後 w₁・w₂」「収束エポック数」**を読む
- **散布図**で青（クラス+1）と赤（クラス−1）を分ける緑の境界線を観察
- 真の境界（灰破線）と学習した境界（緑）の一致を比較

## まとめ

- パーセプトロンは $y=\operatorname{sign}(\boldsymbol w\cdot\boldsymbol x + b)$ の線形分類器
- 学習則は誤分類時のみ $w \leftarrow w + \eta(t-y)x$
- 線形分離可能なら必ず収束（収束定理）、本例は精度 100%
- 単層は XOR を解けない → 多層化がニューラルネットへ

機械学習の原点を、学習率や初期重みを変えながら体感してみてください。

🧠 **[パーセプトロンシミュレーター（NovaSolver）](https://novasolver.jp/tools/perceptron.html)** で、境界線が学習される様子を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。機械学習では [ニューラルネット](https://novasolver.jp/tools/neural-network.html)、[勾配降下法](https://novasolver.jp/tools/gradient-descent.html)、[モンテカルロ法](https://novasolver.jp/tools/monte-carlo-pi.html) もどうぞ。
