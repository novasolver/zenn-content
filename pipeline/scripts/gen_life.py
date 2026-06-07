# -*- coding: utf-8 -*-
"""Conway's Game of Life visuals. B3/S23, toroidal — matches the tool.
Uses the tool's exact Gosper gun / pulsar preset coordinates."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
from scipy.signal import convolve2d
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "game-of-life"
NAVY = "#0a0a1a"; ALIVE = "#00ff88"
K = np.ones((3, 3)); K[1, 1] = 0

def step(g):
    n = convolve2d(g, K, mode="same", boundary="wrap")
    return (((g == 1) & ((n == 2) | (n == 3))) | ((g == 0) & (n == 3))).astype(np.uint8)

GUN = [[0,4],[0,5],[1,4],[1,5],[10,4],[10,5],[10,6],[11,3],[11,7],[12,2],[12,8],[13,2],[13,8],
       [14,5],[15,3],[15,7],[16,4],[16,5],[16,6],[17,5],[20,2],[20,3],[20,4],[21,2],[21,3],[21,4],
       [22,1],[22,5],[24,0],[24,1],[24,5],[24,6],[34,2],[34,3],[35,2],[35,3]]
PULSAR = [[2,0],[3,0],[4,0],[8,0],[9,0],[10,0],[0,2],[5,2],[7,2],[12,2],[0,3],[5,3],[7,3],[12,3],
          [0,4],[5,4],[7,4],[12,4],[2,5],[3,5],[4,5],[8,5],[9,5],[10,5],[2,7],[3,7],[4,7],[8,7],
          [9,7],[10,7],[0,8],[5,8],[7,8],[12,8],[0,9],[5,9],[7,9],[12,9],[0,10],[5,10],[7,10],
          [12,10],[2,12],[3,12],[4,12],[8,12],[9,12],[10,12]]

def place(rows, cols, coords, ox, oy):
    g = np.zeros((rows, cols), np.uint8)
    for x, y in coords:
        g[(oy + y) % rows, (ox + x) % cols] = 1
    return g

def draw_grid(ax, g, title=None):
    ax.set_facecolor(NAVY)
    ax.imshow(g, cmap=plt.matplotlib.colors.ListedColormap([NAVY, ALIVE]),
              origin="upper", interpolation="nearest", vmin=0, vmax=1)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#2a2a44")
    if title: ax.set_title(title, color="white", fontsize=10)

# ---- population history of a random soup (30% density) -> "ash" ----
rng = np.random.RandomState(7)
soup = (rng.rand(80, 80) < 0.30).astype(np.uint8)
pops = []; g = soup.copy()
for _ in range(200):
    pops.append(g.sum()); g = step(g)
ash_density = pops[-1] / (80 * 80)
print(f"random soup 30%: start pop={pops[0]}, end pop={pops[-1]}, ash density={ash_density:.4f}")

# pulsar centered
gp = place(17, 17, PULSAR, 2, 2)

# ---- closeup: pulsar + population history ----
fig = plt.figure(figsize=(9.2, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.04, 0.06, 0.40, 0.86]); draw_grid(ax1, gp, "パルサー（周期3の振動子）")
ax2 = fig.add_axes([0.56, 0.16, 0.40, 0.72]); ax2.set_facecolor(NAVY)
ax2.plot(np.arange(len(pops)), pops, color=ALIVE, lw=1.8)
ax2.axhline(pops[-1], color="#f59e0b", lw=1, ls="--")
ax2.set_xlabel("世代", color="white", fontsize=9)
ax2.set_ylabel("生存セル数", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#2a2a44")
ax2.set_title(f"ランダム初期（30%）→ 安定（密度≈{ash_density:.3f}）", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover: glider gun mid-run ----
gg = place(46, 64, GUN, 1, 1)
for _ in range(90): gg = step(gg)
figc = plt.figure(figsize=(5.4, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.0, 0.0, 1.0, 1.0]); draw_grid(axc, gg)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ライフゲーム", "", "B3/S23 — グライダー銃と創発する生命", cc)
os.remove(cc)

# ---- gif: Gosper glider gun emitting gliders ----
g = place(46, 64, GUN, 1, 1)
frames = []
for s in range(180):
    if s % 3 == 0:
        f2 = plt.figure(figsize=(5.2, 3.7)); f2.patch.set_facecolor(NAVY)
        a2 = f2.add_axes([0.0, 0.0, 1.0, 0.93]); draw_grid(a2, g)
        a2.set_title(f"グライダー銃  世代 {s}", color="white", fontsize=10)
        frames.append(figlib.fig_to_pil(f2, dpi=90))
    g = step(g)
figlib.save_gif(frames, SLUG, duration=85)
print("done.")
