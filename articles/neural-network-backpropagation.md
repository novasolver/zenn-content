---
title: "ニューラルネットがXORを解く仕組み — 誤差逆伝播をJavaScriptで実装する"
emoji: "🧠"
type: "tech"
topics: ["javascript", "機械学習", "ニューラルネットワーク", "可視化", "アルゴリズム"]
published: false
---

![ニューラルネットと誤差逆伝播 — NovaSolver](/images/neural-network/cover.png)

## 単層では解けないXORを、隠れ層が解く

パーセプトロン（単層）には致命的な弱点がありました――**XOR 問題が解けない**。XOR は直線一本で 2 クラスを分けられない（線形分離不可能）からです。これを解決したのが**隠れ層**と、その重みを効率よく学習する**誤差逆伝播法（バックプロパゲーション）**。現代の深層学習の根幹です。

この記事では、多層ニューラルネットの順伝播と誤差逆伝播を JavaScript で実装します。

🧠 **動くデモ**: [ニューラルネットシミュレーター（NovaSolver）](https://novasolver.jp/tools/neural-network.html)

## 順伝播と誤差逆伝播

各層は前層の出力 $\boldsymbol a^{(l-1)}$ に重み・バイアスを掛けて活性化します（**順伝播**）。

$$
z_i^{(l)} = b_i^{(l)} + \sum_j w_{ij}^{(l)} a_j^{(l-1)},\qquad a_i^{(l)} = \sigma(z_i^{(l)})
$$

学習は出力の誤差を**後ろ向きに伝える**ことで行います。出力層の誤差 $\delta$ を計算し、連鎖律で前層へ伝播させ、各重みを勾配方向に更新します。

$$
\delta_i^{(L)} = (a_i^{(L)} - t_i)\,\sigma'(a_i^{(L)}),\quad
\delta_j^{(l)} = \Big(\sum_i w_{ij}^{(l+1)}\delta_i^{(l+1)}\Big)\sigma'(a_j^{(l)})
$$

$$
w_{ij}^{(l)} \leftarrow w_{ij}^{(l)} - \eta\,\delta_i^{(l)} a_j^{(l-1)}
$$

シミュレーターの既定は **入力2 - 隠れ層[4,4] - 出力1** の構成で、XOR データ（[0,0]→0, [0,1]→1, [1,0]→1, [1,1]→0）を学習します。MSE 損失は学習とともに下がり、**最終的に分類精度 100%**。代表的な学習では損失が約 0.13 から 0.001 以下まで減少し、決定境界が XOR を正しく分ける曲線になります（単層では絶対に作れない非線形境界です）。

![XORの決定境界（左, 100%分類）と損失の減少（右）](/images/neural-network/charts-closeup.png)

## JavaScript 実装

シグモイドとその微分を使った順伝播・逆伝播の核心部分です。

```javascript
const sigmoid  = x => 1 / (1 + Math.exp(-x));
const sigmoidD = a => a * (1 - a);            // a=σ(z) を使った微分

// 順伝播
function forward(input) {
  activations[0] = input;
  for (let l = 1; l < layers; l++)
    for (let i = 0; i < sizes[l]; i++) {
      let z = biases[l-1][i];
      for (let j = 0; j < sizes[l-1]; j++) z += weights[l-1][i][j] * activations[l-1][j];
      activations[l][i] = sigmoid(z);
    }
  return activations[layers-1];
}
// 誤差逆伝播（出力層）
deltas[L][i] = (a[L][i] - target[i]) * sigmoidD(a[L][i]);
// 重み更新
weights[l-1][i][j] -= lr * deltas[l][i] * activations[l-1][j];
```

学習率 $\eta$ が大きすぎると損失が振動・発散し、小さすぎると収束が遅くなります。隠れ層のおかげで、入力空間を「折り曲げて」線形分離可能な形に変換できる――これが多層ネットの威力です。

![エポックが進むにつれ決定境界がXORを分ける形に変化](/images/neural-network/slider-anim.gif)

## ツールで遊ぶ

[ニューラルネットシミュレーター](https://novasolver.jp/tools/neural-network.html)で試してほしい操作：

- **「1エポック」「100エポック」「自動学習」ボタン**で損失が下がる様子を観察
- **隠れ層の数・ノード数 スライダー**を変え、表現力（境界の複雑さ）の違いを見る
- **学習率 η スライダー**を上げすぎて学習が不安定になるのを確認
- **「重み再初期化」**で異なる初期値からの収束（局所解）を比較
- **ネットワーク図**で重みの符号（青=正/赤=負）と大きさを読む
- **決定境界**が単層では作れない曲線になることを確認

> 補足：このシミュレーターは XOR の学習に最適化されており、出力層はシグモイドで固定です（隠れ層の活性化関数は選択可能）。

## まとめ

- 単層パーセプトロンは XOR を解けない（線形分離不可能）
- 隠れ層＋誤差逆伝播で非線形な決定境界を学習できる
- 逆伝播は出力の誤差を連鎖律で前層へ伝え、勾配で重みを更新
- 既定の [2,4,4,1] 構成で XOR を精度 100% で分類

深層学習の出発点を、層数・学習率を変えながら体感してみてください。

🧠 **[ニューラルネットシミュレーター（NovaSolver）](https://novasolver.jp/tools/neural-network.html)** で、誤差逆伝播による学習を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。機械学習では [パーセプトロン](https://novasolver.jp/tools/perceptron.html)、[勾配降下法](https://novasolver.jp/tools/gradient-descent.html)、[モンテカルロ法](https://novasolver.jp/tools/monte-carlo-pi.html) もどうぞ。
