# -*- coding: utf-8 -*-
"""Series RLC resonance visuals. f0=1/(2pi sqrt(LC)), Q=w0 L/R, BW=f0/Q.
Faithful to the tool's series formulas."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "rlc-resonance"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"
L, C, V = 1e-3, 100e-9, 5.0
f0 = 1/(2*np.pi*np.sqrt(L*C))

def response(f, R):
    w = 2*np.pi*f; Z = np.sqrt(R*R + (w*L - 1/(w*C))**2)
    return Z, V/Z

f = np.linspace(f0*0.3, f0*2.5, 1500)
print(f"f0={f0:.0f}Hz; R=10: Q={2*np.pi*f0*L/10:.1f} BW={f0/(2*np.pi*f0*L/10):.0f}Hz")

# closeup: |Z| & |I| at R=10 + Q-vs-R family
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.08, 0.15, 0.40, 0.74]); ax1.set_facecolor(NAVY)
Z, I = response(f, 10)
ax1.plot(f/1000, Z, color=CYAN, lw=2, label="|Z| インピーダンス")
ax1.set_xlabel("周波数 f (kHz)", color="white", fontsize=9); ax1.set_ylabel("|Z| (Ω)", color="white", fontsize=9)
ax1.tick_params(colors="#9fb2d6", labelsize=8)
ax1b = ax1.twinx()
ax1b.plot(f/1000, I*1000, color=ORANGE, lw=2, label="|I| 電流")
ax1b.set_ylabel("|I| (mA)", color=ORANGE, fontsize=9); ax1b.tick_params(colors=ORANGE, labelsize=8)
ax1.axvline(f0/1000, color="#9be7a3", lw=1, ls="--")
ax1.text(f0/1000*1.05, ax1.get_ylim()[1]*0.8, f"f₀={f0/1000:.1f}kHz", color="#9be7a3", fontsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.set_title("直列RLC：f₀で|Z|最小・|I|最大", color="white", fontsize=9.5)

ax2 = fig.add_axes([0.58, 0.15, 0.39, 0.74]); ax2.set_facecolor(NAVY)
for R, col in [(5, CYAN), (10, ORANGE), (30, "#f472b6")]:
    _, I = response(f, R); Q = 2*np.pi*f0*L/R
    ax2.plot(f/1000, I*1000, color=col, lw=2, label=f"R={R}Ω  Q={Q:.0f}")
ax2.axvline(f0/1000, color="#9fb2d6", lw=0.8, ls="--")
ax2.set_xlabel("周波数 f (kHz)", color="white", fontsize=9); ax2.set_ylabel("電流 |I| (mA)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)
ax2.set_title("R が小さいほど Q が高く鋭い共振", color="white", fontsize=9.5)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.10, 0.12, 0.86, 0.82]); axc.set_facecolor(NAVY)
for R, col in [(5, CYAN), (10, ORANGE), (30, "#f472b6")]:
    _, I = response(f, R); axc.plot(f/1000, I*1000, color=col, lw=2.2)
axc.axvline(f0/1000, color="#9fb2d6", lw=0.8, ls="--"); axc.set_yticks([]); axc.set_xticks([])
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "RLC共振回路と", "Q値", "f₀=1/(2π√LC)、Q=ω₀L/R を可視化", cc)
os.remove(cc)

# gif: sweep R, sharpness changes
frames = []
for R in list(np.linspace(3, 40, 22)) + list(np.linspace(38, 4, 12)):
    _, I = response(f, R); Q = 2*np.pi*f0*L/R; BW = f0/Q
    f2 = plt.figure(figsize=(5.4, 3.2)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.12, 0.15, 0.84, 0.74]); a.set_facecolor(NAVY)
    a.plot(f/1000, I*1000, color=ORANGE, lw=2.2)
    a.axvline(f0/1000, color="#9be7a3", lw=0.8, ls="--")
    a.set_xlim(f[0]/1000, f[-1]/1000); a.set_ylim(0, V/3*1000)
    a.set_xlabel("f (kHz)", color="white", fontsize=8); a.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    a.set_title(f"R={R:.0f}Ω  Q={Q:.1f}  帯域幅 BW={BW/1000:.2f}kHz", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
