# -*- coding: utf-8 -*-
"""Thin-lens ray tracer visuals. 1/f=1/do+1/di, m=-di/do, 3 principal rays.
Faithful to the tool (mm units, sign conventions). Draws dashed back-extensions
for virtual images."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "lens-ray-tracer"
NAVY = "#0b1020"; RED = "#ff6b6b"; GREEN = "#51cf66"; YEL = "#fcc419"; CYAN = "#7dd3fc"

def thin_lens(f, do):
    if abs(do - f) < 1e-6: return 1e9, 1e9
    di = f * do / (do - f); return di, -di / do

def draw_lens(ax, f, do, ho, xR=340, title=None):
    ax.set_facecolor(NAVY)
    di, m = thin_lens(f, do); hi = m * ho
    real = di > 0
    lh = max(abs(ho) * 1.5, abs(hi) * 1.2, 55)
    ax.axhline(0, color="#3b4a6b", lw=1)
    ax.plot([0, 0], [-lh, lh], color=CYAN, lw=3, alpha=0.85)              # lens
    ax.plot([0], [lh], marker=("^" if f > 0 else "v"), color=CYAN, ms=8)
    ax.plot([0], [-lh], marker=("v" if f > 0 else "^"), color=CYAN, ms=8)
    for fx, lbl in [(f, "F'"), (-f, "F")]:
        ax.plot(fx, 0, "o", color="white", ms=4)
        ax.text(fx, -lh * 0.16, lbl, color="white", fontsize=9, ha="center")
    ax.annotate("", xy=(-do, ho), xytext=(-do, 0),
                arrowprops=dict(arrowstyle="-|>", color="#9be7a3", lw=2.5))  # object

    # exit points & slopes of the 3 principal rays (all pass through (di,hi))
    y3 = ho * (-f) / (do - f)                 # ray-B height at lens (through F)
    rays = [
        (RED,   ho, -ho / f),                 # parallel in -> through F'
        (YEL,   0.0, -ho / do),               # through center, undeviated
        (GREEN, y3,  0.0),                     # through F -> parallel out
    ]
    # incoming segments to the lens
    ax.plot([-do, 0], [ho, ho], color=RED, lw=1.2)
    ax.plot([-do, 0], [ho, 0.0], color=YEL, lw=1.2)
    ax.plot([-do, 0], [ho, y3], color=GREEN, lw=1.2)
    for col, y0, sl in rays:
        ax.plot([0, xR], [y0, y0 + sl * xR], color=col, lw=1.2)            # outgoing forward
        if not real:                                                      # dashed back-extension
            ax.plot([0, di], [y0, y0 + sl * di], color=col, lw=1.0, ls=(0, (4, 3)), alpha=0.7)
    # image arrow
    ax.annotate("", xy=(di, hi), xytext=(di, 0),
                arrowprops=dict(arrowstyle="-|>", color="#ffd166", lw=2.5,
                                linestyle=("solid" if real else "dashed")))
    ax.text(di, hi + np.sign(hi) * 9, ("実像" if real else "虚像"),
            color="#ffd166", fontsize=9, ha="center")

    left = min(-do, di) - 30; right = max(xR, di + 30)
    ax.set_xlim(left, right); ax.set_ylim(-lh * 1.2, lh * 1.2)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if title: ax.set_title(title, color="white", fontsize=10)
    return di, m

# closeup: converging real image + magnifier virtual
fig = plt.figure(figsize=(9.8, 4.4)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.03, 0.10, 0.45, 0.80])
di1, m1 = draw_lens(ax1, 100, 200, 40, xR=300, title="凸レンズ・実像 (do=200,f=100 → di=200, m=−1)")
ax2 = fig.add_axes([0.54, 0.10, 0.44, 0.80])
di2, m2 = draw_lens(ax2, 50, 40, 30, xR=140, title="虫眼鏡・虚像 (do=40,f=50 → di=−200, m=+5)")
print(f"real: di={di1:.0f} m={m1:.2f} | magnifier: di={di2:.0f} m={m2:.2f}")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.4, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.03, 0.05, 0.94, 0.90]); draw_lens(axc, 100, 200, 40, xR=300)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "薄肉レンズ光線追跡", "", "1/f=1/do+1/di と主光線3本を可視化", cc)
os.remove(cc)

# gif: sweep object distance, image moves/flips real<->virtual
frames = []
f = 80.0
dos = np.concatenate([np.linspace(280, 92, 24), np.linspace(92, 36, 16)])
for do in dos:
    f2 = plt.figure(figsize=(5.6, 3.2)); f2.patch.set_facecolor(NAVY)
    a2 = f2.add_axes([0.03, 0.05, 0.94, 0.88])
    di, m = draw_lens(a2, f, do, 34, xR=320)
    typ = "実像(倒立)" if di > 0 else "虚像(正立)"
    a2.set_title(f"do={do:.0f}mm  di={di:.0f}mm  m={m:+.2f}x  {typ}", color="white", fontsize=9)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=110)
print("done.")
