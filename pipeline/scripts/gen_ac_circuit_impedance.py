# -*- coding: utf-8 -*-
"""Visuals for the ac-circuit-impedance tool (Bode + phasor, series/parallel).
Faithful to the tool's exact JS formulas and defaults:
  defaults R=100 Ohm, L=16 mH, C=1.6 uF, series, log10(f)=3 -> f=1000 Hz
  series: Z = R + j(wL - 1/(wC)); |Z|=sqrt(R^2+X^2); phi=atan2(X,R)
  parallel: Y = 1/R + j(wC - 1/(wL)); |Z|=1/|Y|; phi=-atan2(B,G)
  f0 = 1/(2 pi sqrt(LC)) = 994.7 Hz
  series Q = w0 L / R ; parallel Q = R / (w0 L)
Matplotlib only (RECIPE STEP 5). ASCII-safe filenames.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "ac-circuit-impedance"
NAVY = "#0b1020"; CYAN = "#00B4D8"; ORANGE = "#FFD166"; PINK = "#f472b6"; GREEN = "#9be7a3"
L, C = 16e-3, 1.6e-6                      # tool defaults
f0 = 1 / (2 * np.pi * np.sqrt(L * C))     # = 994.7 Hz


def Zmag_series(f, R):
    w = 2 * np.pi * f
    return np.hypot(R, w * L - 1 / (w * C))


def phase_series(f, R):
    w = 2 * np.pi * f
    return np.degrees(np.arctan2(w * L - 1 / (w * C), R))


# log frequency axis matching the tool slider (10^1 .. 10^8 Hz)
f = np.logspace(1, 6, 1600)

# ---------- charts-closeup: Bode |Z| (Q family) + phase ----------
fig = plt.figure(figsize=(9.6, 4.3)); fig.patch.set_facecolor(NAVY)

ax1 = fig.add_axes([0.075, 0.16, 0.40, 0.70]); ax1.set_facecolor(NAVY)
for R, col in [(10, CYAN), (100, ORANGE), (1000, PINK)]:
    Q = 2 * np.pi * f0 * L / R
    ax1.loglog(f, Zmag_series(f, R), color=col, lw=2, label=f"R={R}Ω  Q={Q:.2g}")
ax1.axvline(f0, color=GREEN, lw=1, ls="--")
ax1.text(f0 * 1.15, 130, f"f₀={f0:.0f}Hz", color=GREEN, fontsize=8)
ax1.set_xlabel("周波数 f (Hz, log)", color="white", fontsize=9)
ax1.set_ylabel("|Z| (Ω, log)", color="white", fontsize=9)
ax1.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="upper center")
ax1.set_title("ボード線図 |Z|：f₀で最小（=R）のV字", color="white", fontsize=9.5)

ax2 = fig.add_axes([0.585, 0.16, 0.39, 0.70]); ax2.set_facecolor(NAVY)
for R, col in [(10, CYAN), (100, ORANGE), (1000, PINK)]:
    ax2.semilogx(f, phase_series(f, R), color=col, lw=2, label=f"R={R}Ω")
ax2.axvline(f0, color=GREEN, lw=1, ls="--")
ax2.axhline(0, color="#9fb2d6", lw=0.7, ls=":")
ax2.text(15, 62, "誘導性 φ>0", color="#9fb2d6", fontsize=7.5)
ax2.text(15, -72, "容量性 φ<0", color="#9fb2d6", fontsize=7.5)
ax2.set_ylim(-95, 95)
ax2.set_xlabel("周波数 f (Hz, log)", color="white", fontsize=9)
ax2.set_ylabel("位相角 φ (°)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("位相：f₀を境に容量性→誘導性", color="white", fontsize=9.5)

closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---------- cover ----------
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.10, 0.10, 0.86, 0.84]); axc.set_facecolor(NAVY)
for R, col in [(10, CYAN), (100, ORANGE), (1000, PINK)]:
    axc.loglog(f, Zmag_series(f, R), color=col, lw=2.4)
axc.axvline(f0, color=GREEN, lw=1, ls="--")
axc.set_xticks([]); axc.set_yticks([])
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "交流回路インピーダンス", "とRLC共振",
                  "Z=R+j(ωL−1/ωC)、f₀=1/(2π√LC)、Q=ω₀L/R", cc)
os.remove(cc)

# ---------- gif: sweep operating frequency across the V-curve (default R=100) ----------
R = 100.0
frames = []
fsweep = np.logspace(np.log10(60), np.log10(20000), 30)
fsweep = np.concatenate([fsweep, fsweep[::-1][1:]])
for fc in fsweep:
    Zc = Zmag_series(fc, R); phic = phase_series(fc, R)
    fr = plt.figure(figsize=(5.4, 3.2)); fr.patch.set_facecolor(NAVY)
    a = fr.add_axes([0.15, 0.17, 0.81, 0.66]); a.set_facecolor(NAVY)
    a.loglog(f, Zmag_series(f, R), color=CYAN, lw=2.2)
    a.axvline(f0, color=GREEN, lw=0.8, ls="--")
    a.plot([fc], [Zc], "o", color=ORANGE, ms=9, mec="white", mew=1.2)
    a.set_xlim(f[0], f[-1]); a.set_ylim(80, 2e4)
    a.set_xlabel("f (Hz, log)", color="white", fontsize=8)
    a.set_ylabel("|Z| (Ω, log)", color="white", fontsize=8)
    a.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    a.set_title(f"f={fc:.0f}Hz   |Z|={Zc:.0f}Ω   φ={phic:+.0f}°", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(fr, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
