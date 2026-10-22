# -*- coding: utf-8 -*-
"""Column buckling visuals. Pcr=pi^2 EI/(KL)^2; secant P-delta curve.
Deformed column shapes by end condition + P-delta curves for several e."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "column-buckling-adv"
NAVY = "#0a1628"
BLUE, CYAN, RED, ORANGE, GREEN, PURPLE = "#007BFF", "#00B4D8", "#dc3545", "#f39c12", "#2ecc71", "#c084fc"

E_steel = 200e3  # MPa

def props_rect(b, h):
    I = b*h**3/12; A = b*h
    return I, A, math.sqrt(I/A)

def pcr(E, I, K, L):
    return math.pi**2 * E * I / (K*L)**2 / 1000  # kN

def secant_delta(e, ratio):
    if e <= 0 or ratio <= 0: return 0.0
    ang = (math.pi/2)*math.sqrt(ratio)
    return e*(1/math.cos(ang)-1)

# Lead example: rect 100x100, L=3000, K=1
b, h, L = 100, 100, 3000
I, A, r = props_rect(b, h)
Pcr = pcr(E_steel, I, 1.0, L)
print(f"rect {b}x{h} L={L} K=1: I={I:.0f} Pcr={Pcr:.1f}kN lambda={L/r:.1f}")

# ---- deformed column shapes by end condition (mode shapes) ----
def mode_shape(K, t):
    # t in 0..1 along length; return lateral x normalized
    if K == 1.0:   return math.sin(math.pi*t)                 # pin-pin
    if K == 0.5:   return 0.5*(1-math.cos(2*math.pi*t))       # fixed-fixed
    if K == 0.7:   return math.sin(1.43*math.pi*t) - 0.7*1.43*math.pi*t*(1-t)*0  # approx fixed-pin
    if K == 2.0:   return 1-math.cos(math.pi*t/2)             # fixed-free (cantilever)
    return math.sin(math.pi*t)

# ---- closeup: deformed shapes (left) + P-delta curves (right) ----
fig = plt.figure(figsize=(9.6, 4.4)); fig.patch.set_facecolor(NAVY)

# left: 4 end conditions deformed shapes
axL = fig.add_axes([0.04, 0.10, 0.40, 0.82]); axL.set_facecolor(NAVY)
conds = [(1.0,"両端ピン",BLUE),(0.5,"両端固定",GREEN),(0.7,"固定-ピン",ORANGE),(2.0,"固定-自由",RED)]
ts = np.linspace(0,1,80)
for i,(K,name,col) in enumerate(conds):
    xoff = i*1.8
    amp = 0.5
    xs = xoff + amp*np.array([mode_shape(K,t) for t in ts])
    ys = ts*4
    axL.plot(xs, ys, color=col, lw=2.4)
    axL.plot([xoff],[0],"s",color="#445566",ms=7)
    Pc = pcr(E_steel, I, K, L)
    axL.text(xoff, -0.45, f"K={K}\n{Pc:.0f}kN", color=col, fontsize=8, ha="center", va="top")
axL.set_xlim(-0.8, 6.5); axL.set_ylim(-1.3, 4.4)
axL.axis("off")
axL.set_title("端末条件と座屈モード形（100×100, L=3m）", color="white", fontsize=10)

# right: P-delta curves for several eccentricities
axR = fig.add_axes([0.56, 0.15, 0.40, 0.74]); axR.set_facecolor(NAVY)
ratios = np.linspace(0, 0.97, 60)
for e,col in [(2,CYAN),(5,BLUE),(10,ORANGE),(20,RED)]:
    deltas = [secant_delta(e, rr) for rr in ratios]
    Ps = ratios*Pcr
    axR.plot(deltas, Ps, color=col, lw=2.2, label=f"e={e}mm")
axR.axhline(Pcr, color=RED, lw=1.4, ls="--")
axR.text(2, Pcr*0.96, f"P_cr={Pcr:.0f}kN", color=RED, fontsize=8, va="top")
axR.set_xlim(0, 130); axR.set_ylim(0, Pcr*1.05)
axR.set_xlabel("たわみ δ (mm)", color="white", fontsize=9)
axR.set_ylabel("荷重 P (kN)", color="white", fontsize=9)
axR.tick_params(colors="#9fb2d6", labelsize=8)
for sp in axR.spines.values(): sp.set_color("#3b4a6b")
axR.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8, loc="lower right")
axR.set_title("P-δ曲線（初期不整 e の影響）", color="white", fontsize=10)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.14, 0.16, 0.82, 0.74]); axc.set_facecolor(NAVY)
for e,col in [(2,CYAN),(5,BLUE),(10,ORANGE),(20,RED)]:
    deltas = [secant_delta(e, rr) for rr in ratios]
    axc.plot(deltas, ratios*Pcr, color=col, lw=2.2)
axc.axhline(Pcr, color=RED, lw=1.2, ls="--")
axc.set_xlim(0,130); axc.set_ylim(0,Pcr*1.05)
axc.set_xlabel("δ (mm)", color="white", fontsize=8); axc.set_ylabel("P (kN)", color="white", fontsize=8)
axc.tick_params(colors="#9fb2d6", labelsize=7)
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "オイラー座屈と", "初期不整", "Pcr = π²EI/(KL)² と P-δ曲線", cc)
os.remove(cc)

# ---- gif: sweep eccentricity e, P-delta curve grows ----
frames = []
es = list(np.linspace(0.5, 25, 9)) + list(np.linspace(25, 0.5, 9))
for ev in es:
    f2 = plt.figure(figsize=(5.2, 3.5)); f2.patch.set_facecolor(NAVY)
    axg = f2.add_axes([0.15, 0.17, 0.81, 0.72]); axg.set_facecolor(NAVY)
    deltas = [secant_delta(ev, rr) for rr in ratios]
    axg.plot(deltas, ratios*Pcr, color=BLUE, lw=2.6)
    axg.axhline(Pcr, color=RED, lw=1.3, ls="--")
    axg.text(2, Pcr*0.95, f"P_cr={Pcr:.0f}kN", color=RED, fontsize=8, va="top")
    axg.set_xlim(0,140); axg.set_ylim(0,Pcr*1.05)
    axg.set_xlabel("たわみ δ (mm)", color="white", fontsize=9)
    axg.set_ylabel("荷重 P (kN)", color="white", fontsize=9)
    axg.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in axg.spines.values(): sp.set_color("#3b4a6b")
    axg.set_title(f"偏心 e={ev:.1f}mm → P-δ曲線", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=130)
print("done.")
