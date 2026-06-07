# -*- coding: utf-8 -*-
"""2D heat diffusion visuals. Reproduces the tool's FTCS scheme exactly
(N=100, dt=0.02, dx=1, a=alpha*dt/dx^2), central hot source, Dirichlet 0 edges."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "heat-diffusion"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"
N = 100; dt = 0.02; dx = 1.0
ALPHA = 11.6   # copper (relative), a = 0.232 (stable, < 0.25)

def make_field():
    T = np.full((N, N), 25.0)
    src = np.zeros((N, N), bool)
    src[47:54, 47:54] = True       # presetCenter: 7x7 hot block
    T[src] = 100.0
    return T, src

def step(T, src, a, bc="dirichlet"):
    T2 = T.copy()
    lap = (T[2:, 1:-1] + T[:-2, 1:-1] + T[1:-1, 2:] + T[1:-1, :-2] - 4 * T[1:-1, 1:-1])
    T2[1:-1, 1:-1] = T[1:-1, 1:-1] + a * lap
    if bc == "dirichlet":
        T2[0, :] = T2[-1, :] = T2[:, 0] = T2[:, -1] = 0.0
    else:  # neumann
        T2[0, :] = T2[1, :]; T2[-1, :] = T2[-2, :]; T2[:, 0] = T2[:, 1]; T2[:, -1] = T2[:, -2]
    T2[src] = 100.0
    return T2

a = ALPHA * dt / dx / dx
print(f"alpha={ALPHA} a={a:.3f} ({'stable' if a<=0.25 else 'UNSTABLE'})")

# run, snapshotting
T, src = make_field()
snaps = {}
profiles = {}
mid = N // 2
record_at = [0, 60, 200, 600]
for s in range(601):
    if s in record_at:
        snaps[s] = T.copy(); profiles[s] = T[mid, :].copy()
    T = step(T, src, a, "dirichlet")

# ---- closeup: field snapshot + cross-section broadening ----
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.04, 0.08, 0.40, 0.84]); ax1.set_facecolor(NAVY)
im = ax1.imshow(snaps[200], cmap="jet", vmin=0, vmax=100, origin="lower")
ax1.set_title("温度場（中央熱源, t=4.0s）", color="white", fontsize=10)
ax1.set_xticks([]); ax1.set_yticks([])
cb = fig.colorbar(im, ax=ax1, fraction=0.046, pad=0.04); cb.ax.tick_params(colors="#9fb2d6", labelsize=7)
cb.set_label("温度 (°C)", color="white", fontsize=8)
ax2 = fig.add_axes([0.56, 0.16, 0.40, 0.72]); ax2.set_facecolor(NAVY)
cols = [CYAN, "#9be7a3", ORANGE, "#f472b6"]
for (s, p), c in zip(profiles.items(), cols):
    ax2.plot(np.arange(N), p, color=c, lw=2, label=f"t={s*dt:.1f}s")
ax2.set_xlabel("位置 x (セル)", color="white", fontsize=9)
ax2.set_ylabel("温度 (°C)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)
ax2.set_title("中央断面：熱が時間とともに拡がる", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(4.6, 3.8)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.02, 0.02, 0.96, 0.96])
axc.imshow(snaps[200], cmap="jet", vmin=0, vmax=100, origin="lower"); axc.axis("off")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "2D熱拡散と", "フーリエの法則", "FTCS 陽解法で熱方程式を解く", cc)
os.remove(cc)

# ---- gif: field evolving ----
T, src = make_field()
frames = []
for s in range(660):
    if s % 14 == 0:
        f2 = plt.figure(figsize=(4.0, 4.0)); f2.patch.set_facecolor(NAVY)
        a2 = f2.add_axes([0.0, 0.0, 1.0, 0.93])
        a2.imshow(T, cmap="jet", vmin=0, vmax=100, origin="lower"); a2.axis("off")
        a2.set_title(f"t = {s*dt:.1f} s", color="white", fontsize=11)
        frames.append(figlib.fig_to_pil(f2, dpi=90))
    T = step(T, src, a, "dirichlet")
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
