# -*- coding: utf-8 -*-
"""Fourier series / Gibbs visuals. Coefficients exactly as the tool:
square bn=4A/(n pi) odd, triangle 8A/(n^2 pi^2) sin(n pi/2), sawtooth -2A/(n pi)(-1)^n."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "fourier-series"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; GREY = "#9fb2d6"

def bn(kind, n, A=1.0):
    if kind == "square": return 4 * A / (n * np.pi) if n % 2 == 1 else 0.0
    if kind == "triangle": return 8 * A / (n * n * np.pi**2) * np.sin(n * np.pi / 2)
    if kind == "sawtooth": return -2 * A / (n * np.pi) * (-1)**n
    return 0.0

def partial(kind, N, t, A=1.0):
    s = np.zeros_like(t)
    for n in range(1, N + 1):
        s += bn(kind, n, A) * np.sin(2 * np.pi * n * t)
    return s

def exact(kind, t, A=1.0):
    tp = np.mod(t, 1)
    if kind == "square": return np.where(tp < 0.5, A, -A)
    if kind == "sawtooth": return A * (2 * tp - 1)
    return np.where(tp < 0.25, 4*A*tp, np.where(tp < 0.75, A - 4*A*(tp-0.25), -A + 4*A*(tp-0.75)))

t = np.linspace(0, 1, 2000)
ps = partial("square", 12, t)
overshoot = (ps.max() - 1) * 100
print(f"square N=12: max={ps.max():.3f}, overshoot vs A={overshoot:.1f}% (= jump 2A * ~8.95%)")

# closeup: partial vs exact (Gibbs) + spectrum bars
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.06, 0.14, 0.55, 0.76]); ax1.set_facecolor(NAVY)
ax1.plot(t, exact("square", t), color=GREY, lw=1.2, ls="--", label="厳密な方形波")
ax1.plot(t, ps, color=CYAN, lw=1.8, label="部分和 N=12")
ax1.axhline(1, color="#3b4a6b", lw=0.7); ax1.axhline(ps.max(), color=ORANGE, lw=0.7, ls=":")
ax1.annotate(f"ギブス\nオーバーシュート\n+{overshoot:.0f}%（振幅比）",
             xy=(0.5, ps.max()), xytext=(0.62, 1.35), color=ORANGE, fontsize=8,
             arrowprops=dict(arrowstyle="->", color=ORANGE))
ax1.set_ylim(-1.6, 1.7); ax1.set_xlim(0, 1)
ax1.set_xlabel("t (周期)", color="white", fontsize=9); ax1.tick_params(colors=GREY, labelsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="lower right")
ax1.set_title("方形波の部分和とギブス現象", color="white", fontsize=10)
ax2 = fig.add_axes([0.70, 0.16, 0.27, 0.72]); ax2.set_facecolor(NAVY)
ns = np.arange(1, 13); bns = [abs(bn("square", n)) for n in ns]
ax2.bar(ns, bns, color=CYAN)
ax2.set_xlabel("高調波 n", color="white", fontsize=9); ax2.set_ylabel("|bn|", color="white", fontsize=9)
ax2.tick_params(colors=GREY, labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("方形波の係数 4/(nπ)（奇数のみ）", color="white", fontsize=9)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.04, 0.08, 0.92, 0.84]); axc.set_facecolor(NAVY)
axc.plot(t, exact("square", t), color=GREY, lw=1, ls="--")
axc.plot(t, partial("square", 8, t), color=CYAN, lw=1.6)
axc.plot(t, partial("square", 30, t), color=ORANGE, lw=1.6, alpha=0.8)
axc.set_ylim(-1.5, 1.6); axc.axis("off")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "フーリエ級数と", "ギブス現象", "方形波を高調波で合成、約9%の行き過ぎ", cc)
os.remove(cc)

# gif: increase N, overshoot persists
frames = []
for Nh in list(range(1, 30)) + list(range(29, 1, -2)):
    ps = partial("square", Nh, t); ov = (ps.max() - 1) * 100
    f2 = plt.figure(figsize=(5.4, 3.0)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.05, 0.10, 0.92, 0.80]); a.set_facecolor(NAVY)
    a.plot(t, exact("square", t), color=GREY, lw=1, ls="--")
    a.plot(t, ps, color=CYAN, lw=1.8)
    a.set_ylim(-1.6, 1.7); a.set_xlim(0, 1); a.set_xticks([]); a.set_yticks([])
    a.set_title(f"N={Nh}  ギブス行き過ぎ +{ov:.0f}%（振幅比、≈ジャンプの9%）", color="white", fontsize=9)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
