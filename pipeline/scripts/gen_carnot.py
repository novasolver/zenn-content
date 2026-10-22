# -*- coding: utf-8 -*-
"""Carnot cycle visuals. eta=1-Tc/Th; P-V (isothermal+adiabatic) and T-S rectangle.
Faithful to the tool (gamma=1.4, n=1, R=8.314; Th=600,Tc=300,QH=2000)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "carnot-cycle"
NAVY = "#0b1020"
RED, ORANGE, BLUE, GREEN = "#ff6b6b", "#f59e0b", "#7dd3fc", "#9be7a3"
gamma, n, R = 1.4, 1.0, 8.314

def cycle(TH, TC, QH):
    V1 = 0.001
    er = np.exp(QH/(n*R*TH))
    V2 = V1*er; V3 = V2*(TH/TC)**(1/(gamma-1)); V4 = V3/er
    def iso(T, Va, Vb):
        V = np.linspace(Va, Vb, 40); return V*1000, n*R*T/V/1000
    def adia(Va, Vb, Ts):
        K = n*R*Ts*Va**(gamma-1); V = np.linspace(Va, Vb, 40); return V*1000, K/V**gamma/1000
    s1 = iso(TH, V1, V2); s2 = adia(V2, V3, TH); s3 = iso(TC, V3, V4); s4 = adia(V4, V1, TC)
    return s1, s2, s3, s4, (V1, V2, V3, V4)

def draw_pv(ax, TH, TC, QH, title=None):
    ax.set_facecolor(NAVY)
    s1, s2, s3, s4, Vs = cycle(TH, TC, QH)
    ax.plot(*s1, color=RED, lw=2.2, label="等温膨張 (TH)")
    ax.plot(*s2, color=ORANGE, lw=2.2, label="断熱膨張")
    ax.plot(*s3, color=BLUE, lw=2.2, label="等温圧縮 (TC)")
    ax.plot(*s4, color=GREEN, lw=2.2, label="断熱圧縮")
    ax.set_xlabel("体積 V (L)", color="white", fontsize=9); ax.set_ylabel("圧力 P (kPa)", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="upper right")
    if title: ax.set_title(title, color="white", fontsize=10)

TH, TC, QH = 600, 300, 2000
eta = 1 - TC/TH; W = QH*eta; QC = QH-W; dS = QH/TH
print(f"Th={TH} Tc={TC}: eta={eta:.3f} W={W:.0f}J QC={QC:.0f}J dS={dS:.2f}J/K")

# closeup: P-V + T-S
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.08, 0.14, 0.50, 0.76]); draw_pv(ax1, TH, TC, QH, "P-V 線図（カルノーサイクル）")
ax2 = fig.add_axes([0.66, 0.16, 0.31, 0.72]); ax2.set_facecolor(NAVY)
S = [0, dS, dS, 0, 0]; T = [TC, TC, TH, TH, TC]
ax2.plot(S, T, color="#c084fc", lw=2.2)
ax2.fill(S, T, color="#c084fc", alpha=0.15)
ax2.text(dS/2, (TH+TC)/2, f"W=面積\n={W:.0f}J", color="white", ha="center", fontsize=8)
ax2.set_xlabel("エントロピー S (J/K)", color="white", fontsize=9); ax2.set_ylabel("温度 T (K)", color="white", fontsize=9)
ax2.set_ylim(TC-80, TH+80); ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("T-S 線図は長方形（η=1−Tc/Th=0.5）", color="white", fontsize=9)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.12, 0.12, 0.84, 0.82]); draw_pv(axc, TH, TC, QH)
axc.get_legend().remove()
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "カルノーサイクル", "", "η = 1 − Tc/Th と P-V・T-S 線図", cc)
os.remove(cc)

# gif: sweep TH, efficiency changes
frames = []
for THv in list(range(450, 1300, 50)) + list(range(1250, 450, -50)):
    et = 1 - TC/THv
    f2 = plt.figure(figsize=(5.2, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.12, 0.15, 0.84, 0.76]); draw_pv(a, THv, TC, QH)
    a.get_legend().remove()
    a.set_title(f"TH={THv}K, TC={TC}K  →  η=1−Tc/Th={et:.2f}", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
