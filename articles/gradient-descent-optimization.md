---
title: "勾配降下法とAdamをJavaScriptで実装する — 機械学習が「谷を降りる」仕組み"
emoji: "📉"
type: "tech"
topics: ["javascript", "機械学習", "最適化", "アルゴリズム", "可視化"]
published: false
---

![勾配降下法 — NovaSolver](/images/gradient-descent/cover.png)

## 機械学習は、巨大な谷をどう降りているのか

ニューラルネットの学習も、回帰のフィッティングも、その本質は「損失関数という地形の最も低い谷を探す」最適化です。霧で視界の悪い山で谷へ降りるには、足元の傾き（勾配）を測って一番急な下り方向へ一歩進む――これを繰り返すのが**勾配降下法**。そして現代の深層学習で標準的に使われる **Adam** は、この基本に「慣性」と「適応的な歩幅」を加えた改良版です。

この記事では、勾配降下法と Adam を JavaScript で実装します。

📉 **動くデモ**: [勾配降下法シミュレーター（NovaSolver）](https://novasolver.jp/tools/gradient-descent.html)

## 基本の更新則と4つの最適化手法

最も基本的な勾配降下法（SGD）は、勾配 $\nabla f$ の逆向きに学習率 $\alpha$ だけ進みます。

$$
\boldsymbol\theta_{n+1} = \boldsymbol\theta_n - \alpha\,\nabla f(\boldsymbol\theta_n)
$$

これに改良を重ねた手法が並びます：**Momentum**（過去の勾配を慣性として蓄積）、**RMSprop**（勾配の二乗で歩幅を方向ごとに調整）、そして両者を統合した **Adam**。Adam の更新は 1 次・2 次モーメントの指数移動平均とバイアス補正からなります。

$$
\hat m_t = \frac{m_t}{1-\beta_1^t},\quad \hat v_t = \frac{v_t}{1-\beta_2^t},\quad
\boldsymbol\theta_{n+1} = \boldsymbol\theta_n - \alpha\frac{\hat m_t}{\sqrt{\hat v_t}+\varepsilon}
$$

シンプルな谷 $f(x,y) = x^2+y^2$ を、Adam（$\alpha=0.01$, $\beta_1=0.9$, $\beta_2=0.999$）で開始点 $(-2.52, 2.52)$ から降下させると、損失は 13 から単調に減り、**500 ステップで $(0.07, 0.07)$、損失 0.01** まで原点（最小値）に近づきます。

![ボウル型関数の等高線とAdamの降下経路（左）と損失の減少（右）](/images/gradient-descent/charts-closeup.png)

## JavaScript 実装

勾配は数値微分（中心差分）で求められます。SGD と Adam を並べます。

```javascript
function gradient(x, y) {
  const e = 1e-5;
  return [
    (loss(x+e, y) - loss(x-e, y)) / (2*e),
    (loss(x, y+e) - loss(x, y-e)) / (2*e),
  ];
}
// SGD: 勾配の逆向きへ一歩
px -= lr * gx;  py -= lr * gy;

// Adam: 1次・2次モーメント + バイアス補正
m1 = b1*m1 + (1-b1)*gx;  m2 = b1*m2 + (1-b1)*gy;
v1 = b2*v1 + (1-b2)*gx*gx;  v2 = b2*v2 + (1-b2)*gy*gy;
const m1h = m1/(1 - b1**t), v1h = v1/(1 - b2**t);   // バイアス補正
px -= lr * m1h / (Math.sqrt(v1h) + 1e-8);
```

学習率 $\alpha$ が小さすぎると収束が遅く、大きすぎると谷を飛び越えて発散・振動します。Adam は方向ごとに実効歩幅を自動調整するため、谷が細長い（病的な）地形でも安定して降りられるのが強みです。

![等高線上をAdamがステップごとにジグザグなく降りていく](/images/gradient-descent/slider-anim.gif)

## ツールで遊ぶ

[勾配降下法シミュレーター](https://novasolver.jp/tools/gradient-descent.html)で試してほしい操作：

- **関数の選択**（ボウル・ローゼンブロック・ヒンメルブラウ・鞍点）を変え、地形ごとの難しさを比較
- **アルゴリズム選択**（SGD・Momentum・RMSprop・Adam）を切り替え、収束の違いを観察
- **学習率 α スライダー**を上げすぎて発散・振動が起きるのを見る（小さすぎると遅い）
- **キャンバスをクリック**して開始点を変え、初期値依存（局所最小）を確認
- **β₁・β₂ スライダー**で Momentum/Adam の慣性と適応の強さを調整
- **損失曲線**でステップごとの損失減少を読む

## まとめ

- 勾配降下法は $\theta \leftarrow \theta - \alpha\nabla f$ で損失の谷を降りる
- Momentum・RMSprop・Adam は慣性と適応歩幅で収束を改善
- 勾配は数値微分（中心差分）で簡単に実装できる
- ボウル + Adam（α=0.01）は 500 ステップで損失 0.01 まで降下
- 学習率が大きすぎると発散、小さすぎると低速

機械学習の心臓部である最適化を、関数・手法・学習率を変えながら体感してみてください。

📉 **[勾配降下法シミュレーター（NovaSolver）](https://novasolver.jp/tools/gradient-descent.html)** で、谷を降りるアルゴリズムを確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。数値計算・ML では [ニュートン・ラフソン法](https://novasolver.jp/tools/newton-raphson.html)、[パーセプトロン](https://novasolver.jp/tools/perceptron.html)、[ニューラルネット](https://novasolver.jp/tools/neural-network.html) もどうぞ。
