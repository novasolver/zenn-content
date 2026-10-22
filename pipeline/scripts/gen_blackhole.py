# -*- coding: utf-8 -*-
"""Black hole visuals. r_s=2GM/c^2, Kerr r+, T_H, structure (horizon/photon/ISCO).
Faithful to the tool (SI constants matching the HTML)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "blackhole-event-horizon"
NAVY = "#020d1a"
G=6.674e-11; c=2.998e8; hbar=1.0546e-34; k_B=1.381e-23; M_sun=1.989e30

def r_s(Ms): return 2*G*(Ms*M_sun)/(c*c)
def r_outer(Ms, aM):
    root = np.sqrt(max(0,1-aM*aM)); return (1+root)*r_s(Ms)/2
def T_H(Ms): return (hbar*c**3)/(8*np.pi*G*(Ms*M_sun)*k_B)

def draw_structure(ax, Ms=10, aM=0.0):
    ax.set_facecolor("#0a1830")
    rng = np.random.RandomState(3)
    sx = rng.uniform(-3,3,60); sy = rng.uniform(-3,3,60)
    ax.plot(sx, sy, ".", color=(1,1,1,0.55), ms=1.6)
    rs_u = 1.0  # in r_s units
    ro = r_outer(Ms, aM)/r_s(Ms)        # outer horizon in r_s units
    rph = 1.5; risco = 3.0              # Schwarzschild values (a=0); for cover use a=0
    # accretion disk
    th = np.linspace(0, 2*np.pi, 200)
    for rr, alpha in [(risco*1.3,0.18),(risco*1.1,0.30),(risco*0.0+risco,0.0)]:
        pass
    disk = plt.Circle((0,0), risco*2.2, color="#ff7a3c", alpha=0.10)
    ax.add_patch(disk)
    disk2 = plt.Circle((0,0), risco*1.5, color="#ffb45a", alpha=0.12)
    ax.add_patch(disk2)
    # ISCO (orange dashed)
    ax.add_patch(plt.Circle((0,0), risco, fill=False, ec="#ffa050", lw=1.5, ls=(0,(4,3))))
    # photon sphere (purple dashed)
    ax.add_patch(plt.Circle((0,0), rph, fill=False, ec="#b478ff", lw=1.0, ls=(0,(2,3))))
    # ergosphere if spinning
    if aM > 0.05:
        ergo = (1+np.sqrt(np.maximum(0,1-aM*aM*np.cos(th)**2)))*0.5
        ax.fill(ergo*np.cos(th), ergo*np.sin(th), color="#be8cfa", alpha=0.15)
        ax.plot(ergo*np.cos(th), ergo*np.sin(th), color="#be8cfa", lw=1, alpha=0.55)
    # event horizon (black with glow)
    ax.add_patch(plt.Circle((0,0), ro*1.22, color="#ffc88c", alpha=0.18))
    ax.add_patch(plt.Circle((0,0), ro, color="#000000", ec="white", lw=1.4))
    ax.text(0, risco+0.45, "ISCO", color="#ffa050", ha="center", fontsize=8)
    ax.text(0, -ro-0.35, "事象の地平面", color="white", ha="center", fontsize=8.5)
    ax.text(rph*0.72, rph*0.72, "光子球", color="#b478ff", fontsize=7.5)
    lim = risco*2.4
    ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim)
    ax.set_aspect("equal"); ax.axis("off")

# closeup: structure + r_s vs M log-log
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.02, 0.04, 0.46, 0.9]); draw_structure(ax1, 10, 0.0)
ax1.set_title("構造図（10 Msun, a/M=0）", color="white", fontsize=10)

ax2 = fig.add_axes([0.60, 0.16, 0.37, 0.70]); ax2.set_facecolor(NAVY)
Ms = np.logspace(0, 10, 50)
ax2.loglog(Ms, [r_s(m)/1000 for m in Ms], color="#007BFF", lw=2.2)
marks = {"太陽":1, "恒星質量\n10Msun":10, "Sgr A*":4.3e6, "M87*":6.5e9}
for name,m in marks.items():
    ax2.plot(m, r_s(m)/1000, "o", color="#e17055", ms=6)
    ax2.annotate(name, (m, r_s(m)/1000), color="#cfe3f7", fontsize=7,
                 textcoords="offset points", xytext=(4,4))
ax2.set_xlabel("質量 M (Msun)", color="white", fontsize=9)
ax2.set_ylabel("Schwarzschild 半径 (km)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
ax2.grid(True, which="both", color="#3b4a6b", alpha=0.3, lw=0.4)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("r_s = 2GM/c²（比例）", color="white", fontsize=9)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.02, 0.02, 0.96, 0.94]); draw_structure(axc, 10, 0.6)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ブラックホール", "事象の地平面", "r_s = 2GM/c² と Hawking 温度", cc)
os.remove(cc)

# gif: sweep spin a/M from 0..0.95 (and back) -> horizon shrinks, ergosphere grows
frames = []
seq = list(np.linspace(0, 0.95, 9)) + list(np.linspace(0.95, 0, 9))
for aM in seq:
    f2 = plt.figure(figsize=(4.6, 4.0)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.02, 0.02, 0.96, 0.88]); draw_structure(a, 10, aM)
    ro_km = r_outer(10, aM)/1000
    a.set_title(f"a/M={aM:.2f}   r+={ro_km:.1f} km", color="white", fontsize=11)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=200)
print("done.")
