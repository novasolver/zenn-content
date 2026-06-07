---
title: "気柱の共鳴：開管と閉管で倍音が違う理由 — f=nc/2L と (2n-1)c/4L をJSで"
emoji: "🎵"
type: "tech"
topics: ["javascript", "物理シミュレーション", "波動", "音響", "可視化"]
published: false
---

![気柱の共鳴 — NovaSolver](/images/acoustic-resonance/cover.png)

## フルートとクラリネット、同じ長さでも音が違う

管楽器は、管の中の空気が特定の周波数で共鳴して音を出します。面白いのは、両端が開いた**開管**（フルート）と片端が閉じた**閉管**（クラリネット）では、同じ長さでも基本周波数が 1 オクターブ違い、出る倍音の種類も異なること。クラリネットが独特の音色を持つのは、**奇数倍音しか出ない**からです。

この記事では、開管・閉管の共鳴周波数を JavaScript で計算します。

🎵 **動くデモ**: [気柱の共鳴シミュレーター（NovaSolver）](https://novasolver.jp/tools/acoustic-resonance.html)

## 開管と閉管の共鳴条件

定在波の境界条件が周波数を決めます。**開管**は両端が腹（振動の最大）なので

$$
f_n = \frac{n\,c}{2L}\quad(n=1,2,3,\dots)
$$

と**全ての整数倍音**が現れます。**閉管**は閉端が節・開端が腹なので

$$
f_n = \frac{(2n-1)\,c}{4L}\quad(n=1,2,3,\dots)
$$

と**奇数倍音だけ**になります。音速は温度に依存し $c = 331.3\sqrt{T/273.15}$ m/s。

長さ $L = 0.6\,\mathrm{m}$、$T = 20\,\mathrm{°C}$（$c = 343\,\mathrm{m/s}$）で計算すると、**開管の基本周波数は $f_1 = 286\,\mathrm{Hz}$**（倍音 286, 572, 858, 1144 Hz…）。同じ長さの**閉管は $f_1 = 143\,\mathrm{Hz}$**（開管のちょうど半分＝1 オクターブ低い）で、倍音は 143, 429, 715, 1001 Hz と**奇数倍**のみ。閉管が同じ長さでより低い音を出せるのは、楽器の小型化に有利です。

![開管・閉管の定在波（左）と倍音周波数の比較（右）](/images/acoustic-resonance/charts-closeup.png)

## JavaScript 実装

```javascript
function soundSpeed(T_celsius) {
  return 331.3 * Math.sqrt((T_celsius + 273.15) / 273.15);  // m/s
}
function resonantFreqs(type, L, T, count = 8) {
  const c = soundSpeed(T);
  const freqs = [];
  for (let i = 1; i <= count; i++) {
    if (type === 'open')   freqs.push({ n: i,       f: i * c / (2 * L) });
    else /* closed */      freqs.push({ n: 2*i - 1, f: (2*i - 1) * c / (4 * L) });
  }
  return freqs;
}
// resonantFreqs('open', 0.6, 20) → f1=286Hz; resonantFreqs('closed',0.6,20) → f1=143Hz
```

温度が上がると音速が増え、全ての共鳴周波数が上昇します。だから管楽器は温まると音程（ピッチ）が上がり、演奏前のウォームアップが必要になるのです。

![開管の定在波が腹・節を保ちながら振動する様子](/images/acoustic-resonance/slider-anim.gif)

## ツールで遊ぶ

[気柱の共鳴シミュレーター](https://novasolver.jp/tools/acoustic-resonance.html)で試してほしい操作：

- **管のタイプ**（開管／閉管／ヘルムホルツ）を切り替え、共鳴周波数と倍音構成の違いを見る
- **管の長さ L スライダー**を変え、共鳴周波数が $1/L$ で変わるのを確認
- **温度 T スライダー**を上げ、音速とともに全周波数が上がるのを観察
- **倍音番号 n スライダー**で各モードの定在波（節・腹）を可視化
- **共鳴周波数リスト**で各倍音の周波数と対応する音名を読む
- 開管と閉管で同じ L でも基本周波数が 2 倍違うことを確認

## まとめ

- 開管は $f_n = nc/2L$（全倍音）、閉管は $f_n=(2n-1)c/4L$（奇数倍音）
- 同じ長さなら閉管の基本周波数は開管の半分（1 オクターブ低い）
- 音速 $c = 331.3\sqrt{T/273.15}$ で温度が上がるとピッチも上がる
- L=0.6m で開管 286Hz、閉管 143Hz

管楽器の音色の秘密を、管の種類・長さ・温度を変えながら体感してみてください。

🎵 **[気柱の共鳴シミュレーター（NovaSolver）](https://novasolver.jp/tools/acoustic-resonance.html)** で、開管と閉管の倍音の違いを確かめましょう。

---

NovaSolver では他にも [1600+ の物理・工学シミュレーター](https://novasolver.jp/) を公開しています。波動・音響では [ヘルムホルツ共鳴器](https://novasolver.jp/tools/helmholtz-resonator.html)、[うなり](https://novasolver.jp/tools/acoustic-beats.html)、[弦の共振](https://novasolver.jp/tools/string-resonance.html) もどうぞ。
