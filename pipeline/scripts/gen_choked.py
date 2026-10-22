# -*- coding: utf-8 -*-
"""Choked flow visuals. mdot vs Pb/P0 curve (flat in choked region) + sweep gif.
Faithful to tool: gamma=1.4, R=287; defaults P0=500kPa, T0=300K, A=100mm2."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "choked-flow"
NAVY = "#0a1929"
BLUE, RED, YELLOW = "#4dc4ff", "#ff6b6b", "#ffd166"
GAMMA, R = 1.4, 287.0

def rcr(g=GAMMA):
    return (2/(g+1))**(g/(g-1))

def mdot_max(P0, T0, A, g=GAMMA):
    return A*P0*np.sqrt(g/(R*T0))*(2/(g+1))**((g+1)/(2*(g-1)))

def mdot_sub(P0, T0, A, Pb, g=GAMMA):
    pr = Pb/P0
    if pr >= 1: return 0.0
    term = pr**(2/g) - pr**((g+1)/g)
    coef = np.sqrt(2*g/((g-1)*R*T0))
    return A*P0*coef*np.sqrt(max(term, 0))

def curve(P0, T0, A):
    rc = rcr()
    mmax = mdot_max(P0, T0, A)
    prs = np.linspace(0, 1, 220)
    ms = []
    for pr in prs:
        if pr <= rc:
            ms.append(mmax)
        elif pr >= 1:
            ms.append(0.0)
        else:
            ms.append(mdot_sub(P0, T0, A, pr*P0))
    return prs, np.array(ms), rc, mmax

def draw_curve(ax, P0, T0, A, Pb, title=None):
    ax.set_facecolor(NAVY)
    prs, ms, rc, mmax = curve(P0, T0, A)
    ax.plot(prs, ms, color=BLUE, lw=2.6)
    ax.axvline(rc, color=RED, ls="--", lw=1.6, alpha=0.8)
    ax.fill_betweenx([0, mmax*1.18], 0, rc, color=RED, alpha=0.08)
    ax.text(rc+0.02, mmax*0.12, f"P*/P0\n≈ {rc:.3f}", color="#ff9696", fontsize=8)
    # current operating point
    prCur = min(1.0, Pb/P0)
    mCur = mmax if prCur <= rc else mdot_sub(P0, T0, A, Pb)
    ax.scatter([prCur], [mCur], s=70, color=YELLOW, edgecolor="white", zorder=5)
    ax.axvline(prCur, color=YELLOW, ls=":", lw=1.2, alpha=0.7)
    ax.set_xlim(0, 1); ax.set_ylim(0, mmax*1.18)
    ax.set_xlabel("背圧比  Pb / P0", color="white", fontsize=9)
    ax.set_ylabel("質量流量  mdot (kg/s)", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.grid(True, color="#22344f", lw=0.6)
    if title: ax.set_title(title, color="white", fontsize=10)

P0, T0, A, Pb = 500e3, 300.0, 100e-6, 200e3
rc = rcr(); mmax = mdot_max(P0, T0, A)
Tstar = T0*2/(GAMMA+1); astar = np.sqrt(GAMMA*R*Tstar)
print(f"rcr={rc:.4f} mmax={mmax:.4f} T*={Tstar:.1f} a*={astar:.1f}")

# closeup: curve + annotation panel
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.09, 0.15, 0.55, 0.74])
draw_curve(ax1, P0, T0, A, Pb, "mdot vs 背圧比（左半分がチョーク領域＝頭打ち）")
ax2 = fig.add_axes([0.70, 0.15, 0.27, 0.74]); ax2.set_facecolor(NAVY); ax2.axis("off")
lines = [
    ("臨界圧力比", f"P*/P0 = {rc:.3f}"),
    ("最大質量流量", f"mdot_max = {mmax:.3f} kg/s"),
    ("喉部温度", f"T* = {Tstar:.0f} K"),
    ("喉部音速", f"a* = {astar:.0f} m/s"),
    ("臨界圧力", f"P* = {rc*P0/1000:.0f} kPa"),
]
y = 0.92
ax2.text(0.0, y, "空気 γ=1.4, R=287", color=YELLOW, fontsize=9, transform=ax2.transAxes)
y -= 0.16
for name, val in lines:
    ax2.text(0.0, y, name, color="#9fb2d6", fontsize=8.5, transform=ax2.transAxes)
    ax2.text(0.0, y-0.07, val, color="white", fontsize=10, transform=ax2.transAxes)
    y -= 0.17
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.16, 0.17, 0.80, 0.78]); draw_curve(axc, P0, T0, A, Pb)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "チョーク流れ", "", "収束ノズルの臨界条件と最大質量流量", cc)
os.remove(cc)

# gif: sweep Pb from high to low; marker slides, curve fixed
frames = []
pbs = list(range(480, 10, -30)) + list(range(20, 490, 30))
for pbv in pbs:
    f2 = plt.figure(figsize=(5.4, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.15, 0.17, 0.81, 0.72])
    draw_curve(a, P0, T0, A, pbv*1e3)
    ch = "CHOKED" if (pbv*1e3/P0) <= rc else "亜音速"
    a.set_title(f"Pb={pbv} kPa  (Pb/P0={pbv*1e3/P0:.2f})  →  {ch}",
                color="white", fontsize=9.5)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=110)
print("done.")
