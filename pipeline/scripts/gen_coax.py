# -*- coding: utf-8 -*-
"""Coaxial cable impedance visuals. Z0=(60/sqrt(er))*ln(b/a).
Faithful to the tool: a=0.5mm,b=3.5mm,er=2.3 default; Z0 vs b/a curves + cross-section."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import figlib

SLUG = "coaxial-cable-impedance"
NAVY = "#0a1929"
ACCENT, CYAN, GOLD, RED, GREEN = "#007BFF", "#00B4D8", "#FFD166", "#e74c3c", "#7da6cc"

def z0(ba, er):
    return (60/np.sqrt(er))*np.log(ba)

def draw_curve(ax, cur_ba=7.0, cur_er=2.3, title=None, legend=True):
    ax.set_facecolor(NAVY)
    ba = np.logspace(np.log10(1.5), np.log10(12), 200)
    ers = [(1.0, CYAN, "εr=1.0 (空気)"), (2.3, GREEN, "εr=2.3 (PE/PTFE)"),
           (4.5, GOLD, "εr=4.5"), (9.0, "#e17055", "εr=9.0")]
    for er, col, lab in ers:
        ax.plot(ba, z0(ba, er), color=col, lw=2.2, label=lab)
    # 50/75 reference lines
    ax.axhline(50, color="#FFD166", ls="--", lw=1.4, alpha=0.8)
    ax.axhline(75, color="#e74c3c", ls="--", lw=1.4, alpha=0.8)
    ax.text(11.5, 52, "50 Ω", color="#FFD166", fontsize=8, ha="right")
    ax.text(11.5, 77, "75 Ω", color="#e74c3c", fontsize=8, ha="right")
    # current point
    zc = z0(cur_ba, cur_er)
    ax.plot([cur_ba], [zc], "o", color=RED, ms=9, mec="white", mew=1.4, zorder=5)
    ax.set_xscale("log")
    ax.set_xlim(1.5, 12); ax.set_ylim(0, 130)
    ax.set_xlabel("b / a (log)", color="white", fontsize=9)
    ax.set_ylabel("特性インピーダンス Z₀ [Ω]", color="white", fontsize=9)
    ax.set_xticks([2, 3, 5, 7, 10]); ax.set_xticklabels(["2", "3", "5", "7", "10"])
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if legend:
        ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="upper left")
    if title: ax.set_title(title, color="white", fontsize=10)

def draw_section(ax, a=0.5, b=3.5, title=None):
    ax.set_facecolor(NAVY)
    ax.add_patch(Circle((0, 0), b*1.18, color="#b1bcc7", zorder=1))
    ax.add_patch(Circle((0, 0), b, color="#f3d56b", zorder=2))
    ax.add_patch(Circle((0, 0), a, color="#d99560", zorder=3))
    for r in (b*1.18, b, a):
        ax.add_patch(Circle((0, 0), r, fill=False, ec="#0a1929", lw=1, zorder=4))
    ax.annotate("", xy=(a, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="#0a1929", lw=1.3), zorder=5)
    ax.annotate("", xy=(b*np.cos(np.pi*0.78), b*np.sin(np.pi*0.78)), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="#0a1929", lw=1.3), zorder=5)
    ax.text(a*0.5, 0.25, "a", color="#0a1929", fontsize=11, ha="center", fontweight="bold")
    ax.text(b*np.cos(np.pi*0.78)*0.55-0.4, b*np.sin(np.pi*0.78)*0.55, "b",
            color="#0a1929", fontsize=11, ha="center", fontweight="bold")
    lim = b*1.35
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal"); ax.axis("off")
    ax.text(0, -lim*0.92, f"a={a} mm  b={b} mm  b/a={b/a:.1f}", color="#cfe3f7",
            fontsize=8, ha="center", family="monospace")
    if title: ax.set_title(title, color="white", fontsize=10)

# verify printout
print(f"default a0.5 b3.5 er2.3: Z0={z0(7.0,2.3):.2f}  VF={1/np.sqrt(2.3):.3f}")

# ---- closeup: cross-section + Z0 curve ----
fig = plt.figure(figsize=(9.6, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.04, 0.10, 0.38, 0.80]); draw_section(ax1, 0.5, 3.5, "同軸断面 (内導体・誘電体・外導体)")
ax2 = fig.add_axes([0.52, 0.16, 0.45, 0.74]); draw_curve(ax2, 7.0, 2.3, "Z₀ vs b/a（赤丸＝既定 b/a=7, εr=2.3）")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.4, 3.3)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.16, 0.16, 0.80, 0.78]); draw_curve(axc, 7.0, 2.3, legend=False)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "同軸ケーブルの", "特性インピーダンス", "Z₀=(60/√εr)·ln(b/a) — 50Ω と 75Ω", cc)
os.remove(cc)

# ---- gif: sweep b/a, current point rides the curve ----
frames = []
seq = list(np.linspace(2.0, 11.0, 14)) + list(np.linspace(11.0, 2.0, 14))
for ba in seq:
    f2 = plt.figure(figsize=(5.4, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.15, 0.17, 0.82, 0.72]); draw_curve(a, ba, 2.3, legend=False)
    a.set_title(f"b/a={ba:.1f}  →  Z₀={z0(ba,2.3):.1f} Ω (εr=2.3)", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=110)
print("done.")
