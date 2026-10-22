# -*- coding: utf-8 -*-
"""Snell's law visuals. n1 sin th1 = n2 sin th2; critical angle asin(n2/n1).
Ray diagram + theta2-theta1 curve + TIR. Faithful to the tool."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "snells-law"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; RED = "#ff6b6b"; GREEN = "#9be7a3"

def ray_diagram(ax, n1, n2, th1deg, title=None):
    ax.set_facecolor(NAVY)
    ax.axhspan(0, 1.1, color="#13233f", alpha=0.7)        # medium 1
    ax.axhspan(-1.1, 0, color="#1d3a5c", alpha=0.7)       # medium 2
    ax.axhline(0, color="#9fb2d6", lw=1.5)                 # interface
    ax.axvline(0, color="#3b4a6b", lw=1, ls="--")          # normal
    th1 = np.radians(th1deg)
    s2 = n1 / n2 * np.sin(th1); tir = s2 > 1.0
    # incident (from upper-left to origin)
    ax.annotate("", xy=(0, 0), xytext=(-np.sin(th1), np.cos(th1)),
                arrowprops=dict(arrowstyle="-|>", color=CYAN, lw=2.2))
    # reflected (upper-right)
    ax.annotate("", xy=(np.sin(th1), np.cos(th1)), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#9fb2d6", lw=1.4))
    if not tir:
        th2 = np.arcsin(s2)
        ax.annotate("", xy=(np.sin(th2), -np.cos(th2)), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.2))
        ax.text(np.sin(th2)+0.05, -np.cos(th2), f"屈折 θ₂={np.degrees(th2):.1f}°", color=ORANGE, fontsize=8)
    else:
        ax.text(0.3, -0.5, "全反射 (TIR)", color=RED, fontsize=10)
    ax.text(-np.sin(th1)-0.05, np.cos(th1), f"入射 θ₁={th1deg:.0f}°", color=CYAN, fontsize=8, ha="right")
    ax.text(-1.05, 0.95, f"媒質1  n₁={n1}", color=CYAN, fontsize=8)
    ax.text(-1.05, -1.02, f"媒質2  n₂={n2}", color=ORANGE, fontsize=8)
    ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.12, 1.12); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if title: ax.set_title(title, color="white", fontsize=10)

def curve(ax):
    ax.set_facecolor(NAVY)
    t1 = np.linspace(0, 89, 300)
    # air->glass (n1<n2): always refracts
    s2 = 1.0/1.5*np.sin(np.radians(t1)); t2 = np.degrees(np.arcsin(s2))
    ax.plot(t1, t2, color=ORANGE, lw=2, label="空気→ガラス (n1<n2)")
    # glass->air (n1>n2): TIR beyond critical
    s2b = 1.5/1.0*np.sin(np.radians(t1)); valid = s2b <= 1
    t2b = np.degrees(np.arcsin(np.clip(s2b, 0, 1)))
    ax.plot(t1[valid], t2b[valid], color=CYAN, lw=2, label="ガラス→空気 (n1>n2)")
    thc = np.degrees(np.arcsin(1/1.5))
    ax.axvline(thc, color=RED, lw=1.2, ls="--")
    ax.text(thc+1, 30, f"臨界角\nθc={thc:.1f}°\n→全反射", color=RED, fontsize=8)
    ax.plot([0, 89], [0, 89], color="#3b4a6b", lw=0.8, ls=":")
    ax.set_xlabel("入射角 θ₁ (°)", color="white", fontsize=9); ax.set_ylabel("屈折角 θ₂ (°)", color="white", fontsize=9)
    ax.set_xlim(0, 89); ax.set_ylim(0, 90); ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="upper left")

print(f"air->glass th1=40: th2={np.degrees(np.arcsin(1/1.5*np.sin(np.radians(40)))):.1f}; glass->air thc={np.degrees(np.arcsin(1/1.5)):.1f}")

# closeup
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.04, 0.08, 0.42, 0.82]); ray_diagram(ax1, 1.0, 1.5, 40, "光線図（空気→ガラス）")
ax2 = fig.add_axes([0.57, 0.16, 0.40, 0.72]); curve(ax2)
ax2.set_title("屈折角 vs 入射角と臨界角", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(4.8, 3.4)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.04, 0.04, 0.92, 0.92]); ray_diagram(axc, 1.0, 1.5, 40)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "スネルの法則と", "全反射", "n₁sinθ₁=n₂sinθ₂ と臨界角を可視化", cc)
os.remove(cc)

# gif: glass->air sweep incidence, refraction -> TIR
frames = []
for th1 in list(range(0, 80, 3)) + list(range(78, 0, -3)):
    f2 = plt.figure(figsize=(4.6, 4.2)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.04, 0.06, 0.92, 0.86]); ray_diagram(a, 1.5, 1.0, th1)
    s2 = 1.5*np.sin(np.radians(th1))
    a.set_title(f"ガラス→空気 θ₁={th1}°" + ("  ★全反射" if s2 > 1 else ""), color="white", fontsize=9)
    frames.append(figlib.fig_to_pil(f2, dpi=88))
figlib.save_gif(frames, SLUG, duration=100)
print("done.")
