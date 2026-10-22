# -*- coding: utf-8 -*-
"""String resonance visuals. Tool: f_n = (n/2L)sqrt(T/mu), modal superposition
of a plucked string. Reproduced with matplotlib."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "string-resonance"
NAVY = "#0b1020"; ORANGE = "#f59e0b"; CYAN = "#7dd3fc"
COLS = [CYAN, ORANGE, "#9be7a3", "#f472b6"]
L = 1.0

def modal_amp(p, N=12):
    """triangular pluck at fraction p -> An ∝ sin(n*pi*p)/n^2 (normalised)."""
    A = np.array([np.sin(n * np.pi * p) / (n * n) for n in range(1, N + 1)])
    m = np.max(np.abs(A)); return A / m if m > 0 else A

def draw_modes(ax, title=None):
    ax.set_facecolor(NAVY)
    x = np.linspace(0, L, 300)
    for n in range(1, 4):
        y = np.sin(n * np.pi * x / L)
        ax.plot(x, y - 2.4 * (n - 1), color=COLS[n - 1], lw=2)
        ax.plot(x, -y - 2.4 * (n - 1), color=COLS[n - 1], lw=0.8, alpha=0.4)
        # nodes
        for k in range(n + 1):
            ax.plot(k * L / n, -2.4 * (n - 1), "o", color="white", ms=4)
        ax.text(-0.02, -2.4 * (n - 1), f"n={n}", color="white", ha="right", va="center", fontsize=10)
    ax.set_xlim(-0.12, L + 0.02); ax.set_ylim(-6.0, 1.4)
    ax.axis("off")
    if title: ax.set_title(title, color="white", fontsize=11)

def draw_spectrum(ax):
    ax.set_facecolor(NAVY)
    N = 8
    a_half = np.abs(modal_amp(0.5, N))
    a_third = np.abs(modal_amp(1 / 3, N))
    idx = np.arange(1, N + 1)
    ax.bar(idx - 0.2, a_half, width=0.4, color=CYAN, label="中央を弾く（奇数のみ）")
    ax.bar(idx + 0.2, a_third, width=0.4, color=ORANGE, label="1/3点を弾く（n=3が欠落）")
    ax.set_xlabel("倍音次数 n", color="white", fontsize=9)
    ax.set_ylabel("相対振幅 |An|", color="white", fontsize=9)
    ax.set_xticks(idx)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)

# closeup
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.04, 0.05, 0.44, 0.9]); draw_modes(ax1, "弦の固有モード（定在波）n=1,2,3")
ax2 = fig.add_axes([0.58, 0.16, 0.39, 0.74]); draw_spectrum(ax2)
ax2.set_title("弾く位置で消える倍音が決まる", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.0, 3.4)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.06, 0.02, 0.92, 0.96]); draw_modes(axc)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "弦の共振と定在波", "", "fn = (n/2L)√(T/μ) と倍音系列を可視化", cc)
os.remove(cc)

# gif: plucked-at-center string vibrating (sum of modes with cos(omega_n t))
A = modal_amp(0.5, 12)
x = np.linspace(0, L, 240)
basis = np.array([np.sin(n * np.pi * x / L) for n in range(1, 13)])
f1 = 1.0  # normalised; mode n oscillates at n*f1
frames = []
for k in range(40):
    t = k / 40 * 2.0  # 2 periods of fundamental
    coeffs = A * np.cos(2 * np.pi * np.arange(1, 13) * f1 * t)
    y = coeffs @ basis
    fig2 = plt.figure(figsize=(5.2, 2.8)); fig2.patch.set_facecolor(NAVY)
    a2 = fig2.add_axes([0.03, 0.08, 0.94, 0.84]); a2.set_facecolor(NAVY)
    a2.plot(x, y, color=ORANGE, lw=2.5)
    a2.fill_between(x, y, color=ORANGE, alpha=0.12)
    a2.axhline(0, color="#3b4a6b", lw=1)
    a2.plot([0, L], [0, 0], "o", color="white", ms=6)
    a2.set_xlim(-0.03, L + 0.03); a2.set_ylim(-1.3, 1.3); a2.axis("off")
    a2.set_title("中央を弾いた弦の振動（奇数倍音の重ね合わせ）", color="white", fontsize=9)
    frames.append(figlib.fig_to_pil(fig2, dpi=92))
figlib.save_gif(frames, SLUG, duration=80)
print("done.")
