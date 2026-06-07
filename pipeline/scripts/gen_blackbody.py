# -*- coding: utf-8 -*-
"""Blackbody radiation visuals. Planck law + Wien peak + Stefan-Boltzmann.
Faithful to the tool (constants h,c,k,sigma; Sun 5778K etc.)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "blackbody-radiation"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"
h, c, k, sigma = 6.626e-34, 3e8, 1.381e-23, 5.67e-8

def planck(lam_nm, T):
    lam = lam_nm * 1e-9
    return (2*h*c*c/lam**5) / (np.exp(np.clip(h*c/(lam*k*T), 0, 700)) - 1)

def wien(T): return 2.898e-3/T*1e9

TEMPS = [(310, "人体 310K", "#7c5cff"), (2700, "白熱灯 2700K", "#ff6b6b"),
         (5778, "太陽 5778K", "#FFD166"), (10000, "青色星 10000K", "#7dd3fc")]
for T, n, _ in TEMPS:
    print(f"  {n}: lam_peak={wien(T):.0f}nm  P=sigma T^4={sigma*T**4:.2e} W/m2")

# closeup: Planck curves + Wien peak line
fig = plt.figure(figsize=(9.6, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.08, 0.15, 0.52, 0.75]); ax1.set_facecolor(NAVY)
lam = np.linspace(100, 12000, 600)
ax1.axvspan(380, 780, color="white", alpha=0.10)
ax1.text(580, 1.2e14, "可視光", color="white", ha="center", fontsize=8)
for T, lbl, col in TEMPS:
    ax1.semilogy(lam, planck(lam, T), color=col, lw=2, label=lbl)
    ax1.plot(wien(T), planck(wien(T), T), "o", color=col, ms=5)
ax1.set_xlabel("波長 λ (nm)", color="white", fontsize=9); ax1.set_ylabel("分光放射輝度", color="white", fontsize=9)
ax1.set_xlim(0, 12000); ax1.set_ylim(1e6, 1e16); ax1.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="upper right")
ax1.set_title("プランク分布（温度が高いほど明るく短波長へ）", color="white", fontsize=9.5)
ax2 = fig.add_axes([0.68, 0.16, 0.29, 0.72]); ax2.set_facecolor(NAVY)
Ts = np.linspace(200, 12000, 200)
ax2.plot(Ts, wien(Ts), color=ORANGE, lw=2)
ax2.axhspan(380, 780, color="white", alpha=0.12)
for T, lbl, col in TEMPS:
    ax2.plot(T, wien(T), "o", color=col, ms=7)
ax2.set_xlabel("温度 T (K)", color="white", fontsize=9); ax2.set_ylabel("ピーク波長 λpeak (nm)", color="white", fontsize=9)
ax2.set_ylim(0, 4000); ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("ウィーンの変位則 λpeak=2.898e-3/T", color="white", fontsize=8.5)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.10, 0.12, 0.86, 0.82]); axc.set_facecolor(NAVY)
axc.axvspan(380, 780, color="white", alpha=0.10)
for T, lbl, col in TEMPS:
    axc.semilogy(lam, planck(lam, T), color=col, lw=2.2)
axc.set_xlim(0, 8000); axc.set_ylim(1e8, 1e16); axc.axis("off")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "黒体放射と", "プランク分布", "ウィーン変位則・Stefan-Boltzmann則を可視化", cc)
os.remove(cc)

# gif: sweep temperature
def T_rgb(T):
    if T < 3500: return "#ff6b3b"
    if T < 5000: return "#ffb066"
    if T < 6500: return "#fff2cc"
    if T < 9000: return "#d6e8ff"
    return "#9fc4ff"
frames = []
for T in list(range(1000, 11000, 500)) + list(range(10500, 1000, -500)):
    f2 = plt.figure(figsize=(5.4, 3.2)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.12, 0.15, 0.84, 0.74]); a.set_facecolor(NAVY)
    a.axvspan(380, 780, color="white", alpha=0.10)
    a.plot(lam, planck(lam, T), color=T_rgb(T), lw=2.2)
    a.plot(wien(T), planck(wien(T), T), "o", color="white", ms=6)
    a.set_xlim(0, 8000); a.set_ylim(0, max(planck(lam, T))*1.1)
    a.tick_params(colors="#9fb2d6", labelsize=7); a.set_xlabel("λ (nm)", color="white", fontsize=8)
    a.set_yticks([])
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    a.set_title(f"T={T}K  λpeak={wien(T):.0f}nm  P={sigma*T**4/1e6:.1f}MW/m²", color="white", fontsize=9)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=90)
print("done.")
