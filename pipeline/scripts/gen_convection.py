# -*- coding: utf-8 -*-
"""Rayleigh-Benard convection visuals. Tool: Ra=g beta dT L^3/(nu alpha),
Ra_crit~1708, regimes. Idealised counter-rotating roll cells + Nu-Ra curve."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "convection-cells"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"
RA_CRIT = 1708

def roll_field(nrolls=3, nx=240, ny=120, Lx=4.0, amp=0.28):
    x = np.linspace(0, Lx, nx); y = np.linspace(0, 1, ny)
    X, Y = np.meshgrid(x, y)
    k = nrolls * np.pi / Lx
    # stream function psi = sin(kx) sin(pi y); u=psi_y, v=-psi_x
    U = np.pi * np.sin(k * X) * np.cos(np.pi * Y)
    V = -k * np.cos(k * X) * np.sin(np.pi * Y)
    # temperature: conduction (hot bottom y=0) + convective bulge
    T = (1 - Y) + amp * np.cos(k * X) * np.sin(np.pi * Y)
    return X, Y, U, V, T, x, y

def draw_cells(ax, nrolls=3, title=None):
    X, Y, U, V, T, x, y = roll_field(nrolls)
    ax.set_facecolor(NAVY)
    im = ax.imshow(T, origin="lower", extent=[0, 4, 0, 1], aspect="auto",
                   cmap="RdBu_r", vmin=-0.1, vmax=1.1)
    ax.streamplot(x, y, U, V, color="white", density=1.0, linewidth=0.6, arrowsize=0.7)
    ax.set_xticks([]); ax.set_yticks([])
    if title: ax.set_title(title, color="white", fontsize=10)
    return im

# closeup: cells + Nu-Ra curve
fig = plt.figure(figsize=(9.6, 4.2)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.03, 0.12, 0.52, 0.78])
im = draw_cells(ax1, 3, "対流ロール（下=高温赤が上昇、上=低温青が下降）")
ax2 = fig.add_axes([0.64, 0.16, 0.33, 0.72]); ax2.set_facecolor(NAVY)
Ra = np.logspace(2.8, 6, 200)
Nu = np.where(Ra < RA_CRIT, 1.0, (Ra / RA_CRIT) ** (1 / 3))
ax2.semilogx(Ra, Nu, color=ORANGE, lw=2.2)
ax2.axvline(RA_CRIT, color=CYAN, lw=1.2, ls="--")
ax2.text(RA_CRIT * 1.1, 1.05, "Ra_c≈1708\n対流開始", color=CYAN, fontsize=8)
ax2.set_xlabel("レイリー数 Ra", color="white", fontsize=9)
ax2.set_ylabel("ヌッセルト数 Nu（熱伝達比）", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("Ra<Ra_c は伝導(Nu=1)、超えると対流", color="white", fontsize=9)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.4, 3.0)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.02, 0.04, 0.96, 0.92]); draw_cells(axc, 3)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "レイリー・ベナール", "対流セル", "Ra = gβΔT L³/(να)、Ra_c≈1708 で対流開始", cc)
os.remove(cc)

# gif: increasing Ra -> more/intensifying rolls
frames = []
seq = [("Ra=1259 (安定・伝導のみ)", 0, 0.02),
       ("Ra=2512 (定常対流セル)", 3, 0.28),
       ("Ra=10000 (対流強まる)", 4, 0.38),
       ("Ra=31623 (乱流的対流)", 6, 0.5)]
import itertools
order = list(range(len(seq))) + list(range(len(seq) - 2, 0, -1))
for _ in range(2):
    for i in order:
        lbl, nr, amp = seq[i]
        f2 = plt.figure(figsize=(5.6, 3.0)); f2.patch.set_facecolor(NAVY)
        a = f2.add_axes([0.02, 0.10, 0.96, 0.80])
        if nr == 0:
            X, Y, U, V, T, x, y = roll_field(1, amp=0.0)
            a.imshow(T, origin="lower", extent=[0, 4, 0, 1], aspect="auto", cmap="RdBu_r", vmin=-0.1, vmax=1.1)
            a.set_xticks([]); a.set_yticks([])
        else:
            X, Y, U, V, T, x, y = roll_field(nr, amp=amp)
            a.imshow(T, origin="lower", extent=[0, 4, 0, 1], aspect="auto", cmap="RdBu_r", vmin=-0.1, vmax=1.1)
            a.streamplot(x, y, U, V, color="white", density=0.9, linewidth=0.6, arrowsize=0.7)
            a.set_xticks([]); a.set_yticks([])
        a.set_title(lbl, color="white", fontsize=10)
        frames.append(figlib.fig_to_pil(f2, dpi=88))
figlib.save_gif(frames, SLUG, duration=420)
print("done.")
