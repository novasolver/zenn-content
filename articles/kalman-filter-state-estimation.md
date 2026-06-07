---
title: "カルマンフィルタで雑音だらけの観測から真値を推定する — 予測と更新をJSで"
emoji: "🛰️"
type: "tech"
topics: ["javascript", "信号処理", "制御工学", "アルゴリズム", "可視化"]
published: false
---

![カルマンフィルタ — NovaSolver](/images/kalman-filter/cover.png)

## GPSやセンサーの「ノイズ」を最適に取り除く

GPS の位置も、加速度センサーの値も、生のデータは雑音まみれです。**カルマンフィルタ**は「物理モデルによる予測」と「ノイズを含む観測」を、それぞれの不確かさに応じて**最適な重み**で融合し、真の状態を推定します。アポロ計画の航法から自動運転まで、状態推定の標準ツールです。

この記事では、1 次元カルマンフィルタの予測・更新を JavaScript で実装します。

🛰️ **動くデモ**: [カルマンフィルタシミュレーター（NovaSolver）](https://novasolver.jp/tools/kalman-filter.html)

## 予測ステップと更新ステップ

カルマンフィルタは 2 段階を繰り返します。**予測**ではモデルで状態と誤差共分散を進め、**更新**では観測 $z$ を取り込みます（1 次元では $F=H=1$）。

$$
\text{予測:}\quad \hat x^- = \hat x,\quad P^- = P + Q
$$

$$
\text{更新:}\quad K = \frac{P^-}{P^- + R},\quad \hat x = \hat x^- + K(z - \hat x^-),\quad P = (1-K)P^-
$$

$Q$ はプロセスノイズ（モデルの不確かさ）、$R$ は観測ノイズ。**カルマンゲイン $K$** が両者のバランスを決めます：観測が信頼できる（$R$ 小）なら $K$ は大きく観測寄り、モデルが信頼できる（$Q$ 小）なら $K$ は小さく予測寄りになります。

「GPS」プリセット（$Q\approx0.003$, $R=10$, 信号 0.5 Hz, ノイズ振幅 1.2）で 80 ステップ走らせると、生の観測の RMSE が **1.13** なのに対し、カルマン推定の RMSE は **0.71** へと **約 37% 改善**します。ゲイン $K$ と誤差共分散 $P$ は時間とともに一定値（定常）へ収束します。

![真値・観測・カルマン推定（左, GPSプリセット）とK・Pの収束（右）](/images/kalman-filter/charts-closeup.png)

## JavaScript 実装

```javascript
function kalmanStep(xhat, P, z, Q, R) {
  // 予測
  const xPred = xhat;          // F = 1（等速モデル）
  const Ppred = P + Q;
  // 更新
  const K = Ppred / (Ppred + R);        // カルマンゲイン
  const xNew = xPred + K * (z - xPred);  // 観測で補正
  const Pnew = (1 - K) * Ppred;          // 誤差共分散を更新
  return { xhat: xNew, P: Pnew, K };
}
// ループで観測 z を順に処理し、推定を更新していく
```

注意点として、フィルタの効き目はパラメータ調整次第です。たとえば信号が速く（高周波）モデルを過信（$Q$ が小さすぎる）すると、推定が観測に追従できず**遅れ**が出て、かえって生データより誤差が増えることもあります。$Q/R$ のチューニングこそカルマンフィルタの腕の見せ所です。

![観測ノイズの中からカルマン推定が真値を追従していく](/images/kalman-filter/slider-anim.gif)

## ツールで遊ぶ

[カルマンフィルタシミュレーター](https://novasolver.jp/tools/kalman-filter.html)で試してほしい操作：

- **「GPS」「センサー」「予測重視」プリセット**で典型的なチューニングを比較
- **観測ノイズ R スライダー**を上げ、ゲイン $K$ が小さくなり推定がなめらかになるのを確認
- **プロセスノイズ Q スライダー**を上げ、$K$ が大きくなり観測に敏感になるのを見る
- **「生データ RMSE」と「フィルタ後 RMSE」**を比較し、改善幅を確認（設定次第で悪化もする）
- **初期共分散 P₀ スライダー**で立ち上がりの挙動を見る
- **K・P 推移グラフ**で定常値への収束を読む

## まとめ

- カルマンフィルタは予測（$P^-=P+Q$）と更新（$K=P^-/(P^-+R)$）の 2 段階
- ゲイン $K$ が予測と観測の最適なバランスを取る
- GPS プリセットで RMSE が 1.13→0.71（約 37% 改善）
- $Q/R$ の調整が重要：過度な平滑化は追従遅れを招く

ノイズ除去と状態推定の名アルゴリズムを、ノイズパラメータを変えながら体感してみてください。

🛰️ **[カルマンフィルタシミュレーター（NovaSolver）](https://novasolver.jp/tools/kalman-filter.html)** で、予測と観測の融合を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。信号処理・制御では [PID制御](https://novasolver.jp/tools/pid.html)、[FFTアナライザ](https://novasolver.jp/tools/fft-analyzer.html)、[勾配降下法](https://novasolver.jp/tools/gradient-descent.html) もどうぞ。
