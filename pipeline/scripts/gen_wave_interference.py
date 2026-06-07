# -*- coding: utf-8 -*-
"""Wave interference visuals. Tool: y=y1+y2, y_i=A sin(k_i x - w_i t + phi).
Reproduced with matplotlib (superposition, beats, standing wave)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "wave-interference"
NAVY = "#0b1020"; CYAN = "#00B4D8"; ORANGE = "#e17055"; GREEN = "#2ecc71"
XSPAN = 4.0
x = np.linspace(0, XSPAN, 600)

def wave(A, f, phi, v, t, x=x):
    k = 2 * np.pi * f / v; w = 2 * np.pi * f
    return A * np.sin(k * x - w * t + np.radians(phi))

def panel(ax, y, color, label):
    ax.set_facecolor(NAVY)
    ax.plot(x, y, color=color, lw=2)
    ax.axhline(0, color="#3b4a6b", lw=0.8)
    ax.set_xlim(0, XSPAN); ax.set_ylim(-2.2, 2.2); ax.set_xticks([]); ax.set_yticks([])
    ax.text(0.01, 0.97, label, transform=ax.transAxes, color="white", va="top", fontsize=9)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

# closeup: left stacked (w1,w2,sum=beat); right constructive vs destructive
fig = plt.figure(figsize=(9.6, 4.4)); fig.patch.set_facecolor(NAVY)
t = 0.0
y1 = wave(1, 5, 0, 5, t); y2 = wave(1, 6, 0, 5, t)
ax1 = fig.add_axes([0.04, 0.69, 0.44, 0.25]); panel(ax1, y1, CYAN, "波1: f₁=5 Hz")
ax2 = fig.add_axes([0.04, 0.40, 0.44, 0.25]); panel(ax2, y2, ORANGE, "波2: f₂=6 Hz")
ax3 = fig.add_axes([0.04, 0.07, 0.44, 0.28]); panel(ax3, y1 + y2, GREEN, "合成 y₁+y₂（うなり）")
# envelope of beat
env = 2 * np.abs(np.cos(np.pi * (5 - 6) / 5 * x))  # rough spatial beat env
ax3.plot(x, env, color="white", lw=0.8, ls="--", alpha=0.5)
ax3.plot(x, -env, color="white", lw=0.8, ls="--", alpha=0.5)
# right: constructive vs destructive
yc = wave(1, 5, 0, 5, t) + wave(1, 5, 0, 5, t)
yd = wave(1, 5, 0, 5, t) + wave(1, 5, 180, 5, t)
axr1 = fig.add_axes([0.57, 0.56, 0.40, 0.34]); panel(axr1, yc, GREEN, "同位相 Δφ=0°：強め合い（振幅2A）")
axr2 = fig.add_axes([0.57, 0.12, 0.40, 0.34]); panel(axr2, yd, GREEN, "逆位相 Δφ=180°：弱め合い（≈0）")
axr2.set_ylim(-2.2, 2.2)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover: composite beat
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.03, 0.06, 0.94, 0.88]); axc.set_facecolor(NAVY)
axc.plot(x, y1, color=CYAN, lw=1, alpha=0.5)
axc.plot(x, y2, color=ORANGE, lw=1, alpha=0.5)
axc.plot(x, y1 + y2, color=GREEN, lw=2.4)
axc.axhline(0, color="#3b4a6b", lw=0.8)
axc.set_xlim(0, XSPAN); axc.set_ylim(-2.4, 2.4); axc.axis("off")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "波の干渉・重ね合わせ", "", "うなり・定在波・強め合い/弱め合いを可視化", cc)
os.remove(cc)

# gif: beat animating in time
frames = []
for k in range(48):
    t = k / 48 * 1.0  # 1 s -> 1 full beat (|f1-f2|=1)
    y1 = wave(1, 5, 0, 5, t); y2 = wave(1, 6, 0, 5, t)
    f2 = plt.figure(figsize=(5.4, 3.0)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.03, 0.06, 0.94, 0.88]); a.set_facecolor(NAVY)
    a.plot(x, y1, color=CYAN, lw=0.9, alpha=0.45)
    a.plot(x, y2, color=ORANGE, lw=0.9, alpha=0.45)
    a.plot(x, y1 + y2, color=GREEN, lw=2.4)
    a.axhline(0, color="#3b4a6b", lw=0.8)
    a.set_xlim(0, XSPAN); a.set_ylim(-2.4, 2.4); a.axis("off")
    a.set_title("うなり：f₁=5, f₂=6 Hz → ビート周波数 1 Hz", color="white", fontsize=9)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=85)
print("done.")
