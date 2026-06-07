# -*- coding: utf-8 -*-
"""Beam deflection visuals (Euler-Bernoulli). Faithful to the tool's formulas:
ss+UDL w=qx(L^3-2Lx^2+x^3)/(24EI); M=qx(L-x)/2."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "beam-deflection"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"
E, I, L, q = 200e9, 1e-6, 2.0, 10e3   # tool defaults

def ss_udl(x): return q * x * (L**3 - 2*L*x*x + x**3) / (24*E*I)
def moment(x): return q * x * (L - x) / 2

x = np.linspace(0, L, 200)
w = ss_udl(x) * 1000   # mm
M = moment(x) / 1000   # kN.m
dmax = w.max(); Mmax = M.max()
print(f"ss+UDL: delta_center={ss_udl(L/2)*1000:.3f}mm (5qL^4/384EI={5*q*L**4/(384*E*I)*1000:.3f}); M_max={moment(L/2)/1000:.2f}kN.m")

# closeup: deformed beam + moment diagram
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.08, 0.55, 0.86, 0.36]); ax1.set_facecolor(NAVY)
# undeformed
ax1.plot([0, L], [0, 0], color="#3b4a6b", lw=1.2, ls="--")
# distributed load arrows
for xi in np.linspace(0.05, L-0.05, 11):
    ax1.annotate("", xy=(xi, 0.05), xytext=(xi, 0.55), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1))
ax1.plot(x, -w / dmax * 0.5, color=CYAN, lw=2.5)   # deflection (down, exaggerated)
ax1.plot(0, 0, "^", color="white", ms=12); ax1.plot(L, 0, "o", color="white", ms=10)
ax1.set_xlim(-0.15, L+0.15); ax1.set_ylim(-0.75, 0.65); ax1.axis("off")
ax1.set_title(f"単純支持梁＋等分布荷重：たわみ曲線（δ_max={dmax:.2f}mm を誇張表示）", color="white", fontsize=9)
ax2 = fig.add_axes([0.10, 0.13, 0.84, 0.32]); ax2.set_facecolor(NAVY)
ax2.fill_between(x, M, color=ORANGE, alpha=0.25); ax2.plot(x, M, color=ORANGE, lw=2)
ax2.set_xlabel("位置 x (m)", color="white", fontsize=9); ax2.set_ylabel("曲げモーメント M (kN·m)", color="white", fontsize=8)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title(f"曲げモーメント図 M(x)＝qx(L−x)/2（最大 {Mmax:.1f} kN·m）", color="white", fontsize=9)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.0)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.04, 0.10, 0.92, 0.8]); axc.set_facecolor(NAVY)
axc.plot([0, L], [0, 0], color="#3b4a6b", lw=1.2, ls="--")
for xi in np.linspace(0.05, L-0.05, 11):
    axc.annotate("", xy=(xi, 0.05), xytext=(xi, 0.5), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1))
axc.plot(x, -w/dmax*0.5, color=CYAN, lw=2.6)
axc.plot(0, 0, "^", color="white", ms=12); axc.plot(L, 0, "o", color="white", ms=10)
axc.set_ylim(-0.7, 0.6); axc.axis("off")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "梁のたわみと", "曲げモーメント", "Euler-Bernoulli δ=5qL⁴/384EI を可視化", cc)
os.remove(cc)

# gif: increasing load
frames = []
for qf in list(np.linspace(2e3, 20e3, 22)) + list(np.linspace(19e3, 3e3, 12)):
    wf = qf * x * (L**3 - 2*L*x*x + x**3) / (24*E*I) * 1000
    dm = wf.max()
    f2 = plt.figure(figsize=(5.4, 2.8)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.04, 0.10, 0.92, 0.78]); a.set_facecolor(NAVY)
    a.plot([0, L], [0, 0], color="#3b4a6b", lw=1.2, ls="--")
    a.plot(x, -wf, color=CYAN, lw=2.5)
    a.plot(0, 0, "^", color="white", ms=11); a.plot(L, 0, "o", color="white", ms=9)
    a.set_xlim(-0.15, L+0.15); a.set_ylim(-45, 8); a.axis("off")
    a.set_title(f"等分布荷重 q={qf/1000:.0f} kN/m  →  δ_max={dm:.2f} mm", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
