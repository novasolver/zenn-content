# -*- coding: utf-8 -*-
"""Boids visuals. Faithful to the tool's exact rules (separation/alignment/
cohesion, O(n^2), torus wrap, maxForce=0.3). Vectorised with numpy.
Produces cover / charts-closeup / slider-anim.gif."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "boids-flocking"
NAVY = "#0b1020"; ORANGE = "#f59e0b"; CYAN = "#7dd3fc"
W, H = 600.0, 520.0

def init(n, maxSpeed, seed=7):
    rng = np.random.RandomState(seed)
    ang = rng.rand(n) * 2 * np.pi
    spd = (rng.rand(n) * 0.5 + 0.5) * maxSpeed
    x = rng.rand(n) * W; y = rng.rand(n) * H
    vx = np.cos(ang) * spd; vy = np.sin(ang) * spd
    return x, y, vx, vy

def step(x, y, vx, vy, maxSpeed, visualRange, sw, aw, cw):
    n = len(x)
    sepRange = visualRange * 0.4
    r2 = visualRange ** 2; sr2 = sepRange ** 2; maxForce = 0.3
    dx = x[None, :] - x[:, None]; dy = y[None, :] - y[:, None]
    d2 = dx * dx + dy * dy
    eye = np.eye(n, dtype=bool)
    inRange = (d2 <= r2) & (~eye)
    inSep = (d2 < sr2) & (d2 > 0)
    nc = inRange.sum(1)
    safe = np.where(nc > 0, nc, 1)
    # separation: sx -= dx/d*(sepRange/d) = dx*sepRange/d2
    d2s = np.where(inSep, d2, np.inf)
    sx = -(np.where(inSep, dx, 0) * sepRange / d2s).sum(1)
    sy = -(np.where(inSep, dy, 0) * sepRange / d2s).sum(1)
    avgVx = (np.where(inRange, vx[None, :], 0)).sum(1) / safe
    avgVy = (np.where(inRange, vy[None, :], 0)).sum(1) / safe
    comX = (np.where(inRange, x[None, :], 0)).sum(1) / safe
    comY = (np.where(inRange, y[None, :], 0)).sum(1) / safe
    has = nc > 0
    fx = np.where(has, sx * sw + (avgVx - vx) * aw * 0.1 + (comX - x) * cw * 0.002, 0.0)
    fy = np.where(has, sy * sw + (avgVy - vy) * aw * 0.1 + (comY - y) * cw * 0.002, 0.0)
    fm = np.hypot(fx, fy); over = fm > maxForce; fms = np.where(fm > 0, fm, 1.0)
    fx = np.where(over, fx / fms * maxForce, fx); fy = np.where(over, fy / fms * maxForce, fy)
    vx = vx + fx; vy = vy + fy
    s = np.hypot(vx, vy); fast = s > maxSpeed
    vx = np.where(fast, vx / s * maxSpeed, vx); vy = np.where(fast, vy / s * maxSpeed, vy)
    slow = s < 0.3; vx = np.where(slow, vx * 1.05, vx); vy = np.where(slow, vy * 1.05, vy)
    x = (x + vx) % W; y = (y + vy) % H
    return x, y, vx, vy

def order_param(vx, vy):
    return np.hypot(vx.sum(), vy.sum()) / np.hypot(vx, vy).sum()

def clusters(x, y, visualRange):
    n = len(x); r2 = visualRange ** 2
    visited = np.zeros(n, bool); c = 0
    for i in range(n):
        if visited[i]: continue
        c += 1; st = [i]; visited[i] = True
        while st:
            cur = st.pop()
            d2 = (x - x[cur])**2 + (y - y[cur])**2
            nb = (d2 < r2) & (~visited)
            for j in np.where(nb)[0]:
                visited[j] = True; st.append(j)
    return c

PRESETS = {
    "💥 混沌":   (150, 5.0, 30, 0.3, 0.2, 0.1),
    "default":   (100, 2.5, 60, 1.5, 1.0, 1.0),
    "🐦 鳥群":   (80, 3.5, 80, 1.2, 1.5, 1.0),
    "🎯 密集":   (60, 1.5, 100, 0.8, 2.0, 2.5),
}

def run(n, ms, vr, sw, aw, cw, steps, seed=7):
    x, y, vx, vy = init(n, ms, seed)
    for _ in range(steps):
        x, y, vx, vy = step(x, y, vx, vy, ms, vr, sw, aw, cw)
    return x, y, vx, vy

def draw_flock(ax, x, y, vx, vy, ms, title=None):
    ax.set_facecolor(NAVY)
    ang = np.arctan2(vy, vx); spd = np.hypot(vx, vy)
    t = np.clip(spd / ms, 0, 1)
    sz = 90
    for i in range(len(x)):
        a = ang[i]
        # triangle (arrowhead) oriented along velocity
        pts = np.array([[1.0, 0], [-0.5, 0.5], [-0.5, -0.5]]) * np.sqrt(sz)
        R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
        p = pts @ R.T
        col = (0, 0.55 + 0.3 * t[i], 0.85 - 0.25 * t[i])
        ax.fill(x[i] + p[:, 0], y[i] + p[:, 1], color=col, lw=0)
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")
    if title:
        ax.set_title(title, color="white", fontsize=11)

# ---- measure order parameter + clusters for the 4 presets ----
print("preset       n   phi    clusters")
results = {}
for name, (n, ms, vr, sw, aw, cw) in PRESETS.items():
    x, y, vx, vy = run(n, ms, vr, sw, aw, cw, steps=600)
    phi = order_param(vx, vy); cl = clusters(x, y, vr)
    results[name] = (phi, cl)
    print(f"  preset n={n:4d}  phi={phi:.3f}  clusters={cl}")

# ---- closeup: flock snapshot (bird) + order-parameter bars ----
xb, yb, vxb, vyb = run(*PRESETS["🐦 鳥群"], steps=600)
fig = plt.figure(figsize=(9.4, 4.4)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.01, 0.06, 0.50, 0.88])
draw_flock(ax1, xb, yb, vxb, vyb, 3.5, "「鳥の群れ」整列が強いと向きが揃う")
ax2 = fig.add_axes([0.60, 0.16, 0.38, 0.72]); ax2.set_facecolor(NAVY)
names = ["💥 混沌", "default", "🐦 鳥群", "🎯 密集"]
phis = [results[k][0] for k in names]
bars = ax2.bar(range(4), phis, color=[ORANGE, "#7c9fd6", CYAN, "#9be7a3"])
ax2.set_xticks(range(4)); ax2.set_xticklabels(["混沌", "標準", "鳥群", "密集"], color="white", fontsize=9)
ax2.set_ylim(0, 1.0); ax2.set_ylabel("整列度 φ = |Σv| / Σ|v|", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
for b, p in zip(bars, phis):
    ax2.text(b.get_x() + b.get_width() / 2, p + 0.02, f"{p:.2f}", ha="center", color="white", fontsize=9)
ax2.set_title("秩序の度合いは重みで決まる", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.0, 3.4)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.0, 0.0, 1.0, 1.0]); draw_flock(axc, xb, yb, vxb, vyb, 3.5)
cover_chart = os.path.join(figlib.outdir(SLUG), "_coverchart.png")
figlib.save_fig(figc, cover_chart, dpi=120)
figlib.make_cover(SLUG, "Boids 群れの創発", "",
                  "分離・整列・結合の3ルールから秩序が立ち上がる", cover_chart)
os.remove(cover_chart)

# ---- gif: emergence over time (bird preset, random -> ordered) ----
n, ms, vr, sw, aw, cw = PRESETS["🐦 鳥群"]
x, y, vx, vy = init(n, ms, seed=7)
frames = []; capture_every = 6; total = 360
for s in range(total):
    x, y, vx, vy = step(x, y, vx, vy, ms, vr, sw, aw, cw)
    if s % capture_every == 0:
        f2 = plt.figure(figsize=(4.8, 4.2)); f2.patch.set_facecolor(NAVY)
        a2 = f2.add_axes([0.0, 0.0, 1.0, 1.0])
        draw_flock(a2, x, y, vx, vy, ms)
        a2.text(12, H - 22, f"t={s:3d}  φ={order_param(vx,vy):.2f}", color=CYAN, fontsize=11)
        frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=80)
print("done.")
