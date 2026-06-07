# -*- coding: utf-8 -*-
"""Extend queue with 40 NEW real tools (ids 48-87). Verifies tool HTML exists."""
import json, os
os.chdir(r"E:\NovaSolver\zenn-content")
TOOLS = r"E:\NovaSolver\cae-archive\tools"
p = "pipeline/queue.json"
d = json.load(open(p, encoding="utf-8"))
existing_ids = {q["id"] for q in d["queue"]}
existing_slugs = {q["article_slug"] for q in d["queue"]}
done_articles = {f[:-3] for f in os.listdir("articles") if f.endswith(".md")}

# (topic_ja, tool_slug, article_slug, emoji, topics)
new = [
 ("単振り子と単振動", "simple-pendulum", "simple-pendulum-shm-period", "🟤", ["javascript","物理シミュレーション","力学","可視化","数値計算"]),
 ("軌道力学とvis-viva方程式", "orbital-mechanics", "orbital-mechanics-vis-viva", "🛰️", ["javascript","物理シミュレーション","天体力学","数値計算","可視化"]),
 ("ホーマン遷移軌道", "hohmann-transfer", "hohmann-transfer-orbit-delta-v", "🚀", ["javascript","物理シミュレーション","天体力学","数値計算","可視化"]),
 ("脱出速度と重力井戸", "escape-velocity", "escape-velocity-gravity-well", "🌍", ["javascript","物理シミュレーション","天体力学","力学","可視化"]),
 ("コリオリの力と回転系", "coriolis-effect", "coriolis-effect-rotating-frame", "🌀", ["javascript","物理シミュレーション","力学","可視化","数値計算"]),
 ("フーコーの振り子と地球自転", "foucault-pendulum", "foucault-pendulum-earth-rotation", "🌍", ["javascript","物理シミュレーション","力学","可視化","数値計算"]),
 ("ジャイロスコープの歳差運動", "gyroscope", "gyroscope-precession-nutation", "🎡", ["javascript","物理シミュレーション","力学","可視化","数値計算"]),
 ("遠心調速機（ガバナー）", "centrifugal-governor", "centrifugal-governor-control", "🎛️", ["javascript","制御工学","力学","可視化","数値計算"]),
 ("オットーサイクル（ガソリン機関）", "otto-cycle", "otto-cycle-engine-efficiency", "🚗", ["javascript","熱力学","CAE","可視化","数値計算"]),
 ("ランキンサイクル（蒸気動力）", "rankine-cycle", "rankine-cycle-steam-power", "♨️", ["javascript","熱力学","CAE","可視化","数値計算"]),
 ("ブレイトンサイクル（ガスタービン）", "brayton-cycle", "brayton-cycle-gas-turbine", "✈️", ["javascript","熱力学","CAE","可視化","数値計算"]),
 ("ディーゼルサイクル", "diesel-cycle", "diesel-cycle-compression-ignition", "🚛", ["javascript","熱力学","CAE","可視化","数値計算"]),
 ("混合エントロピー", "entropy-mixing", "entropy-of-mixing-gibbs", "⚗️", ["javascript","熱力学","統計力学","可視化","数値計算"]),
 ("ファンデルワールス実在気体", "van-der-waals-gas", "van-der-waals-real-gas", "💨", ["javascript","熱力学","物理シミュレーション","可視化","数値計算"]),
 ("マクスウェル・ボルツマン速度分布", "maxwell-boltzmann", "maxwell-boltzmann-speed-distribution", "🌡️", ["javascript","熱力学","統計力学","可視化","数値計算"]),
 ("シュテファン・ボルツマンの法則", "stefan-boltzmann", "stefan-boltzmann-radiation-law", "🔆", ["javascript","物理シミュレーション","熱力学","可視化","数値計算"]),
 ("フィン（放熱板）の熱伝達", "fin-heat-transfer", "fin-heat-transfer-efficiency", "🌡️", ["javascript","熱力学","CAE","数値計算","可視化"]),
 ("うなり（音のビート）", "acoustic-beats", "acoustic-beats-frequency", "🔊", ["javascript","物理シミュレーション","波動","音響","可視化"]),
 ("気柱の共鳴", "acoustic-resonance", "acoustic-resonance-pipe-modes", "🎵", ["javascript","物理シミュレーション","波動","音響","可視化"]),
 ("ヘルムホルツ共鳴器", "helmholtz-resonator", "helmholtz-resonator-frequency", "🍶", ["javascript","物理シミュレーション","波動","音響","可視化"]),
 ("正規分布（ガウス分布）", "normal-distribution", "normal-distribution-gaussian", "📊", ["javascript","統計","確率","数学","可視化"]),
 ("二項分布", "binomial-distribution", "binomial-distribution-probability", "🎲", ["javascript","統計","確率","数学","可視化"]),
 ("マルコフ連鎖と定常分布", "markov-chain", "markov-chain-stationary", "🔗", ["javascript","確率","アルゴリズム","数学","可視化"]),
 ("ビュフォンの針と円周率", "buffon-needle", "buffon-needle-pi-estimation", "📐", ["javascript","確率","モンテカルロ","数学","可視化"]),
 ("勾配降下法", "gradient-descent", "gradient-descent-optimization", "📉", ["javascript","機械学習","最適化","アルゴリズム","可視化"]),
 ("ニュートン・ラフソン法", "newton-raphson", "newton-raphson-root-finding", "➗", ["javascript","数値計算","アルゴリズム","数学","可視化"]),
 ("二分法による求根", "bisection-method", "bisection-method-root-finding", "🔍", ["javascript","数値計算","アルゴリズム","数学","可視化"]),
 ("ルンゲ・クッタ法（ODE解法）", "runge-kutta", "runge-kutta-ode-solver", "🧮", ["javascript","数値計算","アルゴリズム","数学","可視化"]),
 ("数値積分（台形・シンプソン）", "numerical-integration", "numerical-integration-trapezoid-simpson", "➕", ["javascript","数値計算","アルゴリズム","数学","可視化"]),
 ("テイラー級数による近似", "taylor-series", "taylor-series-approximation", "📈", ["javascript","数学","数値計算","可視化","アルゴリズム"]),
 ("カルマンフィルタ", "kalman-filter", "kalman-filter-state-estimation", "🛰️", ["javascript","信号処理","制御工学","アルゴリズム","可視化"]),
 ("パーセプトロン（線形分類器）", "perceptron", "perceptron-linear-classifier", "🧠", ["javascript","機械学習","アルゴリズム","可視化","数学"]),
 ("ニューラルネットと誤差逆伝播", "neural-network", "neural-network-backpropagation", "🧠", ["javascript","機械学習","ニューラルネットワーク","可視化","アルゴリズム"]),
 ("自己相関と周期性検出", "autocorrelation", "autocorrelation-signal-periodicity", "📡", ["javascript","信号処理","DSP","統計","可視化"]),
 ("ハイパスフィルタ", "high-pass-filter", "high-pass-filter-cutoff-phase", "🎚️", ["javascript","電気回路","信号処理","可視化","数値計算"]),
 ("根軌跡法と安定性", "root-locus", "root-locus-control-stability", "📐", ["javascript","制御工学","信号処理","可視化","数値計算"]),
 ("Z変換と極零配置", "z-transform", "z-transform-pole-zero", "🔢", ["javascript","信号処理","DSP","数学","可視化"]),
 ("ラプラス変換とs平面", "laplace-transform", "laplace-transform-s-plane", "🔣", ["javascript","信号処理","制御工学","数学","可視化"]),
 ("標本化定理とエイリアシング", "nyquist-sampling", "nyquist-sampling-aliasing", "📶", ["javascript","信号処理","DSP","可視化","数値計算"]),
 ("量子トンネル効果", "quantum-tunneling", "quantum-tunneling-barrier", "⚛️", ["javascript","量子力学","物理シミュレーション","可視化","数値計算"]),
]

nid = 48
added = 0; skipped = []
for topic, slug, aslug, emoji, topics in new:
    if not os.path.exists(os.path.join(TOOLS, slug + ".html")):
        skipped.append((slug, "tool html missing")); continue
    if aslug in existing_slugs or aslug in done_articles:
        skipped.append((slug, "article_slug collision")); continue
    while nid in existing_ids:
        nid += 1
    d["queue"].append({"id": nid, "priority": 200 + added, "topic_ja": topic,
        "tool_slug": slug, "article_slug": aslug, "emoji": emoji,
        "topics": topics, "gif_hint": "", "status": "todo"})
    existing_ids.add(nid); existing_slugs.add(aslug); added += 1; nid += 1

json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("added", added, "total", len(d["queue"]))
for s, why in skipped:
    print("SKIP", s, why)
