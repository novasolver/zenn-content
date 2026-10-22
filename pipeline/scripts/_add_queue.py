# -*- coding: utf-8 -*-
import json, os
os.chdir(r"E:\NovaSolver\zenn-content")
p = "pipeline/queue.json"; d = json.load(open(p, encoding="utf-8"))
existing = {q["id"] for q in d["queue"]}
new = [
 (36, "放物運動と射程", "projectile-motion", "projectile-motion-range-optimization", "🎯", ["javascript","物理シミュレーション","力学","可視化","数値計算"]),
 (37, "梁のたわみ", "beam-deflection", "beam-deflection-bending-stress", "🏗️", ["javascript","構造力学","CAE","数値計算","可視化"]),
 (38, "モール円と主応力", "mohr-circle", "mohr-circle-principal-stress", "⭕", ["javascript","構造力学","材料力学","可視化","数値計算"]),
 (39, "オイラー座屈", "euler-buckling", "euler-buckling-critical-load", "📏", ["javascript","構造力学","CAE","数値計算","可視化"]),
 (40, "レイノルズ数と流れ", "reynolds-number", "reynolds-number-laminar-turbulent", "🌊", ["javascript","流体力学","レイノルズ数","可視化","数値計算"]),
 (41, "スネルの法則と全反射", "snells-law", "snells-law-refraction-tir", "🔦", ["javascript","光学","物理シミュレーション","可視化","数値計算"]),
 (42, "回折格子", "diffraction-grating", "diffraction-grating-spectrum", "🌈", ["javascript","光学","波動","可視化","数値計算"]),
 (43, "黒体放射", "blackbody-radiation", "blackbody-radiation-planck-wien", "🔥", ["javascript","物理シミュレーション","熱力学","量子","可視化"]),
 (44, "カルノーサイクル", "carnot-cycle", "carnot-cycle-efficiency", "♻️", ["javascript","熱力学","CAE","可視化","数値計算"]),
 (45, "RLC共振回路", "rlc-resonance", "rlc-resonance-q-factor", "📻", ["javascript","電気回路","信号処理","可視化","数値計算"]),
 (46, "歯車比", "gear-ratio", "gear-ratio-train", "⚙️", ["javascript","機械工学","可視化","数値計算","力学"]),
 (47, "1次元衝突", "collision-1d", "collision-1d-elastic-inelastic", "🎱", ["javascript","物理シミュレーション","力学","可視化","数値計算"]),
]
added = 0
for i, (id_, topic, slug, aslug, emoji, topics) in enumerate(new):
    if id_ in existing: continue
    d["queue"].append({"id": id_, "priority": 100 + i, "topic_ja": topic,
        "tool_slug": slug, "article_slug": aslug, "emoji": emoji,
        "topics": topics, "gif_hint": "", "status": "todo"})
    added += 1
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"added {added}; total queue {len(d['queue'])}")
