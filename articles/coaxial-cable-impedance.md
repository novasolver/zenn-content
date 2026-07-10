---
title: "同軸ケーブルの特性インピーダンス — なぜ50Ωと75Ωなのか"
emoji: "📡"
type: "tech"
topics: ["javascript", "電気工学", "高周波", "可視化", "物理シミュレーション"]
published: true
---

![同軸ケーブルの特性インピーダンス — NovaSolver](/images/coaxial-cable-impedance/cover.png)

## 特性インピーダンスとは

無線機の説明書には「50Ω系」、テレビの同軸には「75Ω」と書かれています。ところがその同軸ケーブルをテスターで測ると、内導体の導通は数Ω、内外導体間は絶縁で無限大。どこにも「50Ω」は出てきません。

この **50Ω は直流抵抗ではなく、特性インピーダンス $Z_0$** です。同軸ケーブルは「伝送線路」で、内導体（半径 $a$）と外導体（内径 $b$）の間を電磁波が TEM モードで進みます。そのとき波が感じる電圧と電流の比、いわば「波動インピーダンス」が $Z_0$ です。

横断面のラプラス方程式を解くと、単位長キャパシタンス $C$ と単位長インダクタンス $L$ が解析的に求まり、そこから $Z_0$ が次の形になります：

$$
Z_0 = \frac{60}{\sqrt{\varepsilon_r}}\,\ln\!\frac{b}{a}\quad[\Omega]
$$

ここで $\varepsilon_r$ は誘電体の比誘電率です。この記事では：

1. $Z_0$ が **寸法ではなく比 $b/a$ だけ**で決まる理由
2. 単位長 $C$・$L$ と伝搬速度・速度因子の関係
3. なぜ業界が 50Ω と 75Ω に収束したのか

を、実際に数値を計算しながら確かめます。

