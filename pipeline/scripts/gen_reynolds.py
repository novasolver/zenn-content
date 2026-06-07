# -*- coding: utf-8 -*-
"""Reynolds number visuals. Re=rho*U*L/mu. U-L regime map (laminar/transition/
turbulent) + laminar-vs-turbulent flow schematic. Faithful to the tool."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "reynolds-number"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"
rho, mu = 998.2, 1.002e-3   # water 20C
nu = mu / rho

def regime_map(ax, Uop=1.0, Lop=0.025):
    ax.set_facecolor(NAVY)
    U = np.logspace(-2, 2, 300); L = np.logspace(-3, 1, 300)
    UU, LL = np.meshgrid(U, L)
    Re = rho * UU * LL / mu
    reg = np.where(Re < 2300, 0, np.where(Re < 4000, 1, 2))
    ax.pcolormesh(U, L, reg, cmap=plt.matplotlib.colors.ListedColormap(["#0d3b2e", "#4a3410", "#3b1414"]),
                  shading="auto", alpha=0.9)
    # constant-Re lines
    for Re0, c, lab in [(2300, "#00b894", "Re=2300 (層流限界)"), (4000, "#d63031", "Re=4000 (乱流)")]:
        Lline = Re0 * nu / U
        ax.plot(U, Lline, color=c, lw=1.8, label=lab)
    ax.plot(Uop, Lop, "o", color="#FFD166", ms=11, mec="white", zorder=5)
    Re_op = rho * Uop * Lop / mu
    ax.text(Uop*1.2, Lop*1.3, f"水 U={Uop}m/s\nD={Lop*1000:.0f}mm\nRe={Re_op:.0f}", color="#FFD166", fontsize=8)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(0.01, 100); ax.set_ylim(0.001, 10)
    ax.set_xlabel("流速 U (m/s)", color="white", fontsize=9); ax.set_ylabel("代表長さ L (m)", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="lower left")

def flow_schematic(ax):
    ax.set_facecolor(NAVY)
    # laminar (top): parallel streamlines
    yt = np.linspace(0.62, 0.95, 6)
    xs = np.linspace(0, 1, 100)
    for y in yt:
        ax.plot(xs, y + 0*xs, color=CYAN, lw=1.2)
    ax.text(0.5, 0.99, "層流（Re<2300）：整然と平行", color=CYAN, ha="center", fontsize=9)
    # turbulent (bottom): wavy + eddies
    rng = np.random.RandomState(3)
    for y in np.linspace(0.08, 0.42, 6):
        yy = y + 0.04*np.sin(12*xs + rng.rand()*6) + 0.02*np.sin(25*xs+rng.rand()*6)
        ax.plot(xs, yy, color=ORANGE, lw=1.1, alpha=0.85)
    ax.text(0.5, 0.46, "乱流（Re>4000）：渦が混ざる", color=ORANGE, ha="center", fontsize=9)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.05); ax.axis("off")

print(f"water D=25mm U=1: Re={rho*1.0*0.025/mu:.0f}; U=1.5: Re={rho*1.5*0.025/mu:.0f}")

# closeup: regime map + flow schematic
fig = plt.figure(figsize=(9.6, 4.4)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07, 0.14, 0.46, 0.76]); regime_map(ax1)
ax1.set_title("流れ場マップ：U×L とレイノルズ数", color="white", fontsize=10)
ax2 = fig.add_axes([0.58, 0.10, 0.40, 0.82]); flow_schematic(ax2)
ax2.set_title("層流 vs 乱流", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.14, 0.14, 0.82, 0.80]); regime_map(axc)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "レイノルズ数と", "層流・乱流", "Re = ρUL/μ、2300/4000 で遷移", cc)
os.remove(cc)

# gif: sweep velocity, operating point crosses regimes (L=25mm water)
frames = []
for U in list(np.logspace(-2, 1, 26)) + list(np.logspace(1, -2, 14)):
    f2 = plt.figure(figsize=(5.2, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.14, 0.15, 0.82, 0.78]); regime_map(a, Uop=U, Lop=0.025)
    a.get_legend().remove()
    Re = rho*U*0.025/mu
    reg = "層流" if Re < 2300 else "遷移域" if Re < 4000 else "乱流"
    a.set_title(f"U={U:.2f}m/s  Re={Re:.0f}  ({reg})", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=100)
print("done.")
