---
title: "マルコフ連鎖はなぜ初期状態を忘れる？ 定常分布と指数収束をJavaScriptで"
emoji: "🔗"
type: "tech"
topics: ["javascript", "確率", "アルゴリズム", "数学", "可視化"]
published: true
---

![マルコフ連鎖と定常分布 — NovaSolver](/images/markov-chain/cover.png)

## 天気予報も検索エンジンも使う「次の状態は今だけで決まる」モデル

「今日が晴れなら明日が雨の確率は 30%」――過去の履歴ではなく**今の状態だけ**で次が決まる確率モデルが**マルコフ連鎖**です。Google の PageRank も、文章生成も、待ち行列も、この枠組みで表せます。面白いのは、十分な時間が経つと**初期状態を完全に忘れて**、一定の確率分布（**定常分布**）に落ち着くこと。

この記事では、2 状態マルコフ連鎖の定常分布と収束を JavaScript で計算します。

🔗 **動くデモ**: [マルコフ連鎖シミュレーター（NovaSolver）](https://novasolver.jp/tools/markov-chain.html)

## 遷移行列と定常分布

状態 1→2 の遷移確率を $p$、2→1 を $q$ とすると、遷移行列は

$$
P = \begin{pmatrix} 1-p & p \\ q & 1-q \end{pmatrix}
$$

分布の更新は $\boldsymbol\pi_{t+1} = \boldsymbol\pi_t P$。十分時間が経つと $\boldsymbol\pi = \boldsymbol\pi P$ を満たす**定常分布**に収束します。2 状態では解析的に解けて

$$
\pi_1 = \frac{q}{p+q},\qquad \pi_2 = \frac{p}{p+q}
$$

時刻 $t$ での状態 1 の確率は、第 2 固有値 $\lambda = 1-p-q$ を使って $P_1(t) = \pi_1 + (P_1(0)-\pi_1)\lambda^t$ と書け、$|\lambda| < 1$ なので**指数的に定常へ収束**します。

既定値 $p=0.30$、$q=0.40$ で計算すると、定常分布は $\pi_1 = 0.5714$、$\pi_2 = 0.4286$。固有値 $\lambda = 0.30$。状態 1 から出発（$P_1(0)=1$）すると $P_1(t)$ は $1 \to 0.70 \to 0.61 \to 0.583 \to \dots$ と急速に 0.5714 へ近づき、99% 収束に要するステップ（混合時間）は $t_{\text{mix}} = \ln(0.01)/\ln 0.30 = 3.82$ ステップです。

![P₁(t)の指数収束（左）と2状態遷移図（右）](/images/markov-chain/charts-closeup.png)

## JavaScript 実装

```javascript
const pi1Of = (p, q) => q / (p + q);     // 定常分布（状態1）
const pi2Of = (p, q) => p / (p + q);
function p1AtT(p, q, p1_init, t) {        // 時刻 t の状態1確率
  const pi1 = pi1Of(p, q);
  const lambda = 1 - p - q;              // 第2固有値
  return pi1 + (p1_init - pi1) * Math.pow(lambda, t);
}
function mixingTime(p, q) {                // 99% 混合時間
  const lambda = Math.abs(1 - p - q);
  if (lambda >= 1 - 1e-12) return Infinity;
  return Math.log(0.01) / Math.log(lambda);
}
// p=0.3, q=0.4 → π1=0.5714, t_mix=3.82
```

収束の速さは固有値 $|\lambda| = |1-p-q|$ で決まります。$p+q$ が 1 に近いほど $\lambda$ が小さく速く収束し、$p+q$ が 0 や 2 に近いと $\lambda$ が 1 に近づきなかなか混ざりません。

![初期状態[1,0]から定常分布へ収束していく様子](/images/markov-chain/slider-anim.gif)

## ツールで遊ぶ

[マルコフ連鎖シミュレーター](https://novasolver.jp/tools/markov-chain.html)で試してほしい操作：

- **遷移確率 p（1→2）・q（2→1）スライダー**を変え、「定常 π₁・π₂」がどう動くか観察
- **初期確率 P₁(0) スライダー**を変え、どこから出発しても同じ定常分布に収束するのを確認
- **観測ステップ t スライダー**を進め、P₁(t) が定常値へ近づくのを見る
- **「t_mix (99%)」**で収束の速さ（混合時間）を読む
- p+q を 1 に近づけて速く収束、0 や 2 に近づけて遅く収束するのを比較
- **状態遷移図**で確率の流れ（矢印）を確認

## まとめ

- マルコフ連鎖は「次は今だけで決まる」確率モデル
- 定常分布は $\pi_1 = q/(p+q)$、$\pi_2 = p/(p+q)$
- 収束は固有値 $\lambda = 1-p-q$ で指数的、初期状態を忘れる
- 既定（p=0.3, q=0.4）で π₁=0.5714、混合時間 3.82 ステップ

検索エンジンから自然言語処理まで支えるマルコフ連鎖を、遷移確率を変えながら体感してみてください。

🔗 **[マルコフ連鎖シミュレーター（NovaSolver）](https://novasolver.jp/tools/markov-chain.html)** で、定常分布への収束を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。確率・アルゴリズムでは [正規分布](https://novasolver.jp/tools/normal-distribution.html)、[2次元ランダムウォーク](https://novasolver.jp/tools/random-walk-2d.html)、[モンテカルロ法でπ推定](https://novasolver.jp/tools/monte-carlo-pi.html) もどうぞ。
