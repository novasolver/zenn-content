# -*- coding: utf-8 -*-
"""Verify magnetic-pendulum numbers + generate figures (matplotlib).

Tool model (RK4, dt=0.05): with magnets at xy-radius r=0.8, height h=0.4,
  ax = -(g/L)x - b*vx + sum ms*(xm-x)/ri^3
  ay = -(g/L)y - b*vy + sum ms*(ym-y)/ri^3,  ri=sqrt((x-xm)^2+(y-ym)^2+h^2)
g=1, defaults L=1, b=0.2, ms=1.

The tool places the 3 magnets at angles 30/90/150 deg (clustered, BUG logged
in pipeline/bugs.md). We render the canonical *symmetric* arrangement
(90/210/330 deg) so the article teaches correct physics (RECIPE STEP 4).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import figlib

SLUG = "magnetic-pendulum"

g, L, b, ms = 1.0, 1.0, 0.2, 1.0
R, H = 0.8, 0.4
# canonical symmetric placement (correct physics)
ang = np.deg2rad([90, 210, 330])
MX = R * np.cos(ang)
MY = R * np.sin(ang)
COLORS = np.array([[231, 76, 60], [46, 204, 113], [52, 152, 219]]) / 255.0


def accel(x, y, vx, vy):
    ax = -(g / L) * x - b * vx
    ay = -(g / L) * y - b * vy
    for k in range(3):
        dx = MX[k] - x
        dy = MY[k] - y
        r3 = (dx * dx + dy * dy + H * H) ** 1.5
        ax += ms * dx / r3
        ay += ms * dy / r3
    return ax, ay


def basin(xs, ys, nsteps=2200, dt=0.05):
    """Vectorised RK4 over a grid; return index of nearest magnet at the end."""
    X, Y = np.meshgrid(xs, ys)
    x = X.ravel().astype(float); y = Y.ravel().astype(float)
    vx = np.zeros_like(x); vy = np.zeros_like(y)
    for _ in range(nsteps):
        ax1, ay1 = accel(x, y, vx, vy)
        ax2, ay2 = accel(x + vx*dt/2, y + vy*dt/2, vx + ax1*dt/2, vy + ay1*dt/2)
        ax3, ay3 = accel(x + vx*dt/2, y + vy*dt/2, vx + ax2*dt/2, vy + ay2*dt/2)
        ax4, ay4 = accel(x + vx*dt,   y + vy*dt,   vx + ax3*dt,   vy + ay3*dt)
        x = x + dt*(vx + 2*(vx+ax1*dt/2) + 2*(vx+ax2*dt/2) + (vx+ax3*dt))/6
        y = y + dt*(vy + 2*(vy+ay1*dt/2) + 2*(vy+ay2*dt/2) + (vy+ay3*dt))/6
        vx = vx + dt*(ax1 + 2*ax2 + 2*ax3 + ax4)/6
        vy = vy + dt*(ay1 + 2*ay2 + 2*ay3 + ay4)/6
    d = np.stack([(x-MX[k])**2 + (y-MY[k])**2 for k in range(3)])
    idx = np.argmin(d, axis=0).reshape(X.shape)
    return idx


def trajectory(x0, y0, nsteps=2000, dt=0.05):
    x, y, vx, vy = x0, y0, 0.0, 0.0
    xs, ys = [x], [y]
    for _ in range(nsteps):
        ax1, ay1 = accel(x, y, vx, vy)
        ax2, ay2 = accel(x+vx*dt/2, y+vy*dt/2, vx+ax1*dt/2, vy+ay1*dt/2)
        ax3, ay3 = accel(x+vx*dt/2, y+vy*dt/2, vx+ax2*dt/2, vy+ay2*dt/2)
        ax4, ay4 = accel(x+vx*dt,   y+vy*dt,   vx+ax3*dt,   vy+ay3*dt)
        x = x + dt*(vx + 2*(vx+ax1*dt/2) + 2*(vx+ax2*dt/2) + (vx+ax3*dt))/6
        y = y + dt*(vy + 2*(vy+ay1*dt/2) + 2*(vy+ay2*dt/2) + (vy+ay3*dt))/6
        vx = vx + dt*(ax1 + 2*ax2 + 2*ax3 + ax4)/6
        vy = vy + dt*(ay1 + 2*ay2 + 2*ay3 + ay4)/6
        xs.append(x); ys.append(y)
        if (vx*vx+vy*vy) < 1e-4 and _ > 200:
            break
    final = int(np.argmin([(x-MX[k])**2+(y-MY[k])**2 for k in range(3)]))
    return np.array(xs), np.array(ys), final


# ---- NUMBER VERIFICATION ----
print("=== magnetic-pendulum verification ===")
print("magnet positions (symmetric):")
for k in range(3):
    print(f"  m{k+1}: ({MX[k]:+.4f}, {MY[k]:+.4f})  r={np.hypot(MX[k],MY[k]):.4f}")

# basin fractions on a coarse grid
N = 240
xs = np.linspace(-1.8, 1.8, N)
ys = np.linspace(-1.8, 1.8, N)
idx = basin(xs, ys)
frac = [np.mean(idx == k) for k in range(3)]
print("basin fractions:", [f"{f:.3f}" for f in frac])

# sensitivity: two nearby starts that land on different magnets
xa, ya, fa = trajectory(0.500, 0.0)
xb, yb, fb = trajectory(0.503, 0.0)
print(f"start (0.500,0): magnet {fa+1}; start (0.503,0): magnet {fb+1}")
# search for a boundary pair near a fractal edge
row = N // 2
changes = np.sum(idx[row, 1:] != idx[row, :-1])
print(f"sign changes along y=0 line: {changes} (fractal boundary crossings)")

# ---- FIGURES ----
# charts-closeup: zoomed fractal basin
Nf = 460
xf = np.linspace(-1.5, 1.5, Nf)
yf = np.linspace(-1.5, 1.5, Nf)
idxf = basin(xf, yf, nsteps=2400)
rgb = COLORS[idxf]
fig, axp = plt.subplots(figsize=(6.2, 6.2))
fig.patch.set_facecolor("#0b1020")
axp.imshow(rgb, origin="lower", extent=[-1.5, 1.5, -1.5, 1.5])
axp.scatter(MX, MY, c="white", edgecolors="black", s=160, zorder=5, marker="o")
for k in range(3):
    axp.scatter(MX[k], MY[k], c=[COLORS[k]], edgecolors="white", s=70, zorder=6)
# overlay one chaotic trajectory
xt, yt, ft = trajectory(0.503, 0.0)
axp.plot(xt, yt, color="white", lw=0.9, alpha=0.85, zorder=4)
axp.set_xlabel("初期位置 x"); axp.set_ylabel("初期位置 y")
axp.set_title("磁気振り子の吸引盆（3磁石・対称配置）", color="white")
axp.tick_params(colors="white")
for s in axp.spines.values():
    s.set_color("white")
axp.xaxis.label.set_color("white"); axp.yaxis.label.set_color("white")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup)
print("  closeup ->", closeup)

# cover
figlib.make_cover(SLUG, "磁気振り子の", "フラクタル吸引盆",
                  "RK4で解く3磁石カオス — どの磁石に落ちるか", closeup)

# slider-anim.gif: vary damping b -> basin morphs
frames = []
Ng = 300
xg = np.linspace(-1.5, 1.5, Ng)
yg = np.linspace(-1.5, 1.5, Ng)
b_vals = list(np.linspace(0.08, 0.45, 12))
b_vals = b_vals + b_vals[::-1]
for bv in b_vals:
    b = bv
    ig = basin(xg, yg, nsteps=1800)
    rgbg = COLORS[ig]
    f2, a2 = plt.subplots(figsize=(4.6, 4.6))
    f2.patch.set_facecolor("#0b1020")
    a2.imshow(rgbg, origin="lower", extent=[-1.5, 1.5, -1.5, 1.5])
    a2.scatter(MX, MY, c="white", edgecolors="black", s=80, zorder=5)
    a2.set_title(f"ダンピング b = {bv:.2f}", color="white")
    a2.set_xticks([]); a2.set_yticks([])
    frames.append(figlib.fig_to_pil(f2, dpi=92))
b = 0.2
figlib.save_gif(frames, SLUG, duration=160)
print("done.")