📐 **動くデモ**: [同軸ケーブル特性インピーダンス計算機（NovaSolver）](https://novasolver.jp/tools/coaxial-cable-impedance.html)

## 単位長 C・L と伝搬速度

特性インピーダンスは、単位長あたりのキャパシタンス $C$ とインダクタンス $L$ から決まります：

$$
C = \frac{2\pi\,\varepsilon_0\,\varepsilon_r}{\ln(b/a)}\ \ [\text{F/m}], \qquad
L = \frac{\mu_0}{2\pi}\,\ln\!\frac{b}{a}\ \ [\text{H/m}]
$$

無損失線路では $Z_0 = \sqrt{L/C}$ で、これを展開すると先ほどの $60/\sqrt{\varepsilon_r}\cdot\ln(b/a)$ に一致します。伝搬速度・速度因子・波長は次の通りです：

$$
v_p = \frac{1}{\sqrt{LC}} = \frac{c}{\sqrt{\varepsilon_r}}, \quad
\text{VF} = \frac{v_p}{c} = \frac{1}{\sqrt{\varepsilon_r}}, \quad
\lambda = \frac{v_p}{f}
$$

注目すべきは、速度因子 VF が **誘電体の比誘電率だけ**で決まること。導体の寸法には一切依存しません。PTFE や固体ポリエチレン（$\varepsilon_r\approx 2.3$）なら VF は約 0.66、発泡 PE（$\varepsilon_r\approx 1.5$）なら 0.8 を超えます。

## 20行で書く同軸計算機

ツールの計算ロジックは、定数3つと数式だけで完結します。JavaScript にするとこうなります：

```javascript
const C0 = 2.998e8;        // 光速 m/s
const EPS0 = 8.854e-12;    // 真空の誘電率 F/m
const MU0 = 4 * Math.PI * 1e-7; // 真空の透磁率 H/m

// a, b は mm、er は比誘電率、f は MHz
function coax(a_mm, b_mm, er, f_MHz) {
  const a = a_mm * 1e-3, b = b_mm * 1e-3;
  const lnr = Math.log(b / a);
  const z0 = (60 / Math.sqrt(er)) * lnr;   // 特性インピーダンス Ω
  const vf = 1 / Math.sqrt(er);            // 速度因子
  const vp = vf * C0;                       // 伝搬速度 m/s
  const lam = vp / (f_MHz * 1e6);           // 波長 m
  const C = (2 * Math.PI * EPS0 * er) / lnr; // 単位長 C [F/m]
  const L = (MU0 / (2 * Math.PI)) * lnr;     // 単位長 L [H/m]
  return { z0, vf, vp, lam, C, L };
}
```

既定値 $a=0.5$ mm、$b=3.5$ mm、$\varepsilon_r=2.3$、$f=100$ MHz を入れると：

```javascript
coax(0.5, 3.5, 2.3, 100);
// z0:  76.99  (Ω)
// vf:  0.659
// lam: 1.977  (m)
// C:   65.75  (pF/m)
// L:   389.2  (nH/m)
```

$Z_0 \approx 77\,\Omega$。これは「最低損失」に近い値で、後述する 75Ω 系のすぐ近くです。

## b/a だけで決まる、という構造

$Z_0$ は $\ln(b/a)$ に比例します。つまり **内導体と外導体の絶対寸法ではなく、比 $b/a$ だけ**で決まります。$a$ と $b$ を同じ倍率で拡大しても $Z_0$ は不変です。

$\varepsilon_r = 2.3$（PE 系）で $b/a$ を振ると：

| $b/a$ | $Z_0$ [$\Omega$] | 用途の目安 |
|---|---|---|
| 2.0 | 27.4 | 大電力寄り |
| 3.4 | 48.4 | **50Ω 系（RF・計測）** |
| 5.0 | 63.7 | — |
| 7.0 | 77.0 | **75Ω 系の近傍（映像）** |
| 10.0 | 91.1 | 高インピーダンス |

50Ω を作るには $b/a\approx 3.5$、75Ω 相当なら $b/a\approx 6.6$ あたり。だから太い RG-8 も細い RG-58 も、50Ω 同軸はみな $b/a$ がほぼ同じです。太さで変わるのは耐電力と損失だけ。「比だけで決まる」この性質のおかげで、携帯機器に細いケーブルが使えます。

実在規格でも確かめられます。RG-58/U 相当（内導体半径 0.405 mm、外導体内径 1.475 mm、$\varepsilon_r=2.25$）を 1 GHz で計算すると、$Z_0\approx 51.7\,\Omega$、$\lambda\approx 200$ mm、$C\approx 96.8$ pF/m と、データシートの 50Ω・約 100 pF/m によく一致します。

## なぜ 50Ω と 75Ω なのか

同じ誘電体・同じ外径でも、$b/a$ を変えると性能のピークがずれます。一般に言われる目安では、空気〜PE 充填の同軸で、最大電力伝送が約 30Ω、最低損失が約 77Ω、最大耐電圧が約 60Ω 付近にあるとされます。

- **50Ω**：これらの妥協点。無線・計測（VNA、SMA/N 型コネクタ、基板のマイクロストリップ）で標準化
- **75Ω**：最低損失に近く、長距離で減衰を抑えたいテレビ・CATV・映像系で標準化

異なる系を直結すると不整合で反射が起きます。50Ω 系に 75Ω をつなぐと、電圧反射係数は

$$
|\Gamma| = \left|\frac{Z_L - Z_0}{Z_L + Z_0}\right| = \frac{|75-50|}{75+50} = 0.2
$$

VSWR は $(1+0.2)/(1-0.2)=1.5$ になります。反射電力は入射の約 4%。送信機保護や映像ゴーストの原因になるので、$\lambda/4$ 変換器（$\sqrt{50\times75}\approx 61\,\Omega$ の同軸を $\lambda/4$ 長）などで整合を取ります。

## ツールで遊ぶ

NovaSolver のツールでは、4つのスライダーを動かすと $Z_0$・VF・波長・単位長キャパシタンスがその場で更新されます：

![b/a と εr を動かすと Z_0 曲線上の現在点が移動する](/images/coaxial-cable-impedance/slider-anim.gif)

試してほしい操作：

- **内導体半径 a** と **外導体内径 b** を同じ倍率で動かして、$Z_0$ が変わらない（比だけで決まる）ことを確認
- **比誘電率 ε_r** を 1.0（空気）→ 2.3（PE）→ 4.5 と上げて、$Z_0$ と速度因子 VF がどちらも下がるのを観察
- 右側の **Z_0 vs b/a 曲線**で、赤い現在点が 50Ω / 75Ω の基準破線をまたぐ位置を探す
- **周波数 f** を変えて、波長 λ（VF を反映した実効波長）の変化を見る
- **リセット**で PTFE 想定の既定値（$a=0.5$, $b=3.5$, $\varepsilon_r=2.3$）に戻す

![同軸断面と Z_0 設計曲線](/images/coaxial-cable-impedance/charts-closeup.png)

## まとめ

- 特性インピーダンスは直流抵抗ではなく、波が感じる $Z_0 = (60/\sqrt{\varepsilon_r})\ln(b/a)$
- $Z_0$ は寸法でなく比 $b/a$ だけで決まる。太さで変わるのは耐電力と損失
- 既定値（PTFE 想定）で $Z_0\approx 77\,\Omega$、VF$\approx 0.66$、$C\approx 66$ pF/m
- 50Ω は電力・損失・耐圧の妥協点、75Ω は最低損失に近く映像系で標準

「比だけで決まる」というシンプルな構造が、ミリ波から海底ケーブルまで同じ式で設計できる理由です。なお本ツールは理想 TEM・周波数無依存の $Z_0$ を扱っており、導体損・誘電損による高周波での偏差は含まない点に留意してください。

📐 **[同軸ケーブル特性インピーダンス計算機（NovaSolver）](https://novasolver.jp/tools/coaxial-cable-impedance.html)** で、$b/a$ と $\varepsilon_r$ を動かして 50Ω/75Ω の境目を探してみてください。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。高周波・伝送線路では [マイクロ波伝送線路計算機](https://novasolver.jp/tools/microwave-transmission.html)、[矩形導波管モード計算](https://novasolver.jp/tools/waveguide-modes.html)、[バンドパスフィルタ](https://novasolver.jp/tools/band-pass-filter.html) なども揃えています。
