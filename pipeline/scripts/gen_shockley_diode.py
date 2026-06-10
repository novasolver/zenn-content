# -*- coding: utf-8 -*-
"""Shockley diode I-V visuals. I = Is*(exp(V/(n*Vt))-1), Vt=kT/q.
Faithful to the tool: semilog |I| vs V, temperature family (25/75/125 C),
operating-point marker at defaults. matplotlib only."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "shockley-diode"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; PINK = "#f472b6"; GREEN = "#9be7a3"
K = 1.380649e-23; Q = 1.602176634e-19

def vt(Tc): return K * (Tc + 273.15) / Q

def fmt_amps(I):
    a = abs(I)
    if a >= 1e-3: return f"{I*1e3:.2f} mA"
    if a >= 1e-6: return f"{I*1e6:.2f} uA"
    if a >= 1e-9: return f"{I*1e9:.2f} nA"
    return f"{I:.1e} A"
def diode_I(V, Is, n, Tc):
    arg = np.clip(V / (n * vt(Tc)), -700, 700)
    return Is * (np.exp(arg) - 1)

Is = 1e-9; n = 1.0
V = np.linspace(-0.4, 1.0, 1400)
Vp = 0.40  # default operating point
I_op = diode_I(Vp, Is, 1.0, 25)
print(f"Vt(25C)={vt(25)*1000:.2f}mV  I_op={I_op*1e3:.2f}mA  rd={1.0*vt(25)/I_op:.2f}ohm")

def semilog(ax, Varr, Iarr, **kw):
    y = np.log10(np.clip(np.abs(Iarr), 1e-16, None))
    ax.plot(Varr, y, **kw)

# ---- closeup: left = semilog I-V (n=1 & n=2), right = temperature family ----
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.08, 0.16, 0.40, 0.72]); ax1.set_facecolor(NAVY)
semilog(ax1, V, diode_I(V, Is, 1.0, 25), color=CYAN, lw=2, label="n = 1.0 (拡散支配)")
semilog(ax1, V, diode_I(V, Is, 2.0, 25), color=PINK, lw=2, label="n = 2.0 (再結合支配)")
y_op = np.log10(abs(I_op))
ax1.plot([Vp], [y_op], "o", color=ORANGE, ms=8)
ax1.annotate(f"動作点 ({Vp:.2f}V, {I_op*1e3:.1f}mA)", (Vp, y_op),
             textcoords="offset points", xytext=(-150, 6), color=ORANGE, fontsize=8)
ax1.set_xlabel("印加電圧 V (V)", color="white", fontsize=9)
ax1.set_ylabel("log10 |I| (A)", color="white", fontsize=9)
ax1.tick_params(colors="#9fb2d6", labelsize=8); ax1.set_ylim(-15, 1)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="lower right")
ax1.set_title("半対数 I-V：傾きは n·60 mV/桁", color="white", fontsize=9.5)

ax2 = fig.add_axes([0.58, 0.16, 0.39, 0.72]); ax2.set_facecolor(NAVY)
for Tc, col in [(25, CYAN), (75, ORANGE), (125, PINK)]:
    semilog(ax2, V[V >= 0], diode_I(V[V >= 0], Is, 1.0, Tc), color=col, lw=2,
            label=f"T = {Tc}°C  (V_T={vt(Tc)*1e3:.1f}mV)")
ax2.set_xlabel("順方向電圧 V_F (V)", color="white", fontsize=9)
ax2.set_ylabel("log10 I (A)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8); ax2.set_ylim(-15, 1)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="lower right")
ax2.set_title("高温ほど V_T が増え曲線が左へ", color="white", fontsize=9.5)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover chart preview ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.12, 0.12, 0.84, 0.82]); axc.set_facecolor(NAVY)
for Tc, col in [(25, CYAN), (75, ORANGE), (125, PINK)]:
    semilog(axc, V[V >= 0], diode_I(V[V >= 0], Is, 1.0, Tc), color=col, lw=2.4)
axc.set_xticks([]); axc.set_yticks([]); axc.set_ylim(-15, 1)
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ショックレーの", "ダイオード式", "I = I_S(exp(V/nV_T)-1)、pn 接合の I-V 特性", cc)
os.remove(cc)

# ---- gif: sweep V_F, marker climbs the exponential curve ----
frames = []
sweep = list(np.linspace(0.0, 1.0, 26)) + list(np.linspace(0.96, 0.04, 14))
for vf in sweep:
    Iv = diode_I(vf, Is, 1.0, 25)
    f2 = plt.figure(figsize=(5.4, 3.2)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.13, 0.16, 0.83, 0.72]); a.set_facecolor(NAVY)
    semilog(a, V, diode_I(V, Is, 1.0, 25), color=CYAN, lw=2.2)
    yv = np.log10(max(abs(Iv), 1e-16))
    yv = min(max(yv, -15), 1)
    a.plot([vf], [yv], "o", color=ORANGE, ms=9)
    a.set_xlim(-0.4, 1.0); a.set_ylim(-15, 1)
    a.set_xlabel("V_F (V)", color="white", fontsize=8)
    a.set_ylabel("log10 |I|", color="white", fontsize=8)
    a.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    a.set_title(f"V_F = {vf:.2f} V   I = {fmt_amps(Iv)}", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
