---
title: "ジャイロスコープの歳差はなぜ速く回すほど遅くなる？ Ωp=mgd/(Iω)を計算する"
emoji: "🎡"
type: "tech"
topics: ["javascript", "物理シミュレーション", "力学", "可視化", "数値計算"]
published: true
---

![ジャイロスコープの歳差運動 — NovaSolver](/images/gyroscope/cover.png)

## 倒れずに首を振るコマの不思議

高速で回るコマは、倒れる代わりに軸がゆっくり円を描きます。これが**歳差運動（precession）**。直感に反するのは「速く回すほど歳差はゆっくりになる」点です。なぜ回転を速めると、軸の首振りが遅くなるのか――答えは角運動量とトルクの関係に隠れています。

この記事では、歳差速度を JavaScript で計算し、回転数との関係を確かめます。

🎡 **動くデモ**: [ジャイロスコープシミュレーター（NovaSolver）](https://novasolver.jp/tools/gyroscope.html)

## トルクが角運動量を「回す」

回転体の角運動量は $L = I\omega$（$I$ は慣性モーメント、$\omega$ はスピン角速度）。重力はピボットまわりにトルク $\tau = mgd\sin\theta$ を生みます（$d$ は重心までの距離、$\theta$ は軸の傾き）。このトルクは $L$ の**大きさ**ではなく**向き**を変えるため、軸は鉛直まわりに歳差します。歳差角速度は次式です。

$$
\Omega_p = \frac{\tau}{L\sin\theta} = \frac{mgd}{I\omega}
$$

ここがポイント：$\sin\theta$ が分子（トルク）と分母（$L$ の水平成分）で打ち消し合い、**歳差速度は傾きによらず $\Omega_p = mgd/(I\omega)$** になります。そして $\omega$ が分母にあるので、**スピンが速いほど歳差は遅い**のです。

円板ロータ（$I = \tfrac12 mr^2$）で既定値 $m=0.5\,\mathrm{kg}$、$r=10\,\mathrm{cm}$、$d=10\,\mathrm{cm}$、$\omega = 3000\,\mathrm{rpm} = 314.2\,\mathrm{rad/s}$ を代入すると、$I = 0.0025\,\mathrm{kg\,m^2}$、$L = 0.785\,\mathrm{kg\,m^2/s}$、$\tau = 0.491\,\mathrm{N\,m}$、**歳差速度 $\Omega_p = 0.625\,\mathrm{rad/s}$**（1 周 約 10.1 秒）と求まります。

![歳差速度とスピン回転数（左）、L・トルク・歳差の関係（右）](/images/gyroscope/charts-closeup.png)

## JavaScript 実装

```javascript
function precession(rpm, m, r_cm, d_cm) {
  const r = r_cm / 100, d = d_cm / 100, g = 9.81;
  const omega = rpm * 2 * Math.PI / 60;   // RPM → rad/s
  const I = 0.5 * m * r * r;              // 円板の慣性モーメント
  const L = I * omega;                    // 角運動量
  const tau = m * g * d;                  // 重力トルク（θ=90°）
  const omegaP = tau / L;                 // = mgd/(Iω)
  return { I, L, tau, omegaP, period: 2 * Math.PI / omegaP };
}
```

回転数を 1000 → 6000 rpm に上げると、歳差速度は $1.874 \to 0.312\,\mathrm{rad/s}$ と**回転数に反比例**して遅くなります。フライホイールや宇宙機の姿勢制御装置（CMG）が「ジャイロ剛性」で安定するのも、この $L$ の大きさが姿勢を保つためです。

![角運動量 L が鉛直軸まわりに歳差する様子](/images/gyroscope/slider-anim.gif)

## ツールで遊ぶ

[ジャイロスコープシミュレーター](https://novasolver.jp/tools/gyroscope.html)で試してほしい操作：

- **スピン回転数 ω スライダー**を上げ、「歳差速度 Ω_p」が反比例で**遅くなる**のを確認
- **ロータ質量 m・半径 r・ピボット距離 d スライダー**を変え、$\Omega_p = mgd/(I\omega)$ の依存性を見る
- **「コマ」「フライホイール」「宇宙機CMG」プリセット**で用途別のパラメータを比較
- **ベクトル図**で角運動量 L・重力トルク τ・歳差 Ω_p の向きの関係を読む
- **歳差速度 vs 回転数グラフ**で反比例カーブを確認

> 補足：歳差速度は本来、軸の傾き $\theta$ によらず一定です（$\sin\theta$ が約分されるため）。傾斜角スライダーは軸の傾きを変えて図示しますが、厳密な歳差速度は傾きに依存しない点に注意してください。

## まとめ

- 歳差速度は $\Omega_p = mgd/(I\omega)$、傾きによらず一定
- スピン $\omega$ に**反比例**：速く回すほど歳差は遅い
- 既定値で $\Omega_p = 0.625\,\mathrm{rad/s}$（1 周 約 10 秒）
- 大きな $L$ が姿勢を保つ「ジャイロ剛性」の源

直感に反するコマの首振りを、回転数や質量を変えながら体感してみてください。

🎡 **[ジャイロスコープシミュレーター（NovaSolver）](https://novasolver.jp/tools/gyroscope.html)** で、角運動量とトルクの不思議を確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。回転・力学系では [フーコーの振り子](https://novasolver.jp/tools/foucault-pendulum.html)、[コリオリの力](https://novasolver.jp/tools/coriolis-effect.html)、[遠心調速機](https://novasolver.jp/tools/centrifugal-governor.html) もどうぞ。
