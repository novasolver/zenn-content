# -*- coding: utf-8 -*-
"""Clausius-Clapeyron vapor pressure visuals. Faithful to the tool:
R=8.314, ln(P2/P1) = -(dH/R)(1/T2 - 1/T1), dH in kJ/mol (x1000)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "clausius-clapeyron-vapor"
NAVY = "#0b1020"
BLUE, RED, GREEN, ORANGE = "#007BFF", "#d63031", "#00b894", "#e17055"
R = 8.314

def P_of_T(T, T1, P1, dH_kJ):
    HoR = dH_kJ*1000/R
    return P1*np.exp(-HoR*(1.0/T - 1.0/T1))

def draw_pt(ax, T1, P1, dH, Tmin=300, Tmax=420, title=None):
    ax.set_facecolor(NAVY)
    T = np.linspace(Tmin, Tmax, 200)
    P = P_of_T(T, T1, P1, dH)
    ax.plot(T, P, color=BLUE, lw=2.4)
    ax.fill_between(T, 0, P, color=BLUE, alpha=0.14)
    ax.plot(T1, P1, 'o', color=GREEN, ms=8)
    ax.annotate("基準点 (T₁,P₁)", (T1,P1), textcoords="offset points", xytext=(-8,10),
                color="white", fontsize=8, ha="right")
    ax.set_xlabel("温度 T (K)", color="white", fontsize=9)
    ax.set_ylabel("蒸気圧 P (kPa)", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    if title: ax.set_title(title, color="white", fontsize=10)

# defaults: T1=373.15, P1=101.325, dH=40.7
T1, P1, dH = 373.15, 101.325, 40.7
print(f"P(400K)={P_of_T(400,T1,P1,dH):.1f} kPa")

# closeup: P-T curve + ln P vs 1/T line
fig = plt.figure(figsize=(9.6,4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.08,0.15,0.50,0.74]); draw_pt(ax1,T1,P1,dH,300,420,"蒸気圧曲線 P(T) — 指数的上昇")
ax2 = fig.add_axes([0.66,0.15,0.31,0.74]); ax2.set_facecolor(NAVY)
T = np.linspace(300,420,200)
invT = 1000.0/T
lnP = np.log(P_of_T(T,T1,P1,dH))
ax2.plot(invT, lnP, color=RED, lw=2.4)
ax2.plot(1000.0/T1, np.log(P1), 'o', color=GREEN, ms=8)
ax2.set_xlabel("1000/T (1/K)", color="white", fontsize=9)
ax2.set_ylabel("ln P", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("ln P − 1/T は直線（傾き −ΔH/R）", color="white", fontsize=9)
closeup = os.path.join(figlib.outdir(SLUG),"charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2,3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.14,0.14,0.82,0.80]); draw_pt(axc,T1,P1,dH,300,420)
cc = os.path.join(figlib.outdir(SLUG),"_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG,"クラウジウス・","クラペイロン","蒸気圧は温度の指数関数 — 沸点・蒸留・気象の基礎式", cc)
os.remove(cc)

# gif: sweep dH (slope changes)
frames=[]
dHseq = list(np.arange(30,51,2.5)) + list(np.arange(48,29,-2.5))
for dHv in dHseq:
    f2 = plt.figure(figsize=(5.2,3.5)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.15,0.16,0.81,0.74]); a.set_facecolor(NAVY)
    T = np.linspace(300,420,200)
    invT = 1000.0/T
    lnP = np.log(P_of_T(T,T1,P1,dHv))
    a.plot(invT, lnP, color=RED, lw=2.4)
    a.plot(1000.0/T1, np.log(P1), 'o', color=GREEN, ms=8)
    a.set_xlabel("1000/T (1/K)", color="white", fontsize=9)
    a.set_ylabel("ln P", color="white", fontsize=9)
    a.tick_params(colors="#9fb2d6", labelsize=8)
    a.set_ylim(-2, 8)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    a.set_title(f"ΔH_vap = {dHv:.1f} kJ/mol  →  傾き −ΔH/R", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=150)
print("done.")
