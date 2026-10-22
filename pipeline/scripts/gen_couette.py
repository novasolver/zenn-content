# -*- coding: utf-8 -*-
"""Couette flow visuals. Velocity profile u(y)=Uy/h - (1/2mu)dpdx y(h-y).
Faithful to tool: water rho=1000; defaults U=1 m/s, h=2mm, mu=0.001, dpdx=0."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "couette-flow"
NAVY = "#0a1929"
BLUE, GRAY, RED = "#00B4D8", "#c8c8c8", "#ff6b6b"
U, H, MU = 1.0, 2e-3, 0.001  # SI

def prof(yrel, dpdx):
    y = H*yrel
    u = U*(y/H) - (1/(2*MU))*dpdx*y*(H-y)
    return u/U  # normalized u/U

def draw_profile(ax, dpdx, title=None, legend=True):
    ax.set_facecolor(NAVY)
    yr = np.linspace(0, 1, 200)
    uN = np.array([prof(y, dpdx) for y in yr])
    # pure couette reference (dpdx=0) = straight line y
    ax.plot(yr, yr, color=GRAY, ls="--", lw=1.6, label="純粋クェット (直線)")
    ax.plot(yr, uN, color=BLUE, lw=2.8, label="合成プロファイル")
    # reverse-flow shading
    if (uN < 0).any():
        ax.fill_between(yr, np.minimum(uN, 0), 0, color=RED, alpha=0.18)
    ax.axhline(0, color="#3b4a6b", lw=1)
    ax.set_xlabel("y / h", color="white", fontsize=9)
    ax.set_ylabel("u / U", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.grid(True, color="#22344f", lw=0.6)
    ax.set_xlim(0, 1)
    if legend:
        ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white",
                  fontsize=7.5, loc="upper left")
    if title: ax.set_title(title, color="white", fontsize=10)

# verified numbers
tau = MU*U/H
Qp = U*H/2
Re = 1000*U*H/MU
print(f"tau={tau:.3f} Pa  Q'={Qp:.2e}  Re={Re:.0f}  rev_onset={2*MU*U/H**2:.0f} Pa/m")

# closeup: three profiles (dp/dx = 0, 1000, 2000) side by side
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
for i, dp in enumerate([0, 1000, 2000]):
    ax = fig.add_axes([0.07 + i*0.32, 0.16, 0.26, 0.72])
    draw_profile(ax, dp, f"dp/dx = {dp} Pa/m", legend=(i == 0))
    if i > 0:
        ax.set_ylabel("")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.16, 0.17, 0.80, 0.78]); draw_profile(axc, 1500)
axc.get_legend().remove()
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "クェット流れ", "", "平行平板間の粘性流とポアズイユ合成", cc)
os.remove(cc)

# gif: sweep dp/dx from -2000 to +2000 and back
frames = []
dps = list(range(-2000, 2001, 200)) + list(range(1800, -2001, -200))
for dp in dps:
    f2 = plt.figure(figsize=(5.2, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.16, 0.17, 0.80, 0.72])
    draw_profile(a, dp, legend=False)
    tag = "逆流あり" if dp > 500 else ("純粋クェット" if dp == 0 else "")
    a.set_title(f"dp/dx = {dp} Pa/m   {tag}", color="white", fontsize=10)
    a.set_ylim(-0.45, 1.15)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=100)
print("done.")
