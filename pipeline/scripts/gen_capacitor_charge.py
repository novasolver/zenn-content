# -*- coding: utf-8 -*-
"""Capacitor charge/discharge (RC circuit) visuals.
Faithful to the tool's formulas:
  charge:    V(t) = V0 (1 - e^{-t/tau})
  discharge: V(t) = V0 e^{-t/tau}
  current:   I(t) = (V0/R) e^{-t/tau}
  tau = R C
Matplotlib only (RECIPE STEP 5)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "capacitor-charge"
NAVY = "#0b1020"; CYAN = "#7dd3fc"; ORANGE = "#f59e0b"; PINK = "#f472b6"; GREEN = "#9be7a3"

# Reference RC: R=1kOhm, C=1000uF -> tau=1.0s (matches the tool's own example)
R, C, V0 = 1000.0, 1000e-6, 9.0
tau = R * C
print(f"tau=RC={tau:.2f}s  V(tau)={V0*(1-np.exp(-1)):.2f}V (63.2%)  5tau={5*tau:.0f}s  I0={V0/R*1000:.1f}mA")

t = np.linspace(0, 6*tau, 600)
Vc = V0 * (1 - np.exp(-t/tau))   # charge
Vd = V0 * np.exp(-t/tau)         # discharge
I  = (V0/R) * np.exp(-t/tau)     # current (same shape both modes)

# ---- closeup: charge vs discharge curves + current overlay ----
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.08, 0.15, 0.40, 0.72]); ax1.set_facecolor(NAVY)
ax1.plot(t/tau, Vc, color=CYAN, lw=2.4, label="充電 V₀(1-e^{-t/τ})")
ax1.plot(t/tau, Vd, color=ORANGE, lw=2.4, label="放電 V₀e^{-t/τ}")
ax1.axhline(V0*(1-np.exp(-1)), color=GREEN, lw=0.9, ls=":")
ax1.axvline(1, color=GREEN, lw=0.9, ls="--")
ax1.text(1.05, V0*0.30, "t=τ → 63.2%", color=GREEN, fontsize=8)
ax1.set_xlabel("時間 t / τ", color="white", fontsize=9)
ax1.set_ylabel("電圧 V (V)", color="white", fontsize=9)
ax1.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="center right")
ax1.set_title("充電と放電は互いに鏡像", color="white", fontsize=9.5)

ax2 = fig.add_axes([0.58, 0.15, 0.39, 0.72]); ax2.set_facecolor(NAVY)
ax2.plot(t/tau, Vc, color=CYAN, lw=2.4, label="V(t) 電圧")
ax2.set_xlabel("時間 t / τ", color="white", fontsize=9)
ax2.set_ylabel("V (V)", color=CYAN, fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
ax2b = ax2.twinx()
ax2b.plot(t/tau, I*1000, color=PINK, lw=2.2, ls="--", label="I(t) 電流")
ax2b.set_ylabel("I (mA)", color=PINK, fontsize=9); ax2b.tick_params(colors=PINK, labelsize=8)
for k in (1, 2, 3, 5):
    ax2.axvline(k, color="#3b4a6b", lw=0.7, ls=":")
ax2.text(5.02, V0*0.55, "5τ→99.3%", color=GREEN, fontsize=7.5)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.set_title("充電中は電流が指数的に減衰", color="white", fontsize=9.5)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.10, 0.12, 0.86, 0.82]); axc.set_facecolor(NAVY)
axc.plot(t/tau, Vc, color=CYAN, lw=2.6)
axc.plot(t/tau, Vd, color=ORANGE, lw=2.6)
axc.axvline(1, color=GREEN, lw=0.9, ls="--")
axc.set_yticks([]); axc.set_xticks([])
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "コンデンサの充放電と", "時定数 τ=RC",
                  "充電 V₀(1-e^{-t/τ})・放電 V₀e^{-t/τ} を可視化", cc)
os.remove(cc)

# ---- gif: sweep tau (vary R), watch the curve speed change ----
frames = []
Rseq = list(np.linspace(300, 3000, 20)) + list(np.linspace(2700, 400, 12))
for Rg in Rseq:
    taug = Rg * C
    tg = np.linspace(0, 5.0, 400)          # fixed 5 s window
    Vg = V0 * (1 - np.exp(-tg/taug))
    f2 = plt.figure(figsize=(5.4, 3.2)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.13, 0.16, 0.83, 0.72]); a.set_facecolor(NAVY)
    a.plot(tg, Vg, color=CYAN, lw=2.6)
    a.axhline(V0*(1-np.exp(-1)), color=GREEN, lw=0.8, ls=":")
    if taug <= tg[-1]:
        a.axvline(taug, color=ORANGE, lw=1.0, ls="--")
    a.set_xlim(0, tg[-1]); a.set_ylim(0, V0*1.05)
    a.set_xlabel("時間 t (s)", color="white", fontsize=8)
    a.set_ylabel("電圧 V (V)", color="white", fontsize=8)
    a.tick_params(colors="#9fb2d6", labelsize=7)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    a.set_title(f"R={Rg/1000:.2f}kΩ  C=1000µF  →  τ={taug:.2f}s", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=95)
print("done.")
