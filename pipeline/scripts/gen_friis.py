# -*- coding: utf-8 -*-
"""Friis transmission equation visuals.
FSPL=20log10(d_km)+20log10(f_MHz)+32.44; Prx=Ptx+Gtx+Grx-FSPL (all dB/dBm).
Faithful to the tool: default Ptx10W Gtx12 Grx12 f2400MHz d10km, RX_SENS=-90dBm."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "antenna-friis-equation"
NAVY = "#0a1929"
BLUE, GREEN, RED, ORANGE = "#007BFF", "#00b894", "#d63031", "#e17055"
RX_SENS = -90.0

def fspl(d_km, f_MHz):
    return 20*np.log10(d_km) + 20*np.log10(f_MHz) + 32.44

def prx(Ptx_W, Gtx, Grx, f_MHz, d_km):
    txdbm = 10*np.log10(Ptx_W*1000)
    return txdbm + Gtx + Grx - fspl(d_km, f_MHz)

def draw_dist(ax, f_MHz=2400, cur_d=10.0, title=None, legend=True):
    ax.set_facecolor(NAVY)
    d = np.logspace(np.log10(0.1), np.log10(40000), 200)
    rx = prx(10, 12, 12, f_MHz, d)
    ax.plot(d, rx, color=BLUE, lw=2.4, label="受信電力 P_rx")
    ax.axhline(RX_SENS, color=RED, ls="--", lw=1.8, label="受信感度 −90 dBm")
    cr = prx(10, 12, 12, f_MHz, cur_d)
    ax.plot([cur_d], [cr], "o", color=ORANGE, ms=9, mec="white", mew=1.3, zorder=5,
            label="現在の距離")
    ax.set_xscale("log")
    ax.set_xlim(0.1, 40000); ax.set_ylim(-130, 10)
    ax.set_xlabel("通信距離 d [km] (log)", color="white", fontsize=9)
    ax.set_ylabel("受信電力 [dBm]", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.grid(True, color="#1f3350", lw=0.6)
    if legend:
        ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="upper right")
    if title: ax.set_title(title, color="white", fontsize=10)

def draw_fspl(ax, d_km=10.0, cur_f=2400, title=None):
    ax.set_facecolor(NAVY)
    f = np.logspace(np.log10(30), np.log10(30000), 200)
    ax.plot(f, fspl(d_km, f), color=GREEN, lw=2.4, label="FSPL")
    ax.fill_between(f, fspl(d_km, f), 0, color=GREEN, alpha=0.10)
    cf = fspl(d_km, cur_f)
    ax.plot([cur_f], [cf], "o", color=BLUE, ms=9, mec="white", mew=1.3, zorder=5)
    ax.set_xscale("log")
    ax.set_xlim(30, 30000); ax.set_ylim(40, 145)
    ax.set_xlabel("周波数 f [MHz] (log)", color="white", fontsize=9)
    ax.set_ylabel("自由空間伝搬損失 [dB]", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.grid(True, color="#1f3350", lw=0.6)
    if title: ax.set_title(title, color="white", fontsize=10)

print(f"default 10W 12/12 2400MHz 10km: FSPL={fspl(10,2400):.2f} Prx={prx(10,12,12,2400,10):.2f} dBm")

# ---- closeup: Prx vs distance + FSPL vs frequency ----
fig = plt.figure(figsize=(9.8, 4.2)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07, 0.16, 0.41, 0.72]); draw_dist(ax1, 2400, 10.0, "受信電力 vs 距離（2.4GHz, 10W, 12/12dBi）")
ax2 = fig.add_axes([0.58, 0.16, 0.40, 0.72]); draw_fspl(ax2, 10.0, 2400, "自由空間伝搬損失 vs 周波数（d=10km）")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.4, 3.3)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.16, 0.17, 0.80, 0.76]); draw_dist(axc, 2400, 10.0, legend=False)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "フリスの伝達公式", "", "Prx=Ptx+Gtx+Grx−FSPL（リンクバジェット）", cc)
os.remove(cc)

# ---- gif: sweep distance, current point rides receive-power curve ----
frames = []
ds = list(np.logspace(np.log10(0.3), np.log10(3000), 14))
seq = ds + ds[::-1]
for dv in seq:
    f2 = plt.figure(figsize=(5.4, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.16, 0.17, 0.81, 0.72]); draw_dist(a, 2400, dv, legend=False)
    cr = prx(10, 12, 12, 2400, dv); m = cr - RX_SENS
    a.set_title(f"d={dv:.0f} km  →  P_rx={cr:.0f} dBm  (margin {m:+.0f} dB)",
                color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=120)
print("done.")
