# -*- coding: utf-8 -*-
"""Arc-flash (IEEE 1584 simplified) visuals.
Faithful to the tool's formulas:
  Ia = 0.6 * Ibf * k       (k=1.0 box / 0.85 open)
  E  = 0.0093 * Ia^2 * t / D_cm^2 * (G/32)^0.18
  AFB at E = 1.2 cal/cm2
The article cites only the verified SCALING (E ~ 1/D^2, ~t, ~Ia^2),
so the figures plot relative energy E/E_ref to stay honest about magnitude.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "arc-flash"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; PINK = "#f472b6"; GREEN = "#9be7a3"


def E_rel(D_mm, t=0.2, Ibf=20.0, G=32.0, k=1.0, Dref=300.0):
    Ia = 0.6 * Ibf * k
    gf = (max(10.0, G) / 32.0) ** 0.18
    E = 0.0093 * Ia * Ia * t / (D_mm / 10.0) ** 2 * gf
    Iaref = 0.6 * 20.0 * 1.0
    Eref = 0.0093 * Iaref * Iaref * 0.2 / (Dref / 10.0) ** 2
    return E / Eref


D = np.linspace(100, 3000, 600)

# ---- closeup: two panels (distance inverse-square + current-quadratic) ----
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)

ax1 = fig.add_axes([0.08, 0.16, 0.40, 0.72]); ax1.set_facecolor(NAVY)
ax1.plot(D, E_rel(D), color=CYAN, lw=2.4)
for d in (300, 600, 900, 1200):
    ax1.plot(d, E_rel(np.array([d]))[0], "o", color=ORANGE, ms=6)
    ax1.annotate(f"{E_rel(np.array([d]))[0]:.2f}", (d, E_rel(np.array([d]))[0]),
                 textcoords="offset points", xytext=(8, 6), color="white", fontsize=8)
ax1.set_xlabel("作業距離 D (mm)", color="white", fontsize=9)
ax1.set_ylabel("入射エネルギー（相対）", color="white", fontsize=9)
ax1.tick_params(colors="#9fb2d6", labelsize=8)
ax1.set_title("距離の逆二乗則  E ∝ 1/D²", color="white", fontsize=10)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")

ax2 = fig.add_axes([0.58, 0.16, 0.39, 0.72]); ax2.set_facecolor(NAVY)
Ibf = np.linspace(1, 65, 400)
for d, col in [(600, CYAN), (300, ORANGE)]:
    ax2.plot(Ibf, [E_rel(np.array([d]), Ibf=i)[0] for i in Ibf], color=col, lw=2.2,
             label=f"D={d}mm")
ax2.set_xlabel("事故電流 Ibf (kA)", color="white", fontsize=9)
ax2.set_ylabel("入射エネルギー（相対）", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
ax2.set_title("電流の二乗則  E ∝ Ia² = (0.6 Ibf)²", color="white", fontsize=10)
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")

closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover preview chart ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.10, 0.12, 0.86, 0.82]); axc.set_facecolor(NAVY)
for t, col in [(0.1, GREEN), (0.2, ORANGE), (0.4, PINK)]:
    axc.plot(D, E_rel(D, t=t), color=col, lw=2.4, label=f"t={t}s")
axc.set_xticks([]); axc.set_yticks([])
axc.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="upper right")
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "アークフラッシュ解析", "入門",
                  "E ∝ Ia² t / D² ・ PPEカテゴリを支配する4法則", cc)
os.remove(cc)

# ---- gif: sweep work distance, energy curve + moving marker ----
frames = []
sweep = list(np.linspace(200, 2800, 26)) + list(np.linspace(2700, 250, 14))
for d in sweep:
    f2 = plt.figure(figsize=(5.4, 3.3)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.13, 0.17, 0.83, 0.70]); a.set_facecolor(NAVY)
    a.plot(D, E_rel(D), color=CYAN, lw=2.2)
    er = E_rel(np.array([d]))[0]
    a.plot(d, er, "o", color=ORANGE, ms=10)
    a.vlines(d, 0, er, color=ORANGE, lw=1, ls="--")
    a.set_xlim(D[0], D[-1]); a.set_ylim(0, E_rel(np.array([D[0]]))[0] * 1.05)
    a.set_xlabel("作業距離 D (mm)", color="white", fontsize=8)
    a.set_ylabel("E（相対）", color="white", fontsize=8)
    a.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    a.set_title(f"D={d:.0f}mm  →  E（相対）={er:.3f}", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
