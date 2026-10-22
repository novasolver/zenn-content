# -*- coding: utf-8 -*-
"""Belt friction (capstan) visuals. ratio=exp(mu*beta); T(phi)=Thold*exp(mu*phi).
Drum with color-coded rope wrap + tension distribution curve."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import figlib

SLUG = "belt-friction"
NAVY = "#0a1929"
BLUE, CYAN, RED, ORANGE, GOLD = "#007BFF", "#00B4D8", "#e74c3c", "#f39c12", "#FFD166"

def cmap_br(f):  # blue->red
    f = max(0.0, min(1.0, f))
    return (0.16+0.8*f, (120-abs(f-0.5)*90)/255, (220-190*f)/255)

def draw_drum(ax, mu, betaDeg, Tload):
    ax.set_facecolor(NAVY)
    beta = math.radians(betaDeg)
    ratio = math.exp(mu*beta)
    Thold = Tload/ratio
    R = 1.0
    a0 = -math.pi*0.5 - beta*0.5
    n = 300
    ts = np.linspace(0, beta, n)
    # spiral out slightly for multi-turn clarity
    maxR = R + min(R*0.9, 0.12 + (beta/(2*math.pi))*0.10)
    rr = R + (maxR-R)*(ts/beta if beta > 0 else 0)
    ang = a0 + ts
    xs = rr*np.cos(ang); ys = rr*np.sin(ang)
    Tvals = Thold*np.exp(mu*ts)
    logLo, logHi = math.log(max(Thold,1e-9)), math.log(max(Tload,Thold+1e-9))
    fr = (np.log(np.maximum(Tvals,1e-9))-logLo)/(logHi-logLo) if logHi>logLo else np.zeros_like(Tvals)
    pts = np.array([xs, ys]).T.reshape(-1,1,2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    lc = LineCollection(segs, colors=[cmap_br(f) for f in fr[:-1]], linewidths=6, capstyle="round")
    ax.add_collection(lc)
    # drum body
    circ = plt.Circle((0,0), R, color="#1c2f47", zorder=1)
    ax.add_patch(circ)
    ax.add_patch(plt.Circle((0,0), R, fill=False, color="#3d567a", lw=2, zorder=2))
    ax.add_patch(plt.Circle((0,0), R*0.16, color="#3d567a", zorder=3))
    # tangent ends
    holdAng, loadAng = a0, a0+beta
    hx, hy = R*math.cos(holdAng), R*math.sin(holdAng)
    lx, ly = maxR*math.cos(loadAng), maxR*math.sin(loadAng)
    hdx, hdy = math.sin(holdAng), -math.cos(holdAng)
    ldx, ldy = -math.sin(loadAng), math.cos(loadAng)
    seg = 0.9
    ax.plot([hx, hx+hdx*seg], [hy, hy+hdy*seg], color=cmap_br(0), lw=3.5)
    ax.plot([lx, lx+ldx*seg], [ly, ly+ldy*seg], color=cmap_br(1), lw=7)
    ax.annotate(f"T_hold={Thold:.0f}N", (hx+hdx*seg, hy+hdy*seg), color="#cfe3f7", fontsize=8.5,
                ha="center", xytext=(0,-12), textcoords="offset points")
    ax.annotate(f"T_load={Tload:.0f}N", (lx+ldx*seg, ly+ldy*seg), color="#cfe3f7", fontsize=8.5,
                ha="center", xytext=(0,8), textcoords="offset points")
    ax.set_xlim(-2.3, 2.3); ax.set_ylim(-2.3, 1.8)
    ax.set_aspect("equal"); ax.axis("off")
    return ratio, Thold

def draw_dist(ax, mu, betaDeg, Tload):
    ax.set_facecolor(NAVY)
    beta = math.radians(betaDeg)
    ratio = math.exp(mu*beta); Thold = Tload/ratio
    phis = np.linspace(0, beta, 200)
    T = Thold*np.exp(mu*phis)
    ax.plot(np.degrees(phis), T, color=CYAN, lw=2.6)
    ax.fill_between(np.degrees(phis), T, color=CYAN, alpha=0.12)
    ax.axhline(Tload, color=RED, lw=1.4, ls="--", label=f"T_load={Tload:.0f}N")
    ax.set_xlabel("保持側からの角度 φ (°)", color="white", fontsize=9)
    ax.set_ylabel("張力 T (N)", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="upper left")

mu, betaDeg, Tload = 0.30, 540, 1000
ratio = math.exp(mu*math.radians(betaDeg))
print(f"closeup mu={mu} beta={betaDeg} Tload={Tload}: ratio={ratio:.2f} Thold={Tload/ratio:.2f}")

# closeup: drum + distribution
fig = plt.figure(figsize=(9.6, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.02, 0.04, 0.46, 0.9])
r1, th1 = draw_drum(ax1, mu, betaDeg, Tload)
ax1.set_title(f"ロープの張力（青→赤＝小→大）  倍力比={r1:.1f}×", color="white", fontsize=10)
ax2 = fig.add_axes([0.58, 0.16, 0.39, 0.72])
draw_dist(ax2, mu, betaDeg, Tload)
ax2.set_title("接触区間に沿った張力分布 T(φ)", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.02, 0.02, 0.96, 0.92])
draw_drum(axc, 0.30, 360, 1000)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ベルト摩擦", "キャプスタン方程式", "T_load/T_hold = e^(μβ) / 巻くほど指数的に増幅", cc)
os.remove(cc)

# gif: sweep wrap angle, ratio explodes
frames = []
for bd in list(range(60, 1081, 120)) + list(range(1080, 59, -120)):
    r = math.exp(0.30*math.radians(bd)); th = 1000/r
    f2 = plt.figure(figsize=(5.0, 3.6)); f2.patch.set_facecolor(NAVY)
    axg = f2.add_axes([0.0, 0.0, 1.0, 0.9])
    draw_drum(axg, 0.30, bd, 1000)
    axg.set_title(f"β={bd}° (μ=0.3) → 倍力比={r:.1f}×, T_hold={th:.0f}N", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=140)
print("done.")
