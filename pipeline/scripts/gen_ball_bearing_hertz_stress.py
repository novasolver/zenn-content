# -*- coding: utf-8 -*-
"""Ball-bearing Hertz contact stress visuals. Faithful to ball-bearing-hertz-stress.html:
  Fmax = 5*F/(Z*cos a)  (a=0),  rb=Db/2, Ri=(Dp-Db)/2, Ro=(Dp+Db)/2
  1/Req_i = 1/rb - 1/Ri,  1/Req_o = 1/rb + 1/Ro
  p_max = (1/pi)*(6*Fmax*E*^2/Req^2)^(1/3),  a = (3*Fmax*Req/(4*E*))^(1/3),  E*=115.4 GPa
Produces cover.png, charts-closeup.png, slider-anim.gif. ASCII labels only (use <v>)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import figlib

SLUG = "ball-bearing-hertz-stress"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; GREEN = "#00e676"; BLUE = "#3aa6ff"
RED = "#ff5c5c"; ORANGE = "#f59e0b"; YELLOW = "#fff3a3"

ESTAR = 115.4e9  # Pa


def hertz(Fmax, Req):
    return (6 * Fmax * ESTAR * ESTAR / (Req * Req)) ** (1.0 / 3.0) / np.pi


def cradius(Fmax, Req):
    return (3 * Fmax * Req / (4 * ESTAR)) ** (1.0 / 3.0)


def compute(F_kN, Db_mm, Z, Dp_mm):
    F = F_kN * 1000.0; Db = Db_mm / 1000.0; Dp = Dp_mm / 1000.0
    rb = Db / 2.0; Ri = (Dp - Db) / 2.0; Ro = (Dp + Db) / 2.0
    Fmax = 5.0 * F / Z
    ReqI = rb * Ri / (Ri - rb)
    ReqO = rb * Ro / (Ro + rb)
    return Fmax, hertz(Fmax, ReqI), hertz(Fmax, ReqO), cradius(Fmax, ReqI), ReqI, ReqO


# defaults
Fmax, pI, pO, aI, ReqI, ReqO = compute(10, 12, 8, 50)
print(f"DEFAULT Fmax={Fmax/1000:.2f}kN pI={pI/1e9:.3f}GPa pO={pO/1e9:.3f}GPa "
      f"ratio={pO/pI:.3f} a={aI*1000:.3f}mm")


def draw_bearing(ax, Db_mm, Z, Dp_mm, pI, pO):
    """Schematic cross-section: outer ring, inner ring, balls, loaded contact points."""
    ax.set_facecolor(NAVY)
    rb = Db_mm / 2.0; Ri = (Dp_mm - Db_mm) / 2.0; Ro = (Dp_mm + Db_mm) / 2.0
    Rp = Dp_mm / 2.0
    # rings (annuli drawn as circle outlines)
    for r, col in [(Ro + rb * 0.9, "#3d567a"), (Ro, "#3d567a"),
                   (Ri, "#3d567a"), (max(1.0, Ri - rb * 0.9), "#3d567a")]:
        ax.add_patch(Circle((0, 0), r, fill=False, ec=col, lw=1.4))
    ax.add_patch(Circle((0, 0), Ro + rb * 0.9, fill=True, fc="#1c2f47", ec="none", zorder=0))
    ax.add_patch(Circle((0, 0), Ro, fill=True, fc=NAVY, ec="none", zorder=0))
    ax.add_patch(Circle((0, 0), Ri, fill=True, fc="#1c2f47", ec="none", zorder=0))
    ax.add_patch(Circle((0, 0), max(1.0, Ri - rb * 0.9), fill=True, fc=NAVY, ec="none", zorder=0))
    # pitch circle
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(Rp * np.cos(th), Rp * np.sin(th), "--", color="#8fb8e0", lw=0.9, alpha=0.5)
    # balls
    for k in range(Z):
        ang = -np.pi / 2 + k * 2 * np.pi / Z  # bottom-most is loaded
        bx, by = Rp * np.cos(ang), Rp * np.sin(ang)
        loaded = (k == 0)
        ax.add_patch(Circle((bx, by), rb * 0.95, fc=(YELLOW if loaded else CYAN),
                            ec=(ORANGE if loaded else "#3d567a"), lw=1.2, zorder=3))
        if loaded:
            # outer contact (higher stress, red), inner contact (orange)
            ax.plot([Ro * np.cos(ang)], [Ro * np.sin(ang)], "o", color=RED, ms=9, zorder=5)
            ax.plot([Ri * np.cos(ang)], [Ri * np.sin(ang)], "o", color=ORANGE, ms=7, zorder=5)
    lim = (Ro + rb) * 1.12
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal"); ax.axis("off")


# ---------- charts-closeup: stress bars + p_max vs Z sweep ----------
fig = plt.figure(figsize=(9.4, 4.2)); fig.patch.set_facecolor(NAVY)

ax1 = fig.add_axes([0.07, 0.16, 0.36, 0.70]); ax1.set_facecolor(NAVY)
bars = ax1.bar(["inner\np_max,i", "outer\np_max,o"], [pI / 1e9, pO / 1e9],
               color=[ORANGE, RED])
for b, v in zip(bars, [pI / 1e9, pO / 1e9]):
    ax1.text(b.get_x() + b.get_width() / 2, v + 0.15, f"{v:.2f}", color="white",
             ha="center", fontsize=10, weight="bold")
ax1.axhline(4.2, ls="--", color=CYAN, lw=1.4)
ax1.text(1.45, 4.35, "static limit ~4.2 GPa", color=CYAN, fontsize=8, ha="right")
ax1.set_ylabel("max contact stress (GPa)", color="white", fontsize=9)
ax1.set_ylim(0, 10)
ax1.set_title("inner (concave) vs outer (convex)\nF=10kN Db=12 Z=8 Dp=50", color="white", fontsize=9.5)
ax1.tick_params(colors="#9fb2d6", labelsize=9)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")

ax2 = fig.add_axes([0.56, 0.16, 0.40, 0.70]); ax2.set_facecolor(NAVY)
Zs = np.arange(5, 21)
piZ = [compute(10, 12, z, 50)[1] / 1e9 for z in Zs]
poZ = [compute(10, 12, z, 50)[2] / 1e9 for z in Zs]
ax2.plot(Zs, poZ, color=RED, lw=2.2, marker="o", ms=3, label="outer p_max,o")
ax2.plot(Zs, piZ, color=ORANGE, lw=2.2, marker="o", ms=3, label="inner p_max,i")
ax2.plot([8], [pI / 1e9], "o", color=YELLOW, ms=9, zorder=5)
ax2.set_xlabel("number of balls Z", color="white", fontsize=9)
ax2.set_ylabel("max contact stress (GPa)", color="white", fontsize=9)
ax2.set_title("stress falls only as Z^(-1/3)", color="white", fontsize=9.5)
ax2.tick_params(colors="#9fb2d6", labelsize=9)
ax2.grid(alpha=0.18, color="#3b4a6b")
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)

closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---------- cover ----------
figc = plt.figure(figsize=(5.0, 5.0)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.0, 0.0, 1.0, 1.0]); draw_bearing(axc, 12, 8, 50, pI, pO)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "玉軸受の", "接触応力", "Hertz 接触 / 内輪・外輪と Stribeck 荷重分布", cc)
os.remove(cc)

# ---------- gif: sweep total load F, bearing + stress bars ----------
frames = []
F_list = list(range(4, 31, 2)) + list(range(30, 3, -2))
for Fk in F_list:
    Fmaxg, pIg, pOg, aIg, _, _ = compute(Fk, 12, 8, 50)
    f2 = plt.figure(figsize=(6.2, 3.3)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.0, 0.06, 0.55, 0.88]); draw_bearing(a, 12, 8, 50, pIg, pOg)
    ax = f2.add_axes([0.62, 0.20, 0.34, 0.62]); ax.set_facecolor(NAVY)
    ax.bar(["inner", "outer"], [pIg / 1e9, pOg / 1e9], color=[ORANGE, RED])
    ax.axhline(4.2, ls="--", color=CYAN, lw=1.2)
    ax.set_ylim(0, 14); ax.set_ylabel("p_max (GPa)", color="white", fontsize=8)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.set_title(f"o/i = {pOg/pIg:.2f}", color="white", fontsize=9)
    f2.text(0.30, 0.95, f"F_total = {Fk} kN   F_max = {Fmaxg/1000:.1f} kN",
            color="white", ha="center", fontsize=10, weight="bold")
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=130)
print("done.")
