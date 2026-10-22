# -*- coding: utf-8 -*-
"""Newton's cradle visuals. Faithful to the tool: N=5 equal-mass pendulums,
theta'' = -(g/L) sin theta (Verlet), elastic swap on adjacent contact (e=1).
Produces cover / charts-closeup / slider-anim.gif."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import figlib

SLUG = "newtons-cradle"
NAVY = "#0b1020"; ORANGE = "#f59e0b"; CYAN = "#7dd3fc"
N = 5
L = 1.0          # string length (m)
g = 9.81
BALLR = 0.085    # ball radius (visual units, == half spacing)
SPACING = 2 * BALLR
PIVOTS = np.arange(N) * SPACING          # pivot x positions
PIVOT_Y = 0.0

def ball_xy(theta):
    return PIVOTS + np.sin(theta) * L, PIVOT_Y + np.cos(theta) * L

def simulate(theta0_left=-0.40, e=1.0, tmax=3.6, dt=0.0015):
    theta = np.zeros(N); omega = np.zeros(N)
    theta[0] = theta0_left
    nrec = int(tmax / dt)
    Th = np.zeros((nrec, N)); KE = np.zeros(nrec); PE = np.zeros(nrec); T = np.zeros(nrec)
    for s in range(nrec):
        # pendulum step
        alpha = -(g / L) * np.sin(theta)
        omega += alpha * dt
        theta += omega * dt
        # adjacent collisions (equal mass): swap angular velocity (v=omega*L) if approaching
        for i in range(N - 1):
            x1, y1 = PIVOTS[i] + np.sin(theta[i]) * L, np.cos(theta[i]) * L
            x2, y2 = PIVOTS[i + 1] + np.sin(theta[i + 1]) * L, np.cos(theta[i + 1]) * L
            dist = np.hypot(x2 - x1, y2 - y1)
            if dist <= SPACING:
                v1 = omega[i] * L; v2 = omega[i + 1] * L
                if v1 - v2 > 1e-6:
                    # momentum-conserving restitution (correct physics)
                    nv1 = ((1 - e) / 2) * v1 + ((1 + e) / 2) * v2
                    nv2 = ((1 + e) / 2) * v1 + ((1 - e) / 2) * v2
                    omega[i] = nv1 / L; omega[i + 1] = nv2 / L
        Th[s] = theta
        v = omega * L
        KE[s] = 0.5 * np.sum(v * v)
        PE[s] = np.sum(g * L * (1 - np.cos(theta)))
        T[s] = s * dt
    return T, Th, KE, PE

def draw_cradle(ax, theta, title=None):
    ax.set_facecolor(NAVY)
    bx = PIVOTS.mean()
    # top bar + legs
    ax.plot([PIVOTS[0] - BALLR, PIVOTS[-1] + BALLR], [PIVOT_Y, PIVOT_Y],
            color="#3b4a6b", lw=4, solid_capstyle="round", zorder=1)
    xb, yb = ball_xy(theta)
    for i in range(N):
        ax.plot([PIVOTS[i], xb[i]], [PIVOT_Y, yb[i]], color="#9fb2d6", lw=0.9, zorder=2)
        col = ORANGE if i in (0, N - 1) else "#9bb4e0"
        ax.add_patch(Circle((xb[i], yb[i]), BALLR, color=col, ec="white", lw=0.8, zorder=3))
        ax.add_patch(Circle((xb[i] - BALLR * 0.3, yb[i] - BALLR * 0.3), BALLR * 0.22,
                            color="white", alpha=0.6, zorder=4))
    ax.set_xlim(PIVOTS[0] - 0.55, PIVOTS[-1] + 0.55)
    ax.set_ylim(1.18, -0.12)          # y inverted (balls hang down)
    ax.set_aspect("equal"); ax.axis("off")
    if title:
        ax.set_title(title, color="white", fontsize=11)

# ---- simulate (e=1 for the clean swap, used by cover/closeup/gif) ----
T, Th, KE, PE = simulate(e=1.0)
TE = KE + PE
print(f"total energy: mean={TE.mean():.3f} J, drift={(TE.max()-TE.min())/TE.mean()*100:.3f}%")
print(f"PE0 (ball pulled to {np.degrees(0.40):.1f} deg) = {PE[0]:.3f} J")

# ---- closeup: cradle snapshot (1 in) + energy exchange history ----
fig = plt.figure(figsize=(9.2, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.02, 0.08, 0.42, 0.86])
draw_cradle(ax1, Th[0], "1球を引いて離す → 反対側が1球だけ飛ぶ")
ax2 = fig.add_axes([0.54, 0.16, 0.43, 0.74]); ax2.set_facecolor(NAVY)
ax2.plot(T, KE, color=ORANGE, lw=1.6, label="運動エネルギー KE")
ax2.plot(T, PE, color=CYAN, lw=1.6, label="位置エネルギー PE")
ax2.plot(T, TE, color="white", lw=1.2, ls="--", label="合計 E（保存）")
ax2.set_xlabel("時間 t (s)", color="white", fontsize=9)
ax2.set_ylabel("エネルギー (J)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="upper right")
ax2.set_title("KE ⇄ PE の交換、合計は一定", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.0, 3.4)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.02, 0.02, 0.96, 0.96]); draw_cradle(axc, Th[0])
cover_chart = os.path.join(figlib.outdir(SLUG), "_coverchart.png")
figlib.save_fig(figc, cover_chart, dpi=120)
figlib.make_cover(SLUG, "ニュートンのゆりかご", "",
                  "運動量保存と弾性衝突 — KE⇄PE の交換を可視化", cover_chart)
os.remove(cover_chart)

# ---- gif: the cradle in motion (real mechanism, looping) ----
frames = []
step = max(1, len(T) // 60)
idxs = list(range(0, len(T), step))
for k in idxs:
    f2 = plt.figure(figsize=(4.8, 3.4)); f2.patch.set_facecolor(NAVY)
    a2 = f2.add_axes([0.02, 0.02, 0.96, 0.92])
    draw_cradle(a2, Th[k])
    a2.text(PIVOTS.mean(), -0.05, f"t = {T[k]:.2f} s", color=CYAN,
            ha="center", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=70)
print("done.")
