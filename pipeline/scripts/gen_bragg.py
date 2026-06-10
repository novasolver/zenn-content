# -*- coding: utf-8 -*-
"""Bragg diffraction visuals. 2d sinθ=nλ; d_eff=d(1+ε); nmax=floor(2d_eff/λ).
Faithful to the tool (Cu Kα λ=1.54 Å, d=2.5 Å default)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "bragg-diffraction"
NAVY = "#0a1929"
YELLOW, CYAN, RED, GREEN = "#FFD166", "#7fdcff", "#ff6b6b", "#9be7a3"

def two_theta(d, lam, n, eps=0.0):
    dEff = d*(1+eps)
    s = (n*lam)/(2*dEff)
    if s > 1 or s < 0: return None
    return 2*math.degrees(math.asin(s))

def peaks(d, lam, eps=0.0):
    out=[]
    for n in range(1,11):
        tt = two_theta(d, lam, n, eps)
        if tt is None: break
        out.append((n, tt, 1.0/n**1.4))
    return out

def style(ax):
    ax.set_facecolor(NAVY)
    ax.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#3b4a6b")

# ---- closeup: peaks (Cu Kα) + strain shift ----
fig = plt.figure(figsize=(9.6, 4.3)); fig.patch.set_facecolor(NAVY)
ax1 = fig.add_axes([0.07, 0.16, 0.52, 0.72]); style(ax1)
d, lam = 2.5, 1.54
for n, tt, I in peaks(d, lam):
    ax1.vlines(tt, 0, I, color=YELLOW if n==1 else CYAN, lw=2.6 if n==1 else 2.0)
    ax1.plot(tt, I, "o", color=YELLOW if n==1 else CYAN, ms=7 if n==1 else 5)
    ax1.text(tt, I+0.05, f"n={n}\n{tt:.1f}°", color="white", ha="center", fontsize=8)
ax1.set_xlim(0,180); ax1.set_ylim(0,1.18)
ax1.set_xlabel("回折角 2θ (°)", color="white", fontsize=9)
ax1.set_ylabel("相対強度", color="white", fontsize=9)
ax1.set_title("多次数回折ピーク（Cu Kα, d=2.5 Å）", color="white", fontsize=10)

ax2 = fig.add_axes([0.67, 0.16, 0.30, 0.72]); style(ax2)
eps_vals = np.linspace(-0.05, 0.05, 60)
tt_eps = [two_theta(d, lam, 1, e) for e in eps_vals]
ax2.plot(eps_vals*100, tt_eps, color=GREEN, lw=2.4)
ax2.axvline(0, color="#3b4a6b", lw=1, ls=":")
for e in (-0.01, 0.0, 0.01):
    ax2.plot(e*100, two_theta(d,lam,1,e), "o", color=RED, ms=6)
ax2.set_xlabel("格子ひずみ ε (%)", color="white", fontsize=9)
ax2.set_ylabel("回折角 2θ (°, n=1)", color="white", fontsize=9)
ax2.set_title("ひずみによるピークシフト", color="white", fontsize=9)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# ---- cover ----
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.13, 0.16, 0.83, 0.74]); style(axc)
for n, tt, I in peaks(d, lam):
    axc.vlines(tt, 0, I, color=YELLOW if n==1 else CYAN, lw=2.6 if n==1 else 2.0)
    axc.plot(tt, I, "o", color=YELLOW if n==1 else CYAN, ms=6)
axc.set_xlim(0,180); axc.set_ylim(0,1.1)
axc.set_xlabel("2θ (°)", color="white", fontsize=9)
axc.set_ylabel("強度", color="white", fontsize=9)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "ブラッグの法則", "2d sinθ = nλ", "X 線回折で結晶構造を測る", cc)
os.remove(cc)

# ---- gif: sweep λ (like the tool's λ sweep) ----
frames = []
lam_seq = list(np.arange(0.7, 2.6, 0.13)) + list(np.arange(2.6, 0.7, -0.13))
for lv in lam_seq:
    f2 = plt.figure(figsize=(5.4, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.13, 0.17, 0.83, 0.72]); style(a)
    pk = peaks(d, lv)
    for n, tt, I in pk:
        a.vlines(tt, 0, I, color=YELLOW if n==1 else CYAN, lw=2.4 if n==1 else 1.8)
        a.plot(tt, I, "o", color=YELLOW if n==1 else CYAN, ms=5)
    a.set_xlim(0,180); a.set_ylim(0,1.1)
    a.set_xlabel("2θ (°)", color="white", fontsize=9)
    a.set_ylabel("強度", color="white", fontsize=9)
    a.set_title(f"λ={lv:.2f} Å, d=2.5 Å  →  最大次数 {len(pk)}", color="white", fontsize=10)
    frames.append(figlib.fig_to_pil(f2, dpi=90))
figlib.save_gif(frames, SLUG, duration=130)
print("done.")
