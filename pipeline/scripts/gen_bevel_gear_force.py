# -*- coding: utf-8 -*-
"""Bevel-gear tooth-force visuals. Faithful to bevel-gear-force.html:
  Ft = T/rm,  Fa = Ft*tan(a)*sin(g),  Fr = Ft*tan(a)*cos(g),  F = sqrt(Ft^2+Fa^2+Fr^2).
Produces cover.png, charts-closeup.png, slider-anim.gif. ASCII labels only (use <v>)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "bevel-gear-force"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; GREEN = "#00e676"; BLUE = "#3aa6ff"; RED = "#ff5c5c"; ORANGE = "#f59e0b"


def forces(rm_mm, gamma_deg, T, alpha_deg):
    rm = rm_mm / 1000.0
    g = np.radians(gamma_deg); a = np.radians(alpha_deg)
    Ft = T / rm
    Fa = Ft * np.tan(a) * np.sin(g)
    Fr = Ft * np.tan(a) * np.cos(g)
    F = np.sqrt(Ft**2 + Fa**2 + Fr**2)
    return Ft, Fa, Fr, F


def draw_cone(ax, gamma_deg):
    """Side view of a bevel-gear pitch cone with the 3 force vectors at the mesh point."""
    ax.set_facecolor(NAVY)
    g = np.radians(gamma_deg)
    # pitch cone: apex at origin, axis along +x, half-angle gamma
    L = 1.0
    xr = L * np.cos(g); yr = L * np.sin(g)
    ax.plot([0, xr], [0, yr], color="#9fb2d6", lw=1.4)
    ax.plot([0, xr], [0, -yr], color="#9fb2d6", lw=1.4)
    ax.plot([xr, xr], [-yr, yr], color="#9fb2d6", lw=1.2)
    ax.fill([0, xr, xr], [0, yr, -yr], color=CYAN, alpha=0.12)
    ax.plot([0, 1.25], [0, 0], "--", color="#5b6b8c", lw=1.0)  # gear axis
    # mesh point on the upper cone surface
    mx, my = xr, yr
    s = 0.42
    # F_t tangential (out of plane -> draw down-right green), F_a axial (+x blue), F_r radial (+y red)
    ax.annotate("", xy=(mx + s*0.55, my + s*0.40), xytext=(mx, my),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.4))
    ax.annotate("", xy=(mx + s*np.tan(np.radians(20))*np.sin(g)*2.4, my), xytext=(mx, my),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.4))
    ax.annotate("", xy=(mx, my + s*np.tan(np.radians(20))*np.cos(g)*2.4), xytext=(mx, my),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.4))
    ax.text(mx + s*0.58, my + s*0.46, "F_t", color=GREEN, fontsize=9, weight="bold")
    ax.text(mx + 0.30, my - 0.07, "F_a", color=BLUE, fontsize=9, weight="bold")
    ax.text(mx + 0.02, my + 0.30, "F_r", color=RED, fontsize=9, weight="bold")
    ax.plot([mx], [my], "o", color=ORANGE, ms=6)
    ax.text(0.30, 0.04, f"g = {gamma_deg:.0f} deg", color="#cfe0ff", fontsize=9)
    ax.set_xlim(-0.1, 1.7); ax.set_ylim(-1.0, 1.2)
    ax.set_aspect("equal"); ax.axis("off")


# ---- charts-closeup: bar chart of 3 forces + Fa vs gamma sensitivity ----
rm, gamma, T, alpha = 50, 30, 100, 20
Ft, Fa, Fr, F = forces(rm, gamma, T, alpha)
print(f"default Ft={Ft:.0f} Fa={Fa:.0f} Fr={Fr:.0f} F={F:.0f} ratio={Fa/Ft*100:.1f}%")

fig = plt.figure(figsize=(9.4, 4.2)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07, 0.16, 0.38, 0.70]); ax1.set_facecolor(NAVY)
bars = ax1.bar(["F_t", "F_a", "F_r"], [Ft, Fa, Fr], color=[GREEN, BLUE, RED])
for b, val in zip(bars, [Ft, Fa, Fr]):
    ax1.text(b.get_x()+b.get_width()/2, val+40, f"{val:.0f}", color="white", ha="center", fontsize=9)
ax1.set_ylabel("force (N)", color="white", fontsize=9)
ax1.set_title("3 force components (g=30, a=20, T=100)", color="white", fontsize=9.5)
ax1.tick_params(colors="#9fb2d6", labelsize=9)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")

ax2 = fig.add_axes([0.56, 0.16, 0.40, 0.70]); ax2.set_facecolor(NAVY)
gs = np.linspace(15, 75, 80)
Fa_curve = [forces(rm, gg, T, alpha)[1] for gg in gs]
ax2.plot(gs, Fa_curve, color=BLUE, lw=2.2, label="F_a(g)")
ax2.plot([30], [Fa], "o", color=ORANGE, ms=8, label="current g=30")
ax2.set_xlabel("pitch angle g (deg)", color="white", fontsize=9)
ax2.set_ylabel("axial force F_a (N)", color="white", fontsize=9)
ax2.set_title("axial force vs pitch angle", color="white", fontsize=9.5)
ax2.tick_params(colors="#9fb2d6", labelsize=9)
ax2.grid(alpha=0.18, color="#3b4a6b")
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.4, 3.0)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.0, 0.0, 1.0, 1.0]); draw_cone(axc, 35)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ベベルギアの", "歯面3力", "F_t / F_a / F_r とスラスト軸受の必要性", cc)
os.remove(cc)

# ---- gif: pitch angle sweep, vectors + Fa readout ----
frames = []
for gg in list(range(15, 76, 3)) + list(range(75, 14, -3)):
    Ft, Fa, Fr, F = forces(rm, gg, T, alpha)
    f2 = plt.figure(figsize=(5.6, 3.2)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.0, 0.10, 0.62, 0.84]); draw_cone(a, gg)
    ax = f2.add_axes([0.66, 0.18, 0.31, 0.66]); ax.set_facecolor(NAVY)
    ax.bar(["F_t", "F_a", "F_r"], [Ft, Fa, Fr], color=[GREEN, BLUE, RED])
    ax.set_ylim(0, 2200); ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.set_title(f"F_a/F_t = {Fa/Ft*100:.1f}%", color="white", fontsize=9)
    f2.text(0.31, 0.95, f"pitch angle g = {gg} deg", color="white", ha="center", fontsize=10, weight="bold")
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=110)
print("done.")
