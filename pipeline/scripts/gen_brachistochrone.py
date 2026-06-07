# -*- coding: utf-8 -*-
"""Brachistochrone visuals. Tool: cycloid vs straight ramp race.
Cycloid parameter theta increases linearly with time (tautochrone property),
so the tool's cycloidAtTime is exact. Reproduced faithfully."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "brachistochrone"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; GREEN = "#9be7a3"
g = 9.81

def solve_thetaf(ratio):
    f = lambda th: (th - np.sin(th)) / (1 - np.cos(th)) - ratio
    lo, hi = 1e-3, 2 * np.pi - 1e-3
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

def setup(D, H):
    thf = solve_thetaf(D / H); a = H / (1 - np.cos(thf))
    bt = thf * np.sqrt(a / g); L = np.hypot(D, H); st = np.sqrt(2 * L * L / (g * H))
    return thf, a, bt, st

D, H = 5.0, 3.0
thf, a, bt, st = setup(D, H)
print(f"thetaF={thf:.3f} a={a:.3f} brach={bt:.3f}s straight={st:.3f}s saved={(st-bt)/st*100:.1f}%")

def cycloid_curve(thf, a, npts=200):
    th = np.linspace(0, thf, npts)
    return a * (th - np.sin(th)), -a * (1 - np.cos(th))

def cyc_pos(t, thf, a, bt):
    th = thf * min(t / bt, 1.0)
    return a * (th - np.sin(th)), -a * (1 - np.cos(th))

def ramp_pos(t, D, H, st):
    s = min(t / st, 1.0) ** 2
    return D * s, -H * s

def draw_paths(ax, beads_t=None):
    ax.set_facecolor(NAVY)
    cx, cy = cycloid_curve(thf, a)
    ax.plot(cx, cy, color=CYAN, lw=2.5, label="サイクロイド（最速）")
    ax.plot([0, D], [0, -H], color=ORANGE, lw=2, ls="--", label="直線スロープ")
    ax.plot(0, 0, "o", color="white", ms=8); ax.plot(D, -H, "*", color=GREEN, ms=14)
    if beads_t is not None:
        bx, by = cyc_pos(beads_t, thf, a, bt); rx, ry = ramp_pos(beads_t, D, H, st)
        ax.plot(bx, by, "o", color=CYAN, ms=12, mec="white")
        ax.plot(rx, ry, "o", color=ORANGE, ms=12, mec="white")
    ax.set_xlim(-0.4, D + 0.4); ax.set_ylim(-H - 0.4, 0.4)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="upper right")

# closeup: paths + descent time vs H
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.04, 0.10, 0.50, 0.82]); draw_paths(ax1)
ax1.set_title("最速降下線 = サイクロイド（直線より速い）", color="white", fontsize=10)
ax2 = fig.add_axes([0.63, 0.18, 0.34, 0.70]); ax2.set_facecolor(NAVY)
Hs = np.linspace(0.5, 12, 60); bts = []; sts = []
for h in Hs:
    tf2, a2, b2, s2 = setup(D, h); bts.append(b2); sts.append(s2)
ax2.plot(Hs, bts, color=CYAN, lw=2, label="サイクロイド")
ax2.plot(Hs, sts, color=ORANGE, lw=2, ls="--", label="直線")
ax2.scatter([H], [bt], s=60, color=CYAN, ec="white", zorder=5)
ax2.set_xlabel("垂直降下 H (m)", color="white", fontsize=9)
ax2.set_ylabel("降下時間 T (s)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)
ax2.set_title("降下時間 vs 落差", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.04, 0.06, 0.92, 0.88]); draw_paths(axc, beads_t=bt * 0.55)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ブラキストクロン", "最速降下線", "サイクロイド vs 直線のビーズ競争", cc)
os.remove(cc)

# gif: the race
frames = []
tmax = st * 1.05
for k in range(46):
    t = k / 45 * tmax
    f2 = plt.figure(figsize=(5.2, 3.4)); f2.patch.set_facecolor(NAVY)
    a2 = f2.add_axes([0.04, 0.06, 0.92, 0.86]); draw_paths(a2, beads_t=t)
    winner = "サイクロイド到着!" if t >= bt else ""
    a2.set_title(f"t = {t:.2f}s   {winner}", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=85)
print("done.")
