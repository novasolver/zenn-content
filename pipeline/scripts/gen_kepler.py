# -*- coding: utf-8 -*-
"""Verify kepler-orbit numbers + figures. GM=4*pi^2 (years, AU): T^2=a^3.
Demo: ellipse with Sun at focus, equal-area sectors (Kepler 2nd law),
perihelion/aphelion. Verifies vis-viva and Kepler's 3rd law."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import figlib

SLUG = "kepler-orbit"
NAVY = "#0b1020"; ORANGE = "#f59e0b"; BLUE = "#7dd3fc"; SUN = "#ffd43b"
GM = 4*np.pi**2


def orbit(a, e, n=200000, dt=None):
    """Integrate from perihelion with velocity-Verlet; return positions, period."""
    T = a**1.5
    if dt is None:
        dt = T/n
    r0 = a*(1-e); v0 = np.sqrt(GM*(1+e)/(a*(1-e)))
    pos = np.array([r0, 0.0]); vel = np.array([0.0, v0])
    def acc(p):
        r = np.hypot(*p); return -GM*p/r**3
    out = []; ac = acc(pos); t = 0.0; times = []
    for i in range(n):
        vel = vel + 0.5*ac*dt; pos = pos + vel*dt; ac = acc(pos); vel = vel + 0.5*ac*dt
        out.append(pos.copy()); times.append((i+1)*dt)
    return np.array(out), T, dt, r0, v0


print("=== kepler verification ===")
for a, e, name in [(1.0, 0.017, 'Earth'), (1.524, 0.093, 'Mars'),
                   (0.387, 0.206, 'Mercury'), (17.8, 0.967, 'Halley')]:
    T = a**1.5
    print(f"  {name:8s} a={a} e={e}: T={T:.3f} yr, T^2/a^3={T*T/a**3:.4f}")
a, e = 1.2, 0.5
pos, T, dt, r0, v0 = orbit(a, e, n=120000)
# vis-viva at perihelion / aphelion
r_peri, r_apo = a*(1-e), a*(1+e)
v_peri = np.sqrt(GM*(2/r_peri - 1/a)); v_apo = np.sqrt(GM*(2/r_apo - 1/a))
print(f"  demo a={a} e={e}: T={T:.3f} yr, perihelion r={r_peri:.3f} v={v_peri:.3f}, "
      f"aphelion r={r_apo:.3f} v={v_apo:.3f}, v_peri/v_apo={v_peri/v_apo:.3f} (=(1+e)/(1-e)={(1+e)/(1-e):.3f})")
# equal areas: split one period into 8 equal-time arcs, compare swept areas
nseg = 8; idx = np.linspace(0, len(pos)-1, nseg+1).astype(int)
areas = []
for k in range(nseg):
    seg = pos[idx[k]:idx[k+1]+1]
    A = 0.0
    for j in range(len(seg)-1):
        A += 0.5*abs(seg[j, 0]*seg[j+1, 1] - seg[j+1, 0]*seg[j, 1])  # triangle from focus(origin)
    areas.append(A)
areas = np.array(areas)
print(f"  equal-area check (8 equal-time arcs): area spread = {(areas.max()-areas.min())/areas.mean()*100:.2f}%")


def style(ax):
    ax.set_facecolor(NAVY); ax.set_aspect("equal"); ax.axis("off")


# ---- closeup: ellipse + sun + equal-area sectors + peri/apo ----
fig, ax = plt.subplots(figsize=(6.8, 5.4)); fig.patch.set_facecolor(NAVY); style(ax)
ax.plot(pos[:, 0], pos[:, 1], color=ORANGE, lw=2.2)
# equal-area sectors
cols = plt.cm.viridis(np.linspace(0.2, 0.9, nseg))
for k in range(nseg):
    seg = pos[idx[k]:idx[k+1]+1]
    poly = np.vstack([[0, 0], seg])
    ax.add_patch(Polygon(poly, closed=True, facecolor=cols[k], edgecolor="none", alpha=0.45))
ax.plot([0], [0], marker="o", color=SUN, ms=20, zorder=6)      # Sun at focus
ax.plot([r_peri], [0], marker="o", color=BLUE, ms=8, zorder=6)
ax.plot([-r_apo], [0], marker="o", color="#ff7b7b", ms=8, zorder=6)
ax.text(r_peri, 0.12, "近日点", color=BLUE, ha="center", fontsize=10)
ax.text(-r_apo, 0.12, "遠日点", color="#ff7b7b", ha="center", fontsize=10)
ax.text(0, -0.18, "太陽", color=SUN, ha="center", fontsize=10)
ax.set_title("ケプラー軌道：等時間で等面積（第2法則）", color="white", fontsize=11)
m = a*(1+e)*1.15
ax.set_xlim(-m-0.3, a*(1-e)+0.5); ax.set_ylim(-a*1.1, a*1.1)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup); print("  closeup ->", closeup)

figlib.make_cover(SLUG, "ケプラー軌道と", "2体問題",
                  "楕円・等面積・調和の法則を数式で", closeup)

# ---- GIF: eccentricity sweep ----
frames = []
es = list(np.linspace(0.0, 0.9, 10)); es = es + es[::-1]
for ev in es:
    p, _, _, rp, _ = orbit(a, ev, n=4000)
    f2, a2 = plt.subplots(figsize=(4.8, 4.2)); f2.patch.set_facecolor(NAVY); style(a2)
    a2.plot(p[:, 0], p[:, 1], color=ORANGE, lw=2.0)
    a2.plot([0], [0], marker="o", color=SUN, ms=16)
    a2.set_title(f"離心率 e = {ev:.2f}", color="white")
    mm = a*(1+0.9)*1.1
    a2.set_xlim(-mm-0.3, a*1.1+0.3); a2.set_ylim(-a*1.2, a*1.2)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=180)
print("done.")
