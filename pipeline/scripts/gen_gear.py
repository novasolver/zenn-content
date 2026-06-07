# -*- coding: utf-8 -*-
"""Gear ratio visuals. i=Z2/Z1, n_out=n_in/i, T_out=T_in*i*eta. Meshing gears
(counter-rotating, output slower) + speed-torque trade-off. Faithful to the tool."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "gear-ratio"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"
z1, z2 = 20, 40
n1, t1, eta = 1500, 10.0, 0.98
i = z2/z1; nout = n1/i; tout = t1*i*eta; P = t1*2*np.pi*n1/60
print(f"i={i} nout={nout:.0f}rpm tout={tout:.1f}Nm P={P:.0f}W")

def gear_poly(cx, cy, R, N, angle):
    pts = []
    for k in range(N*2):
        a = angle + np.pi*k/N
        r = R if k % 2 == 0 else R*0.84
        pts.append((cx + r*np.cos(a), cy + r*np.sin(a)))
    return np.array(pts)

def draw_gears(ax, ang=0.0):
    ax.set_facecolor(NAVY)
    m = 0.08   # module-ish scale
    R1, R2 = z1*m/2, z2*m/2
    cx1, cy1 = 0, 0; cx2, cy2 = R1 + R2, 0
    # driven rotates opposite, slower by z1/z2
    g1 = gear_poly(cx1, cy1, R1, z1, ang)
    g2 = gear_poly(cx2, cy2, R2, z2, -ang*z1/z2 + np.pi/z2)
    ax.fill(g1[:, 0], g1[:, 1], color=CYAN, ec="white", lw=0.8)
    ax.fill(g2[:, 0], g2[:, 1], color=ORANGE, ec="white", lw=0.8)
    ax.add_patch(plt.Circle((cx1, cy1), R1*0.18, color=NAVY, ec="white"))
    ax.add_patch(plt.Circle((cx2, cy2), R2*0.18, color=NAVY, ec="white"))
    ax.annotate("", xy=(cx1+R1*0.5*np.cos(ang), cy1+R1*0.5*np.sin(ang)), xytext=(cx1, cy1),
                arrowprops=dict(arrowstyle="-|>", color="white", lw=1.5))
    ax.text(cx1, -R1-0.12, f"駆動 Z₁={z1}", color=CYAN, ha="center", fontsize=8)
    ax.text(cx2, -R2-0.12, f"従動 Z₂={z2}", color=ORANGE, ha="center", fontsize=8)
    ax.set_xlim(-R1-0.2, cx2+R2+0.2); ax.set_ylim(-R2-0.35, R2+0.25)
    ax.set_aspect("equal"); ax.axis("off")

# closeup: gears + speed/torque trade-off
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.02, 0.05, 0.56, 0.86]); draw_gears(ax1)
ax1.set_title(f"噛み合う歯車（歯車比 i = Z₂/Z₁ = {i:.0f}）", color="white", fontsize=10)
ax2 = fig.add_axes([0.66, 0.16, 0.31, 0.70]); ax2.set_facecolor(NAVY)
labels = ["回転数\n(rpm)", "トルク\n(N·m)"]
inp = [n1, t1]; outp = [nout, tout]
x = np.arange(2)
ax2.bar(x-0.2, [1, 1], width=0.4, color=CYAN, label="入力")
ax2.bar(x+0.2, [nout/n1, tout/t1], width=0.4, color=ORANGE, label="出力")
ax2.set_xticks(x); ax2.set_xticklabels(labels, color="white", fontsize=9)
ax2.set_ylabel("入力比", color="white", fontsize=9)
ax2.text(-0.2, 1.03, f"{n1}", color=CYAN, ha="center", fontsize=8)
ax2.text(0.2, nout/n1+0.03, f"{nout:.0f}", color=ORANGE, ha="center", fontsize=8)
ax2.text(0.8, 1.03, f"{t1:.0f}", color=CYAN, ha="center", fontsize=8)
ax2.text(1.2, tout/t1+0.03, f"{tout:.1f}", color=ORANGE, ha="center", fontsize=8)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)
ax2.set_title("減速：回転数↓ トルク↑（i倍）", color="white", fontsize=9.5)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.4, 3.0)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.0, 0.0, 1.0, 0.96]); draw_gears(axc, ang=0.3)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "歯車比と", "回転数・トルク", "i=Z₂/Z₁、回転数↓トルク↑を可視化", cc)
os.remove(cc)

# gif: rotating gears
frames = []
for k in range(40):
    ang = k/40*2*np.pi/z1*4
    f2 = plt.figure(figsize=(5.2, 3.0)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.0, 0.02, 1.0, 0.88]); draw_gears(a, ang=ang)
    a.set_title(f"i={i:.0f}：従動は{1/i:.1f}倍の速さで逆回転", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=70)
print("done.")
