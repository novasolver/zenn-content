# -*- coding: utf-8 -*-
"""Doppler effect visuals. Tool computes f_obs = f0(v+vo)/(v-vs) and draws
circular wavefronts + Mach cone. Reproduced faithfully with matplotlib."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import figlib

SLUG = "doppler-effect"
NAVY = "#0b1020"; ORANGE = "#f59e0b"; CYAN = "#7dd3fc"; RED = "#ff6b6b"

def wavefronts(ax, Ma=0.6, v=1.0, Temit=0.62, K=11, tnow=7.5, title=None):
    ax.set_facecolor(NAVY)
    vs = Ma * v
    for k in range(K):
        tk = k * Temit
        if tk > tnow: break
        xk = vs * tk
        r = v * (tnow - tk)
        col = CYAN
        ax.add_patch(Circle((xk, 0), r, fill=False, ec=col, lw=1.1, alpha=0.8))
    xsrc = vs * tnow
    ax.plot(xsrc, 0, "o", color=ORANGE, ms=11, zorder=5)
    # observer ahead
    ax.plot(xsrc + v * tnow * 0.55, 0, "s", color="#9be7a3", ms=9, zorder=5)
    ax.annotate("", xy=(xsrc + 0.9, 0), xytext=(xsrc, 0),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6))
    lim = v * tnow * 1.15
    ax.set_xlim(-lim * 0.7, lim); ax.set_ylim(-lim * 0.62, lim * 0.62)
    ax.set_aspect("equal"); ax.axis("off")
    ax.text(0.02, 0.95, f"音源 Ma = vs/v = {Ma:.1f}\n前方=圧縮(高音) / 後方=伸長(低音)",
            transform=ax.transAxes, color="white", fontsize=9, va="top")
    if title: ax.set_title(title, color="white", fontsize=11)

def fcurve(ax, v=340.0, f0=440.0):
    ax.set_facecolor(NAVY)
    vs = np.linspace(0, 0.95 * v, 200)
    fa = f0 * v / (v - vs); fr = f0 * v / (v + vs)
    ax.plot(vs / v, fa / f0, color=RED, lw=2.2, label="近づく f0·v/(v−vs)")
    ax.plot(vs / v, fr / f0, color=CYAN, lw=2.2, label="遠ざかる f0·v/(v+vs)")
    ax.axhline(1, color="#9fb2d6", lw=1, ls="--")
    ax.scatter([0.5], [f0 * v / (v - 0.5 * v) / f0], s=70, color="#FFD166", ec="white", zorder=6)
    ax.text(0.5, 2.05, "Ma=0.5→2倍", color="#FFD166", fontsize=8, ha="center")
    ax.set_xlabel("音源マッハ数 vs/v", color="white", fontsize=9)
    ax.set_ylabel("観測周波数比 f/f0", color="white", fontsize=9)
    ax.set_xlim(0, 1); ax.set_ylim(0, 5)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="upper left")

# closeup
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.01, 0.05, 0.52, 0.9]); wavefronts(ax1, title="移動する音源の波面（前が詰まる）")
ax2 = fig.add_axes([0.62, 0.16, 0.35, 0.74]); fcurve(ax2)
ax2.set_title("観測周波数は速度で変わる", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.0, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.0, 0.0, 1.0, 1.0]); wavefronts(axc, Ma=0.6)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ドップラー効果", "", "f = f0(v±vo)/(v∓vs) を波面で可視化", cc)
os.remove(cc)

# gif: source moving, wavefronts emitted continuously (subsonic)
frames = []
v = 1.0; Ma = 0.6; Temit = 0.62
for fr in range(48):
    tnow = 1.0 + fr * 0.22
    f2 = plt.figure(figsize=(5.2, 3.4)); f2.patch.set_facecolor(NAVY)
    a2 = f2.add_axes([0.0, 0.0, 1.0, 1.0])
    wavefronts(a2, Ma=Ma, v=v, Temit=Temit, K=int(tnow / Temit) + 1, tnow=tnow)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=90)
print("done.")
