---
title: "コンプトン散乱 — 光が粒子であることを示した波長シフト Δλ"
emoji: "💥"
type: "tech"
topics: ["javascript", "物理", "量子力学", "可視化", "物理シミュレーション"]
published: false
---

![コンプトン散乱 — NovaSolver](/images/compton-scattering/cover.png)

## コンプトン散乱とは

X 線を物質に当てると、散乱された X 線の波長が「伸びる」現象が観測されます。これが **コンプトン散乱**です。1923 年に Arthur Compton が炭素ターゲットへの X 線散乱で発見しました。

光が純粋な波なら、散乱しても波長（周波数）は変わらないはずです。ところが実験では散乱角に応じて波長が伸びた。この結果は、光を運動量 $p = h/\lambda$ を持つ「光子（粒子）」とみなし、電子との弾性衝突として扱うとピタリと説明できました。光の粒子性を決定づけた歴史的な実験です。

この記事では：

1. 波長シフト $\Delta\lambda = \lambda_C(1-\cos\theta)$ と電子のコンプトン波長
2. 散乱光子エネルギーと反跳電子の JavaScript 実装
3. 角度依存性とエネルギー依存性を数値で確かめる

📐 **動くデモ**: [コンプトン散乱シミュレーター（NovaSolver）](https://novasolver.jp/tools/compton-scattering.html)

## 波長シフトの式

光子と電子のエネルギー・運動量保存則を解くと、散乱前後の波長差は次の驚くほど単純な式になります：

$$
\Delta\lambda = \lambda_f - \lambda_{in} = \lambda_C\,(1 - \cos\theta)
$$

ここで $\theta$ は光子の散乱角、$\lambda_C = h/(m_e c) \approx 2.426$ pm は **電子のコンプトン波長**です。注目すべきは、$\Delta\lambda$ が**入射エネルギーに一切依存せず、散乱角だけで決まる**こと。$\theta=90°$ なら、紫外線でも γ 線でも $\Delta\lambda$ は同じ 2.43 pm です。

散乱後の光子エネルギーと反跳電子は、$\alpha = E_{in}/(m_e c^2)$（$m_e c^2 = 511$ keV）を使って：

$$
E_f = \frac{E_{in}}{1 + \alpha(1 - \cos\theta)},\qquad KE_e = E_{in} - E_f,\qquad \tan\varphi_e = \frac{\cot(\theta/2)}{1 + \alpha}
$$

## JavaScript で実装する

ツールの計算ロジックは、保存則をそのまま関数化したものです：

```javascript
const LAMBDA_C = 2.4263102387;  // 電子のコンプトン波長 [pm]
const MEC2     = 510.99895;     // 電子の静止エネルギー [keV]
const HC       = 1239.84193;    // hc [keV·pm]

function compton(Ein_keV, thetaDeg) {
  const theta  = thetaDeg * Math.PI / 180;
  const dLam   = LAMBDA_C * (1 - Math.cos(theta));  // 波長シフト [pm]
  const lamIn  = HC / Ein_keV;                      // 入射波長 [pm]
  const lamF   = lamIn + dLam;                      // 散乱波長 [pm]
  const Ef     = HC / lamF;                         // 散乱光子E [keV]
  const KE     = Ein_keV - Ef;                      // 反跳電子KE [keV]
  const alpha  = Ein_keV / MEC2;
  const phiE   = Math.atan((1 / Math.tan(theta / 2)) / (1 + alpha)) * 180 / Math.PI;
  return { dLam, lamIn, lamF, Ef, KE, phiE };
}

const r = compton(100, 90);  // 100 keV, θ=90°
console.log(r.dLam.toFixed(4), r.Ef.toFixed(2), r.KE.toFixed(2), r.phiE.toFixed(1));
// 2.4263  83.63  16.37  39.9
```

デフォルト条件（$E_{in}=100$ keV, $\theta=90°$）では、散乱光子は 83.63 keV、波長シフトは 2.43 pm、電子に渡るエネルギーは 16.37 keV、反跳電子は前方 39.9° へ飛びます。

## 可視化：散乱の幾何と Δλ(θ) 曲線

ツールは入射光子（黄）・散乱光子（青）・反跳電子（赤）の幾何と、波長シフトの角度依存性 $\Delta\lambda(\theta)$ を描きます。

![散乱の幾何と Δλ(θ) 曲線](/images/compton-scattering/charts-closeup.png)

$\Delta\lambda(\theta) = \lambda_C(1-\cos\theta)$ は $\theta=0°$ でゼロ、$\theta=90°$ で $\lambda_C$、$\theta=180°$（真後ろへの後方散乱）で最大値 $2\lambda_C \approx 4.85$ pm を取る、なめらかな曲線になります。

## 角度依存とエネルギー依存を数値で確かめる

まず**波長シフトは角度だけ**で決まることを確認します（入射エネルギーに依存しない）：

| 散乱角 $\theta$ | $\Delta\lambda$ [pm] | 備考 |
|---|---|---|
| 0° | 0.000 | 前方散乱、シフトなし |
| 45° | 0.711 | |
| 90° | 2.426 | $= \lambda_C$ |
| 135° | 4.142 | |
| 180° | 4.853 | $= 2\lambda_C$（最大、後方散乱） |

一方、**相対的なエネルギー損失** $KE_e/E_{in}$ は入射エネルギーに強く依存します（$\theta=90°$ 固定）：

| 入射 $E_{in}$ | 散乱光子 $E_f$ | エネルギー損失 $KE_e/E_{in}$ | 反跳角 $\varphi_e$ |
|---|---|---|---|
| 100 keV | 83.6 keV | 16.4 % | 39.9° |
| 200 keV | 143.7 keV | 28.1 % | 35.7° |
| 500 keV | 252.7 keV | 49.5 % | 26.8° |
| 1 MeV | 338.2 keV | 66.2 % | 18.7° |

入射エネルギーが高いほど（$\alpha$ が大きいほど）電子に渡るエネルギーの割合が増え、反跳電子は前方に集中します。

最後に **コンプトンエッジ**。Cs-137 の 662 keV γ 線を $\theta=180°$ で散乱させると、反跳電子の運動エネルギーは 477.7 keV になります。これを独立の閉形式 $KE_{max} = \dfrac{2\alpha^2}{1+2\alpha}\,m_ec^2$ で計算しても 477.7 keV で一致しました。γ 線スペクトルに現れる鋭い段差「コンプトンエッジ」の位置として、検出器較正に使われる量です。

なお標的を陽子（電子の約 1836 倍の質量）にすると $\lambda_C$ が質量に反比例して縮み、$\theta=90°$ での $\Delta\lambda$ は約 1.32 fm（フェムトメートル）と桁外れに小さくなります。重い標的ではコンプトン散乱が事実上の弾性散乱（トムソン散乱）に漸近する、という事情がここから読み取れます。

## ツールで遊ぶ

NovaSolver のツールでは、4 つのパラメータで散乱条件を組み立てられます：

![散乱角をスイープすると Δλ が変化する](/images/compton-scattering/slider-anim.gif)

試してほしい操作：

- **入射光子エネルギー $E_{in}$**（10〜1000 keV）を動かして、$\Delta\lambda$ は一定なのに $E_f$・$KE_e$ が大きく変わる様子を確認
- **散乱角 $\theta$**（0〜180°）を変え、$\Delta\lambda(\theta)$ 曲線上の現在位置（黄点）を観察
- **「散乱角をスイープ」ボタン**で $\theta$ を自動掃引し、後方散乱で $\Delta\lambda$ が最大になることを体感
- **標的質量倍率 $m/m_e$** を上げて、Δλ がほぼゼロに漸近する（トムソン散乱化）様子を確認
- **検出閾値 $E_{detect}$** を設定し、散乱光子が検出されるかの判定を確認

## まとめ

- 波長シフトは $\Delta\lambda = \lambda_C(1-\cos\theta)$、$\lambda_C = h/(m_ec) \approx 2.43$ pm
- $\Delta\lambda$ は入射エネルギーに依存せず散乱角だけで決まり、$\theta=180°$ で最大 $2\lambda_C \approx 4.85$ pm
- 散乱光子は $E_f = E_{in}/[1+\alpha(1-\cos\theta)]$ で、高エネルギーほど電子へのエネルギー移行が大きい
- Cs-137（662 keV）のコンプトンエッジは 477.7 keV で、閉形式と一致

コンプトン散乱は、医用 CT・PET の散乱補正、γ 線分光のコンプトンエッジ、X 線天文学のコンプトン望遠鏡など、放射線を扱う現場の基礎になっています。「光は波であり粒子でもある」という二重性を、たった一本の式で体感できるのが魅力です。

📐 **[コンプトン散乱シミュレーター（NovaSolver）](https://novasolver.jp/tools/compton-scattering.html)** で、$E_{in}$ と $\theta$ を動かして波長シフトとエネルギー移行を確かめてみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。量子・放射線分野では [ボーア水素原子モデル](https://novasolver.jp/tools/bohr-hydrogen-model.html)、[黒体放射とプランクの法則](https://novasolver.jp/tools/blackbody-radiation.html)、[放射性崩壊と半減期](https://novasolver.jp/tools/radioactive-decay.html) なども揃えています。
