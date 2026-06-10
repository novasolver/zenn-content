# -*- coding: utf-8 -*-
"""Series RLC AC impedance & resonance visuals for ac-impedance-rlc tool.
Faithful to the tool's exact formulas and defaults:
  R=100 Ohm, L=10 mH, C=1 uF, f=1592 Hz
  |Z|=sqrt(R^2 + (wL - 1/(wC))^2), phi=atan2(X,R)
  f0 = 1/(2 pi sqrt(LC)) = 1591.5 Hz, Q = (1/R) sqrt(L/C)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "ac-impedance-rlc"
NAVY = "#0b1020"; CYAN = "#00B4D8"; ORANGE = "#FFD166"; PINK = "#f472b6"
L, C = 10e-3, 1e-6
f0 = 1 / (2 * np.pi * np.sqrt(L * C))


def Zmag(f, R):
    w = 2 * np.pi * f
    X = w * L - 1 / (w * C)
    return np.sqrt(R * R + X * X)


def phase(f, R):
    w = 2 * np.pi * f
    X = w * L - 1 / (w * C)
    return np.degrees(np.arctan2(X, R))


# log frequency axis matching the tool (1 Hz .. 100 kHz)
f = np.logspace(0, 5, 1600)

# ---------- charts-closeup: |Z|(f) log-log V-curve + phase ----------
fig = plt.figure(figsize=(9.6, 4.3)); fig.patch.set_facecolor(NAVY)

ax1 = fig.add_axes([0.075, 0.16, 0.40, 0.72]); ax1.set_facecolor(NAVY)
for R, col in [(10, CYAN), (100, ORANGE), (1000, PINK)]:
    Q = (1 / R) * np.sqrt(L / C)
    ax1.loglog(f, Zmag(f, R), color=col, lw=2, label=f"R={R}Ω  Q={Q:.2g}")
ax1.axvline(f0, color="#9be7a3", lw=1, ls="--")
ax1.text(f0 * 1.15, ax1.get_ylim()[1] * 0.25, f"f₀={f0:.0f}Hz", color="#9be7a3", fontsize=8)
ax1.set_xlabel("周波数 f (Hz, log)", color="white", fontsize=9)
ax1.set_ylabel("|Z| (Ω, log)", color="white", fontsize=9)
ax1.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="upper center")
ax1.set_title("直列RLC：f₀で|Z|最小（=R）のV字", color="white", fontsize=9.5)

ax2 = fig.add_axes([0.585, 0.16, 0.39, 0.72]); ax2.set_facecolor(NAVY)
for R, col in [(10, CYAN), (100, ORANGE), (1000, PINK)]:
    ax2.semilogx(f, phase(f, R), color=col, lw=2, label=f"R={R}Ω")
ax2.axvline(f0, color="#9be7a3", lw=1, ls="--")
ax2.axhline(0, color="#9fb2d6", lw=0.7, ls=":")
ax2.text(3, 60, "誘導性 φ>0", color="#9fb2d6", fontsize=7.5)
ax2.text(3, -70, "容量性 φ<0", color="#9fb2d6", fontsize=7.5)
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
    axc.loglog(f, Zmag(f, R), color=col, lw=2.4)
axc.axvline(f0, color="#9be7a3", lw=1, ls="--")
axc.set_xticks([]); axc.set_yticks([])
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "交流インピーダンスと", "直列RLC共振",
                  "|Z|=√(R²+X²)、f₀=1/(2π√LC)、Q=(1/R)√(L/C)", cc)
os.remove(cc)

# ---------- gif: sweep current frequency f across the V-curve ----------
R = 100.0
frames = []
fsweep = np.logspace(np.log10(20), np.log10(80000), 30)
fsweep = np.concatenate([fsweep, fsweep[::-1][1:]])
for fc in fsweep:
    Zc = Zmag(fc, R); phic = phase(fc, R)
    fr = plt.figure(figsize=(5.4, 3.2)); fr.patch.set_facecolor(NAVY)
    a = fr.add_axes([0.14, 0.17, 0.82, 0.70]); a.set_facecolor(NAVY)
    a.loglog(f, Zmag(f, R), color=CYAN, lw=2.2)
    a.axvline(f0, color="#9be7a3", lw=0.8, ls="--")
    a.plot([fc], [Zc], "o", color=ORANGE, ms=9, mec="white", mew=1.2)
    a.set_xlim(f[0], f[-1]); a.set_ylim(60, 2e5)
    a.set_xlabel("f (Hz, log)", color="white", fontsize=8)
    a.set_ylabel("|Z| (Ω, log)", color="white", fontsize=8)
    a.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    a.set_title(f"f={fc:.0f}Hz  |Z|={Zc:.0f}Ω  φ={phic:+.0f}°", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(fr, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
