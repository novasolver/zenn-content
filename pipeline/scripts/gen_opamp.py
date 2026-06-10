# -*- coding: utf-8 -*-
"""Op-amp basic circuits visuals. Faithful to opamp-circuit.html:
Av_inv=-Rf/R1, Av_noninv=1+Rf/R1, clipping at +/-Vcc, BW=GBW/|Av| (GBW=1MHz).
The tool plots vout = Av*vin (clipped at +/-Vcc) and a transfer curve."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "opamp-circuit"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; PINK = "#f472b6"; GREEN = "#9be7a3"
GBW = 1e6


def wave(av, amp, vcc, t, f):
    vin = amp * np.sin(2 * np.pi * f * t)
    vout = np.clip(av * vin, -vcc, vcc)
    return vin, vout


# ---- charts-closeup: input/output waveform (with clipping) + GBW tradeoff ----
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)

ax1 = fig.add_axes([0.07, 0.16, 0.40, 0.70]); ax1.set_facecolor(NAVY)
f = 1000.0; T = 1 / f
t = np.linspace(0, 2 * T, 400)
av = -10.0; amp = 1.0; vcc = 8.0   # |Av|*amp = 10 > 8 -> clips
vin, vout = wave(av, amp, vcc, t, f)
ax1.plot(t * 1000, vin, color=CYAN, lw=2, label="V_in (1V)")
ax1.plot(t * 1000, vout, color=ORANGE, lw=2, label="V_out (Av=-10)")
ax1.axhline(vcc, color=GREEN, lw=0.9, ls="--"); ax1.axhline(-vcc, color=GREEN, lw=0.9, ls="--")
ax1.text(0.02, vcc + 0.3, "+Vcc=8V クリップ", color=GREEN, fontsize=7.5)
ax1.set_xlabel("時間 (ms)", color="white", fontsize=9)
ax1.set_ylabel("電圧 (V)", color="white", fontsize=9)
ax1.set_ylim(-11, 11)
ax1.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="lower right")
ax1.set_title("反転増幅：位相反転 + クリッピング", color="white", fontsize=9.5)

ax2 = fig.add_axes([0.58, 0.16, 0.39, 0.70]); ax2.set_facecolor(NAVY)
gains = np.array([1, 2, 5, 10, 20, 50, 100, 200])
bw = GBW / gains
ax2.loglog(gains, bw / 1e3, "o-", color=ORANGE, lw=2, ms=5)
for g in (10, 100):
    ax2.annotate(f"Av={g}\nBW={GBW/g/1e3:.0f}kHz",
                 (g, GBW / g / 1e3), color="white", fontsize=7.5,
                 xytext=(6, 6), textcoords="offset points")
ax2.set_xlabel("電圧ゲイン |Av|", color="white", fontsize=9)
ax2.set_ylabel("帯域幅 BW (kHz)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8, which="both")
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.grid(True, which="both", color="#22304d", lw=0.5)
ax2.set_title("GBW一定：ゲイン×帯域幅 = 1MHz", color="white", fontsize=9.5)

closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.12, 0.12, 0.84, 0.82]); axc.set_facecolor(NAVY)
vin, vout = wave(-10.0, 1.0, 8.0, t, f)
axc.plot(t * 1000, vin, color=CYAN, lw=2.2)
axc.plot(t * 1000, vout, color=ORANGE, lw=2.4)
axc.axhline(8, color=GREEN, lw=0.9, ls="--"); axc.axhline(-8, color=GREEN, lw=0.9, ls="--")
axc.set_ylim(-11, 11); axc.set_xticks([]); axc.set_yticks([])
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "オペアンプ基本回路と", "クリッピング",
                  "Av=-Rf/R1、帯域幅 BW=GBW/|Av| を可視化", cc)
os.remove(cc)

# ---- gif: sweep gain (Rf) -> output amplitude grows then clips ----
frames = []
amp = 1.0; vcc = 12.0; R1 = 10e3
rf_list = list(np.linspace(20, 200, 22)) + list(np.linspace(190, 30, 12))
for rf_k in rf_list:
    Rf = rf_k * 1e3
    av = -(Rf / R1)
    vin, vout = wave(av, amp, vcc, t, f)
    clipped = np.any(np.abs(av * vin) > vcc)
    f2 = plt.figure(figsize=(5.4, 3.2)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.13, 0.16, 0.83, 0.72]); a.set_facecolor(NAVY)
    a.plot(t * 1000, vin, color=CYAN, lw=1.8)
    a.plot(t * 1000, vout, color=ORANGE, lw=2.2)
    a.axhline(vcc, color=GREEN, lw=0.8, ls="--"); a.axhline(-vcc, color=GREEN, lw=0.8, ls="--")
    a.set_ylim(-14, 14); a.set_xlim(0, 2 * T * 1000)
    a.set_xlabel("時間 (ms)", color="white", fontsize=8)
    a.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    tag = "  ★クリップ発生" if clipped else ""
    a.set_title(f"Rf={rf_k:.0f}kΩ  Av={av:.0f}  ({20*np.log10(abs(av)):.0f}dB){tag}",
                color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
