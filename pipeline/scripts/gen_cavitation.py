# -*- coding: utf-8 -*-
"""Cavitation number visuals. sigma = (p-pv)/(0.5 rho V^2).
Faithful to tool defaults: p=101.3kPa, pv=2.34kPa, rho=998, V=12, sigma_i=1.0."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "cavitation-number"
NAVY = "#0a1929"
BLUE, GREEN, RED, ORANGE = "#007BFF", "#00b894", "#d63031", "#e17055"

def sigma(p, pv, rho, V):
    q = 0.5*rho*V*V
    return (p - pv)/q if q > 0 else np.inf

# defaults (Pa)
P, PV, RHO, SIGI = 101.3e3, 2.34e3, 998.0, 1.0

def draw_vel(ax, p, pv, rho, Vcur, sigi, title=None):
    ax.set_facecolor(NAVY)
    Vs = np.linspace(0.5, 40, 200)
    sg = np.array([sigma(p, pv, rho, v) for v in Vs])
    ax.plot(Vs, sg, color=BLUE, lw=2.6, label="σ(V)")
    ax.axhline(sigi, color=RED, ls="--", lw=1.6, label="初生 σ_i")
    sc = sigma(p, pv, rho, Vcur)
    col = GREEN if sc > 1.2*sigi else (ORANGE if sc >= sigi else RED)
    ax.scatter([Vcur], [sc], s=75, color=col, edgecolor="white", zorder=5)
    ax.set_xlabel("流速  V (m/s)", color="white", fontsize=9)
    ax.set_ylabel("キャビテーション数  σ", color="white", fontsize=9)
    ax.set_xlim(0, 40); ax.set_ylim(0, min(8, max(4, sc*1.3)))
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.grid(True, color="#22344f", lw=0.6)
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white",
              fontsize=7.5, loc="upper right")
    if title: ax.set_title(title, color="white", fontsize=10)

def draw_pres(ax, p, pv, rho, Vcur, pcur, sigi, title=None):
    ax.set_facecolor(NAVY)
    q = 0.5*rho*Vcur*Vcur
    Ps = np.linspace(10e3, 500e3, 200)
    sg = (Ps - pv)/q
    ax.plot(Ps/1000, sg, color=GREEN, lw=2.6, label="σ(p)")
    ax.axhline(sigi, color=RED, ls="--", lw=1.6, label="初生 σ_i")
    sc = (pcur - pv)/q
    ax.scatter([pcur/1000], [sc], s=75, color=ORANGE, edgecolor="white", zorder=5)
    ax.set_xlabel("局所静圧  p (kPa)", color="white", fontsize=9)
    ax.set_ylabel("キャビテーション数  σ", color="white", fontsize=9)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")
    ax.grid(True, color="#22344f", lw=0.6)
    ax.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white",
              fontsize=7.5, loc="upper left")
    if title: ax.set_title(title, color="white", fontsize=10)

for V in [6, 12, 18, 24]:
    print(f"V={V} sigma={sigma(P,PV,RHO,V):.3f}")

# closeup: sigma vs V + sigma vs p
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.08, 0.16, 0.40, 0.72])
draw_vel(ax1, P, PV, RHO, 12, SIGI, "σ vs 流速（1/V² で急減）")
ax2 = fig.add_axes([0.58, 0.16, 0.40, 0.72])
draw_pres(ax2, P, PV, RHO, 12, P, SIGI, "σ vs 局所静圧（線形）")
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# cover
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.17, 0.17, 0.79, 0.78]); draw_vel(axc, P, PV, RHO, 18, SIGI)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "キャビテーション数 σ", "", "流れが蒸発に近づく瀬戸際を測る", cc)
os.remove(cc)

# gif: sweep velocity 4..30, marker slides down through sigma_i
frames = []
vels = list(np.arange(4, 30.1, 1.5)) + list(np.arange(28.5, 3.9, -1.5))
for v in vels:
    f2 = plt.figure(figsize=(5.2, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.16, 0.17, 0.80, 0.72])
    draw_vel(a, P, PV, RHO, v, SIGI)
    a.get_legend().remove()
    sc = sigma(P, PV, RHO, v)
    state = "安全" if sc > 1.2*SIGI else ("注意" if sc >= SIGI else "発生")
    a.set_title(f"V={v:.1f} m/s   σ={sc:.2f}   {state}", color="white", fontsize=10)
    a.set_ylim(0, 8)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=100)
print("done.")
