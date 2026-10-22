# -*- coding: utf-8 -*-
"""2D random walk visuals. Reproduces the tool's walk types (lattice4, gauss,
levy) and MSD scaling. Trajectories + log-log MSD (diffusion vs superdiffusion)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "random-walk-2d"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"
COLS = ["#7dd3fc", "#f59e0b", "#9be7a3", "#f472b6", "#c084fc", "#fca5a5"]
A = 5.0   # step size

def levy_step(alpha, rng, size):
    u = rng.uniform(-np.pi/2, np.pi/2, size)
    w = -np.log(rng.uniform(0, 1, size))
    num = np.sin(alpha * u)
    den = np.power(np.cos(u), 1/alpha)
    factor = np.power(np.cos((1-alpha)*u)/w, (1-alpha)/alpha)
    return (num/den) * factor

def walk(kind, nwalk, steps, rng, alpha=1.5, drift=0.0):
    x = np.zeros(nwalk); y = np.zeros(nwalk)
    xs = [x.copy()]; ys = [y.copy()]; msd = []
    for s in range(steps):
        if kind == "lattice4":
            d = rng.randint(0, 4, nwalk)
            x = x + np.where(d==0, A, np.where(d==1, -A, 0.0)) + drift
            y = y + np.where(d==2, A, np.where(d==3, -A, 0.0))
        elif kind == "gauss":
            x = x + rng.randn(nwalk)*A + drift; y = y + rng.randn(nwalk)*A
        else:  # levy
            x = x + A*np.clip(levy_step(alpha, rng, nwalk), -60, 60)
            y = y + A*np.clip(levy_step(alpha, rng, nwalk), -60, 60)
        xs.append(x.copy()); ys.append(y.copy())
        msd.append(np.mean(x*x + y*y))
    return np.array(xs), np.array(ys), np.array(msd)

# ---- trajectories (lattice4, few walkers) ----
rng = np.random.RandomState(3)
xs, ys, _ = walk("lattice4", 6, 500, rng)
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.05, 0.08, 0.42, 0.84]); ax1.set_facecolor(NAVY)
for i in range(6):
    ax1.plot(xs[:, i], ys[:, i], color=COLS[i], lw=1.0, alpha=0.8)
    ax1.plot(xs[-1, i], ys[-1, i], "o", color=COLS[i], ms=5)
ax1.plot(0, 0, "P", color="white", ms=10)
ax1.set_aspect("equal"); ax1.set_xticks([]); ax1.set_yticks([])
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.set_title("6個のウォーカーの軌跡（格子4方向）", color="white", fontsize=10)

# ---- MSD log-log: normal diffusion (no drift, slope 1) vs drift (ballistic, slope 2) ----
rng = np.random.RandomState(11)
_, _, msd_lat = walk("lattice4", 4000, 400, rng)
_, _, msd_dft = walk("lattice4", 4000, 400, rng, drift=1.5)
t = np.arange(1, 401)
ax2 = fig.add_axes([0.58, 0.16, 0.38, 0.72]); ax2.set_facecolor(NAVY)
ax2.loglog(t, msd_lat, color=CYAN, lw=2, label="ドリフト無 → 通常拡散 (傾き1)")
ax2.loglog(t, msd_dft, color=ORANGE, lw=2, label="ドリフト有 → 弾道的 (傾き2)")
ax2.loglog(t, A*A*t, color="white", lw=1, ls="--", alpha=0.6, label="<r2>=4Dt 基準線")
ax2.set_xlabel("ステップ t", color="white", fontsize=9)
ax2.set_ylabel("平均二乗変位 MSD", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="upper left")
ax2.set_title("MSD のべき乗則が拡散型を分ける", color="white", fontsize=10)
slope_lat = np.polyfit(np.log(t[50:]), np.log(msd_lat[50:]), 1)[0]
slope_dft = np.polyfit(np.log(t[200:]), np.log(msd_dft[200:]), 1)[0]
print(f"slope no-drift={slope_lat:.2f} (expect 1.0), drift slope(late)={slope_dft:.2f} (->2)")
print(f"lattice4 <r^2>/t end = {msd_lat[-1]/400:.1f} (expect a^2={A*A:.0f})")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
rng = np.random.RandomState(5)
xs, ys, _ = walk("lattice4", 5, 600, rng)
figc = plt.figure(figsize=(5.0, 3.4)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.02, 0.02, 0.96, 0.96]); axc.set_facecolor(NAVY)
for i in range(5):
    axc.plot(xs[:, i], ys[:, i], color=COLS[i], lw=1.1, alpha=0.85)
axc.plot(0, 0, "P", color="white", ms=10)
axc.set_aspect("equal"); axc.axis("off")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "2Dランダムウォーク", "", "MSD=4Dt とブラウン運動を可視化", cc)
os.remove(cc)

# ---- gif: a cloud of walkers spreading from origin ----
rng = np.random.RandomState(9)
xs, ys, _ = walk("lattice4", 400, 300, rng)
frames = []
for s in range(0, 301, 6):
    f2 = plt.figure(figsize=(4.4, 4.4)); f2.patch.set_facecolor(NAVY)
    a2 = f2.add_axes([0.0, 0.0, 1.0, 0.93]); a2.set_facecolor(NAVY)
    a2.scatter(xs[s], ys[s], s=6, color=CYAN, alpha=0.6, edgecolors="none")
    a2.plot(0, 0, "P", color=ORANGE, ms=9)
    R = 5 * A * np.sqrt(max(s, 1)) / np.sqrt(300) * 6
    lim = 220
    a2.set_xlim(-lim, lim); a2.set_ylim(-lim, lim); a2.set_aspect("equal"); a2.axis("off")
    a2.set_title(f"t={s}  原点から拡がる（RMS∝√t）", color="white", fontsize=9)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=90)
print("done.")
