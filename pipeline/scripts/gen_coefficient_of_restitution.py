# -*- coding: utf-8 -*-
"""Coefficient of restitution visuals. Faithful to coefficient-of-restitution.html:
v0=sqrt(2gh); hn=h*e^(2n); T=(2v0/g)(1+e)/(1-e); D=h(1+e^2)/(1-e^2)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "coefficient-of-restitution"
NAVY = "#0a1929"
CYAN, RED, ORANGE, GREEN, YELLOW = "#00B4D8", "#ff8c8c", "#f59e0b", "#a0ffa0", "#FFD166"
G = 9.81


def vimpact(g, h): return math.sqrt(2 * g * h)
def hn(h, e, n): return h * e ** (2 * n)


def style_ax(ax, xl, yl, title=None):
    ax.set_facecolor(NAVY)
    ax.set_xlabel(xl, color="white", fontsize=9)
    ax.set_ylabel(yl, color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values():
        sp.set_color("#3b4a6b")
    ax.grid(True, color="#22324d", lw=0.6)
    if title:
        ax.set_title(title, color="white", fontsize=10)


def decay_axes(ax, h, hl_e, ns=np.arange(0, 31)):
    refs = [(0.5, RED, "e=0.50"), (0.7, ORANGE, "e=0.70"), (0.9, GREEN, "e=0.90")]
    for ev, c, lab in refs:
        ax.plot(ns, h * ev ** (2 * ns), color=c, lw=1.4, alpha=0.6, label=lab)
    ax.plot(ns, h * hl_e ** (2 * ns), color=CYAN, lw=2.6, label=f"e={hl_e:.2f}（現在）")
    ax.scatter([5], [h * hl_e ** (2 * 5)], color=YELLOW, s=50, zorder=5)
    style_ax(ax, "跳ね回数 n", "跳ね高さ h_n (m)")


# ---- closeup: bounce trajectory + decay curve ----
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
h, e, n = 2.0, 0.8, 5

# left: bounce arcs (apex heights h*e^(2i))
ax1 = fig.add_axes([0.07, 0.15, 0.52, 0.74])
hs = [h] + [hn(h, e, i) for i in range(1, n + 1)]
x = 0.0
for i, hh in enumerate(hs):
    if i == 0:
        ax1.plot([0, 0], [0, hh], color=CYAN, lw=2)
        ax1.scatter([0], [hh], color=YELLOW, s=30)
        ax1.text(0, hh + 0.05, f"{hh:.2f}", color="white", ha="center", fontsize=8)
        x = 1.0
    else:
        xa, xb = x - 1.0, x
        tt = np.linspace(0, 1, 40)
        arc = hh * (1 - 4 * (tt - 0.5) ** 2)
        ax1.plot(xa + (xb - xa) * tt, arc, color=CYAN, lw=1.8, alpha=0.85)
        ax1.scatter([(xa + xb) / 2], [hh], color=YELLOW, s=22)
        if hh > 0.04:
            ax1.text((xa + xb) / 2, hh + 0.04, f"{hh:.3f}", color="#cfe3f7", ha="center", fontsize=7.5)
        x += 1.0
ax1.axhline(0, color="#6b4f2a", lw=4)
style_ax(ax1, "跳ね（左から順に n 回）", "高さ (m)", "跳ねる軌跡（h=2 m, e=0.80）")
ax1.set_ylim(-0.05, h * 1.15)

# right: decay curves
ax2 = fig.add_axes([0.67, 0.15, 0.30, 0.74])
decay_axes(ax2, h, e)
ax2.set_title("幾何級数減衰", color="white", fontsize=10)
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.15, 0.16, 0.81, 0.78])
decay_axes(axc, 2.0, 0.8)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "反発係数 e と", "跳ね返りの減衰", "h_n = h·e^(2n) と無限級数の収束", cc)
os.remove(cc)

# ---- gif: sweep e, watch decay curve change ----
frames = []
e_list = [round(v, 2) for v in list(np.arange(0.40, 0.96, 0.06)) + list(np.arange(0.94, 0.40, -0.06))]
ns = np.arange(0, 31)
for ev in e_list:
    f2 = plt.figure(figsize=(5.2, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.15, 0.17, 0.81, 0.70])
    a.plot(ns, 2.0 * ev ** (2 * ns), color=CYAN, lw=2.8)
    a.fill_between(ns, 0, 2.0 * ev ** (2 * ns), color=CYAN, alpha=0.12)
    style_ax(a, "跳ね回数 n", "跳ね高さ h_n (m)")
    a.set_ylim(0, 2.1)
    v0 = vimpact(G, 2.0)
    T = (2 * v0 / G) * (1 + ev) / (1 - ev)
    a.set_title(f"e={ev:.2f} → 全跳ね時間 T={T:.1f}s", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=120)
print("done.")
