# -*- coding: utf-8 -*-
"""Projectile motion visuals: trajectories at various angles + range-vs-angle.
R = v0^2 sin(2theta)/g (no drag). Faithful to the tool's ideal ballistics."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "projectile-motion"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"
v0, g = 30.0, 9.81

def traj(v0, th, g=9.81, n=200):
    thr = np.radians(th); T = 2 * v0 * np.sin(thr) / g
    t = np.linspace(0, T, n)
    return v0 * np.cos(thr) * t, v0 * np.sin(thr) * t - 0.5 * g * t * t

def draw_trajs(ax, title=None):
    ax.set_facecolor(NAVY)
    angles = [15, 30, 45, 60, 75]
    cols = plt.cm.viridis(np.linspace(0.15, 0.9, len(angles)))
    for th, c in zip(angles, cols):
        x, y = traj(v0, th); R = v0*v0*np.sin(np.radians(2*th))/g
        ax.plot(x, y, color=c, lw=2 if th == 45 else 1.3,
                label=f"{th}°" + (" (最大射程)" if th == 45 else ""))
        ax.plot(R, 0, "o", color=c, ms=5)
    ax.axhline(0, color="#3b4a6b", lw=1)
    ax.set_xlabel("水平距離 x (m)", color="white", fontsize=9)
    ax.set_ylabel("高さ y (m)", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="upper right")
    if title: ax.set_title(title, color="white", fontsize=10)

# closeup: trajectories + range vs angle
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07, 0.14, 0.55, 0.76]); draw_trajs(ax1, "発射角を変えた弾道（v₀=30 m/s）")
ax2 = fig.add_axes([0.70, 0.16, 0.27, 0.72]); ax2.set_facecolor(NAVY)
ths = np.linspace(0, 90, 200); Rs = v0*v0*np.sin(np.radians(2*ths))/g
ax2.plot(ths, Rs, color=ORANGE, lw=2)
ax2.axvline(45, color=CYAN, lw=1, ls="--"); ax2.plot(45, v0*v0/g, "o", color=CYAN, ms=7)
ax2.text(46, v0*v0/g*0.6, "45°で最大\nR=91.7m", color=CYAN, fontsize=8)
ax2.set_xlabel("発射角 θ (°)", color="white", fontsize=9)
ax2.set_ylabel("射程 R (m)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("射程は45°で最大", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.05, 0.08, 0.92, 0.86]); draw_trajs(axc)
axc.get_legend().remove()
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "放物運動と射程", "", "R = v₀²sin(2θ)/g、45°で最大", cc)
os.remove(cc)

# gif: sweep angle
frames = []
for th in list(range(10, 81, 3)) + list(range(78, 10, -3)):
    x, y = traj(v0, th); R = v0*v0*np.sin(np.radians(2*th))/g
    f2 = plt.figure(figsize=(5.4, 3.2)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.10, 0.14, 0.86, 0.78]); a.set_facecolor(NAVY)
    a.plot(x, y, color=CYAN, lw=2); a.fill_between(x, y, color=CYAN, alpha=0.12)
    a.plot(R, 0, "o", color=ORANGE, ms=8); a.axhline(0, color="#3b4a6b", lw=1)
    a.set_xlim(0, 95); a.set_ylim(0, 50)
    a.set_xlabel("x (m)", color="white", fontsize=8); a.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    a.set_title(f"θ={th}°  射程 R={R:.1f}m", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
