# -*- coding: utf-8 -*-
"""ohms-law visuals: V-I-P relations + series/parallel R_eq + V-sweep gif.
Matplotlib only (figlib). Faithful to the tool's real outputs:
defaults V=12, R=100 -> I=120mA, P=1.44W; series/parallel R_eq.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "ohms-law"
NAVY = "#0b1020"; BLUE = "#7dd3fc"; ORANGE = "#f59e0b"
GREEN = "#00b894"; RED = "#e74c3c"; GREY = "#9fb2d6"


def style(ax):
    ax.set_facecolor(NAVY)
    ax.tick_params(colors=GREY, labelsize=8)
    for sp in ax.spines.values():
        sp.set_color("#3b4a6b")


def draw_circuit(ax, V, R):
    """Simple battery-resistor loop with an ammeter, like the tool canvas."""
    ax.set_facecolor(NAVY); ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
    I = V / R
    inten = min(I / 0.5, 1.0)
    wire = (0.2 + 0.6 * inten, 0.55 + 0.35 * inten, 1.0)
    # loop wires
    x0, x1, y0, y1 = 0.18, 0.82, 0.22, 0.80
    ax.plot([x0, x0, 0.42], [0.5, y1, y1], color=wire, lw=2 + 3 * inten)
    ax.plot([0.58, x1, x1, x0, x0], [y1, y1, y0, y0, 0.5],
            color=wire, lw=2 + 3 * inten)
    # battery (left)
    ax.plot([x0 - 0.05, x0 + 0.05], [0.56, 0.56], color="white", lw=2)
    ax.plot([x0 - 0.03, x0 + 0.03], [0.50, 0.50], color="white", lw=4)
    ax.plot([x0 - 0.05, x0 + 0.05], [0.44, 0.44], color="white", lw=2)
    ax.text(x0 - 0.07, 0.56, "+", color=RED, ha="right", va="center", fontsize=12)
    ax.text(x0 - 0.07, 0.44, "-", color=BLUE, ha="right", va="center", fontsize=12)
    ax.text(x0 + 0.02, 0.34, f"{V:.0f}V", color="white", ha="left", fontsize=10)
    # resistor (top, zigzag)
    rx = np.linspace(0.42, 0.58, 9)
    ry = y1 + 0.03 * np.array([0, 1, -1, 1, -1, 1, -1, 1, 0])
    ax.plot(rx, ry, color=ORANGE, lw=2)
    ax.text(0.5, y1 + 0.07, f"{R:.0f}Ω", color=ORANGE, ha="center", fontsize=10)
    # ammeter
    ax.add_patch(plt.Circle((0.5, y0), 0.04, fc=NAVY, ec=GREY, lw=1.5))
    ax.text(0.5, y0, "A", color=GREY, ha="center", va="center", fontsize=9)
    # flow dots
    n = max(2, min(int(I / 0.01), 14))
    ts = np.linspace(0, 1, n, endpoint=False)
    for t in ts:
        px = x0 + (x1 - x0) * t
        ax.plot(px, y0, "o", color=BLUE, ms=4)
    ax.text(0.5, y0 - 0.10, f"I = {I*1000:.0f} mA",
            color=BLUE, ha="center", fontsize=10)


# ---------- charts-closeup: I-V line + P curve + circuit ----------
fig = plt.figure(figsize=(9.2, 4.3)); fig.patch.set_facecolor(NAVY)

axc = fig.add_axes([0.02, 0.05, 0.30, 0.9])
draw_circuit(axc, 12, 100)
axc.set_title("V=12V, R=100Ω → I=120mA", color="white", fontsize=10)

# I vs V at fixed R=100 (Ohm's law line)
ax1 = fig.add_axes([0.40, 0.16, 0.25, 0.72]); style(ax1)
Vs = np.linspace(0, 100, 200)
ax1.plot(Vs, Vs / 100 * 1000, color=BLUE, lw=2.2)
ax1.plot(12, 120, "o", color=ORANGE)
ax1.annotate("12V→120mA", (12, 120), (20, 250), color="white", fontsize=8,
             arrowprops=dict(arrowstyle="->", color=GREY))
ax1.set_xlabel("電圧 V [V]", color="white", fontsize=9)
ax1.set_ylabel("電流 I [mA]", color="white", fontsize=9)
ax1.set_title("I=V/R （R=100Ω 一定）", color="white", fontsize=10)

# P vs R at fixed V=12 (P=V^2/R)
ax2 = fig.add_axes([0.73, 0.16, 0.25, 0.72]); style(ax2)
Rs = np.linspace(10, 1000, 300)
ax2.plot(Rs, 12**2 / Rs, color=GREEN, lw=2.2)
ax2.plot(100, 144 / 100, "o", color=ORANGE)
ax2.annotate("R=100Ω→1.44W", (100, 1.44), (200, 6), color="white",
             fontsize=8, arrowprops=dict(arrowstyle="->", color=GREY))
ax2.set_xlabel("抵抗 R [Ω]", color="white", fontsize=9)
ax2.set_ylabel("電力 P [W]", color="white", fontsize=9)
ax2.set_title("P=V²/R （V=12V 一定）", color="white", fontsize=10)

cu = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, cu, dpi=130); print(" closeup")

# ---------- cover ----------
figc = plt.figure(figsize=(5.0, 3.4)); figc.patch.set_facecolor(NAVY)
axcc = figc.add_axes([0.0, 0.0, 1.0, 1.0])
draw_circuit(axcc, 12, 100)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png")
figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "オームの法則",
                  "V = I × R",
                  "V・Rを動かして電流・電力をリアルタイム計算",
                  cc)
os.remove(cc)

# ---------- slider-anim.gif: sweep V from 2..24V at R=100 ----------
frames = []
seq = list(np.linspace(2, 24, 20)) + list(np.linspace(24, 2, 8))
for V in seq:
    fr = plt.figure(figsize=(4.2, 3.6)); fr.patch.set_facecolor(NAVY)
    g = fr.add_axes([0.0, 0.04, 1.0, 0.86])
    draw_circuit(g, V, 100)
    I = V / 100; P = V * I
    g.set_title(f"V={V:.0f}V  I={I*1000:.0f}mA  P={P:.2f}W",
                color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(fr, dpi=90))
figlib.save_gif(frames, SLUG, duration=110); print("done")
