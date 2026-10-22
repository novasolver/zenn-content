# -*- coding: utf-8 -*-
"""Bezier curve visuals. Faithful to the tool: fixed endpoints P0=(0,0), P3=(100,0),
explicit Bernstein form + De Casteljau construction, curvature with guarded denom.
Charts: curve+polygon+De Casteljau lines, curvature vs t."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "bezier-curve"
NAVY = "#0b1020"
CYAN, ORANGE, GREEN, PURPLE, YELLOW = "#00B4D8", "#f59e0b", "#9be7a3", "#c084fc", "#ffd24b"

P0 = np.array([0.0, 0.0]); P3 = np.array([100.0, 0.0])
P1 = np.array([20.0, 80.0]); P2 = np.array([80.0, 80.0])

def bez(t):
    u = 1-t
    return u**3*P0 + 3*u*u*t*P1 + 3*u*t*t*P2 + t**3*P3
def d1(t):
    u = 1-t
    return 3*u*u*(P1-P0) + 6*u*t*(P2-P1) + 3*t*t*(P3-P2)
def d2(t):
    u = 1-t
    return 6*u*(P2-2*P1+P0) + 6*t*(P3-2*P2+P1)
def curv(t):
    a = d1(t); b = d2(t)
    cross = a[0]*b[1] - a[1]*b[0]
    sp2 = a[0]**2 + a[1]**2
    return abs(cross)/max(sp2, 1e-9)**1.5

def lerp(a, b, t): return a + (b-a)*t

def draw_curve(ax, t_mark=0.5, title=None, show_decast=True):
    ax.set_facecolor(NAVY)
    ctrl = [P0, P1, P2, P3]
    # control polygon
    cp = np.array(ctrl)
    ax.plot(cp[:,0], cp[:,1], "--", color="white", alpha=0.35, lw=1.2)
    # curve
    ts = np.linspace(0, 1, 200)
    pts = np.array([bez(t) for t in ts])
    ax.plot(pts[:,0], pts[:,1], color=CYAN, lw=3.0, solid_capstyle="round")
    # De Casteljau construction at t_mark
    if show_decast:
        layer = [np.array(p, float) for p in ctrl]
        palette = [PURPLE, ORANGE, GREEN]
        depth = 0
        while len(layer) > 1:
            nxt = []
            xs = [p[0] for p in layer]; ys = [p[1] for p in layer]
            ax.plot(xs, ys, color=palette[min(depth, 2)], lw=1.3, alpha=0.8)
            for i in range(len(layer)-1):
                nxt.append(lerp(layer[i], layer[i+1], t_mark))
            for p in nxt:
                ax.plot(p[0], p[1], "o", color=palette[min(depth, 2)], ms=4)
            layer = nxt; depth += 1
        Bt = layer[0]
        ax.plot(Bt[0], Bt[1], "o", color="white", ms=9, zorder=6,
                markeredgecolor=YELLOW, markeredgewidth=2)
    # control points
    for i, p in enumerate(ctrl):
        col = GREEN if i in (0, 3) else ORANGE
        ax.plot(p[0], p[1], "o", color=col, ms=7, zorder=5)
        ax.annotate(f"P{i}", (p[0], p[1]), textcoords="offset points",
                    xytext=(6, 6), color="white", fontsize=9)
    ax.set_xlim(-8, 108); ax.set_ylim(-12, 95)
    ax.set_aspect("equal")
    ax.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if title: ax.set_title(title, color="white", fontsize=10)

def draw_curvature(ax, t_mark=0.5, title=None):
    ax.set_facecolor(NAVY)
    ts = np.linspace(0, 1, 200)
    ks = [curv(t) for t in ts]
    ax.plot(ts, ks, color=PURPLE, lw=2.2)
    ax.fill_between(ts, ks, 0, color=PURPLE, alpha=0.15)
    ax.axvline(t_mark, color=YELLOW, ls="--", lw=1.3)
    ax.plot(t_mark, curv(t_mark), "o", color=YELLOW, ms=6)
    ax.set_xlabel("パラメータ t", color="white", fontsize=9)
    ax.set_ylabel("曲率 κ", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    ax.grid(True, color="#26324d", lw=0.5)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if title: ax.set_title(title, color="white", fontsize=10)

# console verification
print("B(0.5)=", tuple(round(v, 2) for v in bez(0.5)))
print("tangent deg @0.5=", round(math.degrees(math.atan2(*d1(0.5)[::-1])), 1))
print("curvature @0.5=", round(curv(0.5), 5))
arc = sum(np.hypot(*(bez((i+1)/200)-bez(i/200))) for i in range(200))
print("arc length=", round(arc, 2))

# ---- closeup: curve + curvature ----
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.06, 0.10, 0.52, 0.82]); draw_curve(ax1, 0.5, "ベジェ曲線と De Casteljau 構成 (t=0.5)")
ax2 = fig.add_axes([0.67, 0.16, 0.30, 0.70]); draw_curvature(ax2, 0.5, "曲率 κ vs t")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.06, 0.06, 0.90, 0.88]); draw_curve(axc, 0.5)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ベジェ曲線", "De Casteljau 法", "制御点が形をつくる計算幾何", cc)
os.remove(cc)

# ---- gif: sweep t along the curve ----
frames = []
sweep = list(np.linspace(0.02, 0.98, 14)) + list(np.linspace(0.98, 0.02, 14))
for tv in sweep:
    f2 = plt.figure(figsize=(5.2, 3.5)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.05, 0.06, 0.92, 0.84]); draw_curve(a, tv)
    Bt = bez(tv)
    a.set_title(f"t={tv:.2f}  B(t)=({Bt[0]:.0f}, {Bt[1]:.0f})", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=88))
figlib.save_gif(frames, SLUG, duration=120)
print("done.")
