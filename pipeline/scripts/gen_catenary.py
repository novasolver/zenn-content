# -*- coding: utf-8 -*-
"""Catenary cable visuals. y=a*cosh(x/a)-a; H=wa; Tmax=H+wd; S=2a*sinh(L/2a).
Solved by bisection (overflow-safe). Compares catenary vs parabola."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "catenary-cable"
NAVY = "#0a1628"
BLUE, CYAN, RED, ORANGE, GREEN = "#007BFF", "#00B4D8", "#e74c3c", "#f39c12", "#2ecc71"

def solve_a(L, d):
    def f(a):
        try: return a*(math.cosh(L/(2*a))-1) - d
        except OverflowError: return float('inf')
    lo, hi = 1e-2, L*1e4
    for _ in range(300):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo+hi)/2

def catenary(L, d, w):
    a = solve_a(L, d)
    H = w*a; Tmax = H + w*d; S = 2*a*math.sinh(L/(2*a))
    return a, H, Tmax, S

def cat_y(x, a):  # x measured from center, sag downward positive
    return a*(math.cosh(x/a)-1)

def cat_curve(L, d, n=200):
    a = solve_a(L, d)
    xs = np.linspace(-L/2, L/2, n)
    ys = np.array([cat_y(x, a) for x in xs])
    return xs, ys, a

def par_curve(L, d, n=200):
    xs = np.linspace(-L/2, L/2, n)
    t = (xs + L/2)/L
    ys = d*(1 - 4*t*(1-t))   # 0 at supports, d at center (sag downward)
    return xs, ys

def draw_cable(ax, L, d, w, mode="catenary", title=None, legend=True):
    ax.set_facecolor(NAVY)
    a, H, Tmax, S = catenary(L, d, w)
    xc, yc, _ = cat_curve(L, d)
    xp, yp = par_curve(L, d)
    # plot (flip y so sag hangs down)
    ax.plot(xc, -yc, color=CYAN, lw=2.6, label="カテナリー (cosh)")
    if mode == "compare":
        ax.plot(xp, -yp, color=ORANGE, lw=2.0, ls="--", label="放物線近似")
    # supports
    ax.plot([-L/2, L/2], [0, 0], "o", color=GREEN, ms=9, zorder=5)
    # sag marker
    ax.plot([0, 0], [0, -d], color=ORANGE, lw=1, ls=":")
    ax.plot(0, -d, "o", color=ORANGE, ms=7, zorder=5)
    ax.annotate(f"d={d:.0f}m", (0, -d/2), color=ORANGE, fontsize=9, ha="left",
                xytext=(6, 0), textcoords="offset points")
    ax.set_xlabel("水平位置 x (m)", color="white", fontsize=9)
    ax.set_ylabel("たわみ y (m)", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if legend:
        ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="upper center")
    if title: ax.set_title(title, color="white", fontsize=10)
    return H, Tmax, S

# Default case
L, d, w = 100.0, 10.0, 50.0
a, H, Tmax, S = catenary(L, d, w)
print(f"default L={L} d={d} w={w}: a={a:.2f} H={H/1000:.3f}kN Tmax={Tmax/1000:.3f}kN S={S:.2f}m")

# ---- closeup: cable shape (compare) + tension distribution ----
fig = plt.figure(figsize=(9.6, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07, 0.15, 0.52, 0.74])
draw_cable(ax1, L, d, w, mode="compare", title="ケーブル形状：カテナリー vs 放物線 (d/L=10%)")
# tension distribution along span (catenary): T(x)=sqrt(H^2 + (w a sinh(x/a))^2)
ax2 = fig.add_axes([0.69, 0.16, 0.28, 0.72]); ax2.set_facecolor(NAVY)
xs = np.linspace(-L/2, L/2, 120)
Tx = np.array([math.sqrt(H**2 + (w*a*math.sinh(x/a))**2) for x in xs])/1000
ax2.plot(xs, Tx, color=BLUE, lw=2.4)
ax2.fill_between(xs, Tx, color=BLUE, alpha=0.12)
ax2.axhline(H/1000, color=GREEN, lw=1.2, ls=":", label=f"H={H/1000:.2f}kN")
ax2.plot([-L/2, L/2], [Tmax/1000]*2, "o", color=RED, ms=6)
ax2.annotate(f"Tmax={Tmax/1000:.2f}kN", (0, Tmax/1000), color=RED, fontsize=8, ha="center",
             xytext=(0, 6), textcoords="offset points")
ax2.set_xlabel("x (m)", color="white", fontsize=9)
ax2.set_ylabel("張力 T (kN)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="lower center")
ax2.set_title("張力分布（支点で最大）", color="white", fontsize=9)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.12, 0.14, 0.84, 0.8])
draw_cable(axc, L, d, w, mode="compare", legend=False)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "カテナリー曲線", "ケーブル張力", "y = a·cosh(x/a) と放物線近似 / H・Tmax・S", cc)
os.remove(cc)

# ---- gif: sweep sag d, show H rising as cable tightens ----
frames = []
ds = list(np.linspace(4, 30, 9)) + list(np.linspace(30, 4, 9))
for dv in ds:
    a2, H2, Tmax2, S2 = catenary(L, dv, w)
    f2 = plt.figure(figsize=(5.3, 3.4)); f2.patch.set_facecolor(NAVY)
    axg = f2.add_axes([0.13, 0.17, 0.83, 0.74])
    draw_cable(axg, L, dv, w, mode="compare", legend=False)
    axg.set_ylim(-32, 4)
    axg.set_title(f"d={dv:.0f}m (d/L={dv/L*100:.0f}%) → H={H2/1000:.1f}kN, Tmax={Tmax2/1000:.1f}kN",
                  color="white", fontsize=9.5)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=130)
print("done.")
