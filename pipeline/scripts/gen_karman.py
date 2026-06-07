# -*- coding: utf-8 -*-
"""Karman vortex visuals. The tool is analytical (fs = St*V/D), so we faithfully
reproduce its V-fs Strouhal diagram + schematic vortex street with matplotlib.
Produces cover / charts-closeup / slider-anim.gif."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import figlib

SLUG = "karman-vortex"
NAVY = "#0a1929"; ORANGE = "#f59e0b"; CYAN = "#7dd3fc"
RED = "#ff6b6b"; BLUE = "#7fb6ff"
NU_AIR = 1.5e-5

def fs_of(V, D_mm, St): return St * V / (D_mm * 1e-3)

def draw_street(ax, V=5.0, D_mm=50, St=0.2, phase=0.0, title=None):
    """Schematic Karman vortex street behind a cylinder (matches tool layout)."""
    ax.set_facecolor(NAVY)
    W, H = 10.0, 5.0
    cx, cy, rcyl = 2.0, H / 2, 0.42
    # inflow arrows
    for k in range(4):
        yk = 0.6 + (H - 1.2) * (k + 0.5) / 4
        x0 = 0.2 + ((phase + k * 0.13) % 1.0) * 1.0
        ax.annotate("", xy=(x0 + 0.5, yk), xytext=(x0, yk),
                    arrowprops=dict(arrowstyle="-|>", color="white", alpha=0.5, lw=1.2))
    # vortex street
    lam = 1.55
    rv = 0.34
    for i in range(-1, 6):
        xt = cx + rcyl + 0.5 + i * lam + (phase % 1.0) * lam
        if cx + rcyl < xt < W - 0.2:
            _swirl(ax, xt, cy + rcyl * 1.5, rv, RED, +1, phase)   # 上側=赤 CCW
        xb = cx + rcyl + 0.5 + lam * 0.5 + i * lam + (phase % 1.0) * lam
        if cx + rcyl < xb < W - 0.2:
            _swirl(ax, xb, cy - rcyl * 1.5, rv, BLUE, -1, phase)  # 下側=青 CW
    # cylinder
    ax.add_patch(Circle((cx, cy), rcyl, color="#b0bec5", ec="#cfe3f7", lw=1.2, zorder=5))
    ax.text(cx, cy - rcyl - 0.28, f"D = {D_mm:.0f} mm", color="#cfe3f7", ha="center", fontsize=8)
    ax.text(0.15, H - 0.25, f"V = {V:.1f} m/s", color="#cfe3f7", fontsize=9, va="top")
    ax.text(W - 0.15, H - 0.25, f"fs = {fs_of(V,D_mm,St):.1f} Hz", color=ORANGE,
            fontsize=9, va="top", ha="right")
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")
    if title: ax.set_title(title, color="white", fontsize=11)

def _swirl(ax, x, y, r, color, dirn, phase):
    t = np.linspace(0, 4 * np.pi, 60)
    rr = r * (1 - t / (4 * np.pi))
    ang = dirn * t + phase * 6.28
    ax.plot(x + rr * np.cos(ang), y + rr * np.sin(ang), color=color, lw=1.3, alpha=0.9)
    ax.add_patch(Circle((x, y), r, color=color, alpha=0.12, lw=0))

def draw_diagram(ax, V=5.0, D_mm=50, St=0.2, fn=25):
    ax.set_facecolor(NAVY)
    D = D_mm * 1e-3
    Vg = np.linspace(0.1, 30, 200)
    fsg = St * Vg / D
    ax.plot(Vg, fsg, color=CYAN, lw=2.4, label=f"fs = St·V/D (St={St:.2f})")
    ax.axhline(fn, color="#9be7a3", lw=1.8, ls="--", label=f"fn = {fn:.0f} Hz（固有振動数）")
    # lock-in band 0.85fn < fs < 1.15fn
    ax.axhspan(0.85 * fn, 1.15 * fn, color="#ff6b6b", alpha=0.13)
    Vcr = fn * D / St
    ax.axvline(Vcr, color=ORANGE, lw=1.0, ls=":", alpha=0.8)
    ax.text(Vcr + 0.3, fn * 1.5, f"Vcr = {Vcr:.2f} m/s\n(ロックイン)", color=ORANGE, fontsize=8)
    fs_cur = St * V / D
    ax.scatter([V], [fs_cur], s=90, color="#FFD166", ec="white", zorder=6)
    ax.set_xlabel("流速 V (m/s)", color="white", fontsize=9)
    ax.set_ylabel("渦放出周波数 fs (Hz)", color="white", fontsize=9)
    ax.set_xlim(0, 30); ax.set_ylim(0, max(St * 30 / D, fn) * 1.1)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="upper left")

# ---- closeup: vortex street + V-fs diagram ----
fig = plt.figure(figsize=(9.6, 4.4)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.01, 0.08, 0.52, 0.84])
draw_street(ax1, title="円柱後流の渦列（上=赤CCW / 下=青CW）")
ax2 = fig.add_axes([0.60, 0.16, 0.37, 0.74])
draw_diagram(ax2)
ax2.set_title("V-fs 線図とロックイン帯", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.0)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.0, 0.0, 1.0, 1.0]); draw_street(axc, phase=0.3)
cover_chart = os.path.join(figlib.outdir(SLUG), "_coverchart.png")
figlib.save_fig(figc, cover_chart, dpi=120)
figlib.make_cover(SLUG, "カルマン渦列", "",
                  "fs = St·V/D とロックイン現象を可視化", cover_chart)
os.remove(cover_chart)

# ---- gif: V sweep across the Strouhal line, lock-in highlighted ----
frames = []
Vs = np.concatenate([np.linspace(0.5, 12, 30), np.linspace(12, 0.5, 30)])
for k, V in enumerate(Vs):
    f2 = plt.figure(figsize=(5.4, 3.6)); f2.patch.set_facecolor(NAVY)
    a2 = f2.add_axes([0.14, 0.15, 0.82, 0.80])
    draw_diagram(a2, V=V)
    fs_cur = fs_of(V, 50, 0.2); ratio = fs_cur / 25
    lock = 0.85 < ratio < 1.15
    a2.text(0.98, 0.06, f"V={V:.1f}  fs={fs_cur:.1f}Hz  fs/fn={ratio:.2f}"
            + ("  ★LOCK-IN" if lock else ""),
            transform=a2.transAxes, ha="right", fontsize=8.5,
            color=("#ff6b6b" if lock else CYAN))
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=90)
print("done.")
