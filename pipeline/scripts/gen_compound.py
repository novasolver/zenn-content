# -*- coding: utf-8 -*-
"""Compound interest visuals. A=P(1+r/m)^(mn) + annuity FV. Nominal vs real (inflation).
Faithful to compound-interest-sim tool."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(r"E:\NovaSolver\zenn-content")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figlib

SLUG = "compound-interest-sim"
NAVY = "#0b1020"
BLUE, GREEN, ORANGE = "#3b82f6", "#22c55e", "#f59e0b"

def series(P, r, n, C, m, infl):
    yrs = np.arange(0, n+1)
    rp = r/m
    annualR = (1+rp)**m - 1
    nominal=[]; real=[]; simple=[]
    for yr in yrs:
        A = P*(1+rp)**(m*yr)
        if C>0 and yr>0:
            A += C*((1+annualR)**yr - 1)/annualR
        nominal.append(A)
        real.append(A/(1+infl)**yr)
        s = P*(1+r*yr) + (C*yr*(1+r*yr/2) if C>0 else 0)
        simple.append(s)
    return yrs, np.array(nominal), np.array(real), np.array(simple)

# --- closeup: nominal vs real (iDeCo-like) + compound vs simple ---
fig = plt.figure(figsize=(9.4, 4.3)); fig.patch.set_facecolor(NAVY)

ax1 = fig.add_axes([0.09, 0.16, 0.40, 0.72]); ax1.set_facecolor(NAVY)
yrs, nom, real, simp = series(0, 0.05, 30, 18, 12, 0.02)
ax1.plot(yrs, nom, color=BLUE, lw=2.4, label="名目資産額")
ax1.plot(yrs, real, color=GREEN, lw=2.2, ls="--", label="実質購買力（インフレ調整）")
ax1.fill_between(yrs, 0, nom, color=BLUE, alpha=0.08)
ax1.set_xlabel("経過年数", color="white", fontsize=9)
ax1.set_ylabel("資産額 (万円)", color="white", fontsize=9)
ax1.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax1.spines.values(): sp.set_color("#3b4a6b")
ax1.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="upper left")
ax1.set_title("iDeCo: 月1.5万・年5%・30年 → 約1220万円", color="white", fontsize=9.3)

ax2 = fig.add_axes([0.59, 0.16, 0.38, 0.72]); ax2.set_facecolor(NAVY)
yrs2, nom2, real2, simp2 = series(100, 0.05, 30, 0, 1, 0.02)
ax2.plot(yrs2, nom2, color=BLUE, lw=2.4, label="複利")
ax2.plot(yrs2, simp2, color=ORANGE, lw=2.2, ls="--", label="単利")
ax2.fill_between(yrs2, simp2, nom2, color=BLUE, alpha=0.12)
ax2.set_xlabel("経過年数", color="white", fontsize=9)
ax2.set_ylabel("資産額 (万円)", color="white", fontsize=9)
ax2.tick_params(colors="#9fb2d6", labelsize=8)
for sp in ax2.spines.values(): sp.set_color("#3b4a6b")
ax2.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="upper left")
ax2.set_title("100万・年5%・30年: 複利432万 vs 単利250万", color="white", fontsize=9.3)
closeup = os.path.join(figlib.outdir(SLUG), "charts-closeup.png")
figlib.save_fig(fig, closeup, dpi=130); print("  closeup ->", closeup)

# --- cover ---
figc = plt.figure(figsize=(5.2, 3.2)); figc.patch.set_facecolor(NAVY)
axc = figc.add_axes([0.15, 0.16, 0.81, 0.78]); axc.set_facecolor(NAVY)
axc.plot(yrs2, nom2, color=BLUE, lw=2.8, label="複利")
axc.plot(yrs2, simp2, color=ORANGE, lw=2.4, ls="--", label="単利")
axc.fill_between(yrs2, simp2, nom2, color=BLUE, alpha=0.15)
axc.set_xlabel("年数", color="white", fontsize=9); axc.set_ylabel("万円", color="white", fontsize=9)
axc.tick_params(colors="#9fb2d6", labelsize=8)
for sp in axc.spines.values(): sp.set_color("#3b4a6b")
axc.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=8)
cc = os.path.join(figlib.outdir(SLUG), "_cc.png"); figlib.save_fig(figc, cc, dpi=120)
figlib.make_cover(SLUG, "複利と積立の数学", "", "A=P(1+r/m)^(mn)＋年金の将来価値", cc)
os.remove(cc)

# --- gif: sweep annual rate r, compound vs simple ---
frames = []
rates = list(range(1, 11)) + list(range(10, 1, -1))
for rv in rates:
    yrs3, nom3, real3, simp3 = series(100, rv/100, 30, 0, 1, 0.02)
    f2 = plt.figure(figsize=(5.2, 3.4)); f2.patch.set_facecolor(NAVY)
    a = f2.add_axes([0.15, 0.17, 0.81, 0.70]); a.set_facecolor(NAVY)
    a.plot(yrs3, nom3, color=BLUE, lw=2.6, label="複利")
    a.plot(yrs3, simp3, color=ORANGE, lw=2.2, ls="--", label="単利")
    a.fill_between(yrs3, simp3, nom3, color=BLUE, alpha=0.12)
    a.set_xlim(0,30); a.set_ylim(0, 1100)
    a.set_xlabel("経過年数", color="white", fontsize=9); a.set_ylabel("万円", color="white", fontsize=9)
    a.tick_params(colors="#9fb2d6", labelsize=8)
    for sp in a.spines.values(): sp.set_color("#3b4a6b")
    a.legend(facecolor=NAVY, edgecolor="#3b4a6b", labelcolor="white", fontsize=7.5, loc="upper left")
    a.set_title(f"元金100万・年利{rv}%・30年: 最終 {nom3[-1]:.0f}万円", color="white", fontsize=9.5)
    frames.append(figlib.fig_to_pil(f2, dpi=92))
figlib.save_gif(frames, SLUG, duration=150)
print("done.")
