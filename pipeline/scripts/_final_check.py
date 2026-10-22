# -*- coding: utf-8 -*-
import json, os, subprocess, sys
os.chdir(r"E:\NovaSolver\zenn-content")
SESSION = [
 ("newtons-cradle","newtons-cradle-momentum-energy"),("boids-flocking","boids-flocking-emergence"),
 ("karman-vortex","karman-vortex-street-shedding"),("pipe-flow","pipe-flow-reynolds-transition"),
 ("doppler-effect","doppler-effect-frequency-shift"),("string-resonance","string-resonance-standing-waves"),
 ("wave-interference","wave-interference-double-slit"),("heat-diffusion","heat-diffusion-fourier-law"),
 ("game-of-life","game-of-life-cellular-automata"),("random-walk-2d","random-walk-2d-brownian-motion"),
 ("brachistochrone","brachistochrone-fastest-descent"),("lens-ray-tracer","lens-ray-tracer-optics"),
 ("parsevals-theorem","parsevals-theorem-energy"),("goertzel-algorithm","goertzel-algorithm-dtmf"),
 ("cepstrum","cepstrum-pitch-detection"),("fourier-series","fourier-series-gibbs-phenomenon"),
 ("convection-cells","convection-cells-rayleigh-benard"),("spring-pendulum","spring-pendulum-parametric-resonance"),
 ("projectile-motion","projectile-motion-range-optimization"),("beam-deflection","beam-deflection-bending-stress"),
 ("mohr-circle","mohr-circle-principal-stress"),("euler-buckling","euler-buckling-critical-load"),
 ("reynolds-number","reynolds-number-laminar-turbulent"),("snells-law","snells-law-refraction-tir"),
 ("diffraction-grating","diffraction-grating-spectrum"),("blackbody-radiation","blackbody-radiation-planck-wien"),
 ("carnot-cycle","carnot-cycle-efficiency"),("rlc-resonance","rlc-resonance-q-factor"),
 ("gear-ratio","gear-ratio-train"),("collision-1d","collision-1d-elastic-inelastic"),
]
fails = 0
for tool, art in SESSION:
    r = subprocess.run([sys.executable, "pipeline/scripts/qa_check.py", tool, art],
                       capture_output=True, text=True)
    if r.returncode != 0:
        fails += 1; print("FAIL", art); print(r.stdout)
print(f"\nQA: {len(SESSION)-fails}/{len(SESSION)} PASS")
d = json.load(open("pipeline/queue.json", encoding="utf-8"))
drafts = sum(1 for q in d["queue"] if q["status"] == "draft")
todos = sum(1 for q in d["queue"] if q["status"] == "todo")
print(f"queue: {drafts} draft, {todos} todo, {len(d['queue'])} total")
import glob
arts = [a for a in glob.glob("articles/*.md")]
print(f"total article .md files: {len(arts)}")
