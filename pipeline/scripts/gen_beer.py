# -*- coding: utf-8 -*-
"""Beer-Lambert visuals. A=ε·l·(c·1e-3) [c in mmol/L]; T=10^-A.
Faithful to the tool (ε=5000, l=1, c=0.10 mmol/L default)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "beer-lambert-law"
NAVY = "#0a1929"
BLUE, ORANGE, RED = "#007BFF", "#f39c12", "#e74c3c"

def absb(eps, l, c_mmol):  # absorbance
    return eps*l*(c_mmol*1e-3)

def style(ax):
    ax.set_facecolor(NAVY)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.grid(True, color="#23344f", lw=0.6)

eps, l = 5000.0, 1.0

# ---- closeup: calibration line + A-vs-T nonlinear ----
fig = plt.figure(figsize=(9.6, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.08, 0.16, 0.40, 0.72]); style(ax1)
c = np.linspace(0, 0.4, 100)
A = absb(eps, l, c)
ax1.plot(c, A, color=BLUE, lw=2.6, label="検量線 A=εlc")
for cv in (0.10, 0.20, 0.30):
    ax1.plot(cv, absb(eps,l,cv), "o", color=RED, ms=7)
    ax1.text(cv, absb(eps,l,cv)+0.06, f"A={absb(eps,l,cv):.1f}", color="white", ha="center", fontsize=8)
ax1.set_xlabel("濃度 c (mmol/L)", color="white", fontsize=9)
ax1.set_ylabel("吸光度 A", color="white", fontsize=9)
ax1.set_title("検量線（ε=5000, l=1 cm）", color="white", fontsize=10)
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)

ax2 = fig.add_axes([0.58, 0.16, 0.39, 0.72]); style(ax2)
Av = np.linspace(0, 3, 200)
Tv = 10**(-Av)*100
ax2.plot(Av, Tv, color=BLUE, lw=2.6)
ax2.axvspan(0.1, 1.5, color=ORANGE, alpha=0.15)
ax2.text(0.8, 60, "適正域\nA=0.1〜1.5", color=ORANGE, ha="center", fontsize=8.5)
for av in (0.5, 1.0, 2.0):
    ax2.plot(av, 10**(-av)*100, "o", color=RED, ms=6)
ax2.set_xlabel("吸光度 A", color="white", fontsize=9)
ax2.set_ylabel("透過率 T (%)", color="white", fontsize=9)
ax2.set_title("吸光度 vs 透過率（T=10^-A）", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.14, 0.16, 0.82, 0.74]); style(axc)
axc.plot(Av, Tv, color=BLUE, lw=2.8)
axc.axvspan(0.1, 1.5, color=ORANGE, alpha=0.18)
axc.set_xlabel("吸光度 A", color="white", fontsize=9)
axc.set_ylabel("透過率 T (%)", color="white", fontsize=9)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ランベルト・ベール", "A = εlc = -log10(T)", "吸光度で濃度を測る", cc)
os.remove(cc)

# ---- gif: sweep concentration; show beam attenuation profile inside cell ----
frames = []
c_seq = list(np.linspace(0.02, 0.4, 14)) + list(np.linspace(0.4, 0.02, 14))
xs = np.linspace(0, l, 50)
for cv in c_seq:
    f2 = plt.figure(figsize=(5.4, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.14, 0.17, 0.82, 0.70]); style(a)
    I = 10**(-eps*(cv*1e-3)*xs)*100
    a.plot(xs, I, color=ORANGE, lw=2.6)
    a.fill_between(xs, 0, I, color=ORANGE, alpha=0.18)
    A = absb(eps, l, cv); T = 10**(-A)*100
    a.set_xlim(0, l); a.set_ylim(0, 105)
    a.set_xlabel("セル内の距離 (cm)", color="white", fontsize=9)
    a.set_ylabel("光強度 I/I0 (%)", color="white", fontsize=9)
    a.set_title(f"c={cv:.2f} mM  →  A={A:.2f}, T={T:.1f}%", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=120)
print("done.")
