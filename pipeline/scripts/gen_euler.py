# -*- coding: utf-8 -*-
"""Euler buckling visuals. Pcr = pi^2 EI/(KL)^2. End-condition mode shapes +
Pcr-vs-L curve. Faithful to the tool (K=1.0/2.0/0.5/0.7)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "euler-buckling"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"
E = 200e9; d = 0.05; I = np.pi*d**4/64; A = np.pi*d*d/4; r = np.sqrt(I/A)

CASES = [("両端ピン\nK=1.0", 1.0), ("一端固定\n他端自由\nK=2.0", 2.0),
         ("両端固定\nK=0.5", 0.5), ("固定-ピン\nK=0.7", 0.7)]

def mode_shape(K, y):  # y in [0,1]
    if K <= 0.55: return np.sin(2*np.pi*y) * 0.5      # fixed-fixed: S
    if K >= 1.9:  return (1 - np.cos(np.pi/2*y))       # fixed-free: quarter
    if abs(K-0.7) < 0.1: return np.sin(1.43*np.pi*y) * 0.7
    return np.sin(np.pi*y)                              # pinned: half-sine

def draw_modes(ax):
    ax.set_facecolor(NAVY)
    y = np.linspace(0, 1, 100)
    for i, (lbl, K) in enumerate(CASES):
        x0 = i * 1.3
        amp = 0.32
        x = x0 + mode_shape(K, y) * amp
        ax.plot(x, y, color=CYAN, lw=2.5)
        ax.plot([x0, x0], [0, 1], color="#3b4a6b", lw=0.8, ls=":")
        Pcr = np.pi**2*E*I/(K*2.0)**2 / 1000
        ax.text(x0, -0.10, lbl, color="white", ha="center", fontsize=7.5, va="top")
        ax.text(x0, 1.06, f"Pcr={Pcr:.0f}kN", color=ORANGE, ha="center", fontsize=7.5)
    ax.set_xlim(-0.5, 4.4); ax.set_ylim(-0.35, 1.18); ax.axis("off")

# closeup: mode shapes + Pcr-L curve
fig = plt.figure(figsize=(9.6, 4.4)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.02, 0.06, 0.52, 0.84]); draw_modes(ax1)
ax1.set_title("端末条件で座屈モードと臨界荷重が変わる（L=2m）", color="white", fontsize=10)
ax2 = fig.add_axes([0.62, 0.16, 0.35, 0.72]); ax2.set_facecolor(NAVY)
Ls = np.linspace(0.5, 6, 100)
for lbl, K in [("両端ピン K=1.0", 1.0), ("両端固定 K=0.5", 0.5), ("一端自由 K=2.0", 2.0)]:
    Pcr = np.pi**2*E*I/(K*Ls)**2 / 1000
    ax2.plot(Ls, Pcr, lw=2, label=lbl)
ax2.set_xlabel("柱の長さ L (m)", color="white", fontsize=9); ax2.set_ylabel("臨界荷重 Pcr (kN)", color="white", fontsize=9)
ax2.set_ylim(0, 600); ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5)
ax2.set_title("Pcr ∝ 1/L²（長いほど座屈しやすい）", color="white", fontsize=9)
print(f"d=50mm L=2 K=1: I={I:.3e} Pcr={np.pi**2*E*I/(1*2.0)**2/1000:.1f}kN slend={2.0/r:.0f}")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.4, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.0, 0.02, 1.0, 0.92]); draw_modes(axc)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "オイラー座屈", "", "Pcr = π²EI/(KL)² と端末条件 K", cc)
os.remove(cc)

# gif: increasing L -> column buckles, Pcr drops (pinned-pinned)
frames = []
y = np.linspace(0, 1, 100)
for L in list(np.linspace(1.0, 5.0, 22)) + list(np.linspace(4.8, 1.2, 12)):
    Pcr = np.pi**2*E*I/(1*L)**2/1000
    amp = min(0.45, 0.05 + (L-1)/4*0.4)
    f2 = plt.figure(figsize=(3.4, 4.2)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.0, 0.06, 1.0, 0.84]); a.set_facecolor(NAVY)
    a.plot(np.sin(np.pi*y)*amp, y, color=CYAN, lw=3)
    a.plot([0, 0], [0, 1], color="#3b4a6b", lw=1, ls=":")
    a.plot(0, 0, "^", color="white", ms=12); a.plot(0, 1, "v", color="white", ms=12)
    a.set_xlim(-0.6, 0.6); a.set_ylim(-0.05, 1.05); a.axis("off")
    a.set_title(f"L={L:.1f}m  Pcr={Pcr:.0f}kN", color="white", fontsize=11)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
